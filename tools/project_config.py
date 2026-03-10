#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECT_CONFIG_FILE = REPO_ROOT / "tools" / "project_config.json"
TASK_STATE_FILE = REPO_ROOT / "TASKS" / "STATE.md"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGER_NAME = "qf.project_config"
logger = logging.getLogger(LOGGER_NAME)


# project_config 中文：把配置里的路径字段统一解析为绝对路径；已是绝对路径就直接使用，相对路径则相对给定根路径解析。
def resolve_config_path(raw_path: str, base_root: Path) -> Path:
    candidate = Path(str(raw_path))
    if candidate.is_absolute():
        return candidate.resolve()
    return (base_root / candidate).resolve()


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
    git_remote_url_https: str
    git_remote_url_ssh: str
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
    current_task_file: str
    current_status: str
    current_updated_at: str


# project_config 中文：读取原始项目配置 JSON。
def load_project_config_json() -> dict[str, Any]:
    return json.loads(PROJECT_CONFIG_FILE.read_text(encoding="utf-8"))


# project_config 中文：把更新后的项目配置 JSON 回写到磁盘。
def save_project_config_json(config: dict[str, Any]) -> None:
    PROJECT_CONFIG_FILE.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# project_config 中文：把 JSON 配置转换成代码里可直接使用的结构化对象。
def load_project_config() -> ProjectConfig:
    raw = load_project_config_json()
    git_account = dict(raw.get("git_account", {}) or {})
    codex_account = dict(raw.get("codex_account", {}) or {})
    project_root = resolve_config_path(str(raw["project_root"]), REPO_ROOT)
    return ProjectConfig(
        project_id=str(raw["project_id"]),
        project_root=project_root,
        tools_dir=resolve_config_path(str(raw["tools_dir"]), project_root),
        docs_dir=resolve_config_path(str(raw["docs_dir"]), project_root),
        agents_file=resolve_config_path(str(raw["agents_file"]), project_root),
        project_guide_file=resolve_config_path(str(raw["project_guide_file"]), project_root),
        git_repo_path=resolve_config_path(str(git_account.get("repo_path", ".")), project_root),
        git_remote_name=str(git_account.get("remote_name", "")),
        git_remote_url_https=str(git_account.get("remote_url_https", "")),
        git_remote_url_ssh=str(git_account.get("remote_url_ssh", "")),
        github_login=str(git_account.get("github_login", "")),
        git_user_name=str(git_account.get("git_user_name", "")),
        git_user_email=str(git_account.get("git_user_email", "")),
        git_auth_check_command=str(git_account.get("auth_check_command", "")),
        codex_bin=str(raw["codex_bin"]),
        codex_auth_mode=str(codex_account.get("auth_mode", "")),
        codex_account_label=str(codex_account.get("account_label", "")),
        codex_home=str(codex_account.get("codex_home", "")),
        codex_login_status_command=str(codex_account.get("login_status_command", "")),
        app_server_subcommand=str(raw["app_server_subcommand"]),
        app_server_session_env_keys=tuple(str(x) for x in raw["app_server_session_env_keys"]),
        codex_client_name=str(raw["codex_client_name"]),
        codex_client_version=str(raw["codex_client_version"]),
        codex_capabilities=dict(raw["codex_capabilities"]),
        default_model=str(raw["default_model"]),
        default_mode=str(raw["default_mode"]),
        default_effort=str(raw["default_effort"]),
        default_timeout_sec=int(raw["default_timeout_sec"]),
        plan_timeout_sec=int(raw["plan_timeout_sec"]),
        default_thread_name=str(raw["default_thread_name"]),
        default_thread_search_limit=int(raw["default_thread_search_limit"]),
        default_turn_text=str(raw["default_turn_text"]),
        learn_init_thread_name=str(raw["learn_init_thread_name"]),
        learn_init_effort=str(raw["learn_init_effort"]),
        learn_init_turn_text=str(raw["learn_init_turn_text"]),
    )


# project_config 中文：把 JSON 里的 runtime_state 转成结构化运行状态对象。
def load_runtime_state() -> RuntimeState:
    raw = load_project_config_json().get("runtime_state", {}) or {}
    return RuntimeState(
        current_project_id=str(raw.get("current_project_id", "")).strip(),
        current_run_id=str(raw.get("current_run_id", "")).strip(),
        current_task_file=str(raw.get("current_task_file", "")).strip(),
        current_status=str(raw.get("current_status", "")).strip(),
        current_updated_at=str(raw.get("current_updated_at", "")).strip(),
    )


