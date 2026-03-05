#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from tools.codex_transport import (
        MODEL_TRANSPORT_FALLBACK,
        MODEL_TRANSPORT_PRIMARY,
        TransportArtifacts,
        TransportRequest,
        extract_command_evidence,
        run_plan_sync,
        runtime_reasoning_effort,
    )
except Exception:  # pragma: no cover
    from codex_transport import (  # type: ignore
        MODEL_TRANSPORT_FALLBACK,
        MODEL_TRANSPORT_PRIMARY,
        TransportArtifacts,
        TransportRequest,
        extract_command_evidence,
        run_plan_sync,
        runtime_reasoning_effort,
    )

STATE_FILE = Path(os.environ.get("QF_STATE_FILE", "TASKS/STATE.md"))
DEFAULT_PROJECT_ID = os.environ.get("QF_DEFAULT_PROJECT_ID", "project-0")
LEARN_LOG_FILE_TEMPLATE = "learn/{project_id}.stdout.log"
LEARN_MODEL_NAME = "gpt-5.3-codex"
LEARN_REASONING_DEFAULT_PROFILE = "xhigh"
LEARN_REASONING_PROFILE_TO_EFFORT = {
    "minimal": "minimal",
    "low": "low",
    "medium": "medium",
    "high": "high",
    "xhigh": "xhigh",
}


def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)


def normalize_project_id(value: str | None) -> str:
    v = (value or "").strip()
    return v if v else DEFAULT_PROJECT_ID


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


def resolve_project_id_for_cmd(explicit_project_id: str, context: str) -> str:
    state_project_id = normalize_project_id(state_field_value("CURRENT_PROJECT_ID"))
    explicit = explicit_project_id.strip()
    if explicit:
        resolved = normalize_project_id(explicit)
        allow_mismatch = os.environ.get("QF_ALLOW_PROJECT_ID_MISMATCH", "0") == "1"
        if state_project_id and resolved != state_project_id and not allow_mismatch:
            eprint(f"ERROR: {context} project-id mismatch.")
            eprint(f"  explicit: {resolved}")
            eprint(f"  CURRENT_PROJECT_ID (TASKS/STATE.md): {state_project_id}")
            eprint("  Fix: update TASKS/STATE.md or pass QF_ALLOW_PROJECT_ID_MISMATCH=1 for one-time override.")
            raise SystemExit(1)
        return resolved
    if state_project_id:
        return state_project_id
    return DEFAULT_PROJECT_ID


def should_emit_json_stream() -> bool:
    value = os.environ.get("QF_EVENT_STREAM", "0").strip().lower()
    return value in {"1", "json", "jsonl"}


def emit_step(index: int, total: int, detail: str) -> None:
    print(f"LEARN_STEP[{index}/{total}]: {detail}")
    if should_emit_json_stream():
        payload = {
            "ts_utc": datetime.now(timezone.utc).isoformat(),
            "tool": "core",
            "cmd": "learn",
            "step_index": index,
            "step_total": total,
            "detail": detail,
        }
        print(json.dumps(payload, ensure_ascii=False))


def ordered_unique(items: list[str]) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in items:
        s = str(item).strip()
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s)
    return out


