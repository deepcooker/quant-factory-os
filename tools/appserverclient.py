#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
import os
import queue
import shutil
import subprocess
import sys
import threading
import time
from collections import deque
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Deque

try:
    from tools.project_config import (
        REPO_ROOT,
        clear_session_registry,
        describe_runtime_state,
        get_session_registry,
        get_session_thread_id,
        get_session_thread_path,
        load_unified_config,
        load_runtime_state,
        require_session_thread_id,
        update_session_registry,
        update_current_summary,
    )
    from tools.result_schema import ERR_CONFIG_BASE, ERR_SESSION_BASE, err, ok
    from tools.taskclient import (
        get_role_threads,
        get_role_summaries,
        load_active_task,
        normalize_role,
        refresh_run_main_resolution,
        refresh_task_escalation,
        refresh_task_gap_summary,
        update_test_gate,
        update_role_summary,
        update_role_thread,
        update_task_summary,
    )
except Exception:  # pragma: no cover
    from project_config import (  # type: ignore
        REPO_ROOT,
        clear_session_registry,
        describe_runtime_state,
        get_session_registry,
        get_session_thread_id,
        get_session_thread_path,
        load_unified_config,
        load_runtime_state,
        require_session_thread_id,
        update_session_registry,
        update_current_summary,
    )
    from result_schema import ERR_CONFIG_BASE, ERR_SESSION_BASE, err, ok  # type: ignore
    from taskclient import (  # type: ignore
        get_role_threads,
        get_role_summaries,
        load_active_task,
        normalize_role,
        refresh_run_main_resolution,
        refresh_task_escalation,
        refresh_task_gap_summary,
        update_test_gate,
        update_role_summary,
        update_role_thread,
        update_task_summary,
    )


UNIFIED_CONFIG = load_unified_config()
CODEX_CONFIG = dict(UNIFIED_CONFIG["codex"])
RUNTIME_DEFAULTS = dict(UNIFIED_CONFIG["runtime_defaults"])

CODEX_BIN = str(CODEX_CONFIG["bin"])
CODEX_APP_SERVER_SUBCOMMAND = str(CODEX_CONFIG["app_server_subcommand"])
CODEX_CLIENT_NAME = str(CODEX_CONFIG["client_name"])
CODEX_CLIENT_VERSION = str(CODEX_CONFIG["client_version"])
CODEX_CAPABILITIES = dict(CODEX_CONFIG["capabilities"])

DEFAULT_PROJECT_ROOT = Path(str(UNIFIED_CONFIG["project_root"]))
DEFAULT_CODEX_HOME = str(CODEX_CONFIG["home"]).strip() or None
DEFAULT_MODEL = str(RUNTIME_DEFAULTS["default_model"])
DEFAULT_MODE = str(RUNTIME_DEFAULTS["default_mode"])
DEFAULT_EFFORT = str(RUNTIME_DEFAULTS["default_effort"])
DEFAULT_TIMEOUT_SEC = int(RUNTIME_DEFAULTS["default_timeout_sec"])
PLAN_TIMEOUT_SEC = int(RUNTIME_DEFAULTS["plan_timeout_sec"])

DEFAULT_THREAD_NAME = str(RUNTIME_DEFAULTS["default_thread_name"])
DEFAULT_THREAD_SEARCH_LIMIT = int(RUNTIME_DEFAULTS["default_thread_search_limit"])
DEFAULT_TURN_TEXT = str(RUNTIME_DEFAULTS["default_turn_text"])
LEARN_INIT_THREAD_NAME = str(RUNTIME_DEFAULTS["learn_init_thread_name"])
LEARN_INIT_EFFORT = str(RUNTIME_DEFAULTS["learn_init_effort"])
LEARN_INIT_TURN_TEXT = str(RUNTIME_DEFAULTS["learn_init_turn_text"])

DEFAULT_EVENTS_FILE = REPO_ROOT / "test_app.events.jsonl"
DEFAULT_STDERR_FILE = REPO_ROOT / "test_app.stderr.log"
LEARN_INIT_EVENTS_FILE = REPO_ROOT / "test_app.learn_init.events.jsonl"
LEARN_INIT_STDERR_FILE = REPO_ROOT / "test_app.learn_init.stderr.log"
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGER_NAME = "qf.appserverclient"
logger = logging.getLogger(LOGGER_NAME)


class AppServerError(RuntimeError):
    pass


#codex 中文：统一打印当前运行状态，保证 appserverclient 入口与 project_config 的状态口径一致。
def log_active_task() -> None:
    try:
        task = load_active_task()
    except Exception as exc:
        logger.info("APP_ACTIVE_TASK_UNAVAILABLE: %s", exc)
        return
    logger.info("APP_ACTIVE_TASK_START")
    logger.info("active_task.task_id=%s", str(task.get("task_id", "")).strip() or "(none)")
    logger.info("active_task.title=%s", str(task.get("title", "")).strip() or "(none)")
    logger.info("active_task.status=%s", str(task.get("status", "")).strip() or "(none)")
    logger.info("active_task.run_id=%s", str(task.get("run_id", "")).strip() or "(none)")
    logger.info("APP_ACTIVE_TASK_END")


def log_runtime_state() -> None:
    runtime_state = load_runtime_state()
    logger.info("APP_RUNTIME_STATE_START")
    for line in describe_runtime_state(runtime_state):
        logger.info(line)
    logger.info("APP_RUNTIME_STATE_END")
    log_active_task()


#codex 中文：检查当前 thread 是否已有未收口的 inProgress turn，避免在同一工作副本上叠加新 turn。
def detect_inprogress_turn_ids(thread_payload: dict[str, Any]) -> list[str]:
    turn_ids: list[str] = []
    for turn in (thread_payload.get("turns") or []):
        if str((turn or {}).get("status", "")).strip() == "inProgress":
            turn_id = str((turn or {}).get("id", "")).strip()
            if turn_id:
                turn_ids.append(turn_id)
    return turn_ids


def load_prompt_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


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
            for candidate in (
                compact_text(str((item or {}).get("text", "")).strip()),
                "\n".join(collect_text_fragments((item or {}).get("content"))).strip(),
            ):
                text = compact_text(candidate)
                if text:
                    return text
    return ""


def build_summarize_current_text() -> str:
    runtime_state = load_runtime_state()
    active_task: dict[str, Any] = {}
    try:
        active_task = load_active_task()
    except Exception:
        active_task = {}
    prompt = load_prompt_text(REPO_ROOT / "tools" / "summarize_current_prompt.md")
    lines = [prompt, "", "当前运行态："]
    lines.append(f"- current_project_id: {str(runtime_state.current_project_id).strip() or '(none)'}")
    lines.append(f"- current_run_id: {str(runtime_state.current_run_id).strip() or '(none)'}")
    lines.append(f"- current_task_id: {str(runtime_state.current_task_id).strip() or '(none)'}")
    lines.append(f"- current_task_json_file: {str(runtime_state.current_task_json_file).strip() or '(none)'}")
    title = str(active_task.get("title", "")).strip()
    if title:
        lines.append(f"- active_task_title: {title}")
    lines.extend(
        [
            "",
            "输出要求：",
            "- 只输出可直接回灌 baseline 的中文摘要正文。",
            "- 结构固定为三段：主线更新 / 新的约束与风险 / 下一步。",
            "- 不要输出 JSON、标题外话或聊天复述。",
        ]
    )
    return "\n".join(lines).strip()


