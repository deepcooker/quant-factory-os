#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import queue
import subprocess
import threading
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_CONFIG_PATH = REPO_ROOT / "tools" / "project_config.json"
CODEX_BIN = "codex"
APP_SERVER_SUBCOMMAND = "app-server"
DEFAULT_MODEL = "gpt-5.4"
DEFAULT_TIMEOUT_SEC = 60
PLAN_TIMEOUT_SEC = 300
DEFAULT_SLOT = "demo_default"


class DemoError(RuntimeError):
    pass


class JsonRpcAppServer:
    def __init__(self, project_root: Path, events_path: Path, stderr_path: Path) -> None:
        self.project_root = project_root
        self.events_path = events_path
        self.stderr_path = stderr_path
        self.proc: subprocess.Popen[str] | None = None
        self._reader_thread: threading.Thread | None = None
        self._stderr_thread: threading.Thread | None = None
        self._messages: "queue.Queue[dict[str, Any]]" = queue.Queue()
        self._pending: deque[dict[str, Any]] = deque()
        self._next_id = 1
        self._events_fp = None
        self._stderr_fp = None

    def start(self) -> None:
        self.events_path.parent.mkdir(parents=True, exist_ok=True)
        self.stderr_path.parent.mkdir(parents=True, exist_ok=True)
        self._events_fp = self.events_path.open("w", encoding="utf-8")
        self._stderr_fp = self.stderr_path.open("w", encoding="utf-8")
        self.proc = subprocess.Popen(
            [CODEX_BIN, APP_SERVER_SUBCOMMAND],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=str(self.project_root),
        )
        assert self.proc.stdout is not None
        assert self.proc.stderr is not None

        def read_stdout() -> None:
            for line in self.proc.stdout:
                ts = datetime.now(timezone.utc).isoformat()
                self._events_fp.write(f"{ts} {line}")
                self._events_fp.flush()
                raw = line.strip()
                if not raw:
                    continue
                try:
                    self._messages.put(json.loads(raw))
                except json.JSONDecodeError:
                    continue

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
        if self.proc is not None and self.proc.poll() is None:
            if self.proc.stdin is not None and not self.proc.stdin.closed:
                self.proc.stdin.close()
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

    def _send(self, payload: dict[str, Any]) -> None:
        if self.proc is None or self.proc.stdin is None:
            raise DemoError("app-server is not running")
        self.proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        self._send({"method": method, "params": params or {}})

    def request(self, method: str, params: dict[str, Any] | None = None, timeout_sec: int = DEFAULT_TIMEOUT_SEC) -> dict[str, Any]:
        req_id = self._next_id
        self._next_id += 1
        self._send({"id": req_id, "method": method, "params": params or {}})
        deadline = time.time() + timeout_sec

        if self._pending:
            new_pending: deque[dict[str, Any]] = deque()
            while self._pending:
                msg = self._pending.popleft()
                if msg.get("id") == req_id:
                    self._pending = new_pending
                    return msg
                new_pending.append(msg)
            self._pending = new_pending

        while time.time() < deadline:
            try:
                msg = self._messages.get(timeout=max(0.1, deadline - time.time()))
            except queue.Empty:
                continue
            if msg.get("id") == req_id:
                return msg
            self._pending.append(msg)
        raise DemoError(f"timeout waiting for {method}")

    def next_event(self, timeout_sec: float = 1.0) -> dict[str, Any] | None:
        if self._pending:
            return self._pending.popleft()
        try:
            return self._messages.get(timeout=timeout_sec)
        except queue.Empty:
            return None


def load_demo_config() -> dict[str, Any]:
    return json.loads(TOOLS_CONFIG_PATH.read_text(encoding="utf-8"))


def save_demo_config(config: dict[str, Any]) -> None:
    TOOLS_CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_demo_record(method: str) -> dict[str, Any]:
    config = load_demo_config()
    demo_sessions = config.setdefault("demo_sessions", {})
    return dict(demo_sessions.get(method, {}) or {})


def update_demo_record(method: str, **fields: Any) -> None:
    config = load_demo_config()
    demo_sessions = config.setdefault("demo_sessions", {})
    record = demo_sessions.setdefault(method, {})
    record.update(fields)
    record["updated_at"] = datetime.now(timezone.utc).isoformat()
    save_demo_config(config)