def file_sha(path: Path) -> tuple[str, str]:
    if not path.is_file():
        return ("missing", "missing")
    try:
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
    except Exception:
        return ("error", "error")
    return ("ok", digest)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_cli(argv: list[str]) -> dict[str, Any]:
    reasoning_profile = LEARN_REASONING_DEFAULT_PROFILE

    for token in argv:
        if not token:
            continue
        low = token.lower()
        if token.startswith("project_id=") or low.startswith("project_id="):
            eprint("ERROR: PROJECT_ID is no longer accepted by learn; use TASKS/STATE.md CURRENT_PROJECT_ID or default project-0.")
            raise SystemExit(2)
        elif token.startswith("ttl_days=") or low.startswith("ttl_days="):
            eprint("ERROR: TTL_DAYS has been removed from learn.")
            raise SystemExit(2)
        elif token.startswith("model_sync=") or low.startswith("model_sync="):
            eprint("ERROR: MODEL_SYNC is fixed to 1 in learn and cannot be overridden.")
            raise SystemExit(2)
        elif token.startswith("plan_mode=") or low.startswith("plan_mode="):
            eprint("ERROR: PLAN_MODE is fixed to strong in learn and cannot be overridden.")
            raise SystemExit(2)
        elif token.startswith("plan_transport=") or low.startswith("plan_transport="):
            eprint("ERROR: plan_transport has been removed; learn transport is fixed to auto(app-server->exec).")
            raise SystemExit(2)
        elif token.startswith("model_timeout_sec=") or low.startswith("model_timeout_sec="):
            eprint("ERROR: MODEL_TIMEOUT_SEC has been removed from learn.")
            raise SystemExit(2)
        elif token.startswith("model=") or low.startswith("model="):
            eprint("ERROR: model is fixed in learn. Edit LEARN_MODEL_NAME constant in tools/learn.py if needed.")
            raise SystemExit(2)
        elif token.startswith("model_reasoning_effort=") or low.startswith("model_reasoning_effort="):
            eprint("ERROR: use reasoning=<minimal|low|medium|high|xhigh> or -minimal|-low|-medium|-high|-xhigh.")
            raise SystemExit(2)
        elif token.startswith("reasoning="):
            reasoning_profile = token.split("=", 1)[1].strip().lower()
        elif low.startswith("reasoning="):
            eprint("ERROR: parameter key must be lowercase: reasoning=...")
            raise SystemExit(2)
        elif token in {"-minimal", "-low", "-medium", "-high", "-xhigh"}:
            reasoning_profile = token.lstrip("-")
        elif low in {"-minimal", "-low", "-medium", "-high", "-xhigh"}:
            eprint("ERROR: reasoning flag must be lowercase: -minimal|-low|-medium|-high|-xhigh.")
            raise SystemExit(2)
        elif token == "-fast" or low == "-fast":
            eprint("ERROR: -fast has been removed. Use -minimal|-low|-medium|-high|-xhigh.")
            raise SystemExit(2)
        elif token in {"-log", "--log"} or low in {"-log", "--log"}:
            eprint("ERROR: -log/--log is no longer needed; learn always mirrors stdout log.")
            raise SystemExit(2)
        elif token.startswith("log=") or low.startswith("log="):
            eprint("ERROR: LOG=<path> is no longer accepted; log path is a script constant.")
            raise SystemExit(2)
        elif token.startswith("auto_exam=") or token.startswith("require_exam=") or low.startswith("auto_exam=") or low.startswith("require_exam="):
            # Compatibility no-op.
            pass
        elif "=" in token:
            eprint(f"ERROR: unexpected learn arg: {token}")
            raise SystemExit(2)
        elif token.startswith("-"):
            eprint(f"ERROR: unknown learn flag: {token}")
            eprint("Allowed: -minimal|-low|-medium|-high|-xhigh")
            raise SystemExit(2)
        else:
            eprint("ERROR: learn does not accept positional args.")
            raise SystemExit(2)

    if reasoning_profile not in LEARN_REASONING_PROFILE_TO_EFFORT:
        eprint(f"ERROR: invalid reasoning={reasoning_profile} (expected minimal|low|medium|high|xhigh).")
        raise SystemExit(2)
    effective_effort = LEARN_REASONING_PROFILE_TO_EFFORT[reasoning_profile]

    return {
        "explicit_project_id": "",
        "log_file": "",
        "model_sync_mode": "1",
        "plan_mode": "strong",
        "plan_transport": "auto(app-server->exec)",
        "model_name": LEARN_MODEL_NAME,
        "reasoning_profile": reasoning_profile,
        "model_reasoning_effort": effective_effort,
    }


def run_logged_self(project_id: str, cfg: dict[str, Any]) -> int:
    log_file = LEARN_LOG_FILE_TEMPLATE.format(project_id=project_id)
    print(f"LEARN_LOG_FILE: {log_file}")
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    py_bin = sys.executable or shutil.which("python3") or shutil.which("python")
    if not py_bin:
        eprint("ERROR: python runtime is required for learn log mirror self-run.")
        return 1
    cmd = [
        py_bin,
        str(Path(__file__).resolve()),
        f"reasoning={cfg['reasoning_profile']}",
    ]
    env = os.environ.copy()
    env["QF_LEARN_LOG_ACTIVE"] = "1"
    env["PYTHONUNBUFFERED"] = "1"
    with open(log_file, "w", encoding="utf-8") as fh:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            fh.write(line)
        proc.wait()
        return int(proc.returncode or 0)


