#!/usr/bin/env python3
from __future__ import annotations

import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

try:
    from tools.common_helpers import first_line
except Exception:  # pragma: no cover
    from common_helpers import first_line  # type: ignore


INIT_LOG_FILE = Path("init.log")
PROJECT_ROOT = Path.cwd()
print(PROJECT_ROOT)
PROJECT_ID = "quant-factory-os"
TOOLS_DIR = PROJECT_ROOT / "tools"
DOCS_DIR = PROJECT_ROOT / "docs"
AGENTS_FILE = PROJECT_ROOT / "AGENTS.md"
PROJECT_GUIDE_FILE = DOCS_DIR / "PROJECT_GUIDE.md"
GIT_REMOTE_NAME = "origin"
CODEX_BIN = "codex"
APP_SERVER_SESSION_ENV_KEYS = ("QF_APP_SERVER_SESSION_ID", "CODEX_APP_SERVER_SESSION_ID", "APP_SERVER_SESSION_ID")
print(APP_SERVER_SESSION_ENV_KEYS)


@dataclass(frozen=True)
class ProjectConfig:
    project_id: str
    project_root: Path
    tools_dir: Path
    docs_dir: Path
    agents_file: Path
    project_guide_file: Path
    git_remote_name: str
    codex_bin: str
    app_server_session_env_keys: tuple[str, ...]


@dataclass
class CmdResult:
    rc: int
    stdout: str
    stderr: str


@dataclass
class InitArgs:
    log_enabled: bool


@dataclass
class InitContext:
    cfg: ProjectConfig
    run_id: str
    task_file: str
    task_status: str


@dataclass
class InitStepResult:
    reasons: list[str]
    status: dict[str, str]


# init_tools_01 中文：解析 init 命令行参数，当前只允许 -log。
def init_tools_01_parse_args(argv: list[str]) -> InitArgs:
    log_enabled = False
    for arg in argv:
        if arg == "-log":
            log_enabled = True
            continue
        print(f"ERROR: unknown init option: {arg}", file=sys.stderr)
        print("Usage: python3 tools/init.py [-log]", file=sys.stderr)
        raise SystemExit(2)
    return InitArgs(log_enabled=log_enabled)


# init_tools_02 中文：按标准 logging 格式初始化 init 日志器。
def init_tools_02_build_logger(log_enabled: bool) -> logging.Logger:
    logger = logging.getLogger("qf.init")
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


# init_tools_03 中文：关闭并清理 init 日志器。
def init_tools_03_close_logger(logger: logging.Logger) -> None:
    for handler in list(logger.handlers):
        handler.flush()
        handler.close()
        logger.removeHandler(handler)


# init_tools_04 中文：执行直接命令并返回结构化结果。
def init_tools_04_run_cmd(args: list[str]) -> CmdResult:
    cp = subprocess.run(args, capture_output=True, text=True, check=False)
    return CmdResult(rc=int(cp.returncode), stdout=cp.stdout or "", stderr=cp.stderr or "")


# init_tools_05 中文：通过 shell 执行命令字符串并返回结构化结果。
def init_tools_05_run_shell(cmd: str) -> CmdResult:
    cp = subprocess.run(["bash", "-lc", cmd], capture_output=True, text=True, check=False)
    return CmdResult(rc=int(cp.returncode), stdout=cp.stdout or "", stderr=cp.stderr or "")


# init_tools_06 中文：根据文件顶部常量组装固定项目配置。
def init_tools_06_load_project_config() -> ProjectConfig:
    return ProjectConfig(
        project_id=PROJECT_ID,
        project_root=PROJECT_ROOT,
        tools_dir=TOOLS_DIR,
        docs_dir=DOCS_DIR,
        agents_file=AGENTS_FILE,
        project_guide_file=PROJECT_GUIDE_FILE,
        git_remote_name=GIT_REMOTE_NAME,
        codex_bin=CODEX_BIN,
        app_server_session_env_keys=APP_SERVER_SESSION_ENV_KEYS,
    )


# init_tools_07 中文：从 TASKS/STATE.md 读取当前 run/task/status。
def init_tools_07_read_current_state(project_root: Path) -> tuple[str, str, str, str]:
    state_file = project_root / "TASKS/STATE.md"
    run_id = ""
    task_file = ""
    task_status = "active"
    project_id = ""
    if not state_file.is_file():
        return run_id, task_file, task_status, project_id
    for raw in state_file.read_text(encoding="utf-8", errors="replace").splitlines():
        if raw.startswith("CURRENT_RUN_ID:"):
            run_id = raw.split(":", 1)[1].strip()
        elif raw.startswith("CURRENT_TASK_FILE:"):
            task_file = raw.split(":", 1)[1].strip()
        elif raw.startswith("CURRENT_STATUS:"):
            task_status = raw.split(":", 1)[1].strip() or "active"
        elif raw.startswith("CURRENT_PROJECT_ID:"):
            project_id = raw.split(":", 1)[1].strip()
    return run_id, task_file, task_status, project_id