# project_config 中文：统一打印关键项目配置，便于后续各入口做中文参数确认。
def describe_project_config(cfg: ProjectConfig) -> list[str]:
    return [
        f"PROJECT_ID: {cfg.project_id}",
        f"PROJECT_ROOT: {cfg.project_root}",
        f"CODEX_BIN: {cfg.codex_bin}",
        f"DEFAULT_MODEL: {cfg.default_model}",
        f"DEFAULT_MODE: {cfg.default_mode}",
        f"DEFAULT_EFFORT: {cfg.default_effort}",
        f"PLAN_TIMEOUT_SEC: {cfg.plan_timeout_sec}",
    ]


# project_config 中文：统一打印当前运行状态，后续其他脚本应优先从这里读取。
def describe_runtime_state(state: RuntimeState) -> list[str]:
    return [
        f"CURRENT_PROJECT_ID: {state.current_project_id or '(未配置)'}",
        f"CURRENT_RUN_ID: {state.current_run_id or '(未配置)'}",
        f"CURRENT_TASK_FILE: {state.current_task_file or '(未配置)'}",
        f"CURRENT_STATUS: {state.current_status or '(未配置)'}",
        f"CURRENT_UPDATED_AT: {state.current_updated_at or '(未配置)'}",
    ]


# project_config 中文：统一打印 Git 账户与校验命令相关配置。
def describe_git_account_config(cfg: ProjectConfig) -> list[str]:
    return [
        f"GIT_REPO_PATH: {cfg.git_repo_path}",
        f"GIT_REMOTE_NAME: {cfg.git_remote_name}",
        f"GIT_REMOTE_URL_HTTPS: {cfg.git_remote_url_https or '(未配置)'}",
        f"GIT_REMOTE_URL_SSH: {cfg.git_remote_url_ssh or '(未配置)'}",
        f"GITHUB_LOGIN: {cfg.github_login or '(未配置)'}",
        f"GIT_USER_NAME: {cfg.git_user_name or '(未配置)'}",
        f"GIT_USER_EMAIL: {cfg.git_user_email or '(未配置)'}",
        f"GIT_AUTH_CHECK_COMMAND: {cfg.git_auth_check_command or '(未配置)'}",
    ]


# project_config 中文：统一打印 Codex 账户与运行时相关配置。
def describe_codex_account_config(cfg: ProjectConfig) -> list[str]:
    return [
        f"CODEX_BIN: {cfg.codex_bin}",
        f"CODEX_AUTH_MODE: {cfg.codex_auth_mode or '(未配置)'}",
        f"CODEX_ACCOUNT_LABEL: {cfg.codex_account_label or '(未配置)'}",
        f"CODEX_HOME: {cfg.codex_home or '(未配置)'}",
        f"CODEX_LOGIN_STATUS_COMMAND: {cfg.codex_login_status_command or '(未配置)'}",
    ]


# project_config 中文：校验关键项目配置非空和路径存在性。
def validate_project_config(cfg: ProjectConfig) -> list[str]:
    errors: list[str] = []
    if not cfg.project_id.strip():
        errors.append("project_id is empty")
    if not cfg.project_root.exists():
        errors.append(f"project_root missing: {cfg.project_root}")
    if not cfg.tools_dir.exists():
        errors.append(f"tools_dir missing: {cfg.tools_dir}")
    if not cfg.docs_dir.exists():
        errors.append(f"docs_dir missing: {cfg.docs_dir}")
    if not cfg.agents_file.is_file():
        errors.append(f"agents_file missing: {cfg.agents_file}")
    if not cfg.project_guide_file.is_file():
        errors.append(f"project_guide_file missing: {cfg.project_guide_file}")
    if not cfg.codex_bin.strip():
        errors.append("codex_bin is empty")
    if not cfg.git_repo_path.exists():
        errors.append(f"git_account.repo_path missing: {cfg.git_repo_path}")
    if not cfg.git_remote_name.strip():
        errors.append("git_account.remote_name is empty")
    if not cfg.git_remote_url_https.strip() and not cfg.git_remote_url_ssh.strip():
        errors.append("git_account.remote_url_https/remote_url_ssh are both empty")
    if not cfg.git_auth_check_command.strip():
        errors.append("git_account.auth_check_command is empty")
    if not cfg.codex_login_status_command.strip():
        errors.append("codex_account.login_status_command is empty")
    if not cfg.codex_auth_mode.strip():
        errors.append("codex_account.auth_mode is empty")
    return errors