def build_base_learn(project_id: str, learn_file: Path, learn_md: Path) -> None:
    default_required_files = [
        "docs/PROJECT_GUIDE.md",
        "AGENTS.md",
        "docs/WORKFLOW.md",
        "CODEX_CLI_PLAYBOOK.md",
        "TASKS/STATE.md",
    ]
    required_files = default_required_files
    required_files_for_digest = [x for x in required_files if x != "TASKS/STATE.md"]
    missing_required = [path for path in required_files if not Path(path).is_file()]
    context_files = ordered_unique(list(required_files_for_digest))

    skill_files: list[str] = []
    for root in (Path("/root/.codex/skills/.system"), Path(".codex/skills/.system")):
        if not root.is_dir():
            continue
        for skill in sorted(root.glob("*/SKILL.md")):
            skill_files.append(str(skill))
    skill_files = ordered_unique(skill_files)

    context_entries: list[dict[str, str]] = []
    for rel in context_files:
        status, digest = file_sha(Path(rel))
        context_entries.append({"path": rel, "status": status, "sha256": digest})

    skill_entries: list[dict[str, str]] = []
    for rel in skill_files:
        status, digest = file_sha(Path(rel))
        skill_entries.append({"path": rel, "status": status, "sha256": digest})

    digest_lines: list[str] = []
    for item in context_entries:
        digest_lines.append(f"ctx:{item['path']}:{item['sha256']}")
    for item in skill_entries:
        digest_lines.append(f"skill:{item['path']}:{item['sha256']}")
    digest_lines.sort()
    context_digest = hashlib.sha256("\n".join(digest_lines).encode("utf-8")).hexdigest()

    sync_passed = len(missing_required) == 0
    required_total = len(required_files)
    required_read = required_total - len(missing_required)

    project_summary = ""
    project_goal = ""
    if Path("README.md").is_file():
        for raw in Path("README.md").read_text(encoding="utf-8", errors="replace").splitlines():
            s = raw.strip()
            if s and not s.startswith("#"):
                project_summary = s
                break
    if not project_summary:
        project_summary = "quant-factory-os governance/execution base for quant engineering."

    if Path("docs/PROJECT_GUIDE.md").is_file():
        lines = Path("docs/PROJECT_GUIDE.md").read_text(encoding="utf-8", errors="replace").splitlines()
        for i, raw in enumerate(lines):
            if "一句话北极星" not in raw:
                continue
            for cand in lines[i + 1 :]:
                s = cand.strip()
                if not s or s.startswith("#") or s.startswith(">") or s.startswith("-"):
                    continue
                project_goal = s
                break
            break
    if not project_goal:
        project_goal = "自动化 -> 自我迭代 -> 涌现智能。"

    now = datetime.now(timezone.utc)
    obj: dict[str, Any] = {
        "schema": "qf_learn.v2",
        "project_id": project_id,
        "scope": "project-session",
        "created_at_utc": now.isoformat(),
        "learn_passed": bool(sync_passed),
        "project_understanding": {
            "summary": project_summary,
            "goal": project_goal,
        },
        "constitution_and_workflow": {
            "constitution_source": "AGENTS.md",
            "workflow_source": "docs/WORKFLOW.md",
        },
        "session_status": {
            "continuity": "state_only",
            "current_stage": {"current_project_id": project_id},
        },
        "sync": {
            "report_file": "",
            "mode": "project-direct-read",
            "passed": sync_passed,
            "required_total": required_total,
            "required_read": required_read,
            "missing_required_files": missing_required,
        },
        "skills": {
            "count": len(skill_entries),
            "files": [x["path"] for x in skill_entries],
        },
        "context_digest": context_digest,
        "context_files": [x["path"] for x in context_entries],
        "skill_files": [x["path"] for x in skill_entries],
        "next_command": "python3 tools/ready.py",
    }
    write_json(learn_file, obj)

    lines = [
        "# Learn Report",
        "",
        f"PROJECT_ID: `{project_id}`",
        f"Generated At (UTC): {obj['created_at_utc']}",
        f"Status: `{'pass' if obj['learn_passed'] else 'fail'}`",
        "",
        "## Sync",
        "- report: `(none)`",
        f"- required read: {required_read}/{required_total}",
        f"- pass: `{str(sync_passed).lower()}`",
    ]
    if missing_required:
        lines.append("- missing required:")
        for p in missing_required:
            lines.append(f"  - `{p}`")
    lines.extend(
        [
            "",
            "## Skills",
            f"- files: {len(skill_entries)}",
            "",
            "## Context Digest",
            f"- `{context_digest}`",
            "",
            "## Next Command",
            f"- `{obj['next_command']}`",
            "",
        ]
    )
    learn_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"LEARN_STATUS: {'pass' if obj['learn_passed'] else 'fail'}")
    print(f"LEARN_SYNC_REQUIRED_READ: {required_read}/{required_total}")
    print(f"LEARN_SKILLS_COUNT: {len(skill_entries)}")
    print(f"LEARN_CONTEXT_DIGEST: {context_digest}")


def print_base_anchors(learn_file: Path) -> None:
    obj = read_json(learn_file)
    mainline = " ".join(str((obj.get("project_understanding") or {}).get("goal", "")).split())
    stage_text = " ".join(f"project={obj.get('project_id', '')}".split())
    next_step = " ".join(str(obj.get("next_command", "")).split())
    required_files = obj.get("context_files") or []
    required_files_text = ",".join(" ".join(str(x).split()) for x in required_files if str(x).strip())
    print(f"LEARN_MAINLINE: {mainline}")
    print(f"LEARN_CURRENT_STAGE: {stage_text}")
    print(f"LEARN_NEXT_STEP: {next_step}")
    print(f"LEARN_REQUIRED_FILES_READ_LIST: {required_files_text}")