# init_tools_08 中文：统一输出单条 init 日志。
def init_tools_08_log(logger: logging.Logger, message: str) -> None:
    logger.info(message)


# init_tools_09 中文：格式化步骤标题日志。
def init_tools_09_log_step(logger: logging.Logger, index: int, total: int, title: str, desc: str) -> None:
    logger.info(f"INIT_STEP[{index}/{total}]: {title}")
    logger.info(f"INIT_STEP_DESC: {desc}")


# init_tools_10 中文：汇总前置检查结果并计算最终状态。
def init_tools_10_finalize_status(context: InitContext, reasons: list[str]) -> tuple[str, str, str]:
    blocking_codes = {
        "MISSING_PROJECT_ROOT",
        "MISSING_AGENTS_FILE",
        "MISSING_PROJECT_GUIDE_FILE",
        "CODEX_NOT_INSTALLED",
        "APP_SERVER_UNAVAILABLE",
        "GIT_NOT_INSTALLED",
        "GIT_REPO_INVALID",
        "GIT_REMOTE_MISSING",
        "GIT_REMOTE_CONNECTIVITY_FAILED",
    }
    if not reasons:
        return (
            "ready",
            "none",
            f"INIT_RUN_CONTEXT: project_id={context.cfg.project_id},run_id={context.run_id or '(none)'},task={context.task_file or '(none)'},status={context.task_status}\nINIT_NEXT: python3 tools/learn.py",
        )
    if any(code in blocking_codes for code in reasons):
        return (
            "blocked",
            ",".join(reasons),
            f"INIT_RUN_CONTEXT: project_id={context.cfg.project_id},run_id={context.run_id or '(none)'},task={context.task_file or '(none)'},status={context.task_status}\nINIT_NEXT: fix init blockers before learn",
        )
    return (
        "needs_fix",
        ",".join(reasons),
        f"INIT_RUN_CONTEXT: project_id={context.cfg.project_id},run_id={context.run_id or '(none)'},task={context.task_file or '(none)'},status={context.task_status}\nINIT_NEXT: fix init warnings then rerun python3 tools/init.py",
    )


# 1001 中文：第一步，获取项目固定配置和当前上下文。
def init_step_01_load_context(logger: logging.Logger) -> InitContext:
    init_tools_09_log_step(logger, 1, 5, "获取项目配置信息与当前上下文", "从固定项目常量配置和当前 state 中确定本轮自动化上下文。")
    cfg = init_tools_06_load_project_config()
    run_id, task_file, task_status, state_project_id = init_tools_07_read_current_state(cfg.project_root)
    if state_project_id:
        cfg = ProjectConfig(
            project_id=state_project_id,
            project_root=cfg.project_root,
            tools_dir=cfg.tools_dir,
            docs_dir=cfg.docs_dir,
            agents_file=cfg.agents_file,
            project_guide_file=cfg.project_guide_file,
            git_remote_name=cfg.git_remote_name,
            codex_bin=cfg.codex_bin,
            app_server_session_env_keys=cfg.app_server_session_env_keys,
        )
    init_tools_08_log(logger, f"INIT_PROJECT_ID: {cfg.project_id}")
    init_tools_08_log(logger, f"INIT_PROJECT_ROOT: {cfg.project_root}")
    init_tools_08_log(logger, f"INIT_TASK_FILE: {task_file or '(none)'}")
    init_tools_08_log(logger, f"INIT_TASK_STATUS: {task_status}")
    init_tools_08_log(logger, f"INIT_RUN_ID: {run_id or '(none)'}")
    return InitContext(cfg=cfg, run_id=run_id, task_file=task_file, task_status=task_status)


