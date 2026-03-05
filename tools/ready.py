#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


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


def emit_step(index: int, total: int, message: str) -> None:
    print(f"READY_STEP[{index}/{total}]: {message}")
    emit_json_event("ready", "step", "ok", f"{index}/{total} {message}")


def run_cmd(args: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        input=input_text,
        capture_output=True,
        text=True,
        check=False,
    )


def run_shell(cmd: str) -> subprocess.CompletedProcess[str]:
    return run_cmd(["bash", "-lc", cmd])


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


def resolve_state_current_project_id() -> str:
    return normalize_project_id(state_field_value("CURRENT_PROJECT_ID"))


def resolve_state_current_run_id() -> str:
    return state_field_value("CURRENT_RUN_ID").strip()


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


def file_sha(path: Path) -> str:
    if not path.is_file():
        return "missing"
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception:
        return "error"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


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


def learn_file_matches_project(path: Path, project_id: str) -> bool:
    try:
        obj = read_json(path)
    except Exception:
        return False
    pid = str(obj.get("project_id") or "").strip() or DEFAULT_PROJECT_ID
    return pid == project_id


def resolve_learn_file_for_project(project_id: str) -> str:
    learn_file = Path("learn") / f"{project_id}.json"
    if learn_file.is_file() and learn_file_is_valid(learn_file) and learn_file_matches_project(learn_file, project_id):
        return str(learn_file)
    return ""


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


def resolve_sync_file_for_run(run_id: str) -> str:
    sync_file = Path("reports") / run_id / "sync_report.json"
    if sync_file.is_file() and sync_file_is_valid(sync_file):
        return str(sync_file)
    return ""


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


def is_dirty() -> bool:
    return run_shell('! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]').returncode == 0


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