def generate_prompt(learn_file: Path, prompt_file: Path, project_id: str, plan_mode: str) -> None:
    obj = read_json(learn_file)
    required_files = [str(x).strip() for x in (obj.get("context_files") or []) if str(x).strip()]
    schema_lines = [
        "{",
        '  "mainline": "<string>",',
        '  "current_stage": "<string>",',
        '  "next_step": "<string>",',
        '  "files_read": ["<path1>", "<path2>"],',
    ]
    if plan_mode == "strong":
        schema_lines.extend(
            [
                '  "plan_protocol": {',
                '    "goal": "<string>",',
                '    "non_goal": "<string>",',
                '    "evidence": ["<path or claim>"],',
                '    "alternatives": ["<alt1>", "<alt2>"],',
                '    "rebuttal": "<string>",',
                '    "decision_stop_condition": "<string>"',
                "  },",
                '  "oral_restate": {',
                '    "project_understanding": "<string>",',
                '    "constitution_workflow": "<string>",',
                '    "evidence_chain": "<string>",',
                '    "session_continuity": "<string>",',
                '    "current_focus": "<string>",',
                '    "next_action": "<string>"',
                "  },",
                '  "oral_exam": [',
                '    {"question_id":"Q1","question":"<q1>","answer":"<a1>","score":"pass|fail"},',
                '    {"question_id":"Q2","question":"<q2>","answer":"<a2>","score":"pass|fail"},',
                '    {"question_id":"Q3","question":"<q3>","answer":"<a3>","score":"pass|fail"}',
                "  ],",
                '  "anchor_realign": {',
                '    "question_id": "<Q1..Q17 from PROJECT_GUIDE>",',
                '    "status": "on_track|drifted",',
                '    "drift_detail": "<what detail drift happened or none>",',
                '    "return_to_mainline": "<how to return to mainline now>"',
                "  }",
            ]
        )
    schema_lines.append("}")

    lines = [
        "You are performing strict onboarding sync for quant-factory-os.",
        "Use `/plan` strongest planning mindset in this response (plan-first, evidence-first, no execution).",
        "Read the listed files with tools/view.sh and reply with JSON only.",
        "You may run via codex app-server or codex exec transport; still enforce `/plan`-style strong mode output discipline.",
        "",
        f"PROJECT_ID: {project_id}",
        "Required files to read:",
    ]
    for path in required_files:
        lines.append(f"- {path}")
    lines.extend(
        [
            "",
            "Output requirements:",
            "- Do not run write commands.",
            "- Read required files strictly in the listed order (top to bottom).",
            "- Execute only minimal read/shell commands needed to gather evidence from the required files.",
            "- Learning sync sequence must be: project -> constitution/workflow -> evidence chain -> session continuity -> current focus -> next action.",
            "- Do not call python3 tools/init.py/learn/ready inside this model-sync pass.",
            "- Do not include markdown fences.",
            "- JSON must follow this schema exactly:",
        ]
    )
    lines.extend(schema_lines)
    lines.append("")
    if plan_mode == "strong":
        lines.extend(
            [
                "Strong mode gates:",
                "- Treat this pass as `/plan`-equivalent strongest mode; no shortcut answers.",
                "- plan_protocol fields are mandatory.",
                "- plan_protocol.evidence must cover every required file at least once.",
                "- oral_restate fields are mandatory.",
                "- oral_exam must contain at least 3 QA items, each bound to PROJECT_GUIDE question ids (Q1..Q17).",
                "- oral_exam must have at least 2 pass items.",
                "- anchor_realign must map to one PROJECT_GUIDE question id (Q1..Q17).",
                "- practice must include tools/view.sh reads for every required file.",
                "",
            ]
        )
    lines.append("files_read must be a subset of the required files list above.")
    lines.append('For evidence format, use: "<path>#<section>: <concrete fact>".')
    prompt_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_model_output(model_raw_file: Path, model_json_file: Path, plan_mode: str, learn_file: Path, model_events_file: Path) -> dict[str, Any]:
    raw_text = model_raw_file.read_text(encoding="utf-8", errors="replace") if model_raw_file.is_file() else ""
    if not raw_text.strip():
        raise ValueError("model raw empty")
    obj: dict[str, Any] | None = None
    try:
        maybe = json.loads(raw_text)
        if isinstance(maybe, dict):
            obj = maybe
    except Exception:
        decoder = json.JSONDecoder()
        for idx, ch in enumerate(raw_text):
            if ch != "{":
                continue
            try:
                maybe, _end = decoder.raw_decode(raw_text[idx:])
            except Exception:
                continue
            if isinstance(maybe, dict):
                obj = maybe
                break
    if obj is None:
        raise ValueError("model raw is not dict json")

    for key in ["mainline", "current_stage", "next_step", "files_read"]:
        if key not in obj:
            raise ValueError(f"missing key {key}")
    if not isinstance(obj.get("files_read"), list):
        raise ValueError("files_read not list")
    files_read = [str(x).strip() for x in (obj.get("files_read") or []) if str(x).strip()]
    if not files_read:
        raise ValueError("files_read empty")

    learn_obj = read_json(learn_file)
    required_files = [str(x).strip() for x in (learn_obj.get("context_files") or []) if str(x).strip()]
    if not required_files:
        raise ValueError("context_files empty")
    missing_required = [p for p in required_files if p not in set(files_read)]
    if missing_required:
        raise ValueError("files_read missing required files")

    if plan_mode == "strong":
        plan = obj.get("plan_protocol")
        oral = obj.get("oral_restate")
        exam = obj.get("oral_exam")
        anchor = obj.get("anchor_realign")
        if not isinstance(plan, dict):
            raise ValueError("plan_protocol missing")
        for key in ["goal", "non_goal", "evidence", "alternatives", "rebuttal", "decision_stop_condition"]:
            if key not in plan:
                raise ValueError(f"plan_protocol missing {key}")
        evidence = plan.get("evidence") or []
        if not isinstance(evidence, list) or not evidence:
            raise ValueError("plan_protocol.evidence invalid")
        covered_evidence: set[str] = set()
        for ev in evidence:
            ev_text = str(ev).strip()
            if not ev_text:
                continue
            for req in required_files:
                req_abs = str(Path(req).resolve())
                if req in ev_text or f"./{req}" in ev_text or req_abs in ev_text:
                    covered_evidence.add(req)
        missing_evidence = [p for p in required_files if p not in covered_evidence]
        if missing_evidence:
            raise ValueError(f"plan_protocol.evidence missing required files: {missing_evidence}")
        if not isinstance(oral, dict):
            raise ValueError("oral_restate missing")
        for key in ["project_understanding", "constitution_workflow", "evidence_chain", "session_continuity", "current_focus", "next_action"]:
            if key not in oral:
                raise ValueError(f"oral_restate missing {key}")
        if not isinstance(exam, list) or len(exam) < 3:
            raise ValueError("oral_exam invalid")
        for item in exam:
            if not isinstance(item, dict):
                raise ValueError("oral_exam item invalid")
            for key in ["question_id", "question", "answer", "score"]:
                if key not in item:
                    raise ValueError(f"oral_exam missing {key}")
            qid_exam = str(item.get("question_id", "")).strip().upper()
            if not re.fullmatch(r"Q([1-9]|1[0-7])", qid_exam):
                raise ValueError("oral_exam question_id invalid")
            score_exam = str(item.get("score", "")).strip().lower()
            if score_exam not in {"pass", "fail"}:
                raise ValueError("oral_exam score invalid")
        pass_count = sum(1 for item in exam if str(item.get("score", "")).strip().lower() == "pass")
        if pass_count < 2:
            raise ValueError("oral_exam insufficient passes")
        if not isinstance(anchor, dict):
            raise ValueError("anchor_realign missing")
        for key in ["question_id", "status", "drift_detail", "return_to_mainline"]:
            if key not in anchor:
                raise ValueError(f"anchor missing {key}")
        status = str(anchor.get("status", "")).strip()
        if status not in {"on_track", "drifted"}:
            raise ValueError("anchor status invalid")
        qid = str(anchor.get("question_id", "")).strip().upper()
        if not re.fullmatch(r"Q([1-9]|1[0-7])", qid):
            raise ValueError("anchor question_id invalid")

    practice_commands = extract_command_evidence(model_events_file)
    if not practice_commands:
        raise ValueError("no practice command evidence")

    viewed_required: set[str] = set()
    for cmd in practice_commands:
        if "tools/view.sh" not in cmd:
            continue
        cmd_text = str(cmd)
        for req in required_files:
            req_abs = str(Path(req).resolve())
            if req in cmd_text or f"./{req}" in cmd_text or req_abs in cmd_text:
                viewed_required.add(req)
    missing_views = [p for p in required_files if p not in viewed_required]
    if missing_views:
        raise ValueError(f"required files not actually viewed via tools/view.sh: {missing_views}")

    practice_samples: list[str] = []
    seen: set[str] = set()
    for cmd in practice_commands:
        if cmd in seen:
            continue
        seen.add(cmd)
        practice_samples.append(cmd)
        if len(practice_samples) >= 3:
            break
    obj["practice"] = {
        "command_execution_count": len(practice_commands),
        "command_samples": practice_samples,
    }
    write_json(model_json_file, obj)
    return obj


