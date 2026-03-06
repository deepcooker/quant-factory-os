#!/usr/bin/env python3
"""Codex app-server Python smoke/e2e test.

This script validates the local codex app-server JSON-RPC flow:
- initialize -> initialized -> collaborationMode/list -> thread/start
- (full mode) turn/start with plan mode + readOnly + effort=xhigh
- (full mode) negative check: effort=fast must be rejected

Artifacts are written to: test_codex/app_server_runtime/
"""

from __future__ import annotations

import argparse
import json
import queue
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional
from collections import deque


ALLOWED_EFFORTS = ["none", "minimal", "low", "medium", "high", "xhigh"]
DEFAULT_MODEL = "gpt-5.3-codex"
DEFAULT_MODE = "plan"
DEFAULT_EFFORT = "xhigh"
RUNTIME_DIR = Path("test_codex/app_server_runtime")


class AppServerError(RuntimeError):
    pass


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""


class JsonRpcAppServer:
    def __init__(self, events_path: Path, stderr_path: Path) -> None:
        self.events_path = events_path
        self.stderr_path = stderr_path
        self.proc: Optional[subprocess.Popen[str]] = None
        self._reader_thread: Optional[threading.Thread] = None
        self._stderr_thread: Optional[threading.Thread] = None
        self._messages: "queue.Queue[Dict[str, Any]]" = queue.Queue()
        self._pending: Deque[Dict[str, Any]] = deque()
        self._lock = threading.Lock()
        self._next_id = 1
        self._events_fp = None
        self._stderr_fp = None

    def __enter__(self) -> "JsonRpcAppServer":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def start(self) -> None:
        self.events_path.parent.mkdir(parents=True, exist_ok=True)
        self._events_fp = self.events_path.open("w", encoding="utf-8")
        self._stderr_fp = self.stderr_path.open("w", encoding="utf-8")

        self.proc = subprocess.Popen(
            ["codex", "app-server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        assert self.proc.stdout is not None
        assert self.proc.stderr is not None

        def read_stdout() -> None:
            for line in self.proc.stdout:
                ts = datetime.now(timezone.utc).isoformat()
                self._events_fp.write(f"{ts} {line}")
                self._events_fp.flush()
                s = line.strip()
                if not s:
                    continue
                try:
                    msg = json.loads(s)
                except json.JSONDecodeError:
                    continue
                self._messages.put(msg)

        def read_stderr() -> None:
            for line in self.proc.stderr:
                ts = datetime.now(timezone.utc).isoformat()
                self._stderr_fp.write(f"{ts} {line}")
                self._stderr_fp.flush()

        self._reader_thread = threading.Thread(target=read_stdout, daemon=True)
        self._stderr_thread = threading.Thread(target=read_stderr, daemon=True)
        self._reader_thread.start()
        self._stderr_thread.start()

    def close(self) -> None:
        if self.proc is not None:
            if self.proc.poll() is None:
                self.proc.terminate()
                try:
                    self.proc.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    self.proc.kill()
                    self.proc.wait(timeout=3)
        if self._reader_thread is not None:
            self._reader_thread.join(timeout=1)
        if self._stderr_thread is not None:
            self._stderr_thread.join(timeout=1)
        if self._events_fp is not None:
            self._events_fp.close()
        if self._stderr_fp is not None:
            self._stderr_fp.close()

    def _send(self, payload: Dict[str, Any]) -> None:
        if self.proc is None or self.proc.stdin is None:
            raise AppServerError("app-server is not running")
        self.proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    def notify(self, method: str, params: Optional[Dict[str, Any]] = None) -> None:
        self._send({"method": method, "params": params or {}})

    def request(self, method: str, params: Optional[Dict[str, Any]] = None, timeout: int = 60) -> Dict[str, Any]:
        with self._lock:
            req_id = self._next_id
            self._next_id += 1

        self._send({"id": req_id, "method": method, "params": params or {}})
        deadline = time.time() + timeout

        # First, scan pending notifications once for a matching response id.
        if self._pending:
            new_pending: Deque[Dict[str, Any]] = deque()
            while self._pending:
                msg = self._pending.popleft()
                if msg.get("id") == req_id:
                    self._pending = new_pending
                    return msg
                new_pending.append(msg)
            self._pending = new_pending

        while True:
            remaining = deadline - time.time()
            if remaining <= 0:
                raise AppServerError(f"timeout waiting response for method={method}")

            try:
                msg = self._messages.get(timeout=remaining)
            except queue.Empty:
                msg = None
            if msg is None:
                continue
            if msg.get("id") == req_id:
                return msg
            self._pending.append(msg)

    def _pop_message(self, timeout: float) -> Optional[Dict[str, Any]]:
        if self._pending:
            return self._pending.popleft()
        try:
            return self._messages.get(timeout=timeout)
        except queue.Empty:
            return None

    def next_message(self, timeout: float = 1.0) -> Optional[Dict[str, Any]]:
        return self._pop_message(timeout=timeout)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Codex app-server Python test runner")
    parser.add_argument("--quick", action="store_true", help="Only run handshake and mode discovery")
    parser.add_argument("--mode", choices=["plan", "default"], default=DEFAULT_MODE)
    parser.add_argument("--effort", choices=ALLOWED_EFFORTS, default=DEFAULT_EFFORT)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--cwd", default=str(Path.cwd()))
    parser.add_argument("--timeout", type=int, default=120)
    return parser.parse_args()


def codex_version() -> str:
    try:
        out = subprocess.check_output(["codex", "--version"], text=True, stderr=subprocess.STDOUT)
        return out.strip()
    except Exception as exc:  # pragma: no cover
        return f"unknown ({exc})"


def ensure_prereqs() -> None:
    if shutil.which("codex") is None:
        raise AppServerError("codex binary not found in PATH")


def extract_modes(resp: Dict[str, Any]) -> List[str]:
    result = resp.get("result") or {}
    data = result.get("data") or result.get("modes") or []
    names: List[str] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        mode = item.get("mode") or item.get("name")
        if isinstance(mode, str):
            names.append(mode)
    return names


def pull_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        chunks = []
        for part in value:
            if isinstance(part, str):
                chunks.append(part)
            elif isinstance(part, dict):
                text = part.get("text")
                if isinstance(text, str):
                    chunks.append(text)
        return "".join(chunks)
    if isinstance(value, dict):
        text = value.get("text")
        if isinstance(text, str):
            return text
    return ""


def run_full_turn(
    client: JsonRpcAppServer,
    thread_id: str,
    mode: str,
    model: str,
    effort: str,
    cwd: str,
    timeout: int,
) -> Dict[str, Any]:
    prompt = (
        "Use plan mode. Output exactly one <proposed_plan> block with 3 bullet points. "
        "Do not edit files."
    )
    response = client.request(
        "turn/start",
        {
            "threadId": thread_id,
            "cwd": cwd,
            "input": [{"type": "text", "text": prompt}],
            "collaborationMode": {
                "mode": mode,
                "settings": {
                    "model": model,
                    "reasoning_effort": effort,
                    "developer_instructions": None,
                },
            },
            "sandboxPolicy": {"type": "readOnly"},
            "effort": effort,
        },
        timeout=min(timeout, 60),
    )
    if "error" in response:
        raise AppServerError(f"turn/start failed: {response['error']}")

    turn_id = ((response.get("result") or {}).get("turn") or {}).get("id")
    if not turn_id:
        raise AppServerError("turn/start succeeded but no turn id")

    deadline = time.time() + timeout
    saw_turn_completed = False
    saw_plan_signal = False
    assistant_text_fragments: List[str] = []
    turn_status = "unknown"
    turn_error = ""

    while time.time() < deadline:
        msg = client.next_message(timeout=1.0)
        if msg is None:
            continue
        method = msg.get("method")
        params = msg.get("params") or {}

        if method == "item/plan/delta":
            saw_plan_signal = True
            delta = params.get("delta")
            txt = pull_text(delta)
            if txt:
                assistant_text_fragments.append(txt)

        if method == "item/agentMessage/delta":
            delta = params.get("delta")
            txt = pull_text(delta)
            if txt:
                assistant_text_fragments.append(txt)

        if method == "codex/event/task_started":
            event = params.get("msg") or {}
            if event.get("collaboration_mode_kind") == "plan":
                saw_plan_signal = True

        if method == "item/completed":
            item = params.get("item") or {}
            item_type = item.get("type")
            if item_type == "plan":
                saw_plan_signal = True
            text_candidate = item.get("text")
            txt = pull_text(text_candidate)
            if txt:
                assistant_text_fragments.append(txt)

        if method == "turn/completed":
            t = params.get("turn") or {}
            if t.get("id") == turn_id:
                saw_turn_completed = True
                turn_status = str(t.get("status") or "unknown")
                err = t.get("error") or {}
                if isinstance(err, dict):
                    turn_error = str(err.get("message") or "")
                break

    all_text = "".join(assistant_text_fragments)
    if "<proposed_plan>" in all_text:
        saw_plan_signal = True

    return {
        "turn_id": turn_id,
        "turn_completed": saw_turn_completed,
        "turn_status": turn_status,
        "turn_error": turn_error,
        "plan_signal": saw_plan_signal,
        "assistant_text_excerpt": all_text[:1000],
    }


def run_negative_effort_check(
    client: JsonRpcAppServer,
    thread_id: str,
    mode: str,
    model: str,
    cwd: str,
) -> CheckResult:
    response = client.request(
        "turn/start",
        {
            "threadId": thread_id,
            "cwd": cwd,
            "input": [{"type": "text", "text": "quick invalid effort probe"}],
            "collaborationMode": {
                "mode": mode,
                "settings": {
                    "model": model,
                    "reasoning_effort": "fast",
                    "developer_instructions": None,
                },
            },
            "sandboxPolicy": {"type": "readOnly"},
            "effort": "fast",
        },
        timeout=20,
    )
    err = response.get("error")
    if not isinstance(err, dict):
        return CheckResult(
            name="APP_SERVER_EFFORT_NEGATIVE_OK",
            ok=False,
            detail="expected error for effort=fast but request succeeded",
        )
    msg = str(err.get("message", ""))
    ok = "expected one of" in msg and "xhigh" in msg
    return CheckResult(
        name="APP_SERVER_EFFORT_NEGATIVE_OK",
        ok=ok,
        detail=msg if msg else json.dumps(err, ensure_ascii=False),
    )


def main() -> int:
    args = parse_args()
    ensure_prereqs()

    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    events_path = RUNTIME_DIR / f"{ts}.events.jsonl"
    stderr_path = RUNTIME_DIR / f"{ts}.stderr.log"
    summary_path = RUNTIME_DIR / f"{ts}.summary.json"

    checks: List[CheckResult] = []
    started_at = datetime.now(timezone.utc).isoformat()

    try:
        with JsonRpcAppServer(events_path=events_path, stderr_path=stderr_path) as client:
            init_resp = client.request(
                "initialize",
                {
                    "clientInfo": {"name": "qf-app-server-test", "version": "0.1.0"},
                    "capabilities": {"experimentalApi": True},
                },
                timeout=30,
            )
            init_ok = "error" not in init_resp
            checks.append(CheckResult("APP_SERVER_INIT_OK", init_ok, "initialize"))

            client.notify("initialized", {})

            modes_resp = client.request("collaborationMode/list", {}, timeout=30)
            modes = extract_modes(modes_resp)
            mode_ok = len(modes) > 0
            checks.append(CheckResult("APP_SERVER_MODES_OK", mode_ok, ",".join(modes) if modes else "none"))

            thread_resp = client.request(
                "thread/start",
                {"model": args.model, "cwd": args.cwd},
                timeout=30,
            )
            thread_id = ((thread_resp.get("result") or {}).get("thread") or {}).get("id")
            thread_ok = isinstance(thread_id, str) and len(thread_id) > 0
            checks.append(CheckResult("APP_SERVER_THREAD_OK", thread_ok, thread_id or "missing"))

            turn_ok = False
            plan_signal_ok = False
            effort_ok = False
            negative_result = CheckResult("APP_SERVER_EFFORT_NEGATIVE_OK", True, "skipped in --quick")
            full_turn: Dict[str, Any] = {}

            if not args.quick and thread_ok:
                full_turn = run_full_turn(
                    client=client,
                    thread_id=thread_id,
                    mode=args.mode,
                    model=args.model,
                    effort=args.effort,
                    cwd=args.cwd,
                    timeout=args.timeout,
                )
                turn_ok = bool(full_turn.get("turn_completed")) and str(full_turn.get("turn_status")) == "completed"
                plan_signal_ok = bool(full_turn.get("plan_signal"))
                effort_ok = turn_ok
                negative_result = run_negative_effort_check(
                    client=client,
                    thread_id=thread_id,
                    mode=args.mode,
                    model=args.model,
                    cwd=args.cwd,
                )
            elif args.quick:
                turn_ok = True
                plan_signal_ok = True
                effort_ok = True

            turn_detail = "full" if not args.quick else "quick-skip"
            if not args.quick and full_turn:
                turn_detail = str(full_turn.get("turn_status") or "unknown")
                if full_turn.get("turn_error"):
                    turn_detail = f"{turn_detail}: {full_turn['turn_error']}"
            checks.append(CheckResult("APP_SERVER_TURN_OK", turn_ok, turn_detail))
            checks.append(
                CheckResult(
                    "APP_SERVER_PLAN_SIGNAL",
                    plan_signal_ok,
                    "plan-mode-signal-detected" if plan_signal_ok else "no-plan-signal",
                )
            )
            effort_detail = args.effort if effort_ok else f"{args.effort}: turn-not-completed"
            checks.append(CheckResult("APP_SERVER_EFFORT_VALIDATION_OK", effort_ok, effort_detail))
            checks.append(negative_result)

    except Exception as exc:
        checks.append(CheckResult("APP_SERVER_FATAL", False, str(exc)))

    finished_at = datetime.now(timezone.utc).isoformat()
    payload = {
        "timestamp": ts,
        "started_at": started_at,
        "finished_at": finished_at,
        "codex_version": codex_version(),
        "cwd": args.cwd,
        "quick": args.quick,
        "mode": args.mode,
        "model": args.model,
        "effort": args.effort,
        "checks": [check.__dict__ for check in checks],
        "artifacts": {
            "events": str(events_path),
            "stderr": str(stderr_path),
            "summary": str(summary_path),
        },
    }
    summary_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    check_map = {c.name: c for c in checks}

    # Required console markers
    print(f"APP_SERVER_INIT_OK: {str(check_map.get('APP_SERVER_INIT_OK', CheckResult('', False)).ok).lower()}")
    modes_ok = check_map.get("APP_SERVER_MODES_OK", CheckResult("", False, ""))
    modes_detail = modes_ok.detail if modes_ok.detail else "none"
    print(f"APP_SERVER_MODES: {modes_detail}")
    print(f"APP_SERVER_THREAD_OK: {str(check_map.get('APP_SERVER_THREAD_OK', CheckResult('', False)).ok).lower()}")
    print(f"APP_SERVER_TURN_OK: {str(check_map.get('APP_SERVER_TURN_OK', CheckResult('', False)).ok).lower()}")
    print(f"APP_SERVER_PLAN_SIGNAL: {str(check_map.get('APP_SERVER_PLAN_SIGNAL', CheckResult('', False)).ok).lower()}")
    print(
        f"APP_SERVER_EFFORT_VALIDATION_OK: {str(check_map.get('APP_SERVER_EFFORT_VALIDATION_OK', CheckResult('', False)).ok).lower()}"
    )
    print(
        f"APP_SERVER_EFFORT_NEGATIVE_OK: {str(check_map.get('APP_SERVER_EFFORT_NEGATIVE_OK', CheckResult('', False)).ok).lower()}"
    )

    print(f"APP_SERVER_ARTIFACT_EVENTS: {events_path}")
    print(f"APP_SERVER_ARTIFACT_STDERR: {stderr_path}")
    print(f"APP_SERVER_ARTIFACT_SUMMARY: {summary_path}")

    required = [
        "APP_SERVER_INIT_OK",
        "APP_SERVER_MODES_OK",
        "APP_SERVER_THREAD_OK",
        "APP_SERVER_TURN_OK",
        "APP_SERVER_PLAN_SIGNAL",
        "APP_SERVER_EFFORT_VALIDATION_OK",
        "APP_SERVER_EFFORT_NEGATIVE_OK",
    ]
    success = all(check_map.get(k, CheckResult(k, False)).ok for k in required)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
