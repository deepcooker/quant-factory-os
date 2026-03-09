#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from tools.common_helpers import file_sha, parse_bool_flag, read_json, read_text
except Exception:  # pragma: no cover
    from common_helpers import file_sha, parse_bool_flag, read_json, read_text  # type: ignore


STATE_FILE = Path(os.environ.get("QF_STATE_FILE", "TASKS/STATE.md"))
DEFAULT_PROJECT_ID = os.environ.get("QF_DEFAULT_PROJECT_ID", "project-0")


@dataclass
class ReadyContext:
    args: dict[str, Any]
    run_id: str
    project_id: str
    continue_decision: str
    require_sync: str
    auto_sync: str
    require_learn: str
    learn_report_file: str = ""
    sync_report_file: str = ""
    task_file: str = ""
    state_status: str = "active"
    resolution_required: int = 0
    goal_default: str = ""
    scope_default: str = ""
    acceptance_default: str = ""
    stop_default: str = ""
    goal: str = ""
    scope: str = ""
    acceptance: str = ""
    stop: str = ""
    ready_file: str = ""


# ready_tools_01 中文：向标准错误输出 ready 阶段的错误提示。
def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


# ready_tools_02 中文：判断 ready 是否需要输出 JSON 事件流。
def should_emit_json_stream() -> bool:
    value = os.environ.get("QF_EVENT_STREAM", "0").strip().lower()
    return value in {"1", "json", "jsonl"}


# ready_tools_03 中文：输出 ready 阶段的 JSON 结构化事件。
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


# ready_tools_04 中文：输出 ready 阶段的步骤锚点。
def emit_step(index: int, total: int, message: str) -> None:
    print(f"READY_STEP[{index}/{total}]: {message}")
    emit_json_event("ready", "step", "ok", f"{index}/{total} {message}")