def print_model_anchors(obj: dict[str, Any], plan_mode: str) -> None:
    print("LEARN_MODEL_SYNC_STATUS: pass")
    print(f"LEARN_MODEL_MAINLINE: {' '.join(str(obj.get('mainline', '')).split())}")
    print(f"LEARN_MODEL_CURRENT_STAGE: {' '.join(str(obj.get('current_stage', '')).split())}")
    print(f"LEARN_MODEL_NEXT_STEP: {' '.join(str(obj.get('next_step', '')).split())}")
    files_read = [str(x).strip() for x in (obj.get("files_read") or []) if str(x).strip()]
    print(f"LEARN_MODEL_FILES_READ_LIST: {','.join(files_read)}")
    if plan_mode != "strong":
        return
    plan = obj.get("plan_protocol") or {}
    oral = obj.get("oral_restate") or {}
    exam = obj.get("oral_exam") or []
    anchor = obj.get("anchor_realign") or {}
    practice = obj.get("practice") or {}
    print(f"LEARN_MODEL_PLAN_GOAL: {' '.join(str(plan.get('goal', '')).split())}")
    print(f"LEARN_MODEL_PLAN_NON_GOAL: {' '.join(str(plan.get('non_goal', '')).split())}")
    print(f"LEARN_MODEL_PLAN_REBUTTAL: {' '.join(str(plan.get('rebuttal', '')).split())}")
    print(f"LEARN_MODEL_PLAN_DECISION_STOP: {' '.join(str(plan.get('decision_stop_condition', '')).split())}")
    print(f"LEARN_MODEL_ORAL_PROJECT: {' '.join(str(oral.get('project_understanding', '')).split())}")
    print(f"LEARN_MODEL_ORAL_CONSTITUTION: {' '.join(str(oral.get('constitution_workflow', '')).split())}")
    print(f"LEARN_MODEL_ORAL_EVIDENCE: {' '.join(str(oral.get('evidence_chain', '')).split())}")
    print(f"LEARN_MODEL_ORAL_SESSION: {' '.join(str(oral.get('session_continuity', '')).split())}")
    print(f"LEARN_MODEL_ORAL_CURRENT_FOCUS: {' '.join(str(oral.get('current_focus', '')).split())}")
    print(f"LEARN_MODEL_ORAL_NEXT_ACTION: {' '.join(str(oral.get('next_action', '')).split())}")
    print(f"LEARN_MODEL_ANCHOR_QUESTION_ID: {' '.join(str(anchor.get('question_id', '')).split())}")
    print(f"LEARN_MODEL_ANCHOR_STATUS: {' '.join(str(anchor.get('status', '')).split())}")
    print(f"LEARN_MODEL_ANCHOR_DRIFT_DETAIL: {' '.join(str(anchor.get('drift_detail', '')).split())}")
    print(f"LEARN_MODEL_ANCHOR_RETURN_ACTION: {' '.join(str(anchor.get('return_to_mainline', '')).split())}")
    print(f"LEARN_MODEL_PRACTICE_COMMAND_COUNT: {int(practice.get('command_execution_count', 0))}")
    samples = practice.get("command_samples") or []
    for idx, sample in enumerate(samples, start=1):
        print(f"LEARN_MODEL_PRACTICE_SAMPLE_{idx}: {' '.join(str(sample).split())}")
    print(f"LEARN_MODEL_ORAL_EXAM_QA_COUNT: {len(exam)}")
    for idx, item in enumerate(exam, start=1):
        if not isinstance(item, dict):
            continue
        qid = " ".join(str(item.get("question_id", "")).split())
        q = " ".join(str(item.get("question", "")).split())
        a = " ".join(str(item.get("answer", "")).split())
        s = " ".join(str(item.get("score", "")).split())
        print(f"LEARN_MODEL_ORAL_EXAM_QID{idx}: {qid}")
        print(f"LEARN_MODEL_ORAL_EXAM_Q{idx}: {q}")
        print(f"LEARN_MODEL_ORAL_EXAM_A{idx}: {a}")
        print(f"LEARN_MODEL_ORAL_EXAM_SCORE{idx}: {s}")

    print("LEARN_READOUT_BEGIN")
    print(f"LEARN_READOUT_MAINLINE: {' '.join(str(obj.get('mainline', '')).split())}")
    print(f"LEARN_READOUT_CURRENT_STAGE: {' '.join(str(obj.get('current_stage', '')).split())}")
    print(f"LEARN_READOUT_NEXT_STEP: {' '.join(str(obj.get('next_step', '')).split())}")
    print(f"LEARN_READOUT_ORAL_PROJECT: {' '.join(str(oral.get('project_understanding', '')).split())}")
    print(f"LEARN_READOUT_ORAL_CURRENT_FOCUS: {' '.join(str(oral.get('current_focus', '')).split())}")
    print(f"LEARN_READOUT_ANCHOR: {' '.join(str(anchor.get('question_id', '')).split())} | {' '.join(str(anchor.get('status', '')).split())}")
    print(f"LEARN_READOUT_ANCHOR_ACTION: {' '.join(str(anchor.get('return_to_mainline', '')).split())}")
    print(f"LEARN_READOUT_PRACTICE_COUNT: {int(practice.get('command_execution_count', 0))}")
    if samples:
        print(f"LEARN_READOUT_PRACTICE_FIRST: {' '.join(str(samples[0]).split())}")
    print("LEARN_READOUT_END")