def now_compact_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


def build_skill_path(skill_name: str) -> Path:
    return REPO_ROOT / ".agents" / "skills" / skill_name / "SKILL.md"


def validate_slot_exists(slot: str) -> None:
    config = load_demo_config()
    slot_table = config.get("thread_slots") or {}
    if slot_table and slot not in slot_table:
        raise DemoError(f"slot 不存在于 thread_slots 配置中: {slot}")


def validate_skill_exists(skill_name: str) -> str:
    skill = str(skill_name).strip()
    if not skill:
        return ""
    skill_path = build_skill_path(skill)
    if not skill_path.is_file():
        raise DemoError(f"skill 不存在: {skill_path}")
    return str(skill_path)


def build_thread_name(slot: str, thread_id: str, created_at_compact: str, spawn_mode: str, parent_thread_id: str = "") -> str:
    name = f"{slot}:{thread_id}:{created_at_compact}:{spawn_mode}"
    if parent_thread_id:
        name += f":fork_by_{parent_thread_id}"
    return name


def wait_for_rollout_ready(thread_path: str, timeout_sec: int = 5) -> None:
    target = Path(str(thread_path).strip())
    if not str(thread_path).strip():
        return
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        if target.is_file():
            return
        time.sleep(0.2)
    raise DemoError(f"等待 rollout 文件超时: {thread_path}")


def detect_turn_status(thread_payload: dict[str, Any], turn_id: str) -> str:
    target_turn_id = str(turn_id).strip()
    if not target_turn_id:
        return ""
    for turn in (thread_payload.get("turns") or []):
        if str((turn or {}).get("id", "")).strip() == target_turn_id:
            return str((turn or {}).get("status", "")).strip()
    return ""


def compact_text(value: str) -> str:
    return "\n".join(line.rstrip() for line in str(value).replace("\r\n", "\n").replace("\r", "\n").splitlines()).strip()


def collect_text_fragments(value: Any) -> list[str]:
    fragments: list[str] = []
    if isinstance(value, str):
        text = compact_text(value)
        if text:
            fragments.append(text)
        return fragments
    if isinstance(value, dict):
        direct_text = value.get("text")
        if isinstance(direct_text, str):
            text = compact_text(direct_text)
            if text:
                fragments.append(text)
        for key in ("content", "items"):
            nested = value.get(key)
            if isinstance(nested, list):
                for item in nested:
                    fragments.extend(collect_text_fragments(item))
        return fragments
    if isinstance(value, list):
        for item in value:
            fragments.extend(collect_text_fragments(item))
    return fragments


def extract_last_agent_message(thread_payload: dict[str, Any]) -> str:
    turns = list(thread_payload.get("turns") or [])
    for turn in reversed(turns):
        for item in reversed(list((turn or {}).get("items") or [])):
            item_type = str((item or {}).get("type", "")).strip().lower()
            if item_type not in {"agentmessage", "agent_message", "assistantmessage", "assistant_message"}:
                continue
            fragments = collect_text_fragments(item)
            if fragments:
                return "\n\n".join(fragments).strip()
            text = str((item or {}).get("text", "")).strip()
            if text:
                return text
    return ""


def initialize_transport(transport: JsonRpcAppServer) -> None:
    result = transport.request(
        "initialize",
        {
            "clientInfo": {"name": "appserver-demo", "version": "0.1.0"},
            "capabilities": {"experimentalApi": True},
        },
        timeout_sec=DEFAULT_TIMEOUT_SEC,
    )
    if "error" in result:
        raise DemoError(str(result["error"]))
    transport.notify("initialized", {})