# 1002 中文：第二步，检查项目路径和关键 owner docs。
def init_step_02_check_project_files(context: InitContext, logger: logging.Logger) -> InitStepResult:
    init_tools_09_log_step(logger, 2, 5, "检查项目路径和 owner docs 是否齐备", "检查项目根目录、tools、docs、AGENTS、PROJECT_GUIDE 是否存在。")
    checks = {
        "PROJECT_ROOT": context.cfg.project_root,
        "TOOLS_DIR": context.cfg.tools_dir,
        "DOCS_DIR": context.cfg.docs_dir,
        "AGENTS_FILE": context.cfg.agents_file,
        "PROJECT_GUIDE_FILE": context.cfg.project_guide_file,
    }
    reasons: list[str] = []
    status: dict[str, str] = {}
    for label, path in checks.items():
        ok = path.exists()
        status[label] = "ok" if ok else "missing"
        if not ok:
            reasons.append(f"MISSING_{label}")
    init_tools_08_log(logger, f"INIT_PROJECT_PATH_STATUS: {status['PROJECT_ROOT']}")
    init_tools_08_log(logger, f"INIT_TOOLS_DIR_STATUS: {status['TOOLS_DIR']}")
    init_tools_08_log(logger, f"INIT_DOCS_DIR_STATUS: {status['DOCS_DIR']}")
    init_tools_08_log(logger, f"INIT_AGENTS_STATUS: {status['AGENTS_FILE']}")
    init_tools_08_log(logger, f"INIT_PROJECT_GUIDE_STATUS: {status['PROJECT_GUIDE_FILE']}")
    return InitStepResult(reasons=reasons, status=status)


# 1003 中文：第三步，检查 Codex、app-server 和当前 session。
def init_step_03_check_codex_runtime(context: InitContext, logger: logging.Logger) -> InitStepResult:
    init_tools_09_log_step(logger, 3, 5, "检查 Codex、app-server 和当前会话前提", "检查 codex CLI、app-server 能力、认证状态以及 session_id。")
    reasons: list[str] = []
    status: dict[str, str] = {}
    codex_available = init_tools_05_run_shell(f"command -v {context.cfg.codex_bin} >/dev/null 2>&1").rc == 0
    codex_version = "(not installed)"
    if codex_available:
        codex_version = first_line(init_tools_04_run_cmd([context.cfg.codex_bin, "--version"]).stdout, codex_version)
    else:
        reasons.append("CODEX_NOT_INSTALLED")

    app_server_status = "missing"
    if codex_available:
        probe = init_tools_04_run_cmd([context.cfg.codex_bin, "app-server", "--help"])
        app_server_status = "ok" if probe.rc == 0 else "unavailable"
        if app_server_status != "ok":
            reasons.append("APP_SERVER_UNAVAILABLE")

    session_id = ""
    for key in context.cfg.app_server_session_env_keys:
        value = os.environ.get(key, "").strip()
        if value:
            session_id = value
            break

    status["CODEX_CLI_STATUS"] = "ok" if codex_available else "missing"
    status["CODEX_VERSION"] = codex_version
    status["CODEX_AUTH_STATUS"] = "configured" if os.environ.get("OPENAI_API_KEY", "").strip() else "unknown"
    status["APP_SERVER_STATUS"] = app_server_status
    status["APP_SERVER_SESSION_STATUS"] = "present" if session_id else "missing"
    status["APP_SERVER_SESSION_ID"] = session_id or "(none)"
    init_tools_08_log(logger, f"INIT_CODEX_CLI_STATUS: {status['CODEX_CLI_STATUS']}")
    init_tools_08_log(logger, f"INIT_CODEX_VERSION: {status['CODEX_VERSION']}")
    init_tools_08_log(logger, f"INIT_CODEX_AUTH_STATUS: {status['CODEX_AUTH_STATUS']}")
    init_tools_08_log(logger, f"INIT_APP_SERVER_STATUS: {status['APP_SERVER_STATUS']}")
    init_tools_08_log(logger, f"INIT_APP_SERVER_SESSION_STATUS: {status['APP_SERVER_SESSION_STATUS']}")
    init_tools_08_log(logger, f"INIT_APP_SERVER_SESSION_ID: {status['APP_SERVER_SESSION_ID']}")
    return InitStepResult(reasons=reasons, status=status)


