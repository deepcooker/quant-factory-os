#!/usr/bin/env python3
from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from tools.result_schema import ERR_CONFIG_BASE, ERR_RUNTIME_BASE, err, ok
except Exception:  # pragma: no cover
    from result_schema import ERR_CONFIG_BASE, ERR_RUNTIME_BASE, err, ok  # type: ignore


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = REPO_ROOT / "tools"
PROJECT_CONFIG_FILE = TOOLS_DIR / "project_config.json"
PROJECT_CONFIG_TEMPLATE_FILE = TOOLS_DIR / "project_config.template.json"
INIT_LOG_FILE = REPO_ROOT / "init.log"
LOGGER_NAME = "qf.init"
CODEX_BIN = "codex"
GIT_TIMEOUT_SEC = 15

DEFAULT_PROJECT_CONFIG_TEMPLATE = {
    "project_id": "your-project-id",
    "project_name": "Your Project",
    "project_root": "/abs/path/to/your-project",
    "environment": {
        "mode": "dev",
        "log_level": "info",
        "timezone": "UTC",
    },
    "docs": {
        "project_guide": "docs/PROJECT_GUIDE.md",
        "workflow": "docs/WORKFLOW.md",
        "agents": "AGENTS.md",
        "extra_docs": [],
    },
    "skills": {},
    "paths": {
        "state_dir": "state",
        "reports_dir": "reports",
        "artifacts_dir": "artifacts",
        "logs_dir": "logs",
    },
    "baseline": {
        "auto_init": True,
        "auto_refresh": True,
        "refresh_only_from_run_final_summary": True,
        "allow_candidate_truths": True,
    },
    "job_sources": {
        "allow_manual": True,
        "allow_queue_file": True,
        "queue_file": "TASKS/QUEUE.json",
        "allow_derived_jobs": True,
        "allow_event_jobs": False,
    },
    "thread_policy": {
        "max_role_threads_per_job": 6,
        "allow_subagents": True,
        "subagents_only_for_small_parallelism": True,
        "default_needs_thread_roles": ["dev", "test", "arch_review"],
    },
    "verification_policy": {
        "enable_doc_verification": True,
        "enable_code_verification": True,
        "enable_runtime_verification": False,
        "enable_contradiction_check": True,
        "minimum_evidence_for_run_planning": "documented_or_code_verified",
    },
    "state_policy": {
        "auto_save": True,
        "idempotent_resume": True,
        "max_retries": 2,
        "timeout_sec": 600,
    },
    "human_gates": {
        "require_approval_before_baseline_update": False,
        "require_approval_for_high_risk_jobs": False,
    },
    "demo_sessions": {},
    "runtime_state": {
        "current_job_id": "",
        "current_task_id": "",
        "current_task_goal": "",
        "current_task_role": "",
        "current_status": "",
        "current_updated_at": "",
    },
}

MINIMAL_FILES = {
    "AGENTS.md": "",
    "docs/PROJECT_GUIDE.md": "",
    "docs/WORKFLOW.md": "",
    "docs/ENTITIES.md": "",
    "docs/FILE_INDEX.md": "",
    "TASKS/QUEUE.json": '{\n  "items": []\n}\n',
}


@dataclass
class InitArgs:
    log_enabled: bool


def parse_args(argv: list[str]) -> InitArgs:
    log_enabled = False
    for arg in argv:
        if arg == "-log":
            log_enabled = True
            continue
        print(f"ERROR: unknown init option: {arg}", file=sys.stderr)
        print("Usage: python3 tools/init.py [-log]", file=sys.stderr)
        raise SystemExit(2)
    return InitArgs(log_enabled=log_enabled)