def update_learn_with_model(
    learn_file: Path,
    learn_md: Path,
    model_sync_mode: str,
    plan_mode: str,
    plan_transport_effective: str,
    model_sync_status: str,
    model_sync_reason: str,
    model_sync_pass: bool,
    model_prompt_file: Path,
    model_raw_file: Path,
    model_json_file: Path,
    model_events_file: Path,
    model_stderr_file: Path,
) -> None:
    obj = read_json(learn_file)
    model_obj: dict[str, Any] = {
        "mode": model_sync_mode,
        "plan_mode": plan_mode,
        "plan_transport": plan_transport_effective,
        "status": model_sync_status,
        "passed": model_sync_pass,
        "reason": model_sync_reason,
        "prompt_file": str(model_prompt_file),
        "raw_file": str(model_raw_file),
        "json_file": str(model_json_file),
        "events_file": str(model_events_file),
        "stderr_file": str(model_stderr_file),
        "result": {},
    }
    if model_sync_pass and model_json_file.is_file():
        try:
            model_obj["result"] = read_json(model_json_file)
        except Exception:
            model_obj["result"] = {}
    obj["model_sync"] = model_obj
    if model_sync_mode == "1" and not model_sync_pass:
        obj["learn_passed"] = False
    write_json(learn_file, obj)

    lines = learn_md.read_text(encoding="utf-8").splitlines() if learn_md.is_file() else []
    lines.extend(
        [
            "",
            "## Model Sync",
            f"- mode: `{model_sync_mode}`",
            f"- plan_mode: `{plan_mode}`",
            f"- status: `{model_sync_status}`",
            f"- reason: `{model_sync_reason}`",
            f"- prompt: `{model_prompt_file}`",
            f"- raw: `{model_raw_file}`",
            f"- parsed: `{model_json_file}`",
            f"- events: `{model_events_file}`",
            f"- stderr: `{model_stderr_file}`",
        ]
    )
    learn_md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def learn_file_is_valid(learn_file: Path) -> bool:
    try:
        obj = read_json(learn_file)
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
    for key in ["mainline", "current_stage", "next_step", "files_read", "plan_protocol", "oral_restate", "oral_exam", "anchor_realign", "practice"]:
        if key not in model_result:
            return False
    if not isinstance(model_result.get("files_read"), list) or not model_result.get("files_read"):
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
        digest_lines.append(f"ctx:{rel}:{file_sha(Path(str(rel)))[1]}")
    for rel in skill_files:
        digest_lines.append(f"skill:{rel}:{file_sha(Path(str(rel)))[1]}")
    digest_lines.sort()
    current = hashlib.sha256("\n".join(digest_lines).encode("utf-8")).hexdigest()
    return current == str(obj.get("context_digest", "")).strip()