# 1004 中文：第四步，检查 git 仓库、账号、远端和工作区。
def init_step_04_check_git_runtime(context: InitContext, logger: logging.Logger) -> InitStepResult:
    init_tools_09_log_step(logger, 4, 5, "检查 git 仓库、账号、远端和工作区状态", "检查 git 仓库、git 账号、remote 连通性和当前工作区阻塞情况。")
    reasons: list[str] = []
    status: dict[str, str] = {}
    diff_preview: list[str] = []

    git_available = init_tools_05_run_shell("command -v git >/dev/null 2>&1").rc == 0
    if not git_available:
        reasons.append("GIT_NOT_INSTALLED")
        status["GIT_STATUS"] = "missing"
        return InitStepResult(reasons=reasons, status=status)

    status["GIT_STATUS"] = "ok"
    status["GIT_VERSION"] = first_line(init_tools_04_run_cmd(["git", "--version"]).stdout, "(missing)")

    repo_check = init_tools_04_run_cmd(["git", "rev-parse", "--show-toplevel"])
    repo_ok = repo_check.rc == 0
    status["GIT_REPO_STATUS"] = "ok" if repo_ok else "not_repo"
    if not repo_ok:
        reasons.append("GIT_REPO_INVALID")
        init_tools_08_log(logger, f"INIT_GIT_STATUS: {status['GIT_STATUS']}")
        init_tools_08_log(logger, f"INIT_GIT_VERSION: {status['GIT_VERSION']}")
        init_tools_08_log(logger, f"INIT_GIT_REPO_STATUS: {status['GIT_REPO_STATUS']}")
        return InitStepResult(reasons=reasons, status=status)

    branch = first_line(init_tools_04_run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout, "unknown")
    remote = first_line(init_tools_04_run_cmd(["git", "remote", "get-url", context.cfg.git_remote_name]).stdout, "(missing)")
    remote_ok = remote != "(missing)"
    gh_installed = init_tools_05_run_shell("command -v gh >/dev/null 2>&1").rc == 0
    gh_auth_status = "missing"
    if gh_installed:
        gh_auth_status = "logged_in" if init_tools_04_run_cmd(["gh", "auth", "status", "-h", "github.com"]).rc == 0 else "not_logged_in"

    connectivity_status = "skipped"
    if remote_ok:
        probe = init_tools_05_run_shell(f"GIT_TERMINAL_PROMPT=0 git ls-remote --exit-code {context.cfg.git_remote_name} HEAD >/dev/null 2>&1")
        connectivity_status = "ok" if probe.rc == 0 else "failed"

    git_dir = Path(first_line(init_tools_04_run_cmd(["git", "rev-parse", "--git-dir"]).stdout, ".git"))
    git_operation = "none"
    if (git_dir / "MERGE_HEAD").is_file():
        git_operation = "merge_in_progress"
    elif (git_dir / "rebase-merge").is_dir() or (git_dir / "rebase-apply").is_dir():
        git_operation = "rebase_in_progress"
    elif (git_dir / "CHERRY_PICK_HEAD").is_file():
        git_operation = "cherry_pick_in_progress"
    elif (git_dir / "REVERT_HEAD").is_file():
        git_operation = "revert_in_progress"

    worktree_dirty = init_tools_05_run_shell("! git diff --quiet || ! git diff --cached --quiet || [[ -n \"$(git ls-files --others --exclude-standard)\" ]]").rc == 0
    staged_count = first_line(init_tools_05_run_shell("git diff --cached --name-only | wc -l | tr -d '[:space:]'").stdout, "0")
    unstaged_count = first_line(init_tools_05_run_shell("git diff --name-only | wc -l | tr -d '[:space:]'").stdout, "0")
    untracked_count = first_line(init_tools_05_run_shell("git ls-files --others --exclude-standard | wc -l | tr -d '[:space:]'").stdout, "0")
    diff_preview = [line for line in init_tools_05_run_shell("git status --short | head -n 20").stdout.splitlines() if line.strip()]

    if not remote_ok:
        reasons.append("GIT_REMOTE_MISSING")
    if gh_auth_status == "not_logged_in":
        reasons.append("GIT_AUTH_NOT_READY")
    if connectivity_status == "failed":
        reasons.append("GIT_REMOTE_CONNECTIVITY_FAILED")
    if git_operation != "none":
        reasons.append("GIT_OPERATION_IN_PROGRESS")
    if worktree_dirty:
        reasons.append("WORKTREE_DIRTY")

    status["GIT_BRANCH"] = branch
    status["GIT_REMOTE_ORIGIN"] = remote
    status["GIT_REMOTE_STATUS"] = "ok" if remote_ok else "missing"
    status["GIT_AUTH_STATUS"] = gh_auth_status
    status["GIT_CONNECTIVITY_STATUS"] = connectivity_status
    status["GIT_OPERATION"] = git_operation
    status["GIT_DIFF_SUMMARY"] = f"staged={staged_count},unstaged={unstaged_count},untracked={untracked_count}"

    init_tools_08_log(logger, f"INIT_GIT_STATUS: {status['GIT_STATUS']}")
    init_tools_08_log(logger, f"INIT_GIT_VERSION: {status['GIT_VERSION']}")
    init_tools_08_log(logger, f"INIT_GIT_REPO_STATUS: {status['GIT_REPO_STATUS']}")
    init_tools_08_log(logger, f"INIT_BRANCH: {status['GIT_BRANCH']}")
    init_tools_08_log(logger, f"INIT_REMOTE_ORIGIN: {status['GIT_REMOTE_ORIGIN']}")
    init_tools_08_log(logger, f"INIT_GIT_REMOTE_STATUS: {status['GIT_REMOTE_STATUS']}")
    init_tools_08_log(logger, f"INIT_GIT_AUTH_STATUS: {status['GIT_AUTH_STATUS']}")
    init_tools_08_log(logger, f"INIT_GIT_CONNECTIVITY_STATUS: {status['GIT_CONNECTIVITY_STATUS']}")
    init_tools_08_log(logger, f"INIT_GIT_OPERATION: {status['GIT_OPERATION']}")
    init_tools_08_log(logger, f"INIT_DIFF_SUMMARY: {status['GIT_DIFF_SUMMARY']}")
    if diff_preview:
        init_tools_08_log(logger, "INIT_DIFF_FILES_START")
        for line in diff_preview:
            init_tools_08_log(logger, line)
        init_tools_08_log(logger, "INIT_DIFF_FILES_END")
    else:
        init_tools_08_log(logger, "INIT_DIFF_FILES: (clean or unavailable)")
    return InitStepResult(reasons=reasons, status=status)