def build_summarize_role_text(role: str) -> str:
    runtime_state = load_runtime_state()
    active_task: dict[str, Any] = {}
    try:
        active_task = load_active_task()
    except Exception:
        active_task = {}
    prompt = load_prompt_text(REPO_ROOT / "tools" / "summarize_role_prompt.md")
    lines = [prompt, "", "当前运行态："]
    lines.append(f"- current_project_id: {str(runtime_state.current_project_id).strip() or '(none)'}")
    lines.append(f"- current_run_id: {str(runtime_state.current_run_id).strip() or '(none)'}")
    lines.append(f"- current_task_id: {str(runtime_state.current_task_id).strip() or '(none)'}")
    lines.append(f"- role: {str(role).strip() or '(none)'}")
    title = str(active_task.get("title", "")).strip()
    if title:
        lines.append(f"- active_task_title: {title}")
    goal = str(active_task.get("goal", "")).strip()
    if goal:
        lines.append(f"- active_task_goal: {goal}")
    lines.extend(
        [
            "",
            "输出要求：",
            "- 只输出可直接写入 task 机器层的中文 role summary 正文。",
            "- 结构固定为三段：本角色已完成 / 风险与阻塞 / 建议下一步。",
            "- 不要输出 JSON、标题外话或聊天复述。",
        ]
    )
    return "\n".join(lines).strip()