# ready_tools_05 中文：执行直接命令并返回完整进程结果。
def run_cmd(args: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


# ready_tools_06 中文：通过 shell 执行命令字符串。
def run_shell(cmd: str) -> subprocess.CompletedProcess[str]:
    return run_cmd(["bash", "-lc", cmd])


# ready_tools_07 中文：从 TASKS/STATE.md 读取指定字段值。
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


# ready_tools_08 中文：规范化 project_id。
def normalize_project_id(value: str | None) -> str:
    v = (value or "").strip()
    return v if v else DEFAULT_PROJECT_ID


# ready_tools_09 中文：读取当前 active project_id。
def resolve_state_current_project_id() -> str:
    return normalize_project_id(state_field_value("CURRENT_PROJECT_ID"))


# ready_tools_10 中文：读取当前 active run_id。
def resolve_state_current_run_id() -> str:
    return state_field_value("CURRENT_RUN_ID").strip()


# ready_tools_11 中文：在没有显式 run_id 时回退到最近的报告目录。
def resolve_latest_report_run_id() -> str:
    root = Path("reports")
    if not root.exists():
        return ""
    cands: list[tuple[float, str]] = []
    for d in root.glob("run-*"):
        if not d.is_dir():
            continue
        mt = 0.0
        for name in ("ready.json", "execution.jsonl", "conversation.md", "handoff.md", "decision.md", "summary.md", "ship_state.json"):
            p = d / name
            if p.exists():
                mt = max(mt, p.stat().st_mtime)
        if mt > 0:
            cands.append((mt, d.name))
    if cands:
        cands.sort(reverse=True)
        return cands[0][1]
    return ""


# ready_tools_12 中文：解析 ready 使用的 run_id 并校验一致性。
def resolve_run_id_for_cmd(explicit_run_id: str, context: str) -> str:
    state_run_id = resolve_state_current_run_id()
    if explicit_run_id:
        if state_run_id and explicit_run_id != state_run_id and os.environ.get("QF_ALLOW_RUN_ID_MISMATCH", "0") != "1":
            eprint(f"ERROR: {context} run-id mismatch.")
            eprint(f"  explicit: {explicit_run_id}")
            eprint(f"  CURRENT_RUN_ID (TASKS/STATE.md): {state_run_id}")
            eprint("  Fix: update TASKS/STATE.md or pass QF_ALLOW_RUN_ID_MISMATCH=1 for one-time override.")
            raise SystemExit(1)
        return explicit_run_id
    if state_run_id:
        return state_run_id
    latest = resolve_latest_report_run_id()
    if latest:
        eprint(f"WARN: {context} fallback to latest report run-id: {latest}")
        return latest
    return ""


# ready_tools_13 中文：解析 ready 使用的 project_id 并校验一致性。
def resolve_project_id_for_cmd(explicit_project_id: str, context: str) -> str:
    state_project_id = resolve_state_current_project_id()
    explicit = explicit_project_id.strip()
    if explicit:
        resolved = normalize_project_id(explicit)
        if state_project_id and resolved != state_project_id and os.environ.get("QF_ALLOW_PROJECT_ID_MISMATCH", "0") != "1":
            eprint(f"ERROR: {context} project-id mismatch.")
            eprint(f"  explicit: {resolved}")
            eprint(f"  CURRENT_PROJECT_ID (TASKS/STATE.md): {state_project_id}")
            eprint("  Fix: update TASKS/STATE.md or pass QF_ALLOW_PROJECT_ID_MISMATCH=1 for one-time override.")
            raise SystemExit(1)
        return resolved
    if state_project_id:
        return state_project_id
    return DEFAULT_PROJECT_ID


# ready_tools_14 中文：校验 learn 文件是否可作为 ready 输入。
def learn_file_is_valid(path: Path) -> bool:
    try:
        obj = read_json(path)
    except Exception:
        return False
    if not obj.get("learn_passed"):
        return False
    model_sync = obj.get("model_sync")
    if not isinstance(model_sync, dict):
        return False
    if str(model_sync.get("mode", "")).strip() != "1":
        return False
    if str(model_sync.get("plan_mode", "")).strip() != "strong":
        return False
    if str(model_sync.get("status", "")).strip() != "pass":
        return False
    if not bool(model_sync.get("passed")):
        return False
    model_result = model_sync.get("result")
    if not isinstance(model_result, dict):
        return False
    if str(obj.get("schema", "")).strip() != "qf_learn.v3":
        return False
    if str(model_sync.get("plan_transport", "")).strip() != "app-server":
        return False
    for key in ["mainline", "current_stage", "next_step", "files_read", "plan_protocol", "oral_restate", "guide_oral", "anchor_realign", "practice"]:
        if key not in model_result:
            return False
    if not isinstance(model_result.get("files_read"), list) or not model_result.get("files_read"):
        return False
    if not isinstance(model_result.get("guide_oral"), list) or not model_result.get("guide_oral"):
        return False
    anchor = model_result.get("anchor_realign") or {}
    if not isinstance(anchor, dict):
        return False
    for key in ["question_id", "status", "drift_detail", "return_to_mainline"]:
        if key not in anchor:
            return False
    if str(anchor.get("status", "")).strip() not in {"on_track", "drifted"}:
        return False
    practice = model_result.get("practice") or {}
    if not isinstance(practice, dict):
        return False
    if int(practice.get("command_execution_count", 0)) < 1:
        return False
    samples = practice.get("command_samples")
    if not isinstance(samples, list) or not samples:
        return False

    context_files = obj.get("context_files") or []
    skill_files = obj.get("skill_files") or []
    if not isinstance(context_files, list):
        context_files = []
    if not isinstance(skill_files, list):
        skill_files = []
    digest_lines: list[str] = []
    for rel in context_files:
        digest_lines.append(f"ctx:{rel}:{file_sha(Path(str(rel)))}")
    for rel in skill_files:
        digest_lines.append(f"skill:{rel}:{file_sha(Path(str(rel)))}")
    digest_lines.sort()
    current = hashlib.sha256("\n".join(digest_lines).encode("utf-8")).hexdigest()
    return current == str(obj.get("context_digest", "")).strip()


# ready_tools_15 中文：检查 learn 文件是否属于当前项目。
def learn_file_matches_project(path: Path, project_id: str) -> bool:
    try:
        obj = read_json(path)
    except Exception:
        return False
    pid = str(obj.get("project_id") or "").strip() or DEFAULT_PROJECT_ID
    return pid == project_id


# ready_tools_16 中文：定位当前项目对应的 learn 文件。
def resolve_learn_file_for_project(project_id: str) -> str:
    learn_file = Path("learn") / f"{project_id}.json"
    if learn_file.is_file() and learn_file_is_valid(learn_file) and learn_file_matches_project(learn_file, project_id):
        return str(learn_file)
    return ""


# ready_tools_17 中文：校验同步文件是否有效。
def sync_file_is_valid(path: Path) -> bool:
    try:
        obj = read_json(path)
    except Exception:
        return False
    if not obj.get("sync_passed"):
        return False
    if obj.get("missing_required_files"):
        return False
    if not obj.get("files_read"):
        return False
    return True


# ready_tools_18 中文：定位指定 run 的同步文件。
def resolve_sync_file_for_run(run_id: str) -> str:
    sync_file = Path("reports") / run_id / "sync_report.json"
    if sync_file.is_file() and sync_file_is_valid(sync_file):
        return str(sync_file)
    return ""


# ready_tools_19 中文：读取 ready 前已有的决策说明。
def resolve_ready_prior_decision_for_run(run_id: str) -> str:
    if not run_id:
        return ""
    ready_file = Path("reports") / run_id / "ready.json"
    if not ready_file.is_file():
        return ""
    try:
        obj = read_json(ready_file)
    except Exception:
        return ""
    prior = obj.get("prior_run_resolution") or {}
    if isinstance(prior, dict):
        v = prior.get("decision")
        if v is not None:
            return str(v).strip()
    return ""


# ready_tools_20 中文：从 task 文件中提取默认 Goal。
def extract_task_goal_default(task_file: str) -> str:
    p = Path(task_file) if task_file else None
    if not p or not p.is_file():
        return ""
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    in_goal = False
    for raw in lines:
        if re.match(r"^##\s+Goal", raw):
            in_goal = True
            continue
        if in_goal and re.match(r"^##\s+", raw):
            break
        if in_goal and re.search(r"\S", raw):
            return raw.strip()
    return ""


# ready_tools_21 中文：从 task 文件中提取默认 Scope。
def extract_task_scope_default(task_file: str) -> str:
    p = Path(task_file) if task_file else None
    if not p or not p.is_file():
        return ""
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    in_scope = False
    out: list[str] = []
    for raw in lines:
        if re.match(r"^##\s+Scope", raw):
            in_scope = True
            continue
        if in_scope and re.match(r"^##\s+", raw):
            break
        if in_scope and re.match(r"^\s*-\s*", raw):
            line = re.sub(r"^\s*-\s*", "", raw)
            line = line.replace("`", "").strip()
            if line:
                out.append(line)
    return ", ".join(out)


# ready_tools_22 中文：从 task 文件中提取默认 Acceptance。
def extract_task_acceptance_default(task_file: str) -> str:
    p = Path(task_file) if task_file else None
    if not p or not p.is_file():
        return ""
    lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
    in_accept = False
    out: list[str] = []
    for raw in lines:
        if re.match(r"^##\s+Acceptance", raw):
            in_accept = True
            continue
        if in_accept and re.match(r"^##\s+", raw):
            break
        if in_accept and re.match(r"^\s*-\s*", raw):
            line = re.sub(r"^\s*-\s*", "", raw)
            line = re.sub(r"^\[[ xX]\]\s*", "", line)
            line = line.replace("`", "").strip()
            if line:
                out.append(line)
    return "; ".join(out)


# ready_tools_23 中文：解析 ready 字段的环境变量或默认值。
def resolve_ready_field(env_key: str, prompt: str, default_value: str) -> str:
    value = os.environ.get(env_key, "")
    auto_mode = os.environ.get("QF_READY_AUTO", "1")
    if value:
        return value
    if auto_mode == "1" and default_value:
        return default_value
    if sys.stdin.isatty():
        try:
            return input(prompt)
        except EOFError:
            return ""
    eprint(f"ERROR: missing {env_key} and no interactive stdin for prompt: {prompt}")
    raise SystemExit(1)


# ready_tools_24 中文：更新 TASKS/STATE.md 的当前指针。
def update_state_current(run_id: str, task_file: str, status: str, project_id: str) -> None:
    if os.environ.get("QF_STATE_UPDATE_DISABLE", "0") == "1":
        return
    project_id = normalize_project_id(project_id or state_field_value("CURRENT_PROJECT_ID"))
    path = STATE_FILE
    if path.exists():
        lines = path.read_text(encoding="utf-8").splitlines()
    else:
        lines = ["# STATE", ""]

    keys = {"CURRENT_PROJECT_ID", "CURRENT_RUN_ID", "CURRENT_TASK_FILE", "CURRENT_STATUS", "CURRENT_UPDATED_AT"}
    filtered: list[str] = []
    for line in lines:
        if any(re.match(rf"^\s*{re.escape(key)}\s*:", line) for key in keys):
            continue
        filtered.append(line)

    insert_idx = 0
    if filtered and filtered[0].startswith("#"):
        insert_idx = 1
        if len(filtered) > 1 and filtered[1].strip() == "":
            insert_idx = 2

    meta = [
        f"CURRENT_PROJECT_ID: {project_id}",
        f"CURRENT_RUN_ID: {run_id}",
        f"CURRENT_TASK_FILE: {task_file}",
        f"CURRENT_STATUS: {status}",
        f"CURRENT_UPDATED_AT: {datetime.now(timezone.utc).replace(microsecond=0).isoformat()}",
        "",
    ]
    out = filtered[:insert_idx] + meta + filtered[insert_idx:]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")


# ready_tools_25 中文：判断当前工作区是否脏。
def is_dirty() -> bool:
    return run_shell('! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]').returncode == 0


# ready_tools_26 中文：把执行事件追加到 run 级 execution 日志。
def append_execution_event(run_id: str, phase: str, action: str, status: str, command: str, artifacts: str, error: str) -> None:
    if not run_id or os.environ.get("QF_LOG_DISABLE", "0") == "1":
        return
    max_len = int(os.environ.get("QF_LOG_MAX_LEN", "200"))
    def short(s: str) -> str:
        s2 = s
        if len(s2) > max_len:
            s2 = s2[:max_len] + "...(truncated)"
        return s2
    obj = {
        "ts": datetime.now().astimezone().isoformat(timespec="seconds"),
        "run_id": run_id,
        "phase": phase,
        "action": action,
        "status": status,
        "command": short(command),
        "artifacts": short(artifacts),
        "error": short(error),
    }
    path = Path("reports") / run_id / "execution.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


# ready_tools_27 中文：写入 run 级会话检查点文本。
def append_conversation_checkpoint(run_id: str, phase: str, note: str) -> None:
    if not run_id or os.environ.get("QF_AUTO_CONVERSATION", "1") != "1":
        return
    file = Path("reports") / run_id / "conversation.md"
    file.parent.mkdir(parents=True, exist_ok=True)
    now_iso = datetime.now().astimezone().isoformat(timespec="seconds")
    branch = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip() or "unknown"
    head = run_cmd(["git", "rev-parse", "--short", "HEAD"]).stdout.strip() or "none"
    status_line = "dirty" if is_dirty() else "clean"
    with file.open("a", encoding="utf-8") as f:
        f.write(f"## {now_iso}\n")
        f.write(f"- phase: `{phase}`\n")
        f.write(f"- branch: `{branch}`\n")
        f.write(f"- head: `{head}`\n")
        f.write(f"- working_tree: `{status_line}`\n")
        f.write(f"- note: {note if note else '(empty)'}\n\n")


# ready_tools_28 中文：解析 ready 的命令行参数。
def parse_args(argv: list[str]) -> dict[str, Any]:
    explicit_run_id = ""
    explicit_project_id = os.environ.get("QF_PROJECT_ID", os.environ.get("PROJECT_ID", ""))
    continue_decision = os.environ.get("QF_READY_CONTINUE_DECISION", "")
    for token in argv:
        if not token:
            continue
        if token.startswith("RUN_ID="):
            explicit_run_id = token.split("=", 1)[1]
        elif token.startswith("PROJECT_ID="):
            explicit_project_id = token.split("=", 1)[1]
        elif token.startswith("DECISION="):
            continue_decision = token.split("=", 1)[1]
        else:
            if not explicit_run_id:
                explicit_run_id = token
            elif not continue_decision:
                continue_decision = token
    if not explicit_run_id and os.environ.get("RUN_ID"):
        explicit_run_id = os.environ["RUN_ID"]
    return {
        "explicit_run_id": explicit_run_id,
        "explicit_project_id": explicit_project_id,
        "continue_decision": continue_decision.strip(),
    }


# 3001 中文：第一步，解析 ready 运行上下文和门禁配置。
def ready_step_01_resolve_context(argv: list[str]) -> ReadyContext:
    emit_step(1, 5, "resolve run context")
    args = parse_args(argv)
    run_id = resolve_run_id_for_cmd(args["explicit_run_id"], "ready")
    if not run_id:
        eprint("ERROR: ready requires RUN_ID (from explicit arg/env or TASKS/STATE.md CURRENT_RUN_ID).")
        eprint("Usage: python3 tools/ready.py [RUN_ID=<run-id>] [DECISION=resume-close|abandon-new]")
        raise SystemExit(2)
    project_id = resolve_project_id_for_cmd(args["explicit_project_id"], "ready")
    return ReadyContext(
        args=args,
        run_id=run_id,
        project_id=project_id,
        continue_decision=args["continue_decision"],
        require_sync=parse_bool_flag(os.environ.get("QF_READY_REQUIRE_SYNC", "0"), "QF_READY_REQUIRE_SYNC"),
        auto_sync=parse_bool_flag(os.environ.get("QF_READY_AUTO_SYNC", "0"), "QF_READY_AUTO_SYNC"),
        require_learn=parse_bool_flag(os.environ.get("QF_READY_REQUIRE_LEARN", "auto"), "QF_READY_REQUIRE_LEARN", allow_auto=True, auto_as="1"),
    )


# 3002 中文：第二步，校验 learn/sync 输入门禁是否满足。
def ready_step_02_enforce_inputs(context: ReadyContext) -> ReadyContext:
    emit_step(2, 5, "enforce learn and sync gates")
    if context.require_learn == "1":
        context.learn_report_file = resolve_learn_file_for_project(context.project_id)
        if not context.learn_report_file:
            eprint("ERROR: learn gate not satisfied.")
            eprint("Run: python3 tools/learn.py")
            eprint(f"Then retry: python3 tools/ready.py RUN_ID={context.run_id}")
            raise SystemExit(1)

    context.sync_report_file = resolve_sync_file_for_run(context.run_id)
    if context.require_sync == "1":
        if not context.sync_report_file and context.auto_sync == "1":
            print(f"SYNC_AUTO_RUN: bash tools/legacy.sh sync RUN_ID={context.run_id}")
            cp = run_cmd(["bash", "tools/legacy.sh", "sync", f"RUN_ID={context.run_id}"])
            if cp.stdout:
                sys.stdout.write(cp.stdout)
            if cp.stderr:
                sys.stderr.write(cp.stderr)
            if cp.returncode != 0:
                raise SystemExit(int(cp.returncode))
            context.sync_report_file = resolve_sync_file_for_run(context.run_id)
        if not context.sync_report_file:
            eprint(f"ERROR: sync gate not satisfied for run {context.run_id}.")
            eprint(f"Run: bash tools/legacy.sh sync RUN_ID={context.run_id}")
            eprint(f"Then retry: python3 tools/ready.py RUN_ID={context.run_id}")
            raise SystemExit(1)
    return context


# 3003 中文：第三步，处理未收口 run 的继续决策并生成默认合同草稿。
def ready_step_03_resolve_decision(context: ReadyContext) -> ReadyContext:
    emit_step(3, 5, "resolve run decision and derive defaults")
    context.task_file = state_field_value("CURRENT_TASK_FILE")
    context.state_status = state_field_value("CURRENT_STATUS") or "active"
    has_run_context = any(
        (
            Path(f"reports/{context.run_id}/ready.json").is_file(),
            Path(f"reports/{context.run_id}/ship_state.json").is_file(),
            Path(f"reports/{context.run_id}/handoff.md").is_file(),
        )
    )
    prior_resolution_decision = resolve_ready_prior_decision_for_run(context.run_id)
    if context.state_status != "done" and has_run_context:
        if prior_resolution_decision in {"abandon-new", "continue"}:
            context.resolution_required = 0
            if not context.continue_decision:
                context.continue_decision = prior_resolution_decision
        else:
            context.resolution_required = 1

    if context.resolution_required == 1:
        if not context.continue_decision:
            print("READY_NEEDS_DECISION: true")
            print(f"READY_DECISION_REASON: unresolved run context detected for {context.run_id} (CURRENT_STATUS={context.state_status})")
            print("READY_DECISION_OPTIONS: resume-close | abandon-new")
            print(f"READY_NEXT_1: bash tools/legacy.sh resume RUN_ID={context.run_id}")
            print(f"READY_NEXT_2: python3 tools/ready.py RUN_ID={context.run_id} DECISION=abandon-new")
            raise SystemExit(1)
        if context.continue_decision == "resume-close":
            print("READY_DECISION: resume-close")
            print(f"READY_NEXT_COMMAND: bash tools/legacy.sh resume RUN_ID={context.run_id}")
            raise SystemExit(1)
        if context.continue_decision != "abandon-new":
            eprint(f"ERROR: invalid DECISION={context.continue_decision}. expected resume-close or abandon-new.")
            raise SystemExit(2)
    if not context.continue_decision:
        context.continue_decision = "continue"

    context.goal_default = extract_task_goal_default(context.task_file)
    context.scope_default = extract_task_scope_default(context.task_file)
    context.acceptance_default = extract_task_acceptance_default(context.task_file)
    if not context.goal_default:
        context.goal_default = f"Continue {context.run_id} with a scoped, minimal, verifiable change."
    if not context.scope_default:
        context.scope_default = f"Follow declared scope in {context.task_file}" if context.task_file else "Follow active task scope"
    if not context.acceptance_default:
        context.acceptance_default = "make verify; update reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md; keep scope clean"
    context.stop_default = "finish and wait for next instruction; if blocked, record stop reason in decision.md"
    return context


# 3004 中文：第四步，生成 ready 合同并写入 ready.json。
def ready_step_04_write_ready_contract(context: ReadyContext) -> ReadyContext:
    emit_step(4, 5, "capture ready contract and write ready.json")
    context.goal = resolve_ready_field("QF_READY_GOAL", "Goal (one sentence): ", context.goal_default)
    context.scope = resolve_ready_field("QF_READY_SCOPE", "Scope (exact paths): ", context.scope_default)
    context.acceptance = resolve_ready_field("QF_READY_ACCEPTANCE", "Acceptance (verify/evidence/scope): ", context.acceptance_default)
    context.stop = resolve_ready_field("QF_READY_STOP", "Stop condition: ", context.stop_default)
    if not all([context.goal, context.scope, context.acceptance, context.stop]):
        eprint("ERROR: ready fields cannot be empty.")
        raise SystemExit(1)

    Path(f"reports/{context.run_id}").mkdir(parents=True, exist_ok=True)
    context.ready_file = f"reports/{context.run_id}/ready.json"
    ready_obj = {
        "schema": "qf_ready.v2",
        "project_id": context.project_id,
        "run_id": context.run_id,
        "task_file": context.task_file,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "constitution_read": True,
        "workflow_read": True,
        "learn_gate": {
            "required": context.require_learn == "1",
            "learn_report_file": context.learn_report_file,
            "passed": bool(context.learn_report_file) if context.require_learn == "1" else True,
            "learn_passed": bool(context.learn_report_file) if context.require_learn == "1" else True,
        },
        "sync_gate": {
            "required": context.require_sync == "1",
            "sync_report_file": context.sync_report_file,
            "passed": bool(context.sync_report_file) if context.require_sync == "1" else True,
            "sync_passed": bool(context.sync_report_file) if context.require_sync == "1" else True,
        },
        "restatement_passed": True,
        "restatement": {
            "goal": context.goal,
            "scope": context.scope,
            "acceptance": context.acceptance,
            "steps": [],
            "stop_condition": context.stop,
        },
        "prior_run_resolution": {
            "required": bool(context.resolution_required),
            "decision": context.continue_decision,
        },
        "contract": {
            "goal": context.goal,
            "scope": context.scope,
            "acceptance": context.acceptance,
            "stop_condition": context.stop,
        },
        "next_command": "python3 tools/orient.py",
    }
    Path(context.ready_file).write_text(json.dumps(ready_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return context


# 3005 中文：第五步，回写状态、记录证据并打印 ready 结果。
def ready_step_05_finalize(context: ReadyContext) -> int:
    emit_step(5, 5, "publish ready outputs")
    append_execution_event(
        context.run_id,
        "ready",
        "ready_passed",
        "ok",
        "python3 tools/ready.py",
        f"ready_file={context.ready_file};learn_report={context.learn_report_file};sync_report={context.sync_report_file};task_file={context.task_file}",
        "",
    )
    append_conversation_checkpoint(context.run_id, "ready", "ready gate passed; next step orient")
    update_state_current(context.run_id, state_field_value("CURRENT_TASK_FILE"), "active", context.project_id)
    print(f"READY_PROJECT_ID: {context.project_id}")
    print(f"READY_RUN_ID: {context.run_id}")
    if context.task_file:
        print(f"READY_TASK_FILE: {context.task_file}")
    print(f"READY_LEARN_STATUS: {'pass' if context.learn_report_file or context.require_learn == '0' else 'fail'}")
    print(f"READY_DECISION: {context.continue_decision}")
    print(f"READY_GOAL: {context.goal}")
    print(f"READY_SCOPE: {context.scope}")
    print(f"READY_ACCEPTANCE: {context.acceptance}")
    print(f"READY_STOP: {context.stop}")
    print(f"READY_FILE: {context.ready_file}")
    if context.learn_report_file:
        print(f"READY_LEARN_REPORT: {context.learn_report_file}")
    if context.sync_report_file:
        print(f"READY_SYNC_REPORT: {context.sync_report_file}")
    print("READY_NEXT_COMMAND: python3 tools/orient.py")
    return 0


# 3006 中文：执行 ready 主流程，main 只负责分发五个业务步骤。
def main(argv: list[str]) -> int:
    context = ready_step_01_resolve_context(argv)
    context = ready_step_02_enforce_inputs(context)
    context = ready_step_03_resolve_decision(context)
    context = ready_step_04_write_ready_contract(context)
    return ready_step_05_finalize(context)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
