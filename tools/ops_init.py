#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


STATE_FILE = Path(os.environ.get("QF_STATE_FILE", "TASKS/STATE.md"))
DEFAULT_PROJECT_ID = os.environ.get("QF_DEFAULT_PROJECT_ID", "project-0")


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def should_emit_json_stream() -> bool:
    value = os.environ.get("QF_EVENT_STREAM", "0").strip().lower()
    return value in {"1", "json", "jsonl"}


def emit_json_event(phase: str, action: str, status: str, message: str) -> None:
    if not should_emit_json_stream():
        return
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "type": "qf_event",
        "phase": phase,
        "action": action,
        "status": status,
        "message": message,
    }
    print(json.dumps(payload, ensure_ascii=False))


def emit_step(phase: str, index: int, total: int, message: str) -> None:
    prefix = phase.upper()
    print(f"{prefix}_STEP[{index}/{total}]: {message}")
    emit_json_event(phase, "step", "ok", f"{index}/{total} {message}")


def state_field_value(key: str) -> str:
    if not STATE_FILE.is_file():
        return ""
    pat = re.compile(rf"^\s*{re.escape(key)}:\s*(.*?)\s*$")
    try:
        for line in STATE_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
            m = pat.match(line)
            if m:
                return m.group(1)
    except Exception:
        return ""
    return ""


def normalize_project_id(value: str | None) -> str:
    v = (value or "").strip()
    return v if v else DEFAULT_PROJECT_ID


def resolve_state_current_run_id() -> str:
    return state_field_value("CURRENT_RUN_ID").strip()


def resolve_state_current_project_id() -> str:
    return normalize_project_id(state_field_value("CURRENT_PROJECT_ID"))


@dataclass
class CmdResult:
    rc: int
    stdout: str
    stderr: str


def run_cmd(args: list[str]) -> CmdResult:
    cp = subprocess.run(args, capture_output=True, text=True, check=False)
    return CmdResult(rc=int(cp.returncode), stdout=cp.stdout or "", stderr=cp.stderr or "")


def run_shell(cmd: str) -> CmdResult:
    cp = subprocess.run(["bash", "-lc", cmd], capture_output=True, text=True, check=False)
    return CmdResult(rc=int(cp.returncode), stdout=cp.stdout or "", stderr=cp.stderr or "")