def new_thread(transport: JsonRpcAppServer, slot: str, force_new: bool) -> dict[str, Any]:
    validate_slot_exists(slot)
    record = get_demo_record(slot)
    existing_thread_id = str(record.get("thread_id", "")).strip()
    existing_thread_path = str(record.get("thread_path", "")).strip()
    if existing_thread_id and not force_new:
        result = transport.request("thread/resume", {"threadId": existing_thread_id}, timeout_sec=DEFAULT_TIMEOUT_SEC)
        if "error" in result and "no rollout found" in str(result["error"]) and existing_thread_path:
            wait_for_rollout_ready(existing_thread_path, timeout_sec=5)
            result = transport.request("thread/resume", {"threadId": existing_thread_id}, timeout_sec=DEFAULT_TIMEOUT_SEC)
        if "error" not in result:
            update_demo_record(
                slot,
                thread_id=existing_thread_id,
                thread_path=existing_thread_path,
                status="resumed",
                lifecycle="resume",
                spawn_mode=str(record.get("spawn_mode", "")).strip() or "new",
                created_at=str(record.get("created_at", "")).strip(),
            )
            return {
                "thread_id": existing_thread_id,
                "thread_path": existing_thread_path,
                "thread_action": "resumed",
                "raw_result": result,
            }

    params = {
        "model": DEFAULT_MODEL,
        "cwd": str(REPO_ROOT),
        "approvalPolicy": "never",
        "sandboxPolicy": {
            "type": "externalSandbox",
            "networkAccess": "enabled",
        },
        "name": f"demo-{slot}",
    }
    result = transport.request("thread/start", params, timeout_sec=DEFAULT_TIMEOUT_SEC)
    if "error" in result:
        raise DemoError(str(result["error"]))
    thread = ((result.get("result") or {}).get("thread") or {})
    thread_id = str(thread.get("id", "")).strip()
    thread_path = str(thread.get("path", "")).strip()
    if not thread_id:
        raise DemoError("thread/start 未返回 thread_id")
    update_demo_record(
        slot,
        thread_id=thread_id,
        thread_path=thread_path,
        status="started",
        lifecycle="new",
        spawn_mode="new",
        created_at=datetime.now(timezone.utc).isoformat(),
        parent_thread_id="",
    )
    return {
        "thread_id": thread_id,
        "thread_path": thread_path,
        "thread_action": "started",
        "raw_result": result,
    }


def resume_thread(transport: JsonRpcAppServer, thread_id: str, thread_path: str = "") -> dict[str, Any]:
    if not str(thread_id).strip():
        raise DemoError("thread_id 为空")
    result = transport.request("thread/resume", {"threadId": thread_id}, timeout_sec=DEFAULT_TIMEOUT_SEC)
    if "error" in result and "no rollout found" in str(result["error"]) and thread_path:
        wait_for_rollout_ready(thread_path, timeout_sec=5)
        result = transport.request("thread/resume", {"threadId": thread_id}, timeout_sec=DEFAULT_TIMEOUT_SEC)
    if "error" in result:
        raise DemoError(str(result["error"]))
    return {
        "thread_id": thread_id,
        "thread_path": thread_path,
        "thread_action": "resumed",
        "raw_result": result,
    }


def resume_thread_from_slot(transport: JsonRpcAppServer, slot: str) -> dict[str, Any]:
    validate_slot_exists(slot)
    record = get_demo_record(slot)
    thread_id = str(record.get("thread_id", "")).strip()
    thread_path = str(record.get("thread_path", "")).strip()
    if not thread_id:
        raise DemoError(f"slot 没有可恢复的 thread: {slot}")
    resumed = resume_thread(transport, thread_id, thread_path)
    update_demo_record(slot, thread_id=thread_id, thread_path=thread_path, status="resumed", lifecycle="resume")
    return resumed


def fork_thread(transport: JsonRpcAppServer, thread_id: str, thread_path: str = "") -> dict[str, Any]:
    if not str(thread_id).strip():
        raise DemoError("thread_id 为空")
    result = transport.request("thread/fork", {"threadId": thread_id}, timeout_sec=DEFAULT_TIMEOUT_SEC)
    if "error" in result and "no rollout found" in str(result["error"]) and thread_path:
        wait_for_rollout_ready(thread_path, timeout_sec=5)
        result = transport.request("thread/fork", {"threadId": thread_id}, timeout_sec=DEFAULT_TIMEOUT_SEC)
    if "error" in result:
        raise DemoError(str(result["error"]))
    thread = ((result.get("result") or {}).get("thread") or {})
    new_thread_id = str(thread.get("id", "")).strip()
    new_thread_path = str(thread.get("path", "")).strip()
    if not new_thread_id:
        raise DemoError("thread/fork 未返回新 thread_id")
    return {
        "thread_id": new_thread_id,
        "thread_path": new_thread_path,
        "thread_action": "forked",
        "raw_result": result,
    }