# project_config 中文：校验 runtime_state 的关键字段是否完整且与 project_id 语义一致。
def validate_runtime_state(cfg: ProjectConfig, state: RuntimeState) -> list[str]:
    errors: list[str] = []
    if not state.current_project_id:
        errors.append("runtime_state.current_project_id is empty")
    elif state.current_project_id != cfg.project_id:
        errors.append(
            "runtime_state.current_project_id mismatch: "
            f"{state.current_project_id} != {cfg.project_id}"
        )
    if not state.current_run_id:
        errors.append("runtime_state.current_run_id is empty")
    if not state.current_task_file:
        errors.append("runtime_state.current_task_file is empty")
    if not state.current_status:
        errors.append("runtime_state.current_status is empty")
    if not state.current_updated_at:
        errors.append("runtime_state.current_updated_at is empty")
    return errors


# project_config 中文：从配置 registry 读取指定 session 槽位。
def get_session_registry(slot: str) -> dict[str, Any]:
    config = load_project_config_json()
    registry = config.get("session_registry", {})
    return dict(registry.get(slot, {}) or {})


# project_config 中文：读取指定 session 槽位里的 thread_id。
def get_session_thread_id(slot: str) -> str:
    return str(get_session_registry(slot).get("thread_id", "")).strip()


# project_config 中文：读取指定 session 槽位里的 thread_path。
def get_session_thread_path(slot: str) -> str:
    return str(get_session_registry(slot).get("thread_path", "")).strip()


# project_config 中文：要求指定 session 槽位必须已有 thread_id，否则抛出明确错误。
def require_session_thread_id(slot: str, next_command: str) -> str:
    thread_id = get_session_thread_id(slot)
    if not thread_id:
        raise ValueError(f"{slot}.thread_id is empty; run {next_command} first")
    return thread_id


# project_config 中文：按配置里的候选环境变量顺序读取当前 app-server session_id。
def get_app_server_session_id(cfg: ProjectConfig) -> str:
    import os

    for key in cfg.app_server_session_env_keys:
        value = os.environ.get(key, "").strip()
        if value:
            return value
    return ""


# project_config 中文：按点号路径读取常用配置字段，供 shell 脚本统一取值。
def get_config_value(key: str) -> str:
    cfg = load_project_config()
    state = load_runtime_state()
    mapping = {
        "project_id": cfg.project_id,
        "project_root": str(cfg.project_root),
        "runtime.current_project_id": state.current_project_id,
        "runtime.current_run_id": state.current_run_id,
        "runtime.current_task_file": state.current_task_file,
        "runtime.current_status": state.current_status,
        "runtime.current_updated_at": state.current_updated_at,
        "git.repo_path": str(cfg.git_repo_path),
        "git.remote_name": cfg.git_remote_name,
        "git.remote_url_https": cfg.git_remote_url_https,
        "git.remote_url_ssh": cfg.git_remote_url_ssh,
        "git.github_login": cfg.github_login,
        "git.auth_check_command": cfg.git_auth_check_command,
        "codex.bin": cfg.codex_bin,
        "codex.home": cfg.codex_home,
        "codex.auth_mode": cfg.codex_auth_mode,
        "codex.login_status_command": cfg.codex_login_status_command,
    }
    return str(mapping.get(key, ""))


# project_config 中文：把 learn baseline 或当前 fork session 的 thread 信息写入配置 registry。
def update_session_registry(slot: str, thread_id: str, thread_path: str, status: str, source: str, model: str, effort: str, forked_from_thread_id: str = "") -> None:
    config = load_project_config_json()
    registry = config.setdefault("session_registry", {})
    record = registry.setdefault(slot, {})
    record["thread_id"] = thread_id
    record["thread_path"] = thread_path
    record["status"] = status
    record["updated_at"] = datetime.now(timezone.utc).isoformat()
    record["source"] = source
    record["model"] = model
    record["effort"] = effort
    if forked_from_thread_id:
        record["forked_from_thread_id"] = forked_from_thread_id
    elif "forked_from_thread_id" in record:
        record["forked_from_thread_id"] = ""
    save_project_config_json(config)