def first_line(text: str, default: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s
    return default


def count_lines(cmd: str) -> int:
    result = run_shell(cmd)
    raw = first_line(result.stdout, "0")
    try:
        return int(raw.strip())
    except Exception:
        return 0


def list_lines(cmd: str, limit: int = 20) -> list[str]:
    result = run_shell(cmd)
    lines = [line for line in result.stdout.splitlines() if line.strip()]
    return lines[:limit]


def parse_args(argv: list[str]) -> str:
    init_mode = "check"
    for arg in argv:
        if arg == "-status":
            init_mode = "status"
        elif arg == "-main":
            init_mode = "main"
        else:
            eprint(f"ERROR: unknown init option: {arg}")
            eprint("Usage: tools/ops init [-status|-main]")
            raise SystemExit(2)
    return init_mode


def main(argv: list[str]) -> int:
    init_mode = parse_args(argv)
    show_resume_hint = init_mode != "status"

    now_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    init_context_id = os.environ.get("RUN_ID", f"session-{now_id}-init")

    current_run_id = resolve_state_current_run_id()
    current_project_id = resolve_state_current_project_id()
    current_task_file = state_field_value("CURRENT_TASK_FILE").strip()
    current_status = state_field_value("CURRENT_STATUS").strip() or "active"
    if current_run_id:
        init_context_id = current_run_id

    init_steps_total = 7
    reason_codes: list[str] = []

    emit_step("init", 1, init_steps_total, "解析模式与运行上下文")
    print(f"INIT_MODE: {init_mode}")
    print(f"INIT_CONTEXT_ID: {init_context_id}")
    print(f"INIT_PROJECT_ID: {current_project_id or DEFAULT_PROJECT_ID}")
    print(f"INIT_TASK_FILE: {current_task_file or '(none)'}")
    print(f"INIT_TASK_STATUS: {current_status}")
    if current_run_id:
        print("INIT_RUN_ID_SOURCE: CURRENT_RUN_ID")
        print(f"INIT_RUN_ID: {current_run_id}")
    else:
        print("INIT_RUN_ID_SOURCE: session-context-only (init does not create business RUN_ID)")
        print("INIT_RUN_ID: (none)")

    emit_step("init", 2, init_steps_total, "打印账号与工具版本信息")
    gh_status = "missing"
    gh_version = "(not installed)"
    codex_version = "(not installed)"
    git_version = first_line(run_cmd(["git", "--version"]).stdout, "")
    python_version = "(missing)"

    if run_shell("command -v gh >/dev/null 2>&1").rc == 0:
        gh_version = first_line(run_cmd(["gh", "--version"]).stdout, gh_version)
        gh_status = "logged_in" if run_cmd(["gh", "auth", "status", "-h", "github.com"]).rc == 0 else "not_logged_in"
    if run_shell("command -v codex >/dev/null 2>&1").rc == 0:
        codex_version = first_line(run_cmd(["codex", "--version"]).stdout, codex_version)
    if run_shell("command -v python3 >/dev/null 2>&1").rc == 0:
        python_version = first_line(run_cmd(["python3", "--version"]).stdout, python_version)
    elif run_shell("command -v python >/dev/null 2>&1").rc == 0:
        python_version = first_line(run_cmd(["python", "--version"]).stdout, python_version)

    print(f"INIT_GH_STATUS: {gh_status}")
    print(f"INIT_GH_VERSION: {gh_version}")
    print(f"INIT_CODEX_VERSION: {codex_version}")
    print(f"INIT_GIT_VERSION: {git_version}")
    print(f"INIT_PYTHON_VERSION: {python_version}")

    emit_step("init", 3, init_steps_total, "打印分支与远端状态")
    branch = first_line(run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout, "unknown")
    remote_url = first_line(run_cmd(["git", "remote", "get-url", "origin"]).stdout, "(missing)")
    upstream = first_line(run_cmd(["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"]).stdout, "")
    ahead_count = "n/a"
    behind_count = "n/a"
    if upstream:
        lr = run_cmd(["git", "rev-list", "--left-right", "--count", f"{upstream}...HEAD"])
        parts = first_line(lr.stdout, "n/a n/a").split()
        if len(parts) >= 2:
            behind_count = parts[0]
            ahead_count = parts[1]
    print(f"INIT_BRANCH: {branch}")
    print(f"INIT_REMOTE_ORIGIN: {remote_url}")
    print(f"INIT_UPSTREAM: {upstream or '(none)'}")
    print(f"INIT_AHEAD_COUNT: {ahead_count}")
    print(f"INIT_BEHIND_COUNT: {behind_count}")
    if branch != "main":
        reason_codes.append("BRANCH_NOT_MAIN")

    emit_step("init", 4, init_steps_total, "检查工作区与 Git 操作状态")
    git_dir_text = first_line(run_cmd(["git", "rev-parse", "--git-dir"]).stdout, ".git")
    git_dir = Path(git_dir_text)
    git_op_reason = ""
    if (git_dir / "MERGE_HEAD").is_file():
        git_op_reason = "merge_in_progress"
    elif (git_dir / "rebase-merge").is_dir() or (git_dir / "rebase-apply").is_dir():
        git_op_reason = "rebase_in_progress"
    elif (git_dir / "CHERRY_PICK_HEAD").is_file():
        git_op_reason = "cherry_pick_in_progress"
    elif (git_dir / "REVERT_HEAD").is_file():
        git_op_reason = "revert_in_progress"
    if git_op_reason:
        reason_codes.append("GIT_OPERATION_IN_PROGRESS")

    worktree_dirty = run_shell("! git diff --quiet || ! git diff --cached --quiet || [[ -n \"$(git ls-files --others --exclude-standard)\" ]]").rc == 0
    if worktree_dirty:
        reason_codes.append("WORKTREE_DIRTY")

    staged_count = count_lines("git diff --cached --name-only | wc -l | tr -d '[:space:]'")
    unstaged_count = count_lines("git diff --name-only | wc -l | tr -d '[:space:]'")
    untracked_count = count_lines("git ls-files --others --exclude-standard | wc -l | tr -d '[:space:]'")
    diff_preview = list_lines("git status --short | head -n 20", limit=20)

    print(f"INIT_GIT_OPERATION: {git_op_reason or 'none'}")
    print(f"INIT_DIFF_SUMMARY: staged={staged_count},unstaged={unstaged_count},untracked={untracked_count}")
    if diff_preview:
        print("INIT_DIFF_FILES_START")
        for line in diff_preview:
            print(line)
        print("INIT_DIFF_FILES_END")
    else:
        print("INIT_DIFF_FILES: (clean)")

    emit_step("init", 5, init_steps_total, "打印当前 run/task 指针")
    print(
        "INIT_RUN_CONTEXT: "
        f"project_id={current_project_id or DEFAULT_PROJECT_ID},"
        f"run_id={current_run_id or '(none)'},"
        f"task={current_task_file or '(none)'},"
        f"status={current_status}"
    )

    emit_step("init", 6, init_steps_total, "打印最近变更证据")
    if worktree_dirty:
        print("INIT_LAST_CHANGE_SOURCE: worktree")
        if diff_preview:
            print("INIT_LAST_CHANGE_FILES_START")
            for line in diff_preview:
                print(line)
            print("INIT_LAST_CHANGE_FILES_END")
    else:
        commit_head = first_line(run_cmd(["git", "rev-parse", "--short", "HEAD"]).stdout, "(none)")
        commit_time = first_line(run_cmd(["git", "log", "-1", "--pretty=%cI"]).stdout, "(none)")
        commit_subject = first_line(run_cmd(["git", "log", "-1", "--pretty=%s"]).stdout, "(none)")
        print("INIT_LAST_CHANGE_SOURCE: last_commit")
        print(f"INIT_LAST_COMMIT: {commit_head}")
        print(f"INIT_LAST_COMMIT_TIME: {commit_time}")
        print(f"INIT_LAST_COMMIT_SUBJECT: {commit_subject}")
        commit_files = list_lines("git show --name-only --pretty=format: HEAD 2>/dev/null | sed '/^$/d' | head -n 20", limit=20)
        if commit_files:
            print("INIT_LAST_COMMIT_FILES_START")
            for line in commit_files:
                print(line)
            print("INIT_LAST_COMMIT_FILES_END")

    emit_step("init", 7, init_steps_total, "评估状态并输出下一步建议")
    reason_codes_text = ",".join(reason_codes) if reason_codes else "none"
    init_status = "ok"
    if init_mode == "main" and reason_codes:
        init_status = "blocked"
    elif reason_codes:
        init_status = "needs_resume"

    next_cmd = "tools/ops learn"
    if init_status != "ok":
        next_cmd = f"tools/ops resume RUN_ID={current_run_id}" if current_run_id else "tools/ops resume"

    print(f"INIT_STATUS: {init_status}")
    print(f"INIT_REASON_CODES: {reason_codes_text}")
    print(f"INIT_NEXT: {next_cmd}")
    if init_status != "ok" and show_resume_hint:
        print("INIT_HINT: repository state indicates unfinished/abnormal previous cycle; run resume before new work.")
    elif init_mode == "status":
        print("INIT_HINT: status-only mode, no resume reminder emitted.")

    if init_mode == "main" and init_status != "ok":
        return 1
    if init_mode == "check":
        print("== 建议流程 ==")
        print("1) tools/ops learn")
        print("2) tools/ops ready")
        print("3) tools/ops discuss TARGET=prepare")
        print("4) tools/ops do queue-next")
    else:
        print("== 状态查询完成 ==")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