def read_text(path: str) -> str:
    p = Path(path)
    if not p.is_file():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def generate_orient_draft(run_id: str, project_id: str, task_file: str, orient_file: str, orient_md: str) -> None:
    def count_open_queue_items(text: str) -> int:
        return len(re.findall(r"^- \[ \] ", text, flags=re.M))

    docs_paths = [
        "docs/PROJECT_GUIDE.md",
        "docs/WORKFLOW.md",
        "docs/ENTITIES.md",
        "AGENTS.md",
        "TASKS/STATE.md",
        "TASKS/QUEUE.md",
        f"learn/{project_id}.json",
        f"chatlogs/discussion/{run_id}/ready_brief.json",
    ]
    docs_blob = "\n".join(read_text(p) for p in docs_paths)
    queue_text = read_text("TASKS/QUEUE.md")
    open_items = count_open_queue_items(queue_text)
    low = docs_blob.lower()

    def score_for(base: int, keywords: list[str]) -> int:
        s = base
        for k in keywords:
            s += low.count(k.lower()) * 2
        return s

    directions: list[dict[str, Any]] = [
        {
            "id": "ready-exit-resolution",
            "title": "P0: ready 先处理未收尾 run（收尾/抛弃）",
            "why": "避免把历史中断状态混入新需求，先做生命周期分流。",
            "benefit": "减少混乱上下文和重复执行。",
            "risk": "增加一次显式确认步骤。",
            "cost": "S",
            "dependencies": ["TASKS/STATE.md", "reports/<RUN_ID>/ship_state.json"],
            "scope_hint": ["tools/*.py", "tests/"],
            "score": score_for(82, ["ready", "resume", "stop reason", "run", "state"]),
        },
        {
            "id": "ready-strong-brief",
            "title": "P1: ready 输出最强认知摘要与证据链",
            "why": "ready 通过后立即给出项目理解、宪法解读、工作流和下一步建议。",
            "benefit": "降低同频误差，提升决策速度。",
            "risk": "摘要质量受输入文档完整性影响。",
            "cost": "S",
            "dependencies": ["AGENTS.md", "docs/PROJECT_GUIDE.md", "learn/<PROJECT_ID>.json"],
            "scope_hint": ["tools/*.py", "docs/PROJECT_GUIDE.md", "docs/WORKFLOW.md"],
            "score": score_for(78, ["learn", "ready", "workflow", "constitution", "evidence"]),
        },
        {
            "id": "discussion-execution-split",
            "title": "P1: 讨论态与执行态证据分层",
            "why": "未确认方案只写讨论区，确认后再写 reports 执行证据。",
            "benefit": "保持 report 可审计且低噪声。",
            "risk": "需要清晰迁移边界。",
            "cost": "M",
            "dependencies": ["chatlogs/discussion/", "reports/<RUN_ID>/"],
            "scope_hint": ["tools/*.py", "docs/WORKFLOW.md", "AGENTS.md", "chatlogs/discussion/"],
            "score": score_for(76, ["discussion", "report", "confirm", "evidence", "orient"]),
        },
        {
            "id": "council-contract",
            "title": "P2: 多角色评审博弈 -> 统一执行契约",
            "why": "产品/架构/研发/测试独立评审，再收敛成单一 contract。",
            "benefit": "减少单视角偏差，提高执行稳定性。",
            "risk": "初期输出可能偏模板化。",
            "cost": "M",
            "dependencies": ["orient choice", "task contract"],
            "scope_hint": ["tools/*.py", "reports/<RUN_ID>/"],
            "score": score_for(70, ["product", "architect", "dev", "qa", "review", "contract"]),
        },
        {
            "id": "post-exec-drift-review",
            "title": "P2: 执行后偏差审计与自动修复",
            "why": "需求完成后自动检查目标/实现/测试/文档偏差并回补。",
            "benefit": "形成闭环，减少累计偏差。",
            "risk": "规则过严会增加时间成本。",
            "cost": "M",
            "dependencies": ["reports/<RUN_ID>/summary.md", "reports/<RUN_ID>/decision.md"],
            "scope_hint": ["tools/*.py", "tests/", "docs/WORKFLOW.md"],
            "score": score_for(66, ["review", "drift", "summary", "decision", "verify"]),
        },
    ]

    if open_items == 0:
        for item in directions:
            if item["id"] in {"discussion-execution-split", "ready-strong-brief"}:
                item["score"] += 6

    directions.sort(key=lambda x: x["score"], reverse=True)
    for idx, item in enumerate(directions):
        item["priority_rank"] = idx + 1
        item["priority"] = f"P{idx}"

    recommended = directions[0]["id"] if directions else ""
    next_cmd = f"python3 tools/choose.py RUN_ID={run_id} OPTION={recommended}" if recommended else f"python3 tools/choose.py RUN_ID={run_id} OPTION=<id>"
    obj = {
        "project_id": project_id,
        "run_id": run_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "discussion_mode": True,
        "task_file": task_file,
        "open_queue_items": open_items,
        "inputs": docs_paths,
        "directions": directions,
        "recommended_option": recommended,
        "next_command": next_cmd,
    }
    Path(orient_file).parent.mkdir(parents=True, exist_ok=True)
    Path(orient_file).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Orientation Draft",
        "",
        f"PROJECT_ID: `{project_id}`",
        f"RUN_ID: `{run_id}`",
        f"Generated At (UTC): {obj['created_at_utc']}",
        "Mode: discussion-only (not execution evidence)",
        f"Open Queue Items: {open_items}",
        "",
        "## Direction Options",
    ]
    for item in directions:
        lines.append(f"- id=`{item['id']}` | priority=`{item['priority']}` | score={item['score']}")
        lines.append(f"  - title: {item['title']}")
        lines.append(f"  - why: {item['why']}")
        lines.append(f"  - benefit: {item['benefit']}")
        lines.append(f"  - risk: {item['risk']}")
        lines.append(f"  - cost: {item['cost']}")
        lines.append(f"  - dependencies: {', '.join(item['dependencies'])}")
    lines.extend(["", "## Recommended", f"- `{recommended}`", "", "## Next Command", f"- `{next_cmd}`", ""])
    Path(orient_md).write_text("\n".join(lines), encoding="utf-8")

    print(f"ORIENT_OPTIONS: {len(directions)}")
    for idx, item in enumerate(directions[:5], start=1):
        print(
            f"ORIENT_OPTION_{idx}: id={item['id']} | priority={item['priority']} | "
            f"benefit={item['benefit']} | risk={item['risk']} | cost={item['cost']}"
        )
    print(f"ORIENT_RECOMMENDED: {recommended}")
    print(f"ORIENT_NEXT_COMMAND: {next_cmd}")
    print(f"ORIENT_PROJECT_ID: {project_id}")