def build_logger(log_enabled: bool) -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    if log_enabled:
        file_handler = logging.FileHandler(INIT_LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger


def close_logger(logger: logging.Logger) -> None:
    for handler in list(logger.handlers):
        handler.flush()
        handler.close()
        logger.removeHandler(handler)


def log_line(logger: logging.Logger, message: str) -> None:
    logger.info(message)


def log_step(logger: logging.Logger, index: int, total: int, title: str, desc: str) -> None:
    log_line(logger, f"==================== INIT_STEP[{index}/{total}] {title} ====================")
    log_line(logger, f"INIT_STEP_DESC: {desc}")


def run_cmd(args: list[str], cwd: Path | None = None, timeout_sec: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout_sec,
    )


def run_shell(cmd: str, cwd: Path | None = None, timeout_sec: int | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", "-lc", cmd],
        cwd=str(cwd) if cwd else None,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout_sec,
    )


def ensure_dir(path: Path) -> str:
    if path.exists():
        return "ok"
    path.mkdir(parents=True, exist_ok=True, mode=0o755)
    os.chmod(path, 0o755)
    return "created"


def ensure_file(path: Path, content: str) -> str:
    if path.exists():
        return "ok"
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o755)
    path.write_text(content, encoding="utf-8")
    os.chmod(path, 0o644)
    return "created"


