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


CODEX_BIN = "codex"
CODEX_APP_SERVER_SUBCOMMAND = "app-server"
CODEX_CLIENT_NAME = "test-app"
CODEX_CLIENT_VERSION = "0.1.0"
CODEX_CAPABILITIES = {"experimentalApi": True}

DEFAULT_PROJECT_ROOT = Path.cwd()
DEFAULT_CODEX_HOME = None
DEFAULT_MODEL = "gpt-5.4"
DEFAULT_MODE = "default"
DEFAULT_EFFORT = "medium"
DEFAULT_TIMEOUT_SEC = 60

DEFAULT_THREAD_NAME = "test-thread"
DEFAULT_THREAD_SEARCH_LIMIT = 10
DEFAULT_TURN_TEXT = "一条狗"

DEFAULT_EVENTS_FILE = Path("test_app.events.jsonl")
DEFAULT_STDERR_FILE = Path("test_app.stderr.log")
DEFAULT_LOG_LEVEL = logging.INFO
DEFAULT_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


class AppServerError(RuntimeError):
    pass


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
        self.logger = logging.getLogger("test_app")

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
def build_logger() -> None:
    logging.basicConfig(level=DEFAULT_LOG_LEVEL, format=DEFAULT_LOG_FORMAT)


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
    if fork_thread_id:
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
    build_logger()
    try:
        demo()
    except AppServerError as exc:
        logging.getLogger("test_app").error("APP_CLIENT_FAILED: %s", exc)
        sys.exit(1)
