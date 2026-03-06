#!/usr/bin/env python3
from __future__ import annotations

import json
import queue
import re
import subprocess
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

MODEL_TRANSPORT_PRIMARY = "app-server"
APP_SERVER_TURN_TIMEOUT_SEC = 1800.0


@dataclass
class TransportArtifacts:
    prompt_file: Path
    raw_file: Path
    events_file: Path
    stderr_file: Path


@dataclass
class TransportRequest:
    model_name: str
    model_reasoning_effort: str
    cwd: Path


@dataclass
class TransportResult:
    success: bool
    effective_transport: str
    primary_rc: int
    final_rc: int
    reason: str



def runtime_reasoning_effort(requested_effort: str) -> tuple[str, str]:
    effort = str(requested_effort or "").strip().lower()
    if effort == "minimal":
        return ("low", "minimal-not-compatible-with-active-toolset-upgraded-to-low")
    return (effort, "as-requested")



def _extract_text(payload: Any) -> str:
    if isinstance(payload, str):
        return payload
    if isinstance(payload, list):
        chunks: list[str] = []
        for part in payload:
            text = _extract_text(part)
            if text:
                chunks.append(text)
        return "".join(chunks)
    if isinstance(payload, dict):
        for key in ("text", "delta", "message", "content"):
            if key in payload:
                text = _extract_text(payload.get(key))
                if text:
                    return text
    return ""


def _extract_first_json_dict_text(raw_text: str) -> str:
    text = str(raw_text or "").strip()
    if not text:
        return ""
    decoder = json.JSONDecoder()
    for idx, ch in enumerate(text):
        if ch != "{":
            continue
        try:
            maybe, end = decoder.raw_decode(text[idx:])
        except Exception:
            continue
        if isinstance(maybe, dict) and {"mainline", "current_stage", "next_step", "files_read"}.issubset(set(maybe.keys())):
            return text[idx : idx + end]
    return ""


def _maybe_extract_final_json_dict_text(
    text_chunks: list[str],
    json_start_idx: int | None,
    chunk_text: str,
    *,
    force: bool = False,
) -> tuple[str | None, int | None]:
    if chunk_text:
        if json_start_idx is None:
            local_idx = chunk_text.find("{")
            if local_idx >= 0:
                json_start_idx = sum(len(part) for part in text_chunks[:-1]) + local_idx
        if not force and "}" not in chunk_text:
            return (None, json_start_idx)
    elif not force:
        return (None, json_start_idx)
    if json_start_idx is None:
        return (None, None)
    combined = "".join(text_chunks)
    parsed = _extract_first_json_dict_text(combined[json_start_idx:])
    if parsed:
        return (parsed, json_start_idx)
    return (None, json_start_idx)