def fork_thread_from_slot(transport: JsonRpcAppServer, parent_slot: str, slot: str) -> dict[str, Any]:
    validate_slot_exists(slot)
    validate_slot_exists(parent_slot)
    parent_record = get_demo_record(parent_slot)
    parent_thread_id = str(parent_record.get("thread_id", "")).strip()
    parent_thread_path = str(parent_record.get("thread_path", "")).strip()
    if not parent_thread_id:
        raise DemoError(f"父 slot 没有可 fork 的 thread: {parent_slot}")
    forked = fork_thread(transport, parent_thread_id, parent_thread_path)
    update_demo_record(
        slot,
        thread_id=forked["thread_id"],
        thread_path=forked["thread_path"],
        status="forked",
        lifecycle="fork",
        spawn_mode="fork",
        created_at=datetime.now(timezone.utc).isoformat(),
        parent_slot=parent_slot,
        parent_thread_id=parent_thread_id,
    )
    return forked


def rename_thread(transport: JsonRpcAppServer, thread_id: str, name: str) -> dict[str, Any]:
    try:
        result = transport.request("thread/name/set", {"threadId": thread_id, "name": name}, timeout_sec=DEFAULT_TIMEOUT_SEC)
        if "error" in result:
            return {"ok": False, "error": str(result["error"]), "raw_result": result}
        return {"ok": True, "error": "", "raw_result": result}
    except Exception as exc:
        return {"ok": False, "error": str(exc), "raw_result": None}


def wait_for_turn_completion(transport: JsonRpcAppServer, thread_id: str, turn_id: str, timeout_sec: int) -> str:
    deadline = time.time() + timeout_sec
    message_deltas: dict[str, list[str]] = {}
    completed_text = ""
    while time.time() < deadline:
        event = transport.next_event(timeout_sec=0.5)
        if event is not None:
            method = str(event.get("method", "")).strip()
            params = event.get("params") or {}
            if str(params.get("threadId", "")).strip() not in {"", thread_id}:
                continue
            if str(params.get("turnId", "")).strip() not in {"", turn_id}:
                continue
            if method == "item/agentMessage/delta":
                item_id = str(params.get("itemId", "")).strip()
                if item_id:
                    message_deltas.setdefault(item_id, []).append(str(params.get("delta", "")))
            if method == "item/completed":
                item = params.get("item") or {}
                item_type = str(item.get("type", "")).strip().lower()
                if item_type in {"agentmessage", "agent_message"}:
                    completed_text = str(item.get("text", "")).strip()
            if method == "turn/completed":
                turn = params.get("turn") or {}
                if str(turn.get("id", "")).strip() == turn_id:
                    if completed_text:
                        return completed_text
                    for chunks in message_deltas.values():
                        merged = "".join(chunks).strip()
                        if merged:
                            return merged
                    return ""
            msg = params.get("msg") or {}
            if method == "codex/event/task_complete" and str(msg.get("turn_id", "")).strip() == turn_id:
                if completed_text:
                    return completed_text
                for chunks in message_deltas.values():
                    merged = "".join(chunks).strip()
                    if merged:
                        return merged
                return ""
    raise DemoError(f"timeout waiting for turn completion: {turn_id}")