def parse_bool_flag(raw: str, name: str, *, allow_auto: bool = False, auto_as: str = "1") -> str:
    v = raw.strip().lower()
    if allow_auto and v == "auto":
        return auto_as
    if v in {"1", "true", "yes", "y"}:
        return "1"
    if v in {"0", "false", "no", "n"}:
        return "0"
    eprint(f"ERROR: invalid {name}={raw}" + (" (expected auto|0|1)." if allow_auto else " (expected 0|1)."))
    raise SystemExit(2)


def write_ready_and_brief(
    ready_file: str,
    run_id: str,
    project_id: str,
    goal: str,
    scope: str,
    acceptance: str,
    steps: str,
    stop: str,
    learn_report_file: str,
    require_learn: str,
    sync_report_file: str,
    require_sync: str,
    resolution_required: int,
    continue_decision: str,
    ready_brief_json: str,
    ready_brief_md: str,
) -> None:
    sync_obj: dict[str, Any] = {}
    if sync_report_file:
        try:
            sync_obj = read_json(Path(sync_report_file))
        except Exception:
            sync_obj = {}

    project_summary = (sync_obj.get("project_overview") or {}).get("summary", "")
    north_star = (sync_obj.get("project_overview") or {}).get("north_star", "")
    if not project_summary:
        for raw in read_text("README.md").splitlines():
            s = raw.strip()
            if s and not s.startswith("#"):
                project_summary = s
                break
    if not project_summary:
        project_summary = "quant-factory-os governance/execution base for quant engineering."
    if not north_star:
        guide_lines = read_text("docs/PROJECT_GUIDE.md").splitlines()
        for i, raw in enumerate(guide_lines):
            if "一句话北极星" not in raw:
                continue
            for cand in guide_lines[i + 1 :]:
                s = cand.strip()
                if not s or s.startswith("#") or s.startswith(">") or s.startswith("-"):
                    continue
                north_star = s
                break
            break
    if not north_star:
        north_star = "自动化 -> 自我迭代 -> 涌现智能。"

    decision_exists = Path(f"reports/{run_id}/decision.md").is_file()
    summary_exists = Path(f"reports/{run_id}/summary.md").is_file()
    conversation_exists = Path(f"reports/{run_id}/conversation.md").is_file()
    execution_exists = Path(f"reports/{run_id}/execution.jsonl").is_file()
    ship_state_exists = Path(f"reports/{run_id}/ship_state.json").is_file()
    workflow_interpretation = "流程以门禁推进：sync 同频 -> ready 上岗 -> orient/choose 定方向 -> council/arbiter 收敛 -> slice 拆解 -> do 执行 -> verify/review/ship 收尾。"
    constitution_interpretation = "约束是任务驱动、证据优先、scope 严格、文档新鲜度硬门禁。"

    session_handoff = sync_obj.get("session_handoff") or {}
    current_stage = sync_obj.get("current_stage") or {}
    evidence_chain = {
        "learn_report_file": learn_report_file,
        "sync_report_file": sync_report_file,
        "ready_file": ready_file,
        "decision_exists": decision_exists,
        "summary_exists": summary_exists,
        "conversation_exists": conversation_exists,
        "execution_exists": execution_exists,
        "ship_state_exists": ship_state_exists,
    }
    created_at = datetime.now(timezone.utc).isoformat()
    obj = {
        "project_id": project_id,
        "run_id": run_id,
        "created_at_utc": created_at,
        "constitution_read": True,
        "workflow_read": True,
        "sync_gate": {
            "required": require_sync == "1",
            "sync_report_file": sync_report_file,
            "sync_passed": (bool(sync_report_file) if require_sync == "1" else True),
        },
        "learn_gate": {
            "required": require_learn == "1",
            "learn_report_file": learn_report_file,
            "learn_passed": (bool(learn_report_file) if require_learn == "1" else True),
        },
        "restatement_passed": True,
        "restatement": {
            "goal": goal,
            "scope": scope,
            "acceptance": acceptance,
            "steps": steps,
            "stop_condition": stop,
        },
        "prior_run_resolution": {
            "required": bool(resolution_required),
            "decision": continue_decision,
        },
        "understanding": {
            "project_summary": project_summary,
            "project_goal": north_star,
            "constitution_interpretation": constitution_interpretation,
            "workflow_interpretation": workflow_interpretation,
            "evidence_chain": evidence_chain,
            "session_continuity": session_handoff.get("continuity", "unknown"),
            "current_stage": current_stage,
            "suggested_next_step": f"python3 tools/orient.py RUN_ID={run_id}",
        },
    }
    Path(ready_file).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    brief_obj = {
        "project_id": project_id,
        "run_id": run_id,
        "created_at_utc": created_at,
        "project_summary": project_summary,
        "project_goal": north_star,
        "constitution_interpretation": constitution_interpretation,
        "workflow_interpretation": workflow_interpretation,
        "evidence_chain": evidence_chain,
        "session_continuity": session_handoff.get("continuity", "unknown"),
        "current_stage": current_stage,
        "restatement": obj["restatement"],
        "prior_run_resolution": obj["prior_run_resolution"],
    }
    Path(ready_brief_json).parent.mkdir(parents=True, exist_ok=True)
    Path(ready_brief_json).write_text(json.dumps(brief_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Ready Brief (Discussion Draft)",
        "",
        f"PROJECT_ID: `{project_id}`",
        f"RUN_ID: `{run_id}`",
        f"Generated At (UTC): {created_at}",
        "Mode: discussion-only (pre-confirmation)",
        "",
        "## 项目理解",
        f"- Summary: {project_summary}",
        f"- Goal: {north_star}",
        "",
        "## 宪法与工作流解读",
        f"- Constitution: {constitution_interpretation}",
        f"- Workflow: {workflow_interpretation}",
        "",
        "## 证据链状态",
    ]
    for key, value in evidence_chain.items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Session 承接",
            f"- continuity: {session_handoff.get('continuity', 'unknown')}",
            f"- current_run_id: {current_stage.get('current_run_id', run_id)}",
            f"- current_task_file: {current_stage.get('current_task_file', '(unknown)')}",
            f"- current_status: {current_stage.get('current_status', '(unknown)')}",
            "",
            "## Restatement",
            f"- Goal: {goal}",
            f"- Scope: {scope}",
            f"- Acceptance: {acceptance}",
            f"- Steps: {steps}",
            f"- Stop: {stop}",
            "",
            "## Run 决策",
            f"- resolution_required: {str(bool(resolution_required)).lower()}",
            f"- decision: {continue_decision}",
            "",
        ]
    )
    Path(ready_brief_md).write_text("\n".join(lines) + "\n", encoding="utf-8")


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


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    run_id = resolve_run_id_for_cmd(args["explicit_run_id"], "ready")
    if not run_id:
        eprint("ERROR: ready requires RUN_ID (from explicit arg/env or TASKS/STATE.md CURRENT_RUN_ID).")
        eprint("Usage: python3 tools/ready.py [RUN_ID=<run-id>] [DECISION=resume-close|abandon-new]")
        return 2
    project_id = resolve_project_id_for_cmd(args["explicit_project_id"], "ready")
    continue_decision = args["continue_decision"]
    ready_steps_total = 10

    emit_step(1, ready_steps_total, "resolve run context")

    require_sync = parse_bool_flag(os.environ.get("QF_READY_REQUIRE_SYNC", "0"), "QF_READY_REQUIRE_SYNC")
    auto_sync = parse_bool_flag(os.environ.get("QF_READY_AUTO_SYNC", "0"), "QF_READY_AUTO_SYNC")
    require_learn = parse_bool_flag(os.environ.get("QF_READY_REQUIRE_LEARN", "auto"), "QF_READY_REQUIRE_LEARN", allow_auto=True, auto_as="1")
    emit_step(2, ready_steps_total, "enforce learn gate")
    learn_report_file = ""
    if require_learn == "1":
        learn_report_file = resolve_learn_file_for_project(project_id)
        if not learn_report_file:
            eprint("ERROR: learn gate not satisfied.")
            eprint("Run: python3 tools/learn.py")
            eprint(f"Then retry: python3 tools/ready.py RUN_ID={run_id}")
            return 1

    emit_step(3, ready_steps_total, "resolve sync report (optional compatibility)")
    sync_report_file = resolve_sync_file_for_run(run_id)
    if require_sync == "1":
        if not sync_report_file and auto_sync == "1":
            print(f"SYNC_AUTO_RUN: bash tools/legacy.sh sync RUN_ID={run_id}")
            cp = run_cmd(["bash", "tools/legacy.sh", "sync", f"RUN_ID={run_id}"])
            if cp.stdout:
                sys.stdout.write(cp.stdout)
            if cp.stderr:
                sys.stderr.write(cp.stderr)
            if cp.returncode != 0:
                return int(cp.returncode)
            sync_report_file = resolve_sync_file_for_run(run_id)
        if not sync_report_file:
            eprint(f"ERROR: sync gate not satisfied for run {run_id}.")
            eprint(f"Run: bash tools/legacy.sh sync RUN_ID={run_id}")
            eprint(f"Then retry: python3 tools/ready.py RUN_ID={run_id}")
            return 1

    emit_step(4, ready_steps_total, "load task/state and detect unresolved run context")
    task_file = state_field_value("CURRENT_TASK_FILE")
    state_status = state_field_value("CURRENT_STATUS") or "active"
    has_run_context = any((Path(f"reports/{run_id}/ready.json").is_file(), Path(f"reports/{run_id}/ship_state.json").is_file(), Path(f"reports/{run_id}/handoff.md").is_file()))
    prior_resolution_decision = resolve_ready_prior_decision_for_run(run_id)
    resolution_required = 0
    if state_status != "done" and has_run_context:
        if prior_resolution_decision in {"abandon-new", "continue"}:
            resolution_required = 0
            if not continue_decision:
                continue_decision = prior_resolution_decision
        else:
            resolution_required = 1

    emit_step(5, ready_steps_total, "resolve run decision (resume-close / abandon-new / continue)")
    if resolution_required == 1:
        if not continue_decision:
            print("READY_NEEDS_DECISION: true")
            print(f"READY_DECISION_REASON: unresolved run context detected for {run_id} (CURRENT_STATUS={state_status})")
            print("READY_DECISION_OPTIONS: resume-close | abandon-new")
            print(f"READY_NEXT_1: bash tools/legacy.sh resume RUN_ID={run_id}")
            print(f"READY_NEXT_2: python3 tools/ready.py RUN_ID={run_id} DECISION=abandon-new")
            return 1
        if continue_decision == "resume-close":
            print("READY_DECISION: resume-close")
            print(f"READY_NEXT_COMMAND: bash tools/legacy.sh resume RUN_ID={run_id}")
            return 1
        if continue_decision != "abandon-new":
            eprint(f"ERROR: invalid DECISION={continue_decision}. expected resume-close or abandon-new.")
            return 2
    if not continue_decision:
        continue_decision = "continue"

    emit_step(6, ready_steps_total, "derive restatement defaults from task contract")
    goal_default = extract_task_goal_default(task_file)
    scope_default = extract_task_scope_default(task_file)
    acceptance_default = extract_task_acceptance_default(task_file)
    if not goal_default:
        goal_default = f"Continue {run_id} with a scoped, minimal, verifiable change."
    if not scope_default:
        scope_default = f"Follow declared scope in {task_file}" if task_file else "Follow active task scope"
    if not acceptance_default:
        acceptance_default = "make verify; update reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md; keep scope clean"
    stop_default = "finish and wait for next instruction; if blocked, record stop reason in decision.md"

    emit_step(7, ready_steps_total, "capture minimal ready contract")
    goal = resolve_ready_field("QF_READY_GOAL", "Goal (one sentence): ", goal_default)
    scope = resolve_ready_field("QF_READY_SCOPE", "Scope (exact paths): ", scope_default)
    acceptance = resolve_ready_field("QF_READY_ACCEPTANCE", "Acceptance (verify/evidence/scope): ", acceptance_default)
    stop = resolve_ready_field("QF_READY_STOP", "Stop condition: ", stop_default)
    if not all([goal, scope, acceptance, stop]):
        eprint("ERROR: ready fields cannot be empty.")
        return 1

    Path(f"reports/{run_id}").mkdir(parents=True, exist_ok=True)
    ready_file = f"reports/{run_id}/ready.json"
    emit_step(8, ready_steps_total, "write minimal ready.json")
    ready_obj = {
        "schema": "qf_ready.v2",
        "project_id": project_id,
        "run_id": run_id,
        "task_file": task_file,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "learn_gate": {
            "required": require_learn == "1",
            "learn_report_file": learn_report_file,
            "passed": bool(learn_report_file) if require_learn == "1" else True,
        },
        "sync_gate": {
            "required": require_sync == "1",
            "sync_report_file": sync_report_file,
            "passed": bool(sync_report_file) if require_sync == "1" else True,
        },
        "prior_run_resolution": {
            "required": bool(resolution_required),
            "decision": continue_decision,
        },
        "contract": {
            "goal": goal,
            "scope": scope,
            "acceptance": acceptance,
            "stop_condition": stop,
        },
        "next_command": "python3 tools/orient.py",
    }
    Path(ready_file).write_text(json.dumps(ready_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    emit_step(9, ready_steps_total, "append ready checkpoint and update state")
    append_execution_event(
        run_id,
        "ready",
        "ready_passed",
        "ok",
        "python3 tools/ready.py",
        f"ready_file={ready_file};learn_report={learn_report_file};sync_report={sync_report_file};task_file={task_file}",
        "",
    )
    append_conversation_checkpoint(run_id, "ready", "ready gate passed; next step orient")

    emit_step(10, ready_steps_total, "print minimal ready outputs")
    update_state_current(run_id, state_field_value("CURRENT_TASK_FILE"), "active", project_id)
    print(f"READY_PROJECT_ID: {project_id}")
    print(f"READY_RUN_ID: {run_id}")
    if task_file:
        print(f"READY_TASK_FILE: {task_file}")
    print(f"READY_LEARN_STATUS: {'pass' if learn_report_file or require_learn == '0' else 'fail'}")
    print(f"READY_DECISION: {continue_decision}")
    print(f"READY_GOAL: {goal}")
    print(f"READY_SCOPE: {scope}")
    print(f"READY_ACCEPTANCE: {acceptance}")
    print(f"READY_STOP: {stop}")
    print(f"READY_FILE: {ready_file}")
    if learn_report_file:
        print(f"READY_LEARN_REPORT: {learn_report_file}")
    if sync_report_file:
        print(f"READY_SYNC_REPORT: {sync_report_file}")
    print("READY_NEXT_COMMAND: python3 tools/orient.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
