#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
PROJECT_CONFIG_FILE = REPO_ROOT / "tools" / "project_config.json"

GIT_REMOTE_NAME = "origin"
GIT_AUTH_CHECK_COMMAND = "gh auth status"
CODEX_BIN = "codex"
CODEX_AUTH_MODE = "chatgpt"
CODEX_ACCOUNT_LABEL = ""
CODEX_HOME = "~/.codex"
CODEX_LOGIN_STATUS_COMMAND = "codex login status"
APP_SERVER_SUBCOMMAND = "app-server"
APP_SERVER_SESSION_ENV_KEYS = (
    "CODEX_SESSION_ID",
    "OPENAI_SESSION_ID",
    "APP_SERVER_SESSION_ID",
)
CODEX_CLIENT_NAME = "test-app"
CODEX_CLIENT_VERSION = "0.1.0"
CODEX_CAPABILITIES = {"experimentalApi": True}
DEFAULT_MODEL = "gpt-5.4"
DEFAULT_MODE = "default"
DEFAULT_EFFORT = "low"
DEFAULT_TIMEOUT_SEC = 60
PLAN_TIMEOUT_SEC = 3600
DEFAULT_THREAD_NAME = "test-thread"
DEFAULT_THREAD_SEARCH_LIMIT = 10
DEFAULT_TURN_TEXT = "你好"


@dataclass(frozen=True)
class ProjectConfig:
    project_id: str
    project_root: Path
    tools_dir: Path
    docs_dir: Path
    agents_file: Path
    project_guide_file: Path
    git_repo_path: Path
    git_remote_name: str
    git_remote_url: str
    github_login: str
    git_user_name: str
    git_user_email: str
    git_auth_check_command: str
    codex_bin: str
    codex_auth_mode: str
    codex_account_label: str
    codex_home: str
    codex_login_status_command: str
    app_server_subcommand: str
    app_server_session_env_keys: tuple[str, ...]
    codex_client_name: str
    codex_client_version: str
    codex_capabilities: dict[str, Any]
    default_model: str
    default_mode: str
    default_effort: str
    default_timeout_sec: int
    plan_timeout_sec: int
    default_thread_name: str
    default_thread_search_limit: int
    default_turn_text: str
    learn_init_thread_name: str
    learn_init_effort: str
    learn_init_turn_text: str


@dataclass(frozen=True)
class RuntimeState:
    current_project_id: str
    current_run_id: str
    current_task_id: str
    current_task_file: str
    current_task_json_file: str
    current_status: str
    current_updated_at: str


def load_project_config_json() -> dict[str, Any]:
    return json.loads(PROJECT_CONFIG_FILE.read_text(encoding="utf-8"))


def save_project_config_json(config: dict[str, Any]) -> None:
    PROJECT_CONFIG_FILE.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _git_output(args: list[str]) -> str:
    proc = subprocess.run(args, cwd=str(REPO_ROOT), text=True, capture_output=True)
    if proc.returncode != 0:
        return ""
    return (proc.stdout or "").strip()


def _git_remote_url() -> str:
    return _git_output(["git", "remote", "get-url", GIT_REMOTE_NAME])


def load_unified_config() -> dict[str, Any]:
    raw = load_project_config_json()
    project_id = str(raw.get("project_id", "")).strip()
    project_root = Path(str(raw.get("project_root", REPO_ROOT))).resolve()
    runtime_state = dict(raw.get("runtime_state", {}) or {})
    required = {
        "project_id": project_id,
        "project_root": str(project_root),
    }
    git = {
        "repo_path": str(project_root),
        "remote_name": GIT_REMOTE_NAME,
        "remote_url": _git_remote_url(),
        "github_login": "",
        "git_user_name": "",
        "git_user_email": "",
        "auth_check_command": GIT_AUTH_CHECK_COMMAND,
    }
    runtime_state.setdefault("current_project_id", project_id)
    runtime_state.setdefault("current_run_id", "")
    runtime_state.setdefault("current_task_file", "")
    runtime_state.setdefault("current_task_json_file", "")
    runtime_state.setdefault("current_status", "")
    runtime_state.setdefault("current_updated_at", "")
    return {
        "required": required,
        "project_id": project_id,
        "project_root": str(project_root),
        "tools_dir": str(project_root / "tools"),
        "docs_dir": str(project_root / "docs"),
        "agents_file": str(project_root / "AGENTS.md"),
        "project_guide_file": str(project_root / "docs" / "PROJECT_GUIDE.md"),
        "git": git,
        "runtime_state": runtime_state,
        "session_registry": {},
        "codex": {
            "bin": CODEX_BIN,
            "auth_mode": CODEX_AUTH_MODE,
            "account_label": CODEX_ACCOUNT_LABEL,
            "home": str(Path(CODEX_HOME).expanduser()),
            "login_status_command": CODEX_LOGIN_STATUS_COMMAND,
            "app_server_subcommand": APP_SERVER_SUBCOMMAND,
            "app_server_session_env_keys": list(APP_SERVER_SESSION_ENV_KEYS),
            "client_name": CODEX_CLIENT_NAME,
            "client_version": CODEX_CLIENT_VERSION,
            "capabilities": dict(CODEX_CAPABILITIES),
        },
        "runtime_defaults": {
            "default_model": DEFAULT_MODEL,
            "default_mode": DEFAULT_MODE,
            "default_effort": DEFAULT_EFFORT,
            "default_timeout_sec": DEFAULT_TIMEOUT_SEC,
            "plan_timeout_sec": PLAN_TIMEOUT_SEC,
            "default_thread_name": DEFAULT_THREAD_NAME,
            "default_thread_search_limit": DEFAULT_THREAD_SEARCH_LIMIT,
            "default_turn_text": DEFAULT_TURN_TEXT,
            "learn_init_thread_name": "learning-baseline",
            "learn_init_effort": DEFAULT_EFFORT,
            "learn_init_turn_text": "",
        },
    }