def start_turn(
    transport: JsonRpcAppServer,
    thread_id: str,
    prompt: str,
    is_plan: bool = False,
    effort: str = "low",
    skill_name: str = "",
    skill_path: str = "",
) -> dict[str, Any]:
    input_items: list[dict[str, Any]] = [{"type": "text", "text": prompt}]
    if skill_name and skill_path:
        input_items.append({"type": "skill", "name": skill_name, "path": skill_path})

    params: dict[str, Any] = {
        "threadId": thread_id,
        "cwd": str(REPO_ROOT),
        "input": input_items,
        "approvalPolicy": "never",
        "sandboxPolicy": {
            "type": "externalSandbox",
            "networkAccess": "enabled",
        },
        "effort": effort,
    }
    if is_plan:
        params["collaborationMode"] = {
            "mode": "plan",
            "settings": {
                "model": DEFAULT_MODEL,
                "reasoning_effort": effort,
                "developer_instructions": None,
            },
        }

    result = transport.request("turn/start", params, timeout_sec=PLAN_TIMEOUT_SEC if is_plan else DEFAULT_TIMEOUT_SEC)
    if "error" in result:
        raise DemoError(str(result["error"]))
    turn_id = str(((result.get("result") or {}).get("turn") or {}).get("id", "")).strip()
    if not turn_id:
        turn_id = str((result.get("result") or {}).get("turnId", "")).strip()
    if not turn_id:
        raise DemoError("turn/start 未返回 turn_id")

    response_text = wait_for_turn_completion(
        transport,
        thread_id,
        turn_id,
        PLAN_TIMEOUT_SEC if is_plan else DEFAULT_TIMEOUT_SEC,
    )
    return {
        "turn_id": turn_id,
        "response_text": response_text,
    }


def parse_json_text(text: str) -> dict[str, Any] | None:
    try:
        return json.loads(text)
    except Exception:
        return None


def build_seed_prompt(label: str, is_test: bool) -> str:
    return (
        "只返回 JSON："
        + json.dumps(
            {
                "ok": True,
                "identity_label": label,
                "phase": "connectivity",
                "test_mode": bool(is_test),
            },
            ensure_ascii=False,
        )
    )


def build_identity_prompt(slot: str, thread_id: str, is_test: bool) -> str:
    return (
        "只返回 JSON："
        + json.dumps(
            {
                "ok": True,
                "identity_label": slot,
                "thread_id": thread_id,
                "phase": "identity_confirm",
                "test_mode": bool(is_test),
            },
            ensure_ascii=False,
        )
    )