def ensure_project_config_template() -> str:
    if PROJECT_CONFIG_TEMPLATE_FILE.exists():
        return "ok"
    PROJECT_CONFIG_TEMPLATE_FILE.write_text(
        json.dumps(DEFAULT_PROJECT_CONFIG_TEMPLATE, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.chmod(PROJECT_CONFIG_TEMPLATE_FILE, 0o644)
    return "created"


def ensure_project_config() -> str:
    if PROJECT_CONFIG_FILE.exists():
        return "ok"
    config = json.loads(json.dumps(DEFAULT_PROJECT_CONFIG_TEMPLATE))
    config["project_id"] = REPO_ROOT.name
    config["project_name"] = REPO_ROOT.name
    config["project_root"] = str(REPO_ROOT)
    PROJECT_CONFIG_FILE.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(PROJECT_CONFIG_FILE, 0o644)
    return "created"


def load_project_config() -> dict[str, Any]:
    return json.loads(PROJECT_CONFIG_FILE.read_text(encoding="utf-8"))


def validate_project_config(config: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("project_id", "project_name", "project_root", "docs", "skills", "paths", "runtime_state"):
        if key not in config:
            errors.append(f"MISSING_CONFIG_KEY:{key}")
    if str(config.get("project_root", "")).strip() != str(REPO_ROOT):
        errors.append("PROJECT_ROOT_MISMATCH")
    docs = config.get("docs") or {}
    for key in ("project_guide", "workflow", "agents"):
        if not str(docs.get(key, "")).strip():
            errors.append(f"MISSING_DOC_POINTER:{key}")
    runtime_state = config.get("runtime_state") or {}
    for key in ("current_job_id", "current_task_id", "current_status"):
        if key not in runtime_state:
            errors.append(f"MISSING_RUNTIME_STATE_KEY:{key}")
    return errors


def runtime_state_block(config: dict[str, Any]) -> dict[str, Any]:
    state = dict(config.get("runtime_state") or {})
    return {
        "current_job_id": str(state.get("current_job_id", "")).strip(),
        "current_task_id": str(state.get("current_task_id", "")).strip(),
        "current_task_goal": str(state.get("current_task_goal", "")).strip(),
        "current_task_role": str(state.get("current_task_role", "")).strip(),
        "current_status": str(state.get("current_status", "")).strip(),
        "current_updated_at": str(state.get("current_updated_at", "")).strip(),
    }


def step_01_config(logger: logging.Logger) -> tuple[dict[str, Any], list[str]]:
    log_step(logger, 1, 4, "读取并补齐新主线配置", "确保 tools/project_config.template.json 与 tools/project_config.json 存在，并按新实验线字段做校验。")
    template_status = ensure_project_config_template()
    config_status = ensure_project_config()
    config = load_project_config()
    errors = validate_project_config(config)
    log_line(logger, f"INIT_PROJECT_CONFIG_TEMPLATE_STATUS: {template_status}")
    log_line(logger, f"INIT_PROJECT_CONFIG_STATUS: {config_status}")
    log_line(logger, f"INIT_CONFIG_STATUS: {'ok' if not errors else 'invalid'}")
    for error in errors:
        log_line(logger, f"INIT_CONFIG_ERROR: {error}")
    log_line(logger, "APP_RUNTIME_STATE_START")
    for line in json.dumps(runtime_state_block(config), ensure_ascii=False, indent=2).splitlines():
        log_line(logger, line)
    log_line(logger, "APP_RUNTIME_STATE_END")
    return config, errors


def step_02_skeleton(logger: logging.Logger, config: dict[str, Any]) -> list[str]:
    log_step(logger, 2, 4, "确保新主线骨架存在", "检查并补齐 docs、state、reports、artifacts、logs、appserver_log、TASKS 等最小目录和占位文件。")
    errors: list[str] = []
    path_map = config.get("paths") or {}
    required_dirs = [
        REPO_ROOT / "docs",
        REPO_ROOT / "TASKS",
        REPO_ROOT / str(path_map.get("state_dir", "state")),
        REPO_ROOT / str(path_map.get("reports_dir", "reports")),
        REPO_ROOT / str(path_map.get("artifacts_dir", "artifacts")),
        REPO_ROOT / str(path_map.get("logs_dir", "logs")),
        REPO_ROOT / "appserver_log",
        REPO_ROOT / ".agents" / "skills",
        REPO_ROOT / "schemas",
        REPO_ROOT / "tests",
    ]
    for path in required_dirs:
        log_line(logger, f"INIT_DIR_STATUS: {path.relative_to(REPO_ROOT)} -> {ensure_dir(path)}")

    for rel, content in MINIMAL_FILES.items():
        status = ensure_file(REPO_ROOT / rel, content)
        log_line(logger, f"INIT_FILE_STATUS: {rel} -> {status}")

    for rel in ("tools/main.py", "tools/app.py", "core/schema_utils.py"):
        path = REPO_ROOT / rel
        current = "ok" if path.exists() else "missing"
        log_line(logger, f"INIT_RUNTIME_FILE_STATUS: {rel} -> {current}")
        if current != "ok":
            errors.append(f"MISSING_RUNTIME_FILE:{rel}")
    return errors


def step_03_runtime(logger: logging.Logger) -> list[str]:
    log_step(logger, 3, 4, "检查 Codex / app-server / skills / schemas", "检查 codex CLI、app-server 能力、skills 与 schemas 主目录是否到位。")
    errors: list[str] = []
    codex_probe = run_shell(f"command -v {CODEX_BIN} >/dev/null 2>&1")
    codex_ok = codex_probe.returncode == 0
    log_line(logger, f"INIT_CODEX_CLI_STATUS: {'ok' if codex_ok else 'missing'}")
    if not codex_ok:
        errors.append("CODEX_NOT_INSTALLED")
        return errors

    version_probe = run_cmd([CODEX_BIN, "--version"])
    log_line(logger, f"INIT_CODEX_VERSION: {(version_probe.stdout or '').strip() or '(unknown)'}")

    app_probe = run_cmd([CODEX_BIN, "app-server", "--help"])
    app_ok = app_probe.returncode == 0
    log_line(logger, f"INIT_APP_SERVER_STATUS: {'ok' if app_ok else 'unavailable'}")
    if not app_ok:
        errors.append("APP_SERVER_UNAVAILABLE")

    skills_dir = REPO_ROOT / ".agents" / "skills"
    schemas_dir = REPO_ROOT / "schemas"
    log_line(logger, f"INIT_SKILLS_DIR_STATUS: {'ok' if skills_dir.exists() else 'missing'}")
    log_line(logger, f"INIT_SCHEMAS_DIR_STATUS: {'ok' if schemas_dir.exists() else 'missing'}")
    if not skills_dir.exists():
        errors.append("SKILLS_DIR_MISSING")
    if not schemas_dir.exists():
        errors.append("SCHEMAS_DIR_MISSING")
    return errors


def step_04_git(logger: logging.Logger) -> list[str]:
    log_step(logger, 4, 4, "检查 git 工作区", "检查 git 仓库是否有效、当前分支和工作区是否有未提交变更。")
    errors: list[str] = []
    git_probe = run_shell("command -v git >/dev/null 2>&1")
    if git_probe.returncode != 0:
        log_line(logger, "INIT_GIT_STATUS: missing")
        errors.append("GIT_NOT_INSTALLED")
        return errors
    log_line(logger, "INIT_GIT_STATUS: ok")

    repo_probe = run_cmd(["git", "rev-parse", "--show-toplevel"], cwd=REPO_ROOT, timeout_sec=GIT_TIMEOUT_SEC)
    if repo_probe.returncode != 0:
        log_line(logger, "INIT_GIT_REPO_STATUS: not_repo")
        errors.append("GIT_REPO_INVALID")
        return errors
    log_line(logger, "INIT_GIT_REPO_STATUS: ok")

    branch = (run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=REPO_ROOT, timeout_sec=GIT_TIMEOUT_SEC).stdout or "").strip() or "unknown"
    log_line(logger, f"INIT_BRANCH: {branch}")

    dirty_probe = run_shell("! git diff --quiet || ! git diff --cached --quiet || [[ -n \"$(git ls-files --others --exclude-standard)\" ]]", cwd=REPO_ROOT, timeout_sec=GIT_TIMEOUT_SEC)
    worktree_dirty = dirty_probe.returncode == 0
    log_line(logger, f"INIT_WORKTREE_STATUS: {'dirty' if worktree_dirty else 'clean'}")
    if worktree_dirty:
        errors.append("WORKTREE_DIRTY")
    return errors


def finalize(
    logger: logging.Logger,
    config_errors: list[str],
    skeleton_errors: list[str],
    runtime_errors: list[str],
    git_errors: list[str],
    config: dict[str, Any],
) -> dict[str, Any]:
    reason_codes = config_errors + skeleton_errors + runtime_errors + git_errors
    blocking = {"CODEX_NOT_INSTALLED", "APP_SERVER_UNAVAILABLE", "GIT_NOT_INSTALLED", "GIT_REPO_INVALID"}
    if not reason_codes:
        status = "ready"
        next_step = "python3 tools/main.py"
        log_line(logger, f"INIT_STATUS: {status}")
        log_line(logger, "INIT_REASON_CODES: none")
        log_line(logger, f"INIT_NEXT: {next_step}")
        return ok(
            {
                "status": status,
                "reason_codes": "none",
                "project_id": str(config.get("project_id", "")).strip(),
                "project_root": str(config.get("project_root", "")).strip(),
                "next_step": next_step,
            }
        )

    status = "blocked" if any(code in blocking for code in reason_codes) else "needs_fix"
    next_step = "修复阻塞项后重跑 python3 tools/init.py" if status == "blocked" else "处理配置或工作区问题后重跑 python3 tools/init.py"
    log_line(logger, f"INIT_STATUS: {status}")
    log_line(logger, f"INIT_REASON_CODES: {','.join(reason_codes)}")
    log_line(logger, f"INIT_NEXT: {next_step}")
    return err(
        ERR_RUNTIME_BASE + 1 if status == "blocked" else ERR_CONFIG_BASE + 1,
        f"init {status}: {','.join(reason_codes)}",
        {
            "status": status,
            "reason_codes": ",".join(reason_codes),
            "project_id": str(config.get("project_id", "")).strip(),
            "project_root": str(config.get("project_root", "")).strip(),
            "next_step": next_step,
        },
    )


def run_init(argv: list[str]) -> dict[str, Any]:
    args = parse_args(argv)
    logger = build_logger(args.log_enabled)
    try:
        config, config_errors = step_01_config(logger)
        skeleton_errors = step_02_skeleton(logger, config) if not config_errors else []
        runtime_errors = step_03_runtime(logger) if not config_errors else []
        git_errors = step_04_git(logger) if not config_errors else []
        return finalize(logger, config_errors, skeleton_errors, runtime_errors, git_errors, config)
    finally:
        if args.log_enabled:
            log_line(logger, "INIT_LOG_END")
        close_logger(logger)


def main(argv: list[str]) -> int:
    result = run_init(argv)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if int(result.get("err_code", 1)) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
