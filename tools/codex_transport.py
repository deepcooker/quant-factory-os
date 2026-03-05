#!/usr/bin/env python3
from __future__ import annotations

import json
import queue
import re
import shutil
import subprocess
import threading
import time
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MODEL_TRANSPORT_PRIMARY = "app-server"
MODEL_TRANSPORT_FALLBACK = "exec"


@dataclass
class TransportArtifacts:
    prompt_file: Path
    raw_file: Path
    events_file: Path
    stderr_file: Path
    app_events_file: Path | None = None
    app_stderr_file: Path | None = None


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
    fallback_rc: int | None
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


class _AppServerRPC:
    def __init__(self, events_file: Path, stderr_file: Path) -> None:
        self.events_file = events_file
        self.stderr_file = stderr_file
        self.proc: subprocess.Popen[str] | None = None
        self._messages: queue.Queue[dict[str, Any]] = queue.Queue()
        self._pending: deque[dict[str, Any]] = deque()
        self._next_id = 1
        self._lock = threading.Lock()
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
        with self._lock:
            req_id = self._next_id
            self._next_id += 1
        self._send({"id": req_id, "method": method, "params": params or {}})

        if self._pending:
            new_pending: deque[dict[str, Any]] = deque()
            while self._pending:
                msg = self._pending.popleft()
                if msg.get("id") == req_id:
                    self._pending = new_pending
                    return msg
                new_pending.append(msg)
            self._pending = new_pending

        deadline = time.time() + timeout
        while True:
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
            return self._pending.popleft()
        try:
            return self._messages.get(timeout=timeout)
        except queue.Empty:
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

            deadline = time.time() + 240.0
            turn_done = False
            text_chunks: list[str] = []
            while time.time() < deadline:
                event = rpc.next_event(timeout=1.0)
                if event is None:
                    continue
                method = str(event.get("method", "")).strip()
                params = event.get("params") or {}
                if method in {"item/plan/delta", "item/agentMessage/delta"}:
                    t = _extract_text(params.get("delta"))
                    if t:
                        text_chunks.append(t)
                elif method == "item/completed":
                    item = params.get("item") or {}
                    if str(item.get("type", "")).lower() in {"plan", "agentmessage"}:
                        t = _extract_text(item.get("text") or item.get("content"))
                        if t:
                            text_chunks.append(t)
                elif method == "codex/event/agent_message":
                    msg = params.get("msg") or {}
                    t = _extract_text(msg.get("message"))
                    if t:
                        text_chunks.append(t)
                elif method == "turn/completed":
                    t = params.get("turn") or {}
                    if t.get("id") == turn_id:
                        turn_done = True
                        break

            raw_text = "".join(text_chunks).strip()
            raw_file.write_text(raw_text + ("\n" if raw_text else ""), encoding="utf-8")
            return 0 if turn_done and bool(raw_text) else 1
    except Exception as exc:
        with open(stderr_file, "a", encoding="utf-8") as fh:
            fh.write(f"app-server transport failed: {exc}\n")
        return 1


def run_exec_transport(
    prompt_file: Path,
    raw_file: Path,
    events_file: Path,
    stderr_file: Path,
    model_name: str,
    model_reasoning_effort: str,
) -> int:
    try:
        prompt_text = prompt_file.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        stderr_file.write_text(f"read prompt failed: {exc}\n", encoding="utf-8")
        return 1

    cmd = ["codex", "--ask-for-approval", "never"]
    if model_name:
        cmd.extend(["-m", model_name])
    if model_reasoning_effort:
        cmd.extend(["-c", f"model_reasoning_effort={model_reasoning_effort}"])
    cmd.extend(
        [
            "exec",
            "--sandbox",
            "read-only",
            "--json",
            "--output-last-message",
            str(raw_file),
            prompt_text,
        ]
    )

    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except Exception as exc:
        stderr_file.write_text(f"codex exec failed: {exc}\n", encoding="utf-8")
        return 1

    events_file.write_text(proc.stdout or "", encoding="utf-8")
    stderr_file.write_text(proc.stderr or "", encoding="utf-8")
    if not raw_file.is_file() or not raw_file.read_text(encoding="utf-8", errors="replace").strip():
        return 1
    return int(proc.returncode or 0)


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
    if primary_rc == 0:
        return TransportResult(
            success=True,
            effective_transport=MODEL_TRANSPORT_PRIMARY,
            primary_rc=primary_rc,
            fallback_rc=None,
            final_rc=primary_rc,
            reason="ok",
        )

    if artifacts.app_events_file is not None:
        try:
            if artifacts.events_file.is_file():
                shutil.copyfile(artifacts.events_file, artifacts.app_events_file)
        except Exception:
            pass
    if artifacts.app_stderr_file is not None:
        try:
            if artifacts.stderr_file.is_file():
                shutil.copyfile(artifacts.stderr_file, artifacts.app_stderr_file)
        except Exception:
            pass

    fallback_rc = run_exec_transport(
        artifacts.prompt_file,
        artifacts.raw_file,
        artifacts.events_file,
        artifacts.stderr_file,
        request.model_name,
        request.model_reasoning_effort,
    )
    success = fallback_rc == 0
    return TransportResult(
        success=success,
        effective_transport=MODEL_TRANSPORT_FALLBACK,
        primary_rc=primary_rc,
        fallback_rc=fallback_rc,
        final_rc=fallback_rc,
        reason="ok" if success else f"fallback-failed-{fallback_rc}",
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
    for m in re.finditer(r"/bin/bash -lc [^\r\n]+", plain_events):
        cmd = " ".join(m.group(0).split()).strip()
        if cmd:
            commands.append(cmd)
    if not commands and ("Ran " in plain_events or "command_execution" in plain_events):
        commands.append("interactive_plan_tool_run_detected")
    return commands