# 1005 中文：第五步，汇总结果并给出最终状态和下一步动作。
def init_step_05_finalize(
    context: InitContext,
    project_result: InitStepResult,
    codex_result: InitStepResult,
    git_result: InitStepResult,
    logger: logging.Logger,
) -> int:
    init_tools_09_log_step(logger, 5, 5, "汇总自动化前置检查结果并给出下一步", "汇总前四步结果，输出最终状态、原因代码和下一步动作。")
    status, reason_codes, summary_block = init_tools_10_finalize_status(
        context,
        project_result.reasons + codex_result.reasons + git_result.reasons,
    )
    for line in summary_block.splitlines():
        init_tools_08_log(logger, line)
    init_tools_08_log(logger, f"INIT_STATUS: {status}")
    init_tools_08_log(logger, f"INIT_REASON_CODES: {reason_codes}")
    return 0 if status == "ready" else 1


# init_tools_11 中文：汇总结果并计算最终状态。
def init_tools_10_finalize_status(context: InitContext, reasons: list[str]) -> tuple[str, str, str]:
    blocking_codes = {
        "MISSING_PROJECT_ROOT",
        "MISSING_AGENTS_FILE",
        "MISSING_PROJECT_GUIDE_FILE",
        "CODEX_NOT_INSTALLED",
        "APP_SERVER_UNAVAILABLE",
        "GIT_NOT_INSTALLED",
        "GIT_REPO_INVALID",
        "GIT_REMOTE_MISSING",
        "GIT_REMOTE_CONNECTIVITY_FAILED",
    }
    if not reasons:
        next_step = "python3 tools/learn.py"
        status = "ready"
    elif any(code in blocking_codes for code in reasons):
        next_step = "fix init blockers before learn"
        status = "blocked"
    else:
        next_step = "fix init warnings then rerun python3 tools/init.py"
        status = "needs_fix"
    summary = (
        f"INIT_RUN_CONTEXT: project_id={context.cfg.project_id},run_id={context.run_id or '(none)'},task={context.task_file or '(none)'},status={context.task_status}\n"
        f"INIT_NEXT: {next_step}"
    )
    return status, ",".join(reasons) if reasons else "none", summary


# 1006 中文：执行 init 主流程，main 只负责串起 5 个业务步骤。
def main(argv: list[str]) -> int:
    args = init_tools_01_parse_args(argv)
    logger = init_tools_02_build_logger(args.log_enabled)
    try:
        if args.log_enabled:
            init_tools_08_log(logger, f"INIT_LOG_FILE: {INIT_LOG_FILE}")
        context = init_step_01_load_context(logger)
        project_result = init_step_02_check_project_files(context, logger)
        codex_result = init_step_03_check_codex_runtime(context, logger)
        git_result = init_step_04_check_git_runtime(context, logger)
        return init_step_05_finalize(context, project_result, codex_result, git_result, logger)
    finally:
        if args.log_enabled:
            init_tools_08_log(logger, "INIT_LOG_END")
        init_tools_03_close_logger(logger)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
