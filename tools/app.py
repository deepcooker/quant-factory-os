from __future__ import annotations

import argparse
import json
import queue
import subprocess
import threading
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_CONFIG_PATH = REPO_ROOT / "tools" / "project_config.json"
DEFAULT_MODEL = "gpt-5.4"
DEFAULT_TIMEOUT_SEC = 60
PLAN_TIMEOUT_SEC = 300


@dataclass
class SkillRef:
    name: str
    path: str


class AppServerProtocolError(Exception):
    pass


class AppServerTimeoutError(Exception):
    pass


class AppServerClient:
    def __init__(
        self,
        codex_bin: str = "codex",
        cwd: Optional[str] = None,
        startup_timeout: float = 10.0,
        event_timeout: float = 120.0,
        model: str = DEFAULT_MODEL,
    ):
        self.codex_bin = codex_bin
        self.cwd = cwd or str(REPO_ROOT)
        self.startup_timeout = startup_timeout
        self.event_timeout = event_timeout
        self.model = model

        self.proc: Optional[subprocess.Popen[str]] = None
        self._reader_thread: Optional[threading.Thread] = None
        self._stderr_thread: Optional[threading.Thread] = None
        self._line_queue: "queue.Queue[Dict[str, Any]]" = queue.Queue()
        self._pending: deque[dict[str, Any]] = deque()
        self._request_id = 0
        self._thread_paths: Dict[str, str] = {}

    # ----------------------------
    # lifecycle
    # ----------------------------

    def start(self) -> None:
        if self.proc is not None:
            return

        self.proc = subprocess.Popen(
            [self.codex_bin, "app-server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=self.cwd,
            text=True,
            bufsize=1,
        )

        if self.proc.stdin is None or self.proc.stdout is None or self.proc.stderr is None:
            raise RuntimeError("app-server stdio 未正确建立")

        self._reader_thread = threading.Thread(target=self._reader_loop, daemon=True)
        self._stderr_thread = threading.Thread(target=self._stderr_loop, daemon=True)
        self._reader_thread.start()
        self._stderr_thread.start()

        self.initialize()

    def stop(self) -> None:
        if self.proc is None:
            return
        try:
            if self.proc.stdin is not None and not self.proc.stdin.closed:
                self.proc.stdin.close()
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=3)
        finally:
            self.proc = None

    def _reader_loop(self) -> None:
        assert self.proc is not None
        assert self.proc.stdout is not None

        for line in self.proc.stdout:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            self._line_queue.put(msg)

    def _stderr_loop(self) -> None:
        assert self.proc is not None
        assert self.proc.stderr is not None
        for _line in self.proc.stderr:
            pass

    # ----------------------------
    # low-level rpc
    # ----------------------------

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _send(self, message: Dict[str, Any]) -> None:
        if self.proc is None or self.proc.stdin is None:
            raise RuntimeError("app-server 尚未启动")
        self.proc.stdin.write(json.dumps(message, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    def _request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        req_id = self._next_id()
        self._send({"id": req_id, "method": method, "params": params})

        deadline = time.time() + self.startup_timeout

        if self._pending:
            new_pending: deque[dict[str, Any]] = deque()
            while self._pending:
                msg = self._pending.popleft()
                if msg.get("id") == req_id:
                    if "error" in msg:
                        raise AppServerProtocolError(f"{method} 调用失败: {msg['error']}")
                    return msg.get("result", {})
                new_pending.append(msg)
            self._pending = new_pending

        while time.time() < deadline:
            try:
                msg = self._line_queue.get(timeout=max(0.1, deadline - time.time()))
            except queue.Empty:
                continue

            if msg.get("id") == req_id:
                if "error" in msg:
                    raise AppServerProtocolError(f"{method} 调用失败: {msg['error']}")
                return msg.get("result", {})
            self._pending.append(msg)

        raise AppServerTimeoutError(f"{method} 响应超时")

    def _notify(self, method: str, params: Dict[str, Any]) -> None:
        self._send({"method": method, "params": params})

    # ----------------------------
    # initialize
    # ----------------------------

    def initialize(self) -> None:
        self._request(
            "initialize",
            {
                "clientInfo": {
                    "name": "project-orchestrator",
                    "version": "0.2.0",
                },
                "capabilities": {"experimentalApi": True},
            },
        )
        self._notify("initialized", {})

    # ----------------------------
    # thread ops
    # ----------------------------

    def _remember_thread(self, thread_id: str, thread_path: str = "") -> None:
        thread_id = str(thread_id).strip()
        thread_path = str(thread_path).strip()
        if thread_id and thread_path:
            self._thread_paths[thread_id] = thread_path

    def wait_for_rollout_ready(self, thread_path: str, timeout_sec: int = 5) -> None:
        target = Path(str(thread_path).strip())
        if not str(thread_path).strip():
            return
        deadline = time.time() + timeout_sec
        while time.time() < deadline:
            if target.is_file():
                return
            time.sleep(0.2)
        raise AppServerTimeoutError(f"等待 rollout 文件超时: {thread_path}")

    def create_thread(self, title: str, cwd: Optional[str] = None) -> str:
        result = self._request(
            "thread/start",
            {
                "model": self.model,
                "cwd": cwd or self.cwd,
                "approvalPolicy": "never",
                "sandboxPolicy": {
                    "type": "externalSandbox",
                    "networkAccess": "enabled",
                },
                "name": title,
            },
        )
        thread = (result.get("thread") or {})
        thread_id = str(thread.get("id", "")).strip()
        thread_path = str(thread.get("path", "")).strip()
        if not thread_id:
            raise AppServerProtocolError("thread/start 未返回 thread_id")
        self._remember_thread(thread_id, thread_path)
        return thread_id

    def resume_thread(self, thread_id: str, thread_path: str = "") -> str:
        thread_id = str(thread_id).strip()
        if not thread_id:
            raise AppServerProtocolError("resume_thread 缺少 thread_id")
        if thread_path:
            self._remember_thread(thread_id, thread_path)
        thread_path = self._thread_paths.get(thread_id, "")
        try:
            self._request("thread/resume", {"threadId": thread_id})
        except AppServerProtocolError as exc:
            if "no rollout found" in str(exc) and thread_path:
                self.wait_for_rollout_ready(thread_path, timeout_sec=5)
                self._request("thread/resume", {"threadId": thread_id})
            else:
                raise
        return thread_id

    def fork_thread(self, parent_thread_id: str, title: str, parent_thread_path: str = "") -> str:
        parent_thread_id = str(parent_thread_id).strip()
        if not parent_thread_id:
            raise AppServerProtocolError("fork_thread 缺少 parent_thread_id")
        if parent_thread_path:
            self._remember_thread(parent_thread_id, parent_thread_path)
        parent_thread_path = self._thread_paths.get(parent_thread_id, "")
        try:
            result = self._request("thread/fork", {"threadId": parent_thread_id})
        except AppServerProtocolError as exc:
            if "no rollout found" in str(exc) and parent_thread_path:
                self.wait_for_rollout_ready(parent_thread_path, timeout_sec=5)
                result = self._request("thread/fork", {"threadId": parent_thread_id})
            else:
                raise
        thread = (result.get("thread") or {})
        thread_id = str(thread.get("id", "")).strip()
        thread_path = str(thread.get("path", "")).strip()
        if not thread_id:
            raise AppServerProtocolError("thread/fork 未返回新 thread_id")
        self._remember_thread(thread_id, thread_path)
        try:
            self.rename_thread(thread_id, title)
        except Exception:
            pass
        return thread_id

    def rename_thread(self, thread_id: str, name: str) -> Dict[str, Any]:
        try:
            self._request("thread/name/set", {"threadId": thread_id, "name": name})
            return {"ok": True, "error": ""}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}

    def _find_thread_path_in_config(self, thread_id: str) -> str:
        config = _load_config()
        for record in (config.get("demo_sessions") or {}).values():
            if str((record or {}).get("thread_id", "")).strip() == str(thread_id).strip():
                return str((record or {}).get("thread_path", "")).strip()
        return ""

    def run_business_turn(
        self,
        slot: str,
        prompt: str = "",
        force_new: bool = False,
        fork_thread: str = "",
        is_plan: bool = False,
        effort: str = "low",
        skill_name: str = "",
        cwd: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        rename: bool = True,
        identity: bool = False,
        is_test: bool = False,
        parent_slot: str = "",
    ) -> Dict[str, Any]:
        slot = str(slot).strip()
        if not slot:
            raise AppServerProtocolError("slot 不能为空")

        existing = _get_demo_record(slot)
        parent_thread_id = ""
        thread_action = ""

        if str(fork_thread).strip():
            parent_thread_id = str(fork_thread).strip()
            parent_thread_path = self._thread_paths.get(parent_thread_id, "") or self._find_thread_path_in_config(parent_thread_id)
            thread_id = self.fork_thread(parent_thread_id=parent_thread_id, title=f"demo-{slot}", parent_thread_path=parent_thread_path)
            thread_action = "forked"
            lifecycle = "fork"
        else:
            existing_thread_id = str(existing.get("thread_id", "")).strip()
            existing_thread_path = str(existing.get("thread_path", "")).strip()
            if existing_thread_id and not force_new:
                thread_id = self.resume_thread(existing_thread_id, existing_thread_path)
                thread_action = "resumed"
                lifecycle = "resume"
            else:
                thread_id = self.create_thread(title=f"demo-{slot}", cwd=cwd or self.cwd)
                thread_action = "started"
                lifecycle = "new"

        thread_path = self._thread_paths.get(thread_id, "") or str(existing.get("thread_path", "")).strip()
        thread_name = str(existing.get("thread_name", "")).strip()
        rename_result = {"ok": None, "error": ""}
        if rename:
            thread_name = _build_thread_name(slot, thread_id, thread_action if thread_action != "resumed" else lifecycle, parent_thread_id)
            rename_result = self.rename_thread(thread_id, thread_name)

        skill = _build_skill(skill_name)
        turn_result: Dict[str, Any] | None = None
        rollout_ready = False
        rollout_error = ""

        final_prompt = prompt or _build_demo_prompt(slot, thread_id, identity=identity, is_test=is_test)

        if final_prompt:
            turn_result = self.start_turn(
                thread_id=thread_id,
                text=final_prompt,
                skill=skill,
                metadata=metadata,
                cwd=cwd or self.cwd,
                is_plan=is_plan,
                effort=effort,
            )

        if thread_path:
            try:
                self.wait_for_rollout_ready(thread_path, timeout_sec=5)
                rollout_ready = True
            except Exception as exc:
                rollout_error = str(exc)

        _update_demo_record(
            slot,
            thread_id=thread_id,
            thread_path=thread_path,
            status="ready" if turn_result else thread_action,
            lifecycle=lifecycle,
            parent_slot=parent_slot,
            parent_thread_id=parent_thread_id,
            thread_name=thread_name,
            rename_error=rename_result["error"],
            last_turn_id=(turn_result or {}).get("turn_id", ""),
            last_status="ready" if turn_result and (turn_result.get("payload") is not None) else ("thread_ready" if not turn_result else "turn_completed_non_json"),
            last_mode="plan" if is_plan else "default",
            last_skill=str(skill_name).strip(),
            rollout_ready=rollout_ready,
            rollout_error=rollout_error,
        )

        return {
            "ok": True,
            "err_code": 0,
            "slot": slot,
            "thread_action": thread_action,
            "thread_id": thread_id,
            "thread_path": thread_path,
            "parent_thread_id": parent_thread_id,
            "thread_name": thread_name,
            "rename_ok": rename_result["ok"],
            "rename_error": rename_result["error"],
            "turn_id": (turn_result or {}).get("turn_id", ""),
            "final_text": (turn_result or {}).get("final_text", ""),
            "payload": (turn_result or {}).get("payload"),
            "rollout_ready": rollout_ready,
            "rollout_error": rollout_error,
        }

    # ----------------------------
    # turn/start
    # ----------------------------

    def start_turn(
        self,
        thread_id: str,
        text: str,
        skill: Optional[SkillRef] = None,
        metadata: Optional[Dict[str, Any]] = None,
        cwd: Optional[str] = None,
        is_plan: bool = False,
        effort: str = "low",
    ) -> Dict[str, Any]:
        input_items: List[Dict[str, Any]] = [{"type": "text", "text": text}]

        if skill is not None:
            input_items.append(
                {
                    "type": "skill",
                    "name": skill.name,
                    "path": skill.path,
                }
            )

        params: Dict[str, Any] = {
            "threadId": thread_id,
            "cwd": cwd or self.cwd,
            "input": input_items,
            "approvalPolicy": "never",
            "sandboxPolicy": {
                "type": "externalSandbox",
                "networkAccess": "enabled",
            },
            "effort": effort,
        }

        if metadata:
            params["metadata"] = metadata

        if is_plan:
            params["collaborationMode"] = {
                "mode": "plan",
                "settings": {
                    "model": self.model,
                    "reasoning_effort": effort,
                    "developer_instructions": None,
                },
            }

        result = self._request("turn/start", params)
        turn = result.get("turn") or {}
        turn_id = str(turn.get("id", "")).strip() or str(result.get("turnId", "")).strip()
        if not turn_id:
            raise AppServerProtocolError("turn/start 未返回 turnId")

        return self._collect_turn_result(thread_id=thread_id, turn_id=turn_id)

    # ----------------------------
    # event collection
    # ----------------------------

    def _collect_turn_result(self, thread_id: str, turn_id: str) -> Dict[str, Any]:
        deadline = time.time() + self.event_timeout
        raw_events: List[Dict[str, Any]] = []
        text_chunks: List[str] = []
        completed_text = ""
        turn_completed = False

        while time.time() < deadline:
            try:
                msg = self._line_queue.get(timeout=0.5)
            except queue.Empty:
                continue

            raw_events.append(msg)
            method = str(msg.get("method", "")).strip()
            params = msg.get("params", {}) or {}

            if str(params.get("threadId", "")).strip() not in {"", thread_id}:
                continue
            if str(params.get("turnId", "")).strip() not in {"", turn_id}:
                continue

            if method == "item/agentMessage/delta":
                delta = params.get("delta", "")
                if isinstance(delta, str):
                    text_chunks.append(delta)

            elif method == "item/completed":
                item = params.get("item", {}) or {}
                item_type = str(item.get("type", "")).strip().lower()
                if item_type in {"agentmessage", "agent_message"}:
                    text = str(item.get("text", "")).strip()
                    if text:
                        completed_text = text

            elif method == "turn/completed":
                turn = params.get("turn", {}) or {}
                if str(turn.get("id", "")).strip() == turn_id:
                    turn_completed = True
                    break

            elif method == "turn/failed":
                if str(params.get("turnId", "")).strip() == turn_id:
                    raise AppServerProtocolError(f"turn 失败: {params}")

            elif method == "codex/event/task_complete":
                msg_payload = params.get("msg", {}) or {}
                if str(msg_payload.get("turn_id", "")).strip() == turn_id:
                    turn_completed = True
                    break

        if not turn_completed:
            raise AppServerTimeoutError(f"turn {turn_id} 执行超时")

        final_text = completed_text or "".join(text_chunks).strip()
        final_payload = self._extract_json_from_text(final_text)

        return {
            "thread_id": thread_id,
            "turn_id": turn_id,
            "raw_events": raw_events,
            "final_text": final_text,
            "payload": final_payload,
        }

    # ----------------------------
    # payload extraction
    # ----------------------------

    def _extract_payload_from_item(self, item: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        candidates: List[str] = []

        if "text" in item and isinstance(item["text"], str):
            candidates.append(item["text"])

        content = item.get("content")
        if isinstance(content, list):
            for part in content:
                if isinstance(part, dict):
                    txt = part.get("text")
                    if isinstance(txt, str):
                        candidates.append(txt)

        for text in candidates:
            payload = self._extract_json_from_text(text)
            if payload is not None:
                return payload

        return None

    def _extract_json_from_text(self, text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None

        start_marker = "```json"
        end_marker = "```"

        start = text.find(start_marker)
        if start != -1:
            start += len(start_marker)
            end = text.find(end_marker, start)
            if end != -1:
                candidate = text[start:end].strip()
                try:
                    parsed = json.loads(candidate)
                    if isinstance(parsed, dict):
                        return parsed
                except json.JSONDecodeError:
                    pass

        stripped = text.strip()
        if stripped.startswith("{") and stripped.endswith("}"):
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass

        return None


def _load_config() -> dict[str, Any]:
    return json.loads(TOOLS_CONFIG_PATH.read_text(encoding="utf-8"))


def _save_config(config: dict[str, Any]) -> None:
    TOOLS_CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _get_demo_record(slot: str) -> dict[str, Any]:
    config = _load_config()
    return dict((config.setdefault("demo_sessions", {})).get(slot, {}) or {})


def _update_demo_record(slot: str, **fields: Any) -> None:
    config = _load_config()
    demo_sessions = config.setdefault("demo_sessions", {})
    record = demo_sessions.setdefault(slot, {})
    record.update(fields)
    record["updated_at"] = datetime.now(timezone.utc).isoformat()
    _save_config(config)


def _build_thread_name(slot: str, thread_id: str, spawn_mode: str, parent_thread_id: str = "") -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    name = f"{slot}:{thread_id}:{ts}:{spawn_mode}"
    if parent_thread_id:
        name += f":fork_by_{parent_thread_id}"
    return name


def _build_demo_prompt(slot: str, thread_id: str, identity: bool, is_test: bool) -> str:
    if is_test and identity:
        return '只返回 JSON：{"ok": true, "phase": "identity_confirm"}'
    if is_test:
        return '只返回 JSON：{"ok": true, "phase": "connectivity"}'
    payload = {
        "ok": True,
        "slot": slot,
        "thread_id": thread_id,
        "phase": "identity_confirm" if identity else "connectivity",
    }
    return "只返回 JSON：" + json.dumps(payload, ensure_ascii=False)


def _build_skill(skill_name: str) -> Optional[SkillRef]:
    skill_name = str(skill_name).strip()
    if not skill_name:
        return None
    skill_path = REPO_ROOT / ".agents" / "skills" / skill_name / "SKILL.md"
    if not skill_path.is_file():
        raise SystemExit(f"skill 不存在: {skill_path}")
    return SkillRef(name=skill_name, path=str(skill_path))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--thread-op", required=True, choices=["new", "resume", "fork"])
    parser.add_argument("-s", "--slot", required=True)
    parser.add_argument("--parent-slot", default="")
    parser.add_argument("--rename", action="store_true")
    parser.add_argument("--identity", action="store_true")
    parser.add_argument("--plan", nargs="?", const="low", default="")
    parser.add_argument("--skill", default="")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--is-test", action="store_true")
    parser.add_argument("-new", action="store_true", dest="force_new")
    args = parser.parse_args()

    if args.plan and args.plan not in {"low", "medium", "high", "xhigh"}:
        raise SystemExit("--plan 只允许 low|medium|high|xhigh")
    if args.thread_op == "fork" and not str(args.parent_slot).strip():
        raise SystemExit("fork 模式必须提供 --parent-slot")

    client = AppServerClient(cwd=str(REPO_ROOT))
    client.start()
    try:
        fork_thread = ""
        if args.thread_op == "fork":
            parent = _get_demo_record(args.parent_slot)
            fork_thread = str(parent.get("thread_id", "")).strip()
        result = client.run_business_turn(
            slot=args.slot,
            prompt=args.prompt,
            force_new=bool(args.force_new),
            fork_thread=fork_thread,
            is_plan=bool(args.plan),
            effort=args.plan or "low",
            skill_name=str(args.skill).strip(),
            cwd=str(REPO_ROOT),
            metadata={"phase": "demo_identity" if args.identity else "demo_connectivity"},
            rename=bool(args.rename),
            identity=bool(args.identity),
            is_test=bool(args.is_test),
            parent_slot=args.parent_slot,
        )
        result.update(
            {
                "thread_op": args.thread_op,
                "parent_slot": args.parent_slot,
                "plan": bool(args.plan),
                "effort": args.plan or "",
                "skill": str(args.skill).strip(),
                "identity": bool(args.identity),
                "is_test": bool(args.is_test),
            }
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "err_code": 1,
                    "thread_op": args.thread_op,
                    "slot": args.slot,
                    "error": str(exc),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    finally:
        client.stop()


if __name__ == "__main__":
    main()