def load_run_summary_for_current_run() -> dict[str, Any]:
    runtime_state = load_runtime_state()
    run_id = str(runtime_state.current_run_id).strip()
    if not run_id:
        return {}
    run_summary_path = REPO_ROOT / "reports" / run_id / "run_summary.json"
    if not run_summary_path.exists():
        return {}
    try:
        return json.loads(run_summary_path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def format_run_summary_text(run_summary: dict[str, Any]) -> str:
    lines: list[str] = []
    run_goal = compact_text(str(run_summary.get("run_goal", "")).strip())
    if run_goal:
        lines.append(f"- run_goal: {run_goal}")
    for key in ("active_tasks", "completed_tasks", "source_tasks"):
        values = [str(item).strip() for item in list(run_summary.get(key, []) or []) if str(item).strip()]
        if values:
            lines.append(f"- {key}: {', '.join(values)}")
    for key in (
        "key_updates",
        "cross_task_decisions",
        "cross_task_risks",
        "verification_overview",
        "next_run_or_next_tasks",
    ):
        values = [compact_text(str(item).strip()) for item in list(run_summary.get(key, []) or []) if str(item).strip()]
        if not values:
            continue
        lines.append(f"- {key}:")
        for item in values:
            lines.append(f"  - {item}")
    return "\n".join(lines).strip()


def build_refresh_baseline_text(current_summary: dict[str, Any], run_summary: dict[str, Any] | None = None) -> str:
    prompt = load_prompt_text(REPO_ROOT / "tools" / "refresh_baseline_prompt.md")
    run_summary_text = format_run_summary_text(run_summary or {})
    current_summary_text = compact_text(str(current_summary.get("summary_text", "")).strip())
    lines = [prompt, ""]
    if run_summary_text:
        lines.extend(["run_summary:", run_summary_text, ""])
    elif current_summary_text:
        lines.extend(["current_summary:", current_summary_text, ""])
    else:
        raise AppServerError("run summary and current summary are both empty; run --set-run-summary or --summarize-current first")
    lines.extend(
        [
            "输出要求：",
            "- 只输出 baseline 应吸收的增量更新正文。",
            "- 覆盖主线理解、当前阶段、下一步，不复述聊天噪音。",
            "- 不要输出 JSON 或额外解释。",
        ]
    )
    return "\n".join(lines).strip()


class JsonRpcAppServer:
    #codex 中文：初始化底层 JSON-RPC 传输对象，持有 app-server 进程、消息队列和日志文件路径。
    def __init__(self, project_root: Path, codex_home: str | None, events_path: Path, stderr_path: Path) -> None:
        self.project_root = project_root
        self.codex_home = codex_home
        self.events_path = events_path
        self.stderr_path = stderr_path
        self.proc: subprocess.Popen[str] | None = None
        self._reader_thread: threading.Thread | None = None
        self._stderr_thread: threading.Thread | None = None
        self._messages: "queue.Queue[dict[str, Any]]" = queue.Queue()
        self._pending: Deque[dict[str, Any]] = deque()
        self._next_id = 1
        self._events_fp = None
        self._stderr_fp = None

    #codex 中文：启动 `codex app-server` 子进程，并开始读取 stdout/stderr 事件流。
    def start(self) -> None:
        env = None
        if self.codex_home:
            env = os.environ.copy()
            env.update({"CODEX_HOME": self.codex_home})
        self._events_fp = self.events_path.open("w", encoding="utf-8")
        self._stderr_fp = self.stderr_path.open("w", encoding="utf-8")
        self.proc = subprocess.Popen(
            [CODEX_BIN, CODEX_APP_SERVER_SUBCOMMAND],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=str(self.project_root),
            env=env,
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

    #codex 中文：关闭当前 app-server 子进程和相关读线程，不删除任何 thread/session 历史。
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

    #codex 中文：向 app-server 发送一条原始 JSON-RPC 消息。
    def _send(self, payload: dict[str, Any]) -> None:
        if self.proc is None or self.proc.stdin is None:
            raise AppServerError("app-server is not running")
        self.proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    #codex 中文：发送不需要返回值的 JSON-RPC 通知。
    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        self._send({"method": method, "params": params or {}})

    #codex 中文：发送 JSON-RPC 请求并等待匹配同一个 id 的原始响应 JSON。
    def request(self, method: str, params: dict[str, Any] | None = None, timeout_sec: int = DEFAULT_TIMEOUT_SEC) -> dict[str, Any]:
        req_id = self._next_id
        self._next_id += 1
        self._send({"id": req_id, "method": method, "params": params or {}})
        deadline = time.time() + timeout_sec

        if self._pending:
            new_pending: Deque[dict[str, Any]] = deque()
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
        raise AppServerError(f"timeout waiting for {method}")

    #codex 中文：读取下一条事件 JSON，供 turn 流式消费。
    def next_event(self, timeout_sec: float = 1.0) -> dict[str, Any] | None:
        if self._pending:
            return self._pending.popleft()
        try:
            return self._messages.get(timeout=timeout_sec)
        except queue.Empty:
            return None


class CodexAppClient:
    #codex 中文：初始化高层 client，保存项目路径、模型常量、thread 上下文和 transport 配置。
    def __init__(
        self,
        project_root: Path = DEFAULT_PROJECT_ROOT,
        codex_home: str | None = DEFAULT_CODEX_HOME,
        model: str = DEFAULT_MODEL,
        mode: str = DEFAULT_MODE,
        effort: str = DEFAULT_EFFORT,
        timeout_sec: int = DEFAULT_TIMEOUT_SEC,
        events_file: Path = DEFAULT_EVENTS_FILE,
        stderr_file: Path = DEFAULT_STDERR_FILE,
    ) -> None:
        self.project_root = project_root
        self.codex_home = codex_home
        self.model = model
        self.mode = mode
        self.effort = effort
        self.timeout_sec = timeout_sec
        self.events_file = events_file
        self.stderr_file = stderr_file
        self.current_thread_id = ""
        self.transport: JsonRpcAppServer | None = None
        self.logger = logger

    #codex 中文：打印方法级请求和响应日志，便于协议调试。
    def _log_request_response(self, method: str, request_json: dict[str, Any], response_json: dict[str, Any]) -> None:
        self.logger.info("%s REQUEST_JSON=%s", method, json.dumps(request_json, ensure_ascii=False))
        self.logger.info("%s RESPONSE_JSON=%s", method, json.dumps(response_json, ensure_ascii=False))

    #codex 中文：确保底层 transport 已连接，未连接时直接报错。
    def _require_transport(self) -> JsonRpcAppServer:
        if self.transport is None:
            raise AppServerError("client is not connected")
        return self.transport

    #codex 中文：建立 app-server 连接，并完成 `initialize` / `initialized` 连接级初始化。
    def connect(self, project_root: Path | None = None, codex_home: str | None = None) -> dict[str, Any]:
        if shutil.which(CODEX_BIN) is None:
            raise AppServerError("codex not found in PATH")
        if project_root is not None:
            self.project_root = project_root
        if codex_home is not None:
            self.codex_home = codex_home
        self.transport = JsonRpcAppServer(self.project_root, self.codex_home, self.events_file, self.stderr_file)
        self.transport.start()
        request_json = {
            "id": 1,
            "method": "initialize",
            "params": {
                "clientInfo": {"name": CODEX_CLIENT_NAME, "version": CODEX_CLIENT_VERSION},
                "capabilities": CODEX_CAPABILITIES,
            },
        }
        response_json = self.transport.request("initialize", request_json["params"], timeout_sec=self.timeout_sec)
        if "error" in response_json:
            raise AppServerError(str(response_json["error"]))
        self.transport.notify("initialized", {})
        return response_json

    #codex 中文：切换当前活跃 thread，只修改 client 内部上下文，不发网络请求。
    def switch_thread(self, thread_id: str) -> None:
        self.current_thread_id = thread_id.strip()
        if not self.current_thread_id:
            raise AppServerError("thread_id is empty")
        self.logger.info("switch_thread CURRENT_THREAD_ID=%s", self.current_thread_id)

    #codex 中文：创建新的 thread，可选设置名称，并把返回的 thread_id 设为当前 thread。
    def start_thread(self, name: str | None = None) -> dict[str, Any]:
        transport = self._require_transport()
        params = {"model": self.model, "cwd": str(self.project_root)}
        if name:
            params["name"] = name
        request_json = {"method": "thread/start", "params": params}
        response_json = transport.request("thread/start", params, timeout_sec=self.timeout_sec)
        self._log_request_response("thread/start", request_json, response_json)
        if "error" in response_json:
            raise AppServerError(str(response_json["error"]))
        thread_id = ((response_json.get("result") or {}).get("thread") or {}).get("id", "")
        self.switch_thread(str(thread_id))
        return response_json

    #codex 中文：列出当前运行时可见的 threads，默认按当前项目 cwd 过滤。
    def list_threads(self, limit: int = DEFAULT_THREAD_SEARCH_LIMIT) -> dict[str, Any]:
        transport = self._require_transport()
        params = {"cwd": str(self.project_root), "limit": limit}
        request_json = {"method": "thread/list", "params": params}
        response_json = transport.request("thread/list", params, timeout_sec=self.timeout_sec)
        self._log_request_response("thread/list", request_json, response_json)
        if "error" in response_json:
            raise AppServerError(str(response_json["error"]))
        return response_json

    #codex 中文：读取指定 thread 的详情，可选携带 turn 历史。
    def read_thread(self, thread_id: str, include_turns: bool = True) -> dict[str, Any]:
        transport = self._require_transport()
        params = {"threadId": thread_id, "includeTurns": include_turns}
        request_json = {"method": "thread/read", "params": params}
        response_json = transport.request("thread/read", params, timeout_sec=self.timeout_sec)
        self._log_request_response("thread/read", request_json, response_json)
        if "error" in response_json:
            raise AppServerError(str(response_json["error"]))
        return response_json

    #codex 中文：恢复指定 thread，并把它切成当前活跃 thread。
    def resume_thread(self, thread_id: str) -> dict[str, Any]:
        transport = self._require_transport()
        params = {"threadId": thread_id}
        request_json = {"method": "thread/resume", "params": params}
        response_json = transport.request("thread/resume", params, timeout_sec=self.timeout_sec)
        self._log_request_response("thread/resume", request_json, response_json)
        if "error" in response_json:
            raise AppServerError(str(response_json["error"]))
        self.switch_thread(thread_id)
        return response_json

    #codex 中文：基于指定 thread 派生一个 fork 出来的新 thread，并把新 thread 切成当前活跃 thread。
    def fork_thread(self, thread_id: str) -> dict[str, Any]:
        transport = self._require_transport()
        params = {"threadId": thread_id}
        request_json = {"method": "thread/fork", "params": params}
        response_json = transport.request("thread/fork", params, timeout_sec=self.timeout_sec)
        self._log_request_response("thread/fork", request_json, response_json)
        if "error" in response_json:
            raise AppServerError(str(response_json["error"]))
        new_thread_id = ((response_json.get("result") or {}).get("thread") or {}).get("id", "")
        self.switch_thread(str(new_thread_id))
        return response_json

    #codex 中文：给指定 thread 设置名字，底层协议方法名是 `thread/name/set`。
    def set_thread_name(self, thread_id: str, name: str) -> dict[str, Any]:
        transport = self._require_transport()
        params = {"threadId": thread_id, "name": name}
        request_json = {"method": "thread/name/set", "params": params}
        response_json = transport.request("thread/name/set", params, timeout_sec=self.timeout_sec)
        self._log_request_response("thread/name/set", request_json, response_json)
        if "error" in response_json:
            raise AppServerError(str(response_json["error"]))
        return response_json

    #codex 中文：发起指定 thread 的 compact，请求模型压缩该 thread 的上下文。
    def compact_thread(self, thread_id: str) -> dict[str, Any]:
        transport = self._require_transport()
        params = {"threadId": thread_id}
        request_json = {"method": "thread/compact/start", "params": params}
        response_json = transport.request("thread/compact/start", params, timeout_sec=self.timeout_sec)
        self._log_request_response("thread/compact/start", request_json, response_json)
        if "error" in response_json:
            raise AppServerError(str(response_json["error"]))
        return response_json

    #codex 中文：在当前活跃 thread 里发起一轮 turn，把文本交给 Codex 处理。
    def start_turn(self, text: str) -> dict[str, Any]:
        transport = self._require_transport()
        if not self.current_thread_id:
            raise AppServerError("current_thread_id is empty; call start_thread/resume_thread/switch_thread first")
        params = {
            "threadId": self.current_thread_id,
            "cwd": str(self.project_root),
            "input": [{"type": "text", "text": text}],
            "collaborationMode": {
                "mode": self.mode,
                "settings": {
                    "model": self.model,
                    "reasoning_effort": self.effort,
                    "developer_instructions": None,
                },
            },
            "sandboxPolicy": {"type": "readOnly"},
            "effort": self.effort,
        }
        request_json = {"method": "turn/start", "params": params}
        response_json = transport.request("turn/start", params, timeout_sec=self.timeout_sec)
        self._log_request_response("turn/start", request_json, response_json)
        if "error" in response_json:
            raise AppServerError(str(response_json["error"]))
        return response_json

    #codex 中文：查询 app-server 当前支持的 collaboration modes，便于对齐 learn 的计划模式调用链。
    def list_collaboration_modes(self) -> dict[str, Any]:
        transport = self._require_transport()
        params: dict[str, Any] = {}
        request_json = {"method": "collaborationMode/list", "params": params}
        response_json = transport.request("collaborationMode/list", params, timeout_sec=self.timeout_sec)
        self._log_request_response("collaborationMode/list", request_json, response_json)
        if "error" in response_json:
            raise AppServerError(str(response_json["error"]))
        return response_json

    #codex 中文：等待当前 turn 真正收口，直到收到 `task_complete` 或匹配 turn_id 的 `turn/completed`。
    def wait_for_turn_completion(self, turn_id: str) -> dict[str, Any]:
        transport = self._require_transport()
        deadline = time.time() + self.timeout_sec
        while time.time() < deadline:
            event = transport.next_event(timeout_sec=1.0)
            if event is None:
                continue
            method = str(event.get("method", "")).strip()
            params = event.get("params") or {}
            if method == "turn/completed":
                turn = params.get("turn") or {}
                if str(turn.get("id", "")).strip() == turn_id:
                    return event
            msg = params.get("msg") or {}
            if method == "codex/event/task_complete":
                if str(msg.get("turn_id", "")).strip() == turn_id:
                    return event
        raise AppServerError(f"timeout waiting for turn completion: {turn_id}")

    #codex 中文：在 turn 收口后继续等待 rollout 文件真正落盘，避免过早 fork 导致 no rollout found。
    def wait_for_rollout_ready(self, rollout_path: str, timeout_sec: int | None = None) -> Path:
        if not rollout_path.strip():
            raise AppServerError("rollout_path is empty")
        target = Path(rollout_path)
        deadline = time.time() + (timeout_sec or self.timeout_sec)
        while time.time() < deadline:
            if target.is_file():
                return target
            time.sleep(0.5)
        raise AppServerError(f"timeout waiting for rollout file: {rollout_path}")

    #codex 中文：关闭当前 client 持有的 app-server 连接和子进程。
    def close(self) -> None:
        if self.transport is not None:
            self.transport.close()
            self.transport = None
        self.current_thread_id = ""


#codex 中文：初始化根日志，供所有方法统一打印 request/response。
def build_logger() -> logging.Logger:
    logger.setLevel(DEFAULT_LOG_LEVEL)
    logger.handlers.clear()
    logger.propagate = False
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
    logger.addHandler(handler)
    return logger


#codex 中文：专项验证 learn 的 Codex 交互链：initialize -> collaborationMode/list -> thread/start -> turn/start。
def init_main(force_new: bool = False) -> None:
    log_runtime_state()
    baseline_thread_id = get_session_thread_id("learn_session_baseline")
    if baseline_thread_id and not force_new:
        print(f"learnbaseline_exists_thread_id={baseline_thread_id}")
        print("learnbaseline_status=exists")
        return
    if force_new:
        clear_session_registry("learn_session_baseline")
    client = CodexAppClient(
        mode="plan",
        effort=LEARN_INIT_EFFORT,
        timeout_sec=PLAN_TIMEOUT_SEC,
        events_file=LEARN_INIT_EVENTS_FILE,
        stderr_file=LEARN_INIT_STDERR_FILE,
    )
    init_response = client.connect()
    print(f"initialize_learn RESPONSE_JSON={json.dumps(init_response, ensure_ascii=False)}")
    modes_response = client.list_collaboration_modes()
    print(f"collaborationMode/list RESPONSE_JSON={json.dumps(modes_response, ensure_ascii=False)}")
    start_response = client.start_thread(name=LEARN_INIT_THREAD_NAME)
    thread_id = ((start_response.get("result") or {}).get("thread") or {}).get("id", "")
    thread_path = str(((start_response.get("result") or {}).get("thread") or {}).get("path", "")).strip()
    turn_response = client.start_turn(LEARN_INIT_TURN_TEXT)
    print(f"turn_learn RESPONSE_JSON={json.dumps(turn_response, ensure_ascii=False)}")
    turn_id = ((turn_response.get("result") or {}).get("turn") or {}).get("id", "")
    completion_event: dict[str, Any] | None = None
    if turn_id:
        completion_event = client.wait_for_turn_completion(str(turn_id))
        print(f"learn_completion EVENT_JSON={json.dumps(completion_event, ensure_ascii=False)}")
    if thread_path:
        client.wait_for_rollout_ready(thread_path)
    update_session_registry(
        "learn_session_baseline",
        str(thread_id),
        thread_path,
        "ready",
        "init_main",
        client.model,
        client.effort,
    )
    client.close()
    print(f"learn_thread_id={thread_id}")
    print(f"learn_thread_path={thread_path}")
    print(f"learn_events_file={LEARN_INIT_EVENTS_FILE}")
    print(f"learn_stderr_file={LEARN_INIT_STDERR_FILE}")


#codex 中文：从 learn_session_baseline 恢复并 fork 出当前工作 session，写回 fork_current_session。
def fork_current_main() -> None:
    log_runtime_state()
    try:
        baseline_thread_id = require_session_thread_id("learn_session_baseline", "python3 tools/appserverclient.py --learnbaseline")
    except ValueError as exc:
        raise AppServerError(str(exc))
    client = CodexAppClient()
    init_response = client.connect()
    print(f"initialize_fork RESPONSE_JSON={json.dumps(init_response, ensure_ascii=False)}")
    resume_response = client.resume_thread(baseline_thread_id)
    print(f"resume_baseline RESPONSE_JSON={json.dumps(resume_response, ensure_ascii=False)}")
    fork_response = client.fork_thread(baseline_thread_id)
    print(f"fork_current RESPONSE_JSON={json.dumps(fork_response, ensure_ascii=False)}")
    fork_thread_id = ((fork_response.get("result") or {}).get("thread") or {}).get("id", "")
    fork_thread_path = str(((fork_response.get("result") or {}).get("thread") or {}).get("path", "")).strip()
    if fork_thread_path:
        client.wait_for_rollout_ready(fork_thread_path)
    if fork_thread_id:
        update_session_registry(
            "fork_current_session",
            str(fork_thread_id),
            fork_thread_path,
            "ready",
            "fork_current_main",
            client.model,
            client.effort,
            forked_from_thread_id=baseline_thread_id,
        )
    client.close()
    print(f"fork_current_thread_id={fork_thread_id}")
    print(f"fork_current_thread_path={fork_thread_path}")


def build_role_thread_name(role: str, task_id: str) -> str:
    normalized_role = normalize_role(role)
    compact_task_id = str(task_id).strip() or "task"
    return f"{normalized_role}-{compact_task_id}"


def fork_role_main(role: str) -> None:
    log_runtime_state()
    normalized_role = normalize_role(role)
    if normalized_role not in {"run-main", "dev", "test", "arch"}:
        raise AppServerError("fork role must be one of: run-main, dev, test, arch")
    try:
        current_thread_id = require_session_thread_id("fork_current_session", "python3 tools/appserverclient.py --fork-current")
    except ValueError as exc:
        raise AppServerError(str(exc))
    active_task = load_active_task()
    task_id = str(active_task.get("task_id", "")).strip()
    task_json_file = str(active_task.get("artifacts", {}).get("task_json_file", "")).strip() or ""
    if not task_json_file:
        task_json_file = str(load_runtime_state().current_task_json_file).strip()
    if not task_id or not task_json_file:
        raise AppServerError("active task is required before fork-role")
    client = CodexAppClient()
    init_response = client.connect()
    print(f"initialize_fork_role RESPONSE_JSON={json.dumps(init_response, ensure_ascii=False)}")
    resume_response = client.resume_thread(current_thread_id)
    print(f"resume_run_main RESPONSE_JSON={json.dumps(resume_response, ensure_ascii=False)}")
    fork_response = client.fork_thread(current_thread_id)
    print(f"fork_role RESPONSE_JSON={json.dumps(fork_response, ensure_ascii=False)}")
    role_thread_id = str(((fork_response.get("result") or {}).get("thread") or {}).get("id", "")).strip()
    role_thread_path = str(((fork_response.get("result") or {}).get("thread") or {}).get("path", "")).strip()
    if role_thread_path:
        client.wait_for_rollout_ready(role_thread_path)
    if role_thread_id:
        thread_name = build_role_thread_name(normalized_role, task_id)
        name_response = client.set_thread_name(role_thread_id, thread_name)
        print(f"set_role_thread_name RESPONSE_JSON={json.dumps(name_response, ensure_ascii=False)}")
        update_role_thread(task_json_file, normalized_role, role_thread_id, role_thread_path, "ready")
    client.close()
    print(f"role={normalized_role}")
    print(f"role_thread_id={role_thread_id}")
    print(f"role_thread_path={role_thread_path}")


def role_turn_main(role: str, text: str | None = None) -> None:
    log_runtime_state()
    normalized_role = normalize_role(role)
    role_threads = dict(get_role_threads(None).get("role_threads", {}) or {})
    role_record = dict(role_threads.get(normalized_role, {}) or {})
    role_thread_id = str(role_record.get("thread_id", "")).strip()
    role_thread_path = str(role_record.get("thread_path", "")).strip()
    if not role_thread_id:
        raise AppServerError(f"role thread is not bound for role={normalized_role}; run python3 tools/appserverclient.py --fork-role {normalized_role} first")
    active_task = load_active_task()
    task_json_file = str(active_task.get("artifacts", {}).get("task_json_file", "")).strip() or str(load_runtime_state().current_task_json_file).strip()
    client = CodexAppClient()
    init_response = client.connect()
    print(f"initialize_role_turn RESPONSE_JSON={json.dumps(init_response, ensure_ascii=False)}")
    resume_response = client.resume_thread(role_thread_id)
    print(f"resume_role_thread RESPONSE_JSON={json.dumps(resume_response, ensure_ascii=False)}")
    resume_thread_payload = ((resume_response.get("result") or {}).get("thread") or {})
    inprogress_turn_ids = detect_inprogress_turn_ids(resume_thread_payload)
    if inprogress_turn_ids:
        print(f"role_inprogress_turn_ids={json.dumps(inprogress_turn_ids, ensure_ascii=False)}")
    turn_text = (text or DEFAULT_TURN_TEXT).strip()
    if not turn_text:
        raise AppServerError("role turn text is empty")
    turn_response = client.start_turn(turn_text)
    print(f"turn_role RESPONSE_JSON={json.dumps(turn_response, ensure_ascii=False)}")
    turn_id = ((turn_response.get("result") or {}).get("turn") or {}).get("id", "")
    completion_event: dict[str, Any] | None = None
    if turn_id:
        completion_event = client.wait_for_turn_completion(str(turn_id))
        print(f"role_completion EVENT_JSON={json.dumps(completion_event, ensure_ascii=False)}")
    if role_thread_path:
        client.wait_for_rollout_ready(role_thread_path)
    update_role_thread(task_json_file, normalized_role, role_thread_id, role_thread_path, "ready")
    client.close()
    print(f"role={normalized_role}")
    print(f"role_thread_id={role_thread_id}")
    print(f"role_thread_path={role_thread_path}")


def summarize_role_main(role: str) -> None:
    log_runtime_state()
    normalized_role = normalize_role(role)
    role_threads = dict(get_role_threads(None).get("role_threads", {}) or {})
    role_record = dict(role_threads.get(normalized_role, {}) or {})
    role_thread_id = str(role_record.get("thread_id", "")).strip()
    role_thread_path = str(role_record.get("thread_path", "")).strip()
    if not role_thread_id:
        raise AppServerError(f"role thread is not bound for role={normalized_role}; run python3 tools/appserverclient.py --fork-role {normalized_role} first")
    active_task = load_active_task()
    task_json_file = str(load_runtime_state().current_task_json_file).strip()
    client = CodexAppClient()
    init_response = client.connect()
    print(f"initialize_summarize_role RESPONSE_JSON={json.dumps(init_response, ensure_ascii=False)}")
    resume_response = client.resume_thread(role_thread_id)
    print(f"resume_summarize_role RESPONSE_JSON={json.dumps(resume_response, ensure_ascii=False)}")
    turn_text = build_summarize_role_text(normalized_role)
    turn_response = client.start_turn(turn_text)
    print(f"turn_summarize_role RESPONSE_JSON={json.dumps(turn_response, ensure_ascii=False)}")
    turn_id = ((turn_response.get("result") or {}).get("turn") or {}).get("id", "")
    if turn_id:
        completion_event = client.wait_for_turn_completion(str(turn_id))
        print(f"summarize_role_completion EVENT_JSON={json.dumps(completion_event, ensure_ascii=False)}")
    if role_thread_path:
        client.wait_for_rollout_ready(role_thread_path)
    read_response = client.read_thread(role_thread_id, include_turns=True)
    print(f"read_summarize_role RESPONSE_JSON={json.dumps(read_response, ensure_ascii=False)}")
    thread_payload = ((read_response.get("result") or {}).get("thread") or {})
    summary_text = extract_last_agent_message(thread_payload)
    if not summary_text:
        raise AppServerError(f"failed to extract role summary text from role={normalized_role}")
    update_role_thread(task_json_file, normalized_role, role_thread_id, role_thread_path, "ready")
    update_role_summary(
        task_json_file,
        normalized_role,
        role_thread_id,
        role_thread_path,
        "ready",
        summary_text,
        str(turn_id).strip(),
    )
    update_task_summary(
        task_json_file,
        "",
        [],
        [],
        [],
        [],
        [],
        [f"{normalized_role}:{str(turn_id).strip() or role_thread_id}"],
        [f"{normalized_role}:{role_thread_id}"],
    )
    gap_result = refresh_task_gap_summary(task_json_file)
    print(f"refresh_task_gap_summary RESPONSE_JSON={json.dumps(gap_result, ensure_ascii=False)}")
    escalation_result = refresh_task_escalation(task_json_file)
    print(f"refresh_task_escalation RESPONSE_JSON={json.dumps(escalation_result, ensure_ascii=False)}")
    resolution_result = refresh_run_main_resolution(task_json_file)
    print(f"refresh_run_main_resolution RESPONSE_JSON={json.dumps(resolution_result, ensure_ascii=False)}")
    client.close()
    print("role_summary_text_start")
    print(summary_text)
    print("role_summary_text_end")


def mark_test_gate_main(status: str, evidence_text: str | None = None, blocking_issues: list[str] | None = None) -> None:
    log_runtime_state()
    active_task = load_active_task()
    task_json_file = str(active_task.get("artifacts", {}).get("task_json_file", "")).strip() or str(load_runtime_state().current_task_json_file).strip()
    if not task_json_file:
        raise AppServerError("active task is required before mark-test-gate")

    normalized_status = str(status).strip().lower()
    if normalized_status not in {"pending", "blocked", "passed"}:
        raise AppServerError("test gate status must be one of: pending, blocked, passed")

    role_summaries = dict(get_role_summaries(task_json_file).get("role_summaries", {}) or {})
    test_summary = dict(role_summaries.get("test", {}) or {})
    summary_turn_id = str(test_summary.get("summary_turn_id", "")).strip()
    thread_id = str(test_summary.get("thread_id", "")).strip()
    auto_evidence: list[str] = []
    if summary_turn_id:
        auto_evidence.append(f"test-summary-turn:{summary_turn_id}")
    if thread_id:
        auto_evidence.append(f"test-thread:{thread_id}")
    if evidence_text and str(evidence_text).strip():
        auto_evidence.append(str(evidence_text).strip())

    gate_result = update_test_gate(
        task_json_file,
        normalized_status,
        [],
        auto_evidence,
        list(blocking_issues or []),
    )
    print(f"update_test_gate RESPONSE_JSON={json.dumps(gate_result, ensure_ascii=False)}")
    gap_result = refresh_task_gap_summary(task_json_file)
    print(f"refresh_task_gap_summary RESPONSE_JSON={json.dumps(gap_result, ensure_ascii=False)}")
    escalation_result = refresh_task_escalation(task_json_file)
    print(f"refresh_task_escalation RESPONSE_JSON={json.dumps(escalation_result, ensure_ascii=False)}")
    resolution_result = refresh_run_main_resolution(task_json_file)
    print(f"refresh_run_main_resolution RESPONSE_JSON={json.dumps(resolution_result, ensure_ascii=False)}")


#codex 中文：在 fork_current_session 上继续发起一轮新 turn，用于后续讨论、需求和测试工作。
def current_turn_main(text: str | None = None) -> None:
    log_runtime_state()
    current = get_session_registry("fork_current_session")
    try:
        current_thread_id = require_session_thread_id("fork_current_session", "python3 tools/appserverclient.py --fork-current")
    except ValueError as exc:
        raise AppServerError(str(exc))
    current_thread_path = get_session_thread_path("fork_current_session")
    client = CodexAppClient()
    init_response = client.connect()
    print(f"initialize_current RESPONSE_JSON={json.dumps(init_response, ensure_ascii=False)}")
    resume_response = client.resume_thread(current_thread_id)
    print(f"resume_current RESPONSE_JSON={json.dumps(resume_response, ensure_ascii=False)}")
    resume_thread_payload = ((resume_response.get("result") or {}).get("thread") or {})
    inprogress_turn_ids = detect_inprogress_turn_ids(resume_thread_payload)
    if inprogress_turn_ids:
        print(f"current_inprogress_turn_ids={json.dumps(inprogress_turn_ids, ensure_ascii=False)}")
    turn_text = (text or DEFAULT_TURN_TEXT).strip()
    if not turn_text:
        raise AppServerError("current turn text is empty")
    turn_response = client.start_turn(turn_text)
    print(f"turn_current RESPONSE_JSON={json.dumps(turn_response, ensure_ascii=False)}")
    turn_id = ((turn_response.get("result") or {}).get("turn") or {}).get("id", "")
    completion_event: dict[str, Any] | None = None
    if turn_id:
        completion_event = client.wait_for_turn_completion(str(turn_id))
        print(f"current_completion EVENT_JSON={json.dumps(completion_event, ensure_ascii=False)}")
    if current_thread_path:
        client.wait_for_rollout_ready(current_thread_path)
    update_session_registry(
        "fork_current_session",
        current_thread_id,
        current_thread_path,
        "ready",
        "current_turn_main",
        client.model,
        client.effort,
        forked_from_thread_id=str(current.get("forked_from_thread_id", "")).strip(),
    )
    client.close()
    print(f"current_thread_id={current_thread_id}")
    print(f"current_thread_path={current_thread_path}")


def summarize_current_main() -> None:
    log_runtime_state()
    current = get_session_registry("fork_current_session")
    try:
        current_thread_id = require_session_thread_id("fork_current_session", "python3 tools/appserverclient.py --fork-current")
    except ValueError as exc:
        raise AppServerError(str(exc))
    current_thread_path = get_session_thread_path("fork_current_session")
    client = CodexAppClient()
    init_response = client.connect()
    print(f"initialize_summarize_current RESPONSE_JSON={json.dumps(init_response, ensure_ascii=False)}")
    resume_response = client.resume_thread(current_thread_id)
    print(f"resume_summarize_current RESPONSE_JSON={json.dumps(resume_response, ensure_ascii=False)}")
    turn_text = build_summarize_current_text()
    turn_response = client.start_turn(turn_text)
    print(f"turn_summarize_current RESPONSE_JSON={json.dumps(turn_response, ensure_ascii=False)}")
    turn_id = ((turn_response.get("result") or {}).get("turn") or {}).get("id", "")
    completion_event: dict[str, Any] | None = None
    if turn_id:
        completion_event = client.wait_for_turn_completion(str(turn_id))
        print(f"summarize_current_completion EVENT_JSON={json.dumps(completion_event, ensure_ascii=False)}")
    if current_thread_path:
        client.wait_for_rollout_ready(current_thread_path)
    read_response = client.read_thread(current_thread_id, include_turns=True)
    print(f"read_summarize_current RESPONSE_JSON={json.dumps(read_response, ensure_ascii=False)}")
    thread_payload = ((read_response.get("result") or {}).get("thread") or {})
    summary_text = extract_last_agent_message(thread_payload)
    if not summary_text:
        raise AppServerError("failed to extract summary text from current thread")
    update_session_registry(
        "fork_current_session",
        current_thread_id,
        current_thread_path,
        "ready",
        "summarize_current_main",
        client.model,
        client.effort,
        forked_from_thread_id=str(current.get("forked_from_thread_id", "")).strip(),
    )
    update_current_summary(
        current_thread_id,
        current_thread_path,
        "ready",
        "summarize_current_main",
        client.model,
        client.effort,
        summary_text,
        summary_turn_id=str(turn_id).strip(),
    )
    client.close()
    print("current_summary_text_start")
    print(summary_text)
    print("current_summary_text_end")


def refresh_baseline_main() -> None:
    log_runtime_state()
    current_summary = dict(get_session_registry("current_summary"))
    run_summary = load_run_summary_for_current_run()
    try:
        baseline_thread_id = require_session_thread_id("learn_session_baseline", "python3 tools/appserverclient.py --learnbaseline")
    except ValueError as exc:
        raise AppServerError(str(exc))
    baseline_thread_path = get_session_thread_path("learn_session_baseline")
    client = CodexAppClient(mode="plan", effort=LEARN_INIT_EFFORT, timeout_sec=PLAN_TIMEOUT_SEC)
    init_response = client.connect()
    print(f"initialize_refresh_baseline RESPONSE_JSON={json.dumps(init_response, ensure_ascii=False)}")
    resume_response = client.resume_thread(baseline_thread_id)
    print(f"resume_refresh_baseline RESPONSE_JSON={json.dumps(resume_response, ensure_ascii=False)}")
    turn_text = build_refresh_baseline_text(current_summary, run_summary)
    turn_response = client.start_turn(turn_text)
    print(f"turn_refresh_baseline RESPONSE_JSON={json.dumps(turn_response, ensure_ascii=False)}")
    turn_id = ((turn_response.get("result") or {}).get("turn") or {}).get("id", "")
    completion_event: dict[str, Any] | None = None
    if turn_id:
        completion_event = client.wait_for_turn_completion(str(turn_id))
        print(f"refresh_baseline_completion EVENT_JSON={json.dumps(completion_event, ensure_ascii=False)}")
    if baseline_thread_path:
        client.wait_for_rollout_ready(baseline_thread_path, timeout_sec=PLAN_TIMEOUT_SEC)
    read_response = client.read_thread(baseline_thread_id, include_turns=True)
    print(f"read_refresh_baseline RESPONSE_JSON={json.dumps(read_response, ensure_ascii=False)}")
    thread_payload = ((read_response.get("result") or {}).get("thread") or {})
    refresh_text = extract_last_agent_message(thread_payload)
    if not refresh_text:
        raise AppServerError("failed to extract baseline refresh text from baseline thread")
    update_session_registry(
        "learn_session_baseline",
        baseline_thread_id,
        baseline_thread_path,
        "ready",
        "refresh_baseline_main",
        client.model,
        client.effort,
    )
    update_current_summary(
        str(current_summary.get("thread_id", "")).strip(),
        str(current_summary.get("thread_path", "")).strip(),
        "refreshed",
        "refresh_baseline_main",
        str(current_summary.get("model", "")).strip() or client.model,
        str(current_summary.get("effort", "")).strip() or client.effort,
        compact_text(str(current_summary.get("summary_text", "")).strip()),
        summary_turn_id=str(current_summary.get("summary_turn_id", "")).strip(),
        baseline_refresh_text=refresh_text,
        baseline_refresh_turn_id=str(turn_id).strip(),
    )
    client.close()
    print("baseline_refresh_text_start")
    print(refresh_text)
    print("baseline_refresh_text_end")


def run_learnbaseline(force_new: bool = False) -> dict[str, Any]:
    try:
        init_main(force_new=force_new)
        return ok({"action": "learnbaseline", "force_new": force_new})
    except AppServerError as exc:
        return err(ERR_CONFIG_BASE + 10, str(exc), {"action": "learnbaseline", "force_new": force_new})


def run_fork_current() -> dict[str, Any]:
    try:
        fork_current_main()
        return ok({"action": "fork_current"})
    except AppServerError as exc:
        return err(ERR_SESSION_BASE + 10, str(exc), {"action": "fork_current"})


def run_fork_role(role: str) -> dict[str, Any]:
    try:
        fork_role_main(role)
        return ok({"action": "fork_role", "role": normalize_role(role)})
    except AppServerError as exc:
        return err(ERR_SESSION_BASE + 15, str(exc), {"action": "fork_role", "role": str(role).strip()})
    except ValueError as exc:
        return err(ERR_SESSION_BASE + 15, str(exc), {"action": "fork_role", "role": str(role).strip()})


def run_role_turn(role: str, text: str | None = None) -> dict[str, Any]:
    try:
        role_turn_main(role, text)
        return ok({"action": "role_turn", "role": normalize_role(role), "text": (text or DEFAULT_TURN_TEXT).strip()})
    except AppServerError as exc:
        return err(ERR_SESSION_BASE + 25, str(exc), {"action": "role_turn", "role": str(role).strip(), "text": (text or DEFAULT_TURN_TEXT).strip()})


def run_summarize_role(role: str) -> dict[str, Any]:
    try:
        summarize_role_main(role)
        return ok({"action": "summarize_role", "role": normalize_role(role)})
    except AppServerError as exc:
        return err(ERR_SESSION_BASE + 35, str(exc), {"action": "summarize_role", "role": str(role).strip()})
    except ValueError as exc:
        return err(ERR_SESSION_BASE + 35, str(exc), {"action": "summarize_role", "role": str(role).strip()})
    except ValueError as exc:
        return err(ERR_SESSION_BASE + 25, str(exc), {"action": "role_turn", "role": str(role).strip(), "text": (text or DEFAULT_TURN_TEXT).strip()})


def run_mark_test_gate(status: str, evidence_text: str | None = None, blocking_issues: list[str] | None = None) -> dict[str, Any]:
    try:
        mark_test_gate_main(status, evidence_text, blocking_issues)
        return ok(
            {
                "action": "mark_test_gate",
                "status": str(status).strip().lower(),
                "evidence_text": str(evidence_text or "").strip(),
                "blocking_issues": list(blocking_issues or []),
            }
        )
    except AppServerError as exc:
        return err(
            ERR_SESSION_BASE + 45,
            str(exc),
            {
                "action": "mark_test_gate",
                "status": str(status).strip().lower(),
                "evidence_text": str(evidence_text or "").strip(),
                "blocking_issues": list(blocking_issues or []),
            },
        )


def run_current_turn(text: str | None = None) -> dict[str, Any]:
    try:
        current_turn_main(text)
        return ok({"action": "current_turn", "text": (text or DEFAULT_TURN_TEXT).strip()})
    except AppServerError as exc:
        return err(
            ERR_SESSION_BASE + 20,
            str(exc),
            {"action": "current_turn", "text": (text or DEFAULT_TURN_TEXT).strip()},
        )


def run_summarize_current() -> dict[str, Any]:
    try:
        summarize_current_main()
        return ok({"action": "summarize_current"})
    except AppServerError as exc:
        return err(ERR_SESSION_BASE + 30, str(exc), {"action": "summarize_current"})


def run_refresh_baseline() -> dict[str, Any]:
    try:
        refresh_baseline_main()
        return ok({"action": "refresh_baseline"})
    except AppServerError as exc:
        return err(ERR_SESSION_BASE + 40, str(exc), {"action": "refresh_baseline"})


#codex 中文：演示一个完整调用链：connect -> start_thread -> set_name -> start_turn -> list -> read -> fork -> compact -> close。
def demo() -> None:
    client = CodexAppClient()
    init_response = client.connect()
    print(f"initialize RESPONSE_JSON={json.dumps(init_response, ensure_ascii=False)}")
    start_response = client.start_thread(name=DEFAULT_THREAD_NAME)
    thread_id = ((start_response.get("result") or {}).get("thread") or {}).get("id", "")
    thread_path = str(((start_response.get("result") or {}).get("thread") or {}).get("path", "")).strip()
    #client.set_thread_name(thread_id, "demo-thread")
    turn_response = client.start_turn(DEFAULT_TURN_TEXT)
    turn_id = ((turn_response.get("result") or {}).get("turn") or {}).get("id", "")
    if turn_id:
        client.wait_for_turn_completion(str(turn_id))
    if thread_path:
        client.wait_for_rollout_ready(thread_path)
    fork_response = client.fork_thread(thread_id)
    fork_thread_id = ((fork_response.get("result") or {}).get("thread") or {}).get("id", "")
    fork_thread_path = str(((fork_response.get("result") or {}).get("thread") or {}).get("path", "")).strip()
    if fork_thread_id:
        update_session_registry(
            "fork_current_session",
            str(fork_thread_id),
            fork_thread_path,
            "ready",
            "demo",
            client.model,
            client.effort,
            forked_from_thread_id=str(thread_id),
        )
        client.compact_thread(fork_thread_id)
    client.close()
    if fork_thread_id:
        resume_client = CodexAppClient()
        resume_init_response = resume_client.connect()
        print(f"initialize_resume RESPONSE_JSON={json.dumps(resume_init_response, ensure_ascii=False)}")
        resume_response = resume_client.resume_thread(fork_thread_id)
        print(f"resume RESPONSE_JSON={json.dumps(resume_response, ensure_ascii=False)}")
        resume_client.close()


if __name__ == "__main__":
    logger = build_logger()
    if len(sys.argv) > 1 and sys.argv[1] in {"--learnbaseline", "--learnbassline"}:
        result = run_learnbaseline(force_new=(len(sys.argv) > 2 and sys.argv[2] == "-new"))
        print(json.dumps(result, ensure_ascii=False))
        if int(result.get("err_code", 1)) != 0:
            logger.error("APP_CLIENT_FAILED: %s", result.get("err_desc", "unknown error"))
            sys.exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "--fork-current":
        result = run_fork_current()
        print(json.dumps(result, ensure_ascii=False))
        if int(result.get("err_code", 1)) != 0:
            logger.error("APP_CLIENT_FAILED: %s", result.get("err_desc", "unknown error"))
            sys.exit(1)
    elif len(sys.argv) > 2 and sys.argv[1] == "--fork-role":
        result = run_fork_role(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False))
        if int(result.get("err_code", 1)) != 0:
            logger.error("APP_CLIENT_FAILED: %s", result.get("err_desc", "unknown error"))
            sys.exit(1)
    elif len(sys.argv) > 2 and sys.argv[1] == "--role-turn":
        result = run_role_turn(sys.argv[2], " ".join(sys.argv[3:]) if len(sys.argv) > 3 else None)
        print(json.dumps(result, ensure_ascii=False))
        if int(result.get("err_code", 1)) != 0:
            logger.error("APP_CLIENT_FAILED: %s", result.get("err_desc", "unknown error"))
            sys.exit(1)
    elif len(sys.argv) > 2 and sys.argv[1] == "--summarize-role":
        result = run_summarize_role(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False))
        if int(result.get("err_code", 1)) != 0:
            logger.error("APP_CLIENT_FAILED: %s", result.get("err_desc", "unknown error"))
            sys.exit(1)
    elif len(sys.argv) > 2 and sys.argv[1] == "--mark-test-gate":
        status = sys.argv[2]
        evidence_text = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else None
        result = run_mark_test_gate(status, evidence_text, [])
        print(json.dumps(result, ensure_ascii=False))
        if int(result.get("err_code", 1)) != 0:
            logger.error("APP_CLIENT_FAILED: %s", result.get("err_desc", "unknown error"))
            sys.exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "--current-turn":
        result = run_current_turn(" ".join(sys.argv[2:]) if len(sys.argv) > 2 else None)
        print(json.dumps(result, ensure_ascii=False))
        if int(result.get("err_code", 1)) != 0:
            logger.error("APP_CLIENT_FAILED: %s", result.get("err_desc", "unknown error"))
            sys.exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "--summarize-current":
        result = run_summarize_current()
        print(json.dumps(result, ensure_ascii=False))
        if int(result.get("err_code", 1)) != 0:
            logger.error("APP_CLIENT_FAILED: %s", result.get("err_desc", "unknown error"))
            sys.exit(1)
    elif len(sys.argv) > 1 and sys.argv[1] == "--refresh-baseline":
        result = run_refresh_baseline()
        print(json.dumps(result, ensure_ascii=False))
        if int(result.get("err_code", 1)) != 0:
            logger.error("APP_CLIENT_FAILED: %s", result.get("err_desc", "unknown error"))
            sys.exit(1)
    else:
        try:
            demo()
        except AppServerError as exc:
            logger.error("APP_CLIENT_FAILED: %s", exc)
            sys.exit(1)