# project_config 中文：清空指定 session 槽位，供重新建立 baseline 或 current session 时显式重置。
def clear_session_registry(slot: str) -> None:
    config = load_project_config_json()
    registry = config.setdefault("session_registry", {})
    record = registry.setdefault(slot, {})
    record["thread_id"] = ""
    record["thread_path"] = ""
    record["status"] = ""
    record["updated_at"] = ""
    record["source"] = ""
    record["model"] = ""
    record["effort"] = ""
    if "forked_from_thread_id" in record:
        record["forked_from_thread_id"] = ""
    save_project_config_json(config)


# project_config 中文：把 runtime_state 同步镜像到 TASKS/STATE.md，兼容现有文档与旧脚本读取。
def mirror_runtime_state_to_task_state(runtime_state: RuntimeState) -> None:
    lines = [
        "# STATE",
        "",
        f"CURRENT_PROJECT_ID: {runtime_state.current_project_id}",
        f"CURRENT_RUN_ID: {runtime_state.current_run_id}",
        f"CURRENT_TASK_FILE: {runtime_state.current_task_file}",
        f"CURRENT_STATUS: {runtime_state.current_status}",
        f"CURRENT_UPDATED_AT: {runtime_state.current_updated_at}",
    ]
    TASK_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    TASK_STATE_FILE.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


# project_config 中文：把当前运行状态统一写回配置，后续可替代分散 state 读取。
def update_runtime_state(current_project_id: str, current_run_id: str, current_task_file: str, current_status: str) -> None:
    config = load_project_config_json()
    runtime_state = config.setdefault("runtime_state", {})
    runtime_state["current_project_id"] = current_project_id
    runtime_state["current_run_id"] = current_run_id
    runtime_state["current_task_file"] = current_task_file
    runtime_state["current_status"] = current_status
    runtime_state["current_updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    save_project_config_json(config)
    mirror_runtime_state_to_task_state(load_runtime_state())


# project_config 中文：CLI 方式写入 runtime_state，供 shell 脚本统一更新状态。
def set_runtime_state_from_cli(argv: list[str]) -> int:
    if len(argv) != 4:
        print("ERROR: --set-runtime requires 4 values: <project_id> <run_id> <task_file> <status>", file=sys.stderr)
        return 2
    update_runtime_state(argv[0], argv[1], argv[2], argv[3])
    return 0


# project_config 中文：直接运行本文件时，打印配置摘要、校验结果和当前 session registry，便于单文件测试。
def main() -> int:
    if len(sys.argv) == 3 and sys.argv[1] == "--get":
        print(get_config_value(sys.argv[2]))
        return 0
    if len(sys.argv) >= 2 and sys.argv[1] == "--set-runtime":
        return set_runtime_state_from_cli(sys.argv[2:])
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logger.addHandler(handler)
    cfg = load_project_config()
    state = load_runtime_state()
    logger.info("项目配置摘要开始")
    for line in describe_project_config(cfg):
        logger.info(line)
    logger.info("运行状态配置开始")
    for line in describe_runtime_state(state):
        logger.info(line)
    logger.info("运行状态配置结束")
    logger.info("Git 账户配置开始")
    for line in describe_git_account_config(cfg):
        logger.info(line)
    logger.info("Git 账户配置结束")
    logger.info("Codex 账户配置开始")
    for line in describe_codex_account_config(cfg):
        logger.info(line)
    logger.info("Codex 账户配置结束")
    logger.info("项目配置摘要结束")
    errors = validate_project_config(cfg)
    errors.extend(validate_runtime_state(cfg, state))
    logger.info("项目配置校验结果: %s", "通过" if not errors else "失败")
    if errors:
        for item in errors:
            logger.info("项目配置校验错误: %s", item)
    logger.info("TASKS_STATE_MIRROR_FILE: %s", TASK_STATE_FILE)
    logger.info("项目会话注册表开始")
    logger.info(json.dumps(load_project_config_json().get("session_registry", {}), ensure_ascii=False, indent=2))
    logger.info("项目会话注册表结束")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