def main(argv: list[str]) -> int:
    cfg = parse_cli(argv)
    project_id = resolve_project_id_for_cmd(cfg["explicit_project_id"], "learn")

    if os.environ.get("QF_LEARN_LOG_ACTIVE", "0") != "1":
        return run_logged_self(project_id, cfg)

    emit_step(1, 4, "resolve project context")
    print("LEARN_SCOPE_MODE: project-scoped")
    print(f"LEARN_PROJECT_ID: {project_id}")
    print("LEARN_SYNC_MODE: project-direct-read")

    emit_step(2, 4, "prepare learn artifact paths")
    learn_dir = Path("learn")
    learn_dir.mkdir(parents=True, exist_ok=True)
    learn_file = learn_dir / f"{project_id}.json"
    learn_md = learn_dir / f"{project_id}.md"
    model_prompt_file = learn_dir / f"{project_id}.model.prompt.txt"
    model_raw_file = learn_dir / f"{project_id}.model.raw.txt"
    model_json_file = learn_dir / f"{project_id}.model.json"
    model_events_file = learn_dir / f"{project_id}.model.events.jsonl"
    model_stderr_file = learn_dir / f"{project_id}.model.stderr.log"
    model_app_events_file = learn_dir / f"{project_id}.model.app.events.jsonl"
    model_app_stderr_file = learn_dir / f"{project_id}.model.app.stderr.log"
    for p in (
        model_prompt_file,
        model_raw_file,
        model_json_file,
        model_events_file,
        model_stderr_file,
        model_app_events_file,
        model_app_stderr_file,
    ):
        try:
            if p.exists():
                p.unlink()
        except Exception as exc:
            eprint(str(exc))
            return 1

    emit_step(3, 4, "generate learn report (project + constitution + workflow + skills)")
    build_base_learn(project_id, learn_file, learn_md)
    print_base_anchors(learn_file)

    if shutil.which("codex") is None:
        eprint("ERROR: learn requires codex CLI (model sync is mandatory).")
        return 1

    print(f"LEARN_MODEL_SYNC_MODE: {cfg['model_sync_mode']}")
    print(f"LEARN_MODEL_PLAN_MODE: {cfg['plan_mode']}")
    print("LEARN_MODEL_PLAN_TRANSPORT: auto(app-server->exec)")
    print(f"LEARN_MODEL_PLAN_TRANSPORT_PRIMARY: {MODEL_TRANSPORT_PRIMARY}")
    print(f"LEARN_MODEL_PLAN_TRANSPORT_FALLBACK: {MODEL_TRANSPORT_FALLBACK}")
    print(f"LEARN_MODEL: {cfg['model_name']}")
    print(f"LEARN_MODEL_REASONING_PROFILE: {cfg['reasoning_profile']}")
    requested_effort = cfg["model_reasoning_effort"]
    effective_effort, effort_reason = runtime_reasoning_effort(requested_effort)
    print(f"LEARN_MODEL_REASONING_EFFORT: {effective_effort}")
    print(f"LEARN_MODEL_REASONING_EFFORT_REQUESTED: {requested_effort}")
    print(f"LEARN_MODEL_REASONING_EFFORT_EFFECTIVE: {effective_effort}")
    print(f"LEARN_MODEL_REASONING_EFFORT_REASON: {effort_reason}")

    generate_prompt(learn_file, model_prompt_file, project_id, cfg["plan_mode"])
    transport_req = TransportRequest(
        model_name=cfg["model_name"],
        model_reasoning_effort=effective_effort,
        cwd=Path.cwd(),
    )
    transport_artifacts = TransportArtifacts(
        prompt_file=model_prompt_file,
        raw_file=model_raw_file,
        events_file=model_events_file,
        stderr_file=model_stderr_file,
        app_events_file=model_app_events_file,
        app_stderr_file=model_app_stderr_file,
    )
    transport_result = run_plan_sync(transport_req, transport_artifacts)
    print(f"LEARN_MODEL_SYNC_RC_{MODEL_TRANSPORT_PRIMARY}: {transport_result.primary_rc}")
    if transport_result.fallback_rc is not None:
        print(f"LEARN_MODEL_SYNC_RC_{MODEL_TRANSPORT_FALLBACK}: {transport_result.fallback_rc}")
    plan_transport_effective = transport_result.effective_transport
    model_rc = transport_result.final_rc
    print(f"LEARN_MODEL_PLAN_TRANSPORT_EFFECTIVE: {plan_transport_effective}")
    print(f"LEARN_MODEL_SYNC_RC: {model_rc}")

    model_sync_pass = False
    model_sync_status = "fail"
    model_sync_reason = "unknown"
    try:
        parsed = parse_model_output(model_raw_file, model_json_file, cfg["plan_mode"], learn_file, model_events_file)
        print_model_anchors(parsed, cfg["plan_mode"])
        model_sync_pass = True
        model_sync_status = "pass"
        model_sync_reason = "ok"
    except Exception:
        model_sync_pass = False
        model_sync_status = "fail"
        if model_rc != 0:
            model_sync_reason = f"codex-exit-{model_rc}"
        else:
            model_sync_reason = "schema-parse-failed"
        print("LEARN_MODEL_SYNC_STATUS: fail")
        print(f"LEARN_MODEL_SYNC_REASON: {model_sync_reason}")

    update_learn_with_model(
        learn_file,
        learn_md,
        cfg["model_sync_mode"],
        cfg["plan_mode"],
        plan_transport_effective,
        model_sync_status,
        model_sync_reason,
        model_sync_pass,
        model_prompt_file,
        model_raw_file,
        model_json_file,
        model_events_file,
        model_stderr_file,
    )

    if not model_sync_pass:
        eprint("ERROR: learn model sync strict mode failed.")
        eprint(f"Check: {model_stderr_file}")
        return 1
    if not learn_file_is_valid(learn_file):
        eprint("ERROR: learn output validation failed.")
        eprint(f"Check: {learn_file}")
        return 1

    emit_step(4, 4, "print learn artifacts")
    print(f"LEARN_FILE: {learn_file}")
    print(f"LEARN_MD: {learn_md}")
    print(f"LEARN_MODEL_PROMPT_FILE: {model_prompt_file}")
    print(f"LEARN_MODEL_RAW_FILE: {model_raw_file}")
    print(f"LEARN_MODEL_JSON_FILE: {model_json_file}")
    print(f"LEARN_MODEL_EVENTS_FILE: {model_events_file}")
    print(f"LEARN_MODEL_STDERR_FILE: {model_stderr_file}")
    if model_app_events_file.is_file():
        print(f"LEARN_MODEL_APP_EVENTS_FILE: {model_app_events_file}")
    if model_app_stderr_file.is_file():
        print(f"LEARN_MODEL_APP_STDERR_FILE: {model_app_stderr_file}")
    print("LEARN_NEXT_COMMAND: python3 tools/ready.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