def load_project_config() -> ProjectConfig:
    unified = load_unified_config()
    git = dict(unified["git"])
    codex = dict(unified["codex"])
    runtime_defaults = dict(unified["runtime_defaults"])
    return ProjectConfig(
        project_id=str(unified["project_id"]),
        project_root=Path(str(unified["project_root"])),
        tools_dir=Path(str(unified["tools_dir"])),
        docs_dir=Path(str(unified["docs_dir"])),
        agents_file=Path(str(unified["agents_file"])),
        project_guide_file=Path(str(unified["project_guide_file"])),
        git_repo_path=Path(str(git["repo_path"])),
        git_remote_name=str(git["remote_name"]),
        git_remote_url=str(git["remote_url"]),
        github_login=str(git["github_login"]),
        git_user_name=str(git["git_user_name"]),
        git_user_email=str(git["git_user_email"]),
        git_auth_check_command=str(git["auth_check_command"]),
        codex_bin=str(codex["bin"]),
        codex_auth_mode=str(codex["auth_mode"]),
        codex_account_label=str(codex["account_label"]),
        codex_home=str(codex["home"]),
        codex_login_status_command=str(codex["login_status_command"]),
        app_server_subcommand=str(codex["app_server_subcommand"]),
        app_server_session_env_keys=tuple(str(x) for x in codex["app_server_session_env_keys"]),
        codex_client_name=str(codex["client_name"]),
        codex_client_version=str(codex["client_version"]),
        codex_capabilities=dict(codex["capabilities"]),
        default_model=str(runtime_defaults["default_model"]),
        default_mode=str(runtime_defaults["default_mode"]),
        default_effort=str(runtime_defaults["default_effort"]),
        default_timeout_sec=int(runtime_defaults["default_timeout_sec"]),
        plan_timeout_sec=int(runtime_defaults["plan_timeout_sec"]),
        default_thread_name=str(runtime_defaults["default_thread_name"]),
        default_thread_search_limit=int(runtime_defaults["default_thread_search_limit"]),
        default_turn_text=str(runtime_defaults["default_turn_text"]),
        learn_init_thread_name=str(runtime_defaults["learn_init_thread_name"]),
        learn_init_effort=str(runtime_defaults["learn_init_effort"]),
        learn_init_turn_text=str(runtime_defaults["learn_init_turn_text"]),
    )


def load_runtime_state() -> RuntimeState:
    raw = dict(load_unified_config().get("runtime_state", {}) or {})
    return RuntimeState(
        current_project_id=str(raw.get("current_project_id", "")).strip(),
        current_run_id=str(raw.get("current_run_id", "")).strip(),
        current_task_id=str(raw.get("current_task_id", "")).strip(),
        current_task_file=str(raw.get("current_task_file", "")).strip(),
        current_task_json_file=str(raw.get("current_task_json_file", "")).strip(),
        current_status=str(raw.get("current_status", "")).strip(),
        current_updated_at=str(raw.get("current_updated_at", "")).strip(),
    )


def validate_required_json_fields(raw: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not str(raw.get("project_id", "")).strip():
        errors.append("必填字段为空-project_id")
    if not str(raw.get("project_root", "")).strip():
        errors.append("必填字段为空-project_root")
    return errors


def validate_project_config(cfg: ProjectConfig, allow_bootstrap_missing: bool = False) -> list[str]:
    errors: list[str] = []
    if not cfg.project_id:
        errors.append("项目ID为空-project_id")
    if not cfg.project_root.exists():
        errors.append(f"项目根目录不存在-project_root: {cfg.project_root}")
    if not cfg.tools_dir.exists() and not allow_bootstrap_missing:
        errors.append(f"tools目录不存在-tools_dir: {cfg.tools_dir}")
    if not cfg.docs_dir.exists() and not allow_bootstrap_missing:
        errors.append(f"docs目录不存在-docs_dir: {cfg.docs_dir}")
    if not cfg.agents_file.exists() and not allow_bootstrap_missing:
        errors.append(f"AGENTS不存在-agents_file: {cfg.agents_file}")
    if not cfg.project_guide_file.exists() and not allow_bootstrap_missing:
        errors.append(f"PROJECT_GUIDE不存在-project_guide_file: {cfg.project_guide_file}")
    if not cfg.git_repo_path.exists():
        errors.append(f"Git仓库路径不存在-git.repo_path: {cfg.git_repo_path}")
    if not cfg.git_remote_name:
        errors.append("Git远端名称为空-git.remote_name")
    if not cfg.codex_bin:
        errors.append("Codex命令为空-codex_bin")
    return errors


def get_app_server_session_id(cfg: ProjectConfig) -> str:
    for key in cfg.app_server_session_env_keys:
        value = os.environ.get(key, "").strip()
        if value:
            return value
    return ""