def run_once(
    transport: JsonRpcAppServer,
    thread_op: str,
    slot: str,
    parent_slot: str,
    force_new: bool,
    rename_requested: str,
    prompt: str,
    identity: bool,
    is_plan: bool,
    effort: str,
    skill_name: str,
    is_test: bool,
) -> dict[str, Any]:
    if thread_op == "new":
        thread_result = new_thread(transport, slot=slot, force_new=force_new)
    elif thread_op == "resume":
        thread_result = resume_thread_from_slot(transport, slot=slot)
    elif thread_op == "fork":
        thread_result = fork_thread_from_slot(transport, parent_slot=parent_slot, slot=slot)
    else:
        raise DemoError(f"不支持的 thread_op: {thread_op}")

    thread_id = str(thread_result["thread_id"]).strip()
    thread_path = str(thread_result.get("thread_path", "")).strip()
    slot_record = get_demo_record(slot)
    created_at_iso = str(slot_record.get("created_at", "")).strip() or datetime.now(timezone.utc).isoformat()
    try:
        created_compact = datetime.fromisoformat(created_at_iso).strftime("%Y%m%d%H%M%S")
    except Exception:
        created_compact = now_compact_ts()
    spawn_mode = str(slot_record.get("spawn_mode", "")).strip() or thread_op
    parent_thread_id = str(slot_record.get("parent_thread_id", "")).strip()

    rename_result = {"ok": False, "error": "", "raw_result": None}
    if rename_requested != "":
        rename_label = (
            rename_requested
            if rename_requested != "__AUTO__"
            else build_thread_name(slot, thread_id, created_compact, spawn_mode, parent_thread_id)
        )
        rename_result = rename_thread(transport, thread_id, rename_label)
        update_demo_record(slot, thread_name=rename_label, rename_error=rename_result["error"])

    turn_result = None
    response_json = None
    rollout_ready = False
    rollout_error = ""
    skill_path = validate_skill_exists(skill_name)

    should_start_turn = bool(prompt or identity or is_plan or skill_name or thread_op == "new")
    if should_start_turn:
        if identity:
            turn_prompt = build_identity_prompt(slot, thread_id, is_test=is_test)
        elif prompt:
            turn_prompt = prompt
        else:
            current_label = str(get_demo_record(slot).get("thread_name", "")).strip() or build_thread_name(
                slot,
                thread_id,
                created_compact,
                spawn_mode,
                parent_thread_id,
            )
            turn_prompt = build_seed_prompt(current_label, is_test=is_test)

        if is_test and not prompt and not identity:
            turn_prompt = '只返回 JSON：{"ok": true, "phase": "connectivity"}'
        if is_test and identity:
            turn_prompt = '只返回 JSON：{"ok": true, "phase": "identity_confirm"}'

        turn_result = start_turn(
            transport=transport,
            thread_id=thread_id,
            prompt=turn_prompt,
            is_plan=is_plan,
            effort=effort,
            skill_name=skill_name,
            skill_path=skill_path,
        )
        response_json = parse_json_text(turn_result["response_text"])
        if thread_path:
            try:
                wait_for_rollout_ready(thread_path, timeout_sec=5)
                rollout_ready = True
            except Exception as exc:
                rollout_error = str(exc)
        update_demo_record(
            slot,
            last_turn_id=str((turn_result or {}).get("turn_id", "")).strip(),
            last_status="ready" if response_json is not None else "turn_completed_non_json",
            last_mode="plan" if is_plan else "default",
            last_skill=skill_name,
            rollout_ready=rollout_ready,
            rollout_error=rollout_error,
        )

    return {
        "ok": True,
        "err_code": 0,
        "thread_op": thread_op,
        "slot": slot,
        "parent_slot": parent_slot,
        "thread_action": thread_result["thread_action"],
        "thread_id": thread_id,
        "thread_path": thread_path,
        "rename_ok": rename_result["ok"] if rename_requested != "" else None,
        "rename_error": rename_result["error"] if rename_requested != "" else "",
        "plan": is_plan,
        "effort": effort if is_plan else "",
        "skill": skill_name,
        "identity": bool(identity),
        "is_test": bool(is_test),
        "turn_id": (turn_result or {}).get("turn_id", ""),
        "response_text": (turn_result or {}).get("response_text", ""),
        "response_json": response_json,
        "rollout_ready": rollout_ready,
        "rollout_error": rollout_error,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--thread-op", required=True, choices=["new", "resume", "fork"])
    parser.add_argument("-s", "--slot", default=DEFAULT_SLOT)
    parser.add_argument("--parent-slot", default="")
    parser.add_argument("--rename", nargs="?", const="__AUTO__", default="")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--identity", action="store_true")
    parser.add_argument("--plan", nargs="?", const="low", default="")
    parser.add_argument("--skill", default="")
    parser.add_argument("--is-test", action="store_true")
    parser.add_argument("-new", action="store_true", dest="force_new")
    args = parser.parse_args()
    if not TOOLS_CONFIG_PATH.is_file():
        raise SystemExit(f"配置文件不存在: {TOOLS_CONFIG_PATH}")

    if args.plan and args.plan not in {"low", "medium", "high", "xhigh"}:
        raise SystemExit("--plan 只允许 low|medium|high|xhigh")
    if args.thread_op == "fork" and not str(args.parent_slot).strip():
        raise SystemExit("fork 模式必须提供 --parent-slot")

    log_dir = REPO_ROOT / "appserver_log"
    transport = JsonRpcAppServer(
        REPO_ROOT,
        events_path=log_dir / f"demo.{args.thread_op}.{args.slot}.events.jsonl",
        stderr_path=log_dir / f"demo.{args.thread_op}.{args.slot}.stderr.log",
    )
    try:
        transport.start()
        initialize_transport(transport)
        result = run_once(
            transport=transport,
            thread_op=args.thread_op,
            slot=args.slot,
            parent_slot=args.parent_slot,
            force_new=args.force_new,
            rename_requested=args.rename,
            prompt=args.prompt,
            identity=bool(args.identity),
            is_plan=bool(args.plan),
            effort=args.plan or "low",
            skill_name=str(args.skill).strip(),
            is_test=bool(args.is_test),
        )
        result["events_file"] = str(log_dir / f"demo.{args.thread_op}.{args.slot}.events.jsonl")
        result["stderr_file"] = str(log_dir / f"demo.{args.thread_op}.{args.slot}.stderr.log")
    except Exception as exc:
        result = {
            "ok": False,
            "err_code": 1,
            "thread_op": args.thread_op or "",
            "error": str(exc),
        }
    finally:
        transport.close()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