class _AppServerRPC:
    def __init__(self, events_file: Path, stderr_file: Path) -> None:
        self.events_file = events_file
        self.stderr_file = stderr_file
        self.proc: subprocess.Popen[str] | None = None
        self._messages: queue.Queue[dict[str, Any]] = queue.Queue()
        self._pending: list[dict[str, Any]] = []
        self._next_id = 1
        self._stdout_thread: threading.Thread | None = None
        self._stderr_thread: threading.Thread | None = None
        self._events_fp: Any = None
        self._stderr_fp: Any = None

    def __enter__(self) -> "_AppServerRPC":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def start(self) -> None:
        self.events_file.parent.mkdir(parents=True, exist_ok=True)
        self._events_fp = self.events_file.open("w", encoding="utf-8")
        self._stderr_fp = self.stderr_file.open("w", encoding="utf-8")
        self.proc = subprocess.Popen(
            ["codex", "app-server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        assert self.proc.stdout is not None
        assert self.proc.stderr is not None

        def read_stdout() -> None:
            assert self.proc is not None and self.proc.stdout is not None
            for line in self.proc.stdout:
                self._events_fp.write(line)
                self._events_fp.flush()
                s = line.strip()
                if not s:
                    continue
                try:
                    msg = json.loads(s)
                except Exception:
                    continue
                if isinstance(msg, dict):
                    self._messages.put(msg)

        def read_stderr() -> None:
            assert self.proc is not None and self.proc.stderr is not None
            for line in self.proc.stderr:
                self._stderr_fp.write(line)
                self._stderr_fp.flush()

        self._stdout_thread = threading.Thread(target=read_stdout, daemon=True)
        self._stderr_thread = threading.Thread(target=read_stderr, daemon=True)
        self._stdout_thread.start()
        self._stderr_thread.start()

    def close(self) -> None:
        if self.proc is not None and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=3)
        if self._stdout_thread is not None:
            self._stdout_thread.join(timeout=1)
        if self._stderr_thread is not None:
            self._stderr_thread.join(timeout=1)
        if self._events_fp is not None:
            self._events_fp.close()
        if self._stderr_fp is not None:
            self._stderr_fp.close()

    def _send(self, payload: dict[str, Any]) -> None:
        if self.proc is None or self.proc.stdin is None:
            raise RuntimeError("app-server process is not running")
        self.proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        self._send({"method": method, "params": params or {}})

    def request(self, method: str, params: dict[str, Any] | None = None, timeout: float = 60.0) -> dict[str, Any]:
        req_id = self._next_id
        self._next_id += 1
        self._send({"id": req_id, "method": method, "params": params or {}})

        deadline = time.time() + timeout
        while True:
            for idx, pending in enumerate(list(self._pending)):
                if pending.get("id") == req_id:
                    return self._pending.pop(idx)
            left = deadline - time.time()
            if left <= 0:
                raise TimeoutError(f"timeout waiting response for {method}")
            try:
                msg = self._messages.get(timeout=left)
            except queue.Empty:
                continue
            if msg.get("id") == req_id:
                return msg
            self._pending.append(msg)

    def next_event(self, timeout: float = 1.0) -> dict[str, Any] | None:
        if self._pending:
            return self._pending.pop(0)
        try:
            return self._messages.get(timeout=timeout)
        except queue.Empty:
            if self.proc is not None and self.proc.poll() is not None:
                return {
                    "method": "__app_server_exit__",
                    "params": {"returncode": self.proc.returncode},
                }
            return None



def run_app_server_transport(
    prompt_file: Path,
    raw_file: Path,
    events_file: Path,
    stderr_file: Path,
    model_name: str,
    model_reasoning_effort: str,
    cwd: Path,
) -> int:
    try:
        prompt_text = prompt_file.read_text(encoding="utf-8", errors="replace").strip()
    except Exception as exc:
        stderr_file.write_text(f"read prompt failed: {exc}\n", encoding="utf-8")
        return 1
    if not prompt_text:
        stderr_file.write_text("prompt file is empty\n", encoding="utf-8")
        return 1

    try:
        with _AppServerRPC(events_file=events_file, stderr_file=stderr_file) as rpc:
            init_resp = rpc.request(
                "initialize",
                {
                    "clientInfo": {"name": "qf-learn-sync", "version": "0.1.0"},
                    "capabilities": {"experimentalApi": True},
                },
                timeout=30.0,
            )
            if "error" in init_resp:
                return 1
            rpc.notify("initialized", {})

            modes_resp = rpc.request("collaborationMode/list", {}, timeout=30.0)
            if "error" in modes_resp:
                return 1

            thread_resp = rpc.request(
                "thread/start",
                {"model": model_name, "cwd": str(cwd)},
                timeout=30.0,
            )
            if "error" in thread_resp:
                return 1
            thread_id = ((thread_resp.get("result") or {}).get("thread") or {}).get("id")
            if not isinstance(thread_id, str) or not thread_id.strip():
                return 1

            turn_resp = rpc.request(
                "turn/start",
                {
                    "threadId": thread_id,
                    "cwd": str(cwd),
                    "input": [{"type": "text", "text": prompt_text}],
                    "collaborationMode": {
                        "mode": "plan",
                        "settings": {
                            "model": model_name,
                            "reasoning_effort": model_reasoning_effort,
                            "developer_instructions": None,
                        },
                    },
                    "sandboxPolicy": {"type": "readOnly"},
                    "effort": model_reasoning_effort,
                },
                timeout=60.0,
            )
            if "error" in turn_resp:
                return 1

            turn_id = ((turn_resp.get("result") or {}).get("turn") or {}).get("id")
            if not isinstance(turn_id, str) or not turn_id.strip():
                return 1

            deadline = time.time() + APP_SERVER_TURN_TIMEOUT_SEC
            turn_done = False
            text_chunks: list[str] = []
            agent_message_phase: dict[str, str] = {}
            json_start_idx: int | None = None
            while time.time() < deadline:
                event = rpc.next_event(timeout=1.0)
                if event is None:
                    continue
                method = str(event.get("method", "")).strip()
                params = event.get("params") or {}
                if method == "item/started":
                    item = params.get("item") or {}
                    if str(item.get("type", "")).lower() == "agentmessage":
                        item_id = str(item.get("id", "")).strip()
                        phase = str(item.get("phase", "")).strip().lower()
                        if item_id:
                            agent_message_phase[item_id] = phase
                    continue
                if method in {"item/plan/delta", "item/agentMessage/delta"}:
                    if method == "item/agentMessage/delta":
                        item_id = str(params.get("itemId", "")).strip()
                        phase = agent_message_phase.get(item_id, "")
                        if phase and phase != "final_answer":
                            continue
                    t = _extract_text(params.get("delta"))
                    if t:
                        text_chunks.append(t)
                        parsed, json_start_idx = _maybe_extract_final_json_dict_text(
                            text_chunks,
                            json_start_idx,
                            t,
                        )
                        if parsed:
                            raw_file.write_text(parsed + "\n", encoding="utf-8")
                            return 0
                elif method == "item/completed":
                    item = params.get("item") or {}
                    item_type = str(item.get("type", "")).lower()
                    if item_type == "agentmessage":
                        phase = str(item.get("phase", "")).strip().lower()
                        if phase and phase != "final_answer":
                            continue
                    if item_type in {"plan", "agentmessage"}:
                        t = _extract_text(item.get("text") or item.get("content"))
                        if t:
                            text_chunks.append(t)
                        parsed, json_start_idx = _maybe_extract_final_json_dict_text(
                            text_chunks,
                            json_start_idx,
                            t,
                            force=True,
                        )
                        if parsed:
                            raw_file.write_text(parsed + "\n", encoding="utf-8")
                            return 0
                elif method == "turn/completed":
                    turn = params.get("turn") or {}
                    if turn.get("id") == turn_id:
                        turn_done = str(turn.get("status", "")).strip().lower() == "completed"
                        break
                elif method == "__app_server_exit__":
                    break

            raw_text = "".join(text_chunks).strip()
            raw_file.write_text(raw_text + ("\n" if raw_text else ""), encoding="utf-8")
            return 0 if turn_done and bool(raw_text) else 1
    except Exception as exc:
        with open(stderr_file, "a", encoding="utf-8") as fh:
            fh.write(f"app-server transport failed: {exc}\n")
        return 1



def run_plan_sync(request: TransportRequest, artifacts: TransportArtifacts) -> TransportResult:
    primary_rc = run_app_server_transport(
        artifacts.prompt_file,
        artifacts.raw_file,
        artifacts.events_file,
        artifacts.stderr_file,
        request.model_name,
        request.model_reasoning_effort,
        request.cwd,
    )
    success = primary_rc == 0
    return TransportResult(
        success=success,
        effective_transport=MODEL_TRANSPORT_PRIMARY,
        primary_rc=primary_rc,
        final_rc=primary_rc,
        reason="ok" if success else f"app-server-failed-{primary_rc}",
    )



def extract_command_evidence(events_file: Path) -> list[str]:
    if not events_file.is_file():
        return []
    events_text = events_file.read_text(encoding="utf-8", errors="replace")
    commands: list[str] = []

    for raw_line in events_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        try:
            event_obj = json.loads(line)
        except Exception:
            continue
        item = event_obj.get("item")
        if isinstance(item, dict) and item.get("type") == "command_execution":
            raw_cmd = item.get("raw_input") or item.get("command") or item.get("input")
            cmd = " ".join(str(raw_cmd or "").split()).strip()
            if cmd:
                commands.append(cmd)
            continue

        method = str(event_obj.get("method", "")).strip()
        params = event_obj.get("params") or {}
        if method == "item/completed":
            item2 = params.get("item") or {}
            if str(item2.get("type", "")).lower() == "commandexecution":
                raw_cmd = item2.get("command") or item2.get("raw_input") or item2.get("input")
                cmd = " ".join(str(raw_cmd or "").split()).strip()
                if cmd:
                    commands.append(cmd)
                continue
        if method == "codex/event/exec_command_begin":
            msg = params.get("msg") or {}
            raw_cmd = msg.get("command")
            if isinstance(raw_cmd, list):
                cmd = " ".join(str(x) for x in raw_cmd if str(x).strip())
            else:
                cmd = str(raw_cmd or "")
            cmd = " ".join(cmd.split()).strip()
            if cmd:
                commands.append(cmd)

    if commands:
        return commands

    plain_events = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", events_text)
    plain_events = re.sub(r"\x1b\].*?(\x07|\x1b\\)", "", plain_events, flags=re.S)
    plain_events = plain_events.replace("\x1b", "")
    for match in re.finditer(r"/bin/bash -lc [^\r\n]+", plain_events):
        cmd = " ".join(match.group(0).split()).strip()
        if cmd:
            commands.append(cmd)
    return commands
