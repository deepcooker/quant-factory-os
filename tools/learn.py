#!/usr/bin/env python3
from __future__ import annotations

import json
import hashlib
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from tools.common_helpers import (
        file_sha,
        normalize_block,
        normalize_list,
        ordered_unique,
        read_json,
        read_text,
        write_json,
    )
except Exception:  # pragma: no cover
    from common_helpers import (  # type: ignore
        file_sha,
        normalize_block,
        normalize_list,
        ordered_unique,
        read_json,
        read_text,
        write_json,
    )

try:
    from tools.codex_transport import (
        MODEL_TRANSPORT_PRIMARY,
        TransportArtifacts,
        TransportRequest,
        extract_final_answer_json_from_events,
        extract_command_evidence,
        run_plan_sync,
        runtime_reasoning_effort,
    )
except Exception:  # pragma: no cover
    from codex_transport import (  # type: ignore
        MODEL_TRANSPORT_PRIMARY,
        TransportArtifacts,
        TransportRequest,
        extract_final_answer_json_from_events,
        extract_command_evidence,
        run_plan_sync,
        runtime_reasoning_effort,
    )

STATE_FILE = Path(os.environ.get("QF_STATE_FILE", "TASKS/STATE.md"))
DEFAULT_PROJECT_ID = os.environ.get("QF_DEFAULT_PROJECT_ID", "project-0")
LEARN_LOG_FILE_TEMPLATE = "learn/{project_id}.stdout.log"
LEARN_MODEL_NAME = "gpt-5.4"
LEARN_REASONING_DEFAULT_PROFILE = "xhigh"
LEARN_REASONING_PROFILE_TO_EFFORT = {
    "minimal": "minimal",
    "low": "low",
    "medium": "medium",
    "high": "high",
    "xhigh": "xhigh",
}
LEARN_REASONING_PROFILE_ALIASES = {
    "daily": "medium",
}
OWNER_FILES = [
    "docs/PROJECT_GUIDE.md",
    "AGENTS.md",
    "docs/WORKFLOW.md",
]
GUIDE_REQUIRED_SECTION_NAMES = [
    "为什么问这题",
    "标准答案",
    "必查文件",
    "查找线索",
    "主线意义",
]
GUIDE_QUESTION_RE = re.compile(r"^###\s+Q(?P<num>\d+)\.\s*(?P<title>.+?)\s*$", re.M)
GUIDE_SECTION_RE = re.compile(r"^####\s+(?P<title>.+?)\s*$", re.M)


@dataclass
class GuideQuestion:
    question_id: str
    title: str
    why: str
    standard_answer: str
    must_read_files: list[str]
    hint_lines: list[str]
    mainline_lines: list[str]


@dataclass
class LearnContext:
    cfg: dict[str, Any]
    project_id: str
    state: dict[str, str]
    learn_dir: Path | None = None
    learn_file: Path | None = None
    learn_md: Path | None = None
    model_prompt_file: Path | None = None
    model_raw_file: Path | None = None
    model_json_file: Path | None = None
    model_events_file: Path | None = None
    model_stderr_file: Path | None = None



# learn_tools_01 中文：向标准错误输出 learn 阶段的错误提示。
def eprint(msg: str) -> None:
    print(msg, file=sys.stderr)



# learn_tools_02 中文：规范化 project_id，缺省时回退默认项目。
def normalize_project_id(value: str | None) -> str:
    v = (value or "").strip()
    return v if v else DEFAULT_PROJECT_ID



# learn_tools_03 中文：从 TASKS/STATE.md 读取指定字段值。
def state_field_value(key: str) -> str:
    if not STATE_FILE.is_file():
        return ""
    pat = re.compile(rf"^\s*{re.escape(key)}:\s*(.*?)\s*$")
    try:
        for line in STATE_FILE.read_text(encoding="utf-8", errors="replace").splitlines():
            match = pat.match(line)
            if match:
                return match.group(1)
    except Exception:
        return ""
    return ""



# learn_tools_04 中文：读取当前 project/run/task 的状态快照。
def read_state_snapshot() -> dict[str, str]:
    return {
        "current_project_id": normalize_project_id(state_field_value("CURRENT_PROJECT_ID")),
        "current_run_id": state_field_value("CURRENT_RUN_ID").strip(),
        "current_task_file": state_field_value("CURRENT_TASK_FILE").strip(),
        "current_status": state_field_value("CURRENT_STATUS").strip(),
    }



# learn_tools_05 中文：解析 learn 使用的 project_id，并校验是否与状态一致。
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



# learn_tools_06 中文：判断 learn 是否需要输出 JSON 事件流。
def should_emit_json_stream() -> bool:
    value = os.environ.get("QF_EVENT_STREAM", "0").strip().lower()
    return value in {"1", "json", "jsonl"}



# learn_tools_07 中文：输出 learn 阶段的步骤锚点。
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



# learn_tools_08 中文：解析 PROJECT_GUIDE 的北极星主线。
def parse_north_star(lines: list[str]) -> str:
    for idx, raw in enumerate(lines):
        if raw.strip() != "## 一句话北极星":
            continue
        for cand in lines[idx + 1 :]:
            s = cand.strip()
            if not s:
                continue
            if s.startswith("#"):
                break
            return s.removeprefix("- ").strip()
    return "自动化 -> 自我迭代 -> 涌现智能。"



# learn_tools_09 中文：解析带有 project/run 占位符的动态路径。
def resolve_dynamic_path(raw_path: str, project_id: str, current_run_id: str) -> str:
    path = str(raw_path or "").strip()
    if not path:
        return ""
    if ("<RUN_ID>" in path or "<CURRENT_RUN_ID>" in path) and not current_run_id:
        return ""
    path = path.replace("<PROJECT_ID>", project_id)
    path = path.replace("<CURRENT_PROJECT_ID>", project_id)
    path = path.replace("<RUN_ID>", current_run_id)
    path = path.replace("<CURRENT_RUN_ID>", current_run_id)
    return path



# learn_tools_10 中文：解析 PROJECT_GUIDE 题库、答案与必查文件结构。
def parse_project_guide(path: Path, project_id: str, current_run_id: str) -> tuple[str, list[GuideQuestion]]:
    text = read_text(path)
    if not text.strip():
        raise ValueError(f"project guide missing or empty: {path}")
    lines = text.splitlines()
    north_star = parse_north_star(lines)

    matches = list(GUIDE_QUESTION_RE.finditer(text))
    if not matches:
        raise ValueError("PROJECT_GUIDE has no Q sections")

    questions: list[GuideQuestion] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        block = text[start:end].splitlines()
        heading = block[0].strip()
        head_match = GUIDE_QUESTION_RE.match(heading)
        if not head_match:
            raise ValueError(f"invalid question heading: {heading}")
        qid = f"Q{head_match.group('num')}"
        title = head_match.group("title").strip()

        sections: dict[str, list[str]] = {}
        current_section = ""
        for raw in block[1:]:
            sec_match = GUIDE_SECTION_RE.match(raw.strip())
            if sec_match:
                current_section = sec_match.group("title").strip()
                sections[current_section] = []
                continue
            if current_section:
                sections[current_section].append(raw)

        for section_name in GUIDE_REQUIRED_SECTION_NAMES:
            if section_name not in sections:
                raise ValueError(f"{qid} missing section: {section_name}")

        why = normalize_block(sections["为什么问这题"])
        standard_answer = normalize_block(sections["标准答案"])
        if not why or not standard_answer:
            raise ValueError(f"{qid} missing why/standard answer content")

        must_read_files = ordered_unique(
            [
                resolved
                for resolved in (
                    resolve_dynamic_path(item, project_id, current_run_id)
                    for item in normalize_list(sections["必查文件"])
                )
                if resolved
            ]
        )
        if not must_read_files:
            raise ValueError(f"{qid} has no resolved 必查文件")

        hint_lines = normalize_list(sections["查找线索"])
        mainline_lines = normalize_list(sections["主线意义"])
        if not hint_lines or not mainline_lines:
            raise ValueError(f"{qid} missing 查找线索/主线意义 content")

        questions.append(
            GuideQuestion(
                question_id=qid,
                title=title,
                why=why,
                standard_answer=standard_answer,
                must_read_files=must_read_files,
                hint_lines=hint_lines,
                mainline_lines=mainline_lines,
            )
        )

    return north_star, questions



# learn_tools_11 中文：解析 learn 的命令行参数与运行配置。
def parse_cli(argv: list[str]) -> dict[str, Any]:
    reasoning_profile = LEARN_REASONING_DEFAULT_PROFILE
    model_name = LEARN_MODEL_NAME
    reasoning_alias = ""

    i = 0
    while i < len(argv):
        token = argv[i]
        if not token:
            i += 1
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
            eprint("ERROR: plan_transport has been removed; learn transport is fixed to app-server plan mode.")
            raise SystemExit(2)
        elif token.startswith("model_timeout_sec=") or low.startswith("model_timeout_sec="):
            eprint("ERROR: MODEL_TIMEOUT_SEC has been removed from learn.")
            raise SystemExit(2)
        elif token.startswith("model=") or low.startswith("model="):
            model_name = token.split("=", 1)[1].strip()
        elif token == "-model":
            if i + 1 >= len(argv):
                eprint("ERROR: -model requires a value.")
                raise SystemExit(2)
            model_name = argv[i + 1].strip()
            i += 1
        elif token.startswith("-model="):
            model_name = token.split("=", 1)[1].strip()
        elif token.startswith("model_reasoning_effort=") or low.startswith("model_reasoning_effort="):
            eprint("ERROR: use reasoning=<minimal|low|medium|high|xhigh|daily> or -minimal|-low|-medium|-high|-xhigh|-daily.")
            raise SystemExit(2)
        elif token.startswith("reasoning="):
            requested_reasoning = token.split("=", 1)[1].strip().lower()
            reasoning_profile = LEARN_REASONING_PROFILE_ALIASES.get(requested_reasoning, requested_reasoning)
            reasoning_alias = requested_reasoning if requested_reasoning in LEARN_REASONING_PROFILE_ALIASES else ""
        elif low.startswith("reasoning="):
            eprint("ERROR: parameter key must be lowercase: reasoning=...")
            raise SystemExit(2)
        elif token in {"-minimal", "-low", "-medium", "-high", "-xhigh", "-daily"}:
            requested_reasoning = token.lstrip("-")
            reasoning_profile = LEARN_REASONING_PROFILE_ALIASES.get(requested_reasoning, requested_reasoning)
            reasoning_alias = requested_reasoning if requested_reasoning in LEARN_REASONING_PROFILE_ALIASES else ""
        elif low in {"-minimal", "-low", "-medium", "-high", "-xhigh", "-daily"}:
            eprint("ERROR: reasoning flag must be lowercase: -minimal|-low|-medium|-high|-xhigh|-daily.")
            raise SystemExit(2)
        elif token == "-fast" or low == "-fast":
            eprint("ERROR: -fast has been removed. Use -minimal|-low|-medium|-high|-xhigh|-daily.")
            raise SystemExit(2)
        elif token in {"-log", "--log"} or low in {"-log", "--log"}:
            eprint("ERROR: -log/--log is no longer needed; learn always mirrors stdout log.")
            raise SystemExit(2)
        elif token.startswith("log=") or low.startswith("log="):
            eprint("ERROR: LOG=<path> is no longer accepted; log path is a script constant.")
            raise SystemExit(2)
        elif token.startswith("auto_exam=") or token.startswith("require_exam=") or low.startswith("auto_exam=") or low.startswith("require_exam="):
            pass
        elif "=" in token:
            eprint(f"ERROR: unexpected learn arg: {token}")
            raise SystemExit(2)
        elif token.startswith("-"):
            eprint(f"ERROR: unknown learn flag: {token}")
            eprint("Allowed: -minimal|-low|-medium|-high|-xhigh|-daily")
            raise SystemExit(2)
        else:
            eprint("ERROR: learn does not accept positional args.")
            raise SystemExit(2)
        i += 1

    if reasoning_profile not in LEARN_REASONING_PROFILE_TO_EFFORT:
        eprint(f"ERROR: invalid reasoning={reasoning_profile} (expected minimal|low|medium|high|xhigh|daily).")
        raise SystemExit(2)
    if not model_name:
        eprint("ERROR: model cannot be empty.")
        raise SystemExit(2)
    effective_effort = LEARN_REASONING_PROFILE_TO_EFFORT[reasoning_profile]

    return {
        "explicit_project_id": "",
        "log_file": "",
        "model_sync_mode": "1",
        "plan_mode": "strong",
        "plan_transport": MODEL_TRANSPORT_PRIMARY,
        "model_name": model_name,
        "reasoning_profile": reasoning_profile,
        "reasoning_alias": reasoning_alias,
        "model_reasoning_effort": effective_effort,
    }



# learn_tools_12 中文：以日志镜像模式重启 learn 自身。
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
        f"model={cfg['model_name']}",
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



# learn_tools_13 中文：生成基础 learn 产物骨架与证据上下文。
def build_base_learn(project_id: str, learn_file: Path, learn_md: Path, state: dict[str, str]) -> None:
    north_star, questions = parse_project_guide(Path("docs/PROJECT_GUIDE.md"), project_id, state["current_run_id"])
    required_files = ordered_unique(OWNER_FILES + [path for q in questions for path in q.must_read_files])
    missing_required = [path for path in required_files if not Path(path).is_file()]
    context_entries: list[dict[str, str]] = []
    for rel in required_files:
        digest = file_sha(Path(rel))
        status = "ok" if digest not in {"missing", "error"} else digest
        context_entries.append({"path": rel, "status": status, "sha256": digest})
    digest_lines = [f"ctx:{item['path']}:{item['sha256']}" for item in context_entries]
    digest_lines.sort()
    context_digest = hashlib.sha256("\n".join(digest_lines).encode("utf-8")).hexdigest()

    readme_summary = "quant-factory-os governance/execution base for quant engineering."
    if Path("README.md").is_file():
        for raw in Path("README.md").read_text(encoding="utf-8", errors="replace").splitlines():
            s = raw.strip()
            if s and not s.startswith("#"):
                readme_summary = s
                break

    now = datetime.now(timezone.utc)
    learn_passed = len(missing_required) == 0
    obj: dict[str, Any] = {
        "schema": "qf_learn.v3",
        "project_id": project_id,
        "scope": "project-session",
        "created_at_utc": now.isoformat(),
        "learn_passed": bool(learn_passed),
        "owner_files": list(OWNER_FILES),
        "context_files": list(required_files),
        "context_digest": context_digest,
        "project_understanding": {
            "summary": readme_summary,
            "goal": north_star,
        },
        "session_status": {
            "continuity": "run-context" if state["current_run_id"] else "project-only",
            "current_stage": {
                "current_project_id": project_id,
                "current_run_id": state["current_run_id"],
                "current_task_file": state["current_task_file"],
                "current_status": state["current_status"],
            },
        },
        "guide_questions": [
            {
                "question_id": q.question_id,
                "title": q.title,
                "must_read_files": q.must_read_files,
                "why": q.why,
                "mainline": q.mainline_lines,
            }
            for q in questions
        ],
        "sync": {
            "mode": "project-guide-driven-read",
            "passed": learn_passed,
            "required_total": len(required_files),
            "required_read": len(required_files) - len(missing_required),
            "missing_required_files": missing_required,
        },
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
        "## Owner Files",
    ]
    for path in OWNER_FILES:
        lines.append(f"- `{path}`")
    lines.extend(
        [
            "",
            "## Questions",
            f"- count: {len(questions)}",
            "",
            "## Sync",
            f"- required read: {obj['sync']['required_read']}/{obj['sync']['required_total']}",
            f"- pass: `{str(learn_passed).lower()}`",
        ]
    )
    if missing_required:
        lines.append("- missing required:")
        for path in missing_required:
            lines.append(f"  - `{path}`")
    lines.extend(
        [
            "",
            "## Current Stage",
            f"- project: `{project_id}`",
            f"- run: `{state['current_run_id'] or '(none)'}`",
            f"- task: `{state['current_task_file'] or '(none)'}`",
            "",
            "## Mainline",
            f"- {north_star}",
            "",
            "## Next Command",
            f"- `{obj['next_command']}`",
            "",
        ]
    )
    learn_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"LEARN_STATUS: {'pass' if obj['learn_passed'] else 'fail'}")
    print(f"LEARN_SYNC_REQUIRED_READ: {obj['sync']['required_read']}/{obj['sync']['required_total']}")
    print(f"LEARN_GUIDE_QUESTION_COUNT: {len(questions)}")
    print(f"LEARN_CONTEXT_DIGEST: {context_digest}")



# learn_tools_14 中文：打印基础 learn 锚点信息。
def print_base_anchors(learn_file: Path) -> None:
    obj = read_json(learn_file)
    stage = obj.get("session_status", {}).get("current_stage", {})
    stage_parts = [
        f"project={stage.get('current_project_id', '')}",
    ]
    if stage.get("current_run_id"):
        stage_parts.append(f"run={stage.get('current_run_id')}")
    if stage.get("current_task_file"):
        stage_parts.append(f"task={stage.get('current_task_file')}")
    print(f"LEARN_MAINLINE: {' '.join(str((obj.get('project_understanding') or {}).get('goal', '')).split())}")
    print(f"LEARN_CURRENT_STAGE: {' '.join(' '.join(stage_parts).split())}")
    print(f"LEARN_NEXT_STEP: {' '.join(str(obj.get('next_command', '')).split())}")
    print(f"LEARN_REQUIRED_FILES_READ_LIST: {','.join(obj.get('context_files') or [])}")



# learn_tools_15 中文：生成发给 Codex 的 learn prompt。
def generate_prompt(learn_file: Path, prompt_file: Path, project_id: str, plan_mode: str) -> None:
    obj = read_json(learn_file)
    guide_questions = obj.get("guide_questions") or []
    required_files = [str(x).strip() for x in (obj.get("context_files") or []) if str(x).strip()]
    owner_files = [str(x).strip() for x in (obj.get("owner_files") or []) if str(x).strip()]
    stage = ((obj.get("session_status") or {}).get("current_stage") or {})
    schema_lines = [
        "{",
        '  "mainline": "<string>",',
        '  "current_stage": "<string>",',
        '  "next_step": "<string>",',
        '  "files_read": ["<path1>", "<path2>"],',
        '  "plan_protocol": {',
        '    "goal": "<string>",',
        '    "non_goal": "<string>",',
        '    "evidence": ["<path>#<section>: <concrete fact>"],',
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
        '  "guide_oral": [',
        '    {',
        '      "question_id": "Q1",',
        '      "question": "<question title>",',
        '      "answer": "<1-2 sentence oral answer>",',
        '      "standard_alignment": "aligned|partial|drifted",',
        '      "evidence": ["<path>#<section>: <concrete fact>"],',
        '      "drift_note": "<short difference or none>",',
        '      "return_to_mainline": "<how this question returns to mainline>"',
        '    }',
        '  ],',
        '  "anchor_realign": {',
        '    "question_id": "<Q1..Qn from PROJECT_GUIDE>",',
        '    "status": "on_track|drifted",',
        '    "drift_detail": "<what drift happened or none>",',
        '    "return_to_mainline": "<how to return to mainline now>"',
        '  }',
        "}",
    ]

    lines = [
        "You are performing strict onboarding sync for quant-factory-os.",
        "Use `/plan` strongest planning mindset in this response (plan-first, evidence-first, no execution).",
        "This is a real plan-mode onboarding pass, not a summary shortcut.",
        "Read files with tools/view.sh and reply with JSON only.",
        "Your entire final reply must be exactly one JSON object and nothing else.",
        "Any prose before or after the JSON object is a failure.",
        "",
        f"PROJECT_ID: {project_id}",
        f"CURRENT_RUN_ID: {stage.get('current_run_id') or '(none)'}",
        f"CURRENT_TASK_FILE: {stage.get('current_task_file') or '(none)'}",
        "",
        "Owner files:",
    ]
    for path in owner_files:
        lines.append(f"- {path}")
    extra_files = [path for path in required_files if path not in owner_files]
    lines.extend(
        [
            "",
            "Additional required files to read with tools/view.sh:",
        ]
    )
    for path in extra_files:
        lines.append(f"- {path}")
    lines.extend(["", "PROJECT_GUIDE question ids to answer in order:"])
    for item in guide_questions:
        qid = str(item.get("question_id", "")).strip()
        title = str(item.get("title", "")).strip()
        lines.append(f"- {qid}: {title}")
    lines.extend(
        [
            "",
            "Output requirements:",
            "- Do not run write commands.",
            "- Read owner files first in this order: docs/PROJECT_GUIDE.md -> AGENTS.md -> docs/WORKFLOW.md.",
            "- Then read the additional required files listed above.",
            "- Use tools/view.sh for all file reads. If a file is long, read only the relevant chunk(s); do not force full-file reads when a section-sized read is enough.",
            "- Prefer targeted section reads over whole-document sweeps, especially for docs/WORKFLOW.md and CODEX_CLI_* docs.",
            "- Do not search for more files unless a listed required file was truncated or a question's must-read file clearly requires one short section lookup.",
            "- The must-read mapping for each question is already defined inside PROJECT_GUIDE. Use that file as the source of truth instead of rebuilding the mapping yourself.",
            "- Then answer every PROJECT_GUIDE question in order (Q1..Qn) using the guide's own standard answers plus evidence from its must-read files.",
            "- Do not skip any question.",
            "- Keep every answer concise but complete: target 1-2 sentences per question.",
            "- Keep every drift_note to one short sentence.",
            "- For each guide_oral item, include only the minimum evidence needed to cover that question's must_read files.",
            "- For each guide_oral item, evidence count should normally equal the number of must_read files for that question; do not add extra evidence unless required.",
            "- Do not reread a file unless the first read was truncated or the needed section was not covered.",
            "- Once every required file has been read with enough evidence to answer its mapped questions, stop reading and emit the final JSON immediately.",
            "- Do not add any concluding explanation, recap paragraph, or natural-language summary outside the JSON fields.",
            "- Do not use rg, grep, or ls for exploration in this pass unless a required file read was truncated and you need one short section lookup.",
            "- For current-status questions, use current TASKS/STATE plus current run summary/decision only; do not wander into unrelated historical artifacts.",
            "- Do not emit process narration, planning prose, or any text before the final JSON object.",
            "- Do not include markdown fences.",
            "- JSON must follow this schema exactly:",
        ]
    )
    lines.extend(schema_lines)
    lines.extend(
        [
            "",
            "Strong mode gates:",
            "- Treat this pass as true `/plan` strongest mode.",
            "- plan_protocol fields are mandatory.",
            "- plan_protocol.evidence must cover every owner file at least once.",
            "- oral_restate fields are mandatory.",
            "- guide_oral must cover every PROJECT_GUIDE question exactly once and remain in Q-order.",
            "- Each guide_oral item must cite evidence from that question's must_read files.",
            "- anchor_realign must map to one PROJECT_GUIDE question id.",
            "- Practice must include tools/view.sh reads for every required file.",
            "",
            "Evidence format rule:",
            '- Use: "<path>#<section>: <concrete fact>".',
        ]
    )
    prompt_file.write_text("\n".join(lines) + "\n", encoding="utf-8")



# learn_tools_16 中文：判断模型输出里的路径引用是否匹配要求文件。
def path_reference_matches(text: str, required_path: str) -> bool:
    value = str(text or "").strip()
    target = str(required_path or "").strip()
    if not value or not target:
        return False
    resolved = str(Path(target).resolve())
    return target in value or f"./{target}" in value or resolved in value



# learn_tools_17 中文：从原始文本中提取首个合法 learn JSON 数据块。
def extract_first_learn_json_dict(raw_text: str) -> dict[str, Any] | None:
    text = str(raw_text or "").strip()
    if not text:
        return None
    decoder = json.JSONDecoder()
    required = {"mainline", "current_stage", "next_step", "files_read"}
    for idx, ch in enumerate(text):
        if ch != "{":
            continue
        try:
            maybe, _end = decoder.raw_decode(text[idx:])
        except Exception:
            continue
        if isinstance(maybe, dict) and required.issubset(set(maybe.keys())):
            return maybe
    return None


# learn_tools_18 中文：从事件流文件中恢复 learn JSON 结果。
def extract_learn_json_from_events(model_events_file: Path) -> dict[str, Any] | None:
    parsed = extract_final_answer_json_from_events(model_events_file)
    if not parsed:
        return None
    try:
        maybe = json.loads(parsed)
    except Exception:
        return extract_first_learn_json_dict(parsed)
    return maybe if isinstance(maybe, dict) else None



# learn_tools_19 中文：解析模型原始输出并提取结构化 learn 结果。
def parse_model_output(model_raw_file: Path, model_json_file: Path, plan_mode: str, learn_file: Path, model_events_file: Path) -> dict[str, Any]:
    raw_text = model_raw_file.read_text(encoding="utf-8", errors="replace") if model_raw_file.is_file() else ""
    obj: dict[str, Any] | None = None
    if raw_text.strip():
        try:
            maybe = json.loads(raw_text)
            if isinstance(maybe, dict):
                obj = maybe
        except Exception:
            obj = extract_first_learn_json_dict(raw_text)
    if obj is not None and not {"mainline", "current_stage", "next_step", "files_read"}.issubset(set(obj.keys())):
        obj = extract_first_learn_json_dict(raw_text)
    if obj is None:
        obj = extract_learn_json_from_events(model_events_file)
    if obj is None:
        if not raw_text.strip():
            raise ValueError("model raw empty")
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
    owner_files = [str(x).strip() for x in (learn_obj.get("owner_files") or []) if str(x).strip()]
    guide_questions = learn_obj.get("guide_questions") or []
    expected_questions = {
        str(item.get("question_id", "")).strip(): item
        for item in guide_questions
        if str(item.get("question_id", "")).strip()
    }
    if not required_files:
        raise ValueError("context_files empty")
    missing_required = [path for path in required_files if not any(path_reference_matches(value, path) for value in files_read)]
    if missing_required:
        raise ValueError(f"files_read missing required files: {missing_required}")

    if plan_mode == "strong":
        plan = obj.get("plan_protocol")
        oral = obj.get("oral_restate")
        guide_oral = obj.get("guide_oral")
        anchor = obj.get("anchor_realign")
        if not isinstance(plan, dict):
            raise ValueError("plan_protocol missing")
        for key in ["goal", "non_goal", "evidence", "alternatives", "rebuttal", "decision_stop_condition"]:
            if key not in plan:
                raise ValueError(f"plan_protocol missing {key}")
        evidence = plan.get("evidence") or []
        if not isinstance(evidence, list) or not evidence:
            raise ValueError("plan_protocol.evidence invalid")
        missing_owner_evidence = [
            path for path in owner_files if not any(path_reference_matches(str(item), path) for item in evidence)
        ]
        if missing_owner_evidence:
            raise ValueError(f"plan_protocol.evidence missing owner files: {missing_owner_evidence}")
        if not isinstance(oral, dict):
            raise ValueError("oral_restate missing")
        for key in ["project_understanding", "constitution_workflow", "evidence_chain", "session_continuity", "current_focus", "next_action"]:
            if key not in oral:
                raise ValueError(f"oral_restate missing {key}")
        if not isinstance(guide_oral, list):
            raise ValueError("guide_oral invalid")
        if len(guide_oral) != len(expected_questions):
            raise ValueError("guide_oral question count mismatch")
        seen_qids: set[str] = set()
        expected_order = list(expected_questions.keys())
        actual_order: list[str] = []
        for item in guide_oral:
            if not isinstance(item, dict):
                raise ValueError("guide_oral item invalid")
            for key in ["question_id", "question", "answer", "standard_alignment", "evidence", "drift_note", "return_to_mainline"]:
                if key not in item:
                    raise ValueError(f"guide_oral missing {key}")
            qid = str(item.get("question_id", "")).strip().upper()
            if qid not in expected_questions:
                raise ValueError(f"guide_oral unexpected question_id: {qid}")
            if qid in seen_qids:
                raise ValueError(f"guide_oral duplicate question_id: {qid}")
            seen_qids.add(qid)
            actual_order.append(qid)
            if not str(item.get("question", "")).strip() or not str(item.get("answer", "")).strip():
                raise ValueError(f"guide_oral empty question/answer: {qid}")
            alignment = str(item.get("standard_alignment", "")).strip().lower()
            if alignment not in {"aligned", "partial", "drifted"}:
                raise ValueError(f"guide_oral standard_alignment invalid: {qid}")
            evidence_items = item.get("evidence") or []
            if not isinstance(evidence_items, list) or not evidence_items:
                raise ValueError(f"guide_oral evidence invalid: {qid}")
            must_read_files = [str(path).strip() for path in (expected_questions[qid].get("must_read_files") or []) if str(path).strip()]
            missing_question_evidence = [
                path for path in must_read_files if not any(path_reference_matches(str(ev), path) for ev in evidence_items)
            ]
            if missing_question_evidence:
                raise ValueError(f"guide_oral evidence missing required files for {qid}: {missing_question_evidence}")
        if actual_order != expected_order:
            raise ValueError("guide_oral order mismatch")
        if not isinstance(anchor, dict):
            raise ValueError("anchor_realign missing")
        for key in ["question_id", "status", "drift_detail", "return_to_mainline"]:
            if key not in anchor:
                raise ValueError(f"anchor missing {key}")
        status = str(anchor.get("status", "")).strip()
        if status not in {"on_track", "drifted"}:
            raise ValueError("anchor status invalid")
        qid = str(anchor.get("question_id", "")).strip().upper()
        if qid not in expected_questions:
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
            if path_reference_matches(cmd_text, req):
                viewed_required.add(req)
    missing_views = [path for path in required_files if path not in viewed_required]
    if missing_views:
        raise ValueError(f"required files not actually viewed via tools/view.sh: {missing_views}")

    practice_samples: list[str] = []
    seen: set[str] = set()
    for cmd in practice_commands:
        if cmd in seen:
            continue
        seen.add(cmd)
        practice_samples.append(cmd)
        if len(practice_samples) >= 5:
            break
    obj["practice"] = {
        "command_execution_count": len(practice_commands),
        "command_samples": practice_samples,
    }
    write_json(model_json_file, obj)
    return obj



# learn_tools_20 中文：打印模型侧 learn 锚点信息。
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
    guide_oral = obj.get("guide_oral") or []
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
    for idx, sample in enumerate(practice.get("command_samples") or [], start=1):
        print(f"LEARN_MODEL_PRACTICE_SAMPLE_{idx}: {' '.join(str(sample).split())}")
    print(f"LEARN_MODEL_ORAL_Q_COUNT: {len(guide_oral)}")
    for idx, item in enumerate(guide_oral, start=1):
        if not isinstance(item, dict):
            continue
        print(f"LEARN_MODEL_ORAL_QID{idx}: {' '.join(str(item.get('question_id', '')).split())}")
        print(f"LEARN_MODEL_ORAL_Q{idx}: {' '.join(str(item.get('question', '')).split())}")
        print(f"LEARN_MODEL_ORAL_A{idx}: {' '.join(str(item.get('answer', '')).split())}")
        print(f"LEARN_MODEL_ORAL_ALIGNMENT{idx}: {' '.join(str(item.get('standard_alignment', '')).split())}")
        evidence_count = len(item.get("evidence") or []) if isinstance(item.get("evidence"), list) else 0
        print(f"LEARN_MODEL_ORAL_EVIDENCE_COUNT{idx}: {evidence_count}")

    print("LEARN_READOUT_BEGIN")
    print(f"LEARN_READOUT_MAINLINE: {' '.join(str(obj.get('mainline', '')).split())}")
    print(f"LEARN_READOUT_CURRENT_STAGE: {' '.join(str(obj.get('current_stage', '')).split())}")
    print(f"LEARN_READOUT_NEXT_STEP: {' '.join(str(obj.get('next_step', '')).split())}")
    print(f"LEARN_READOUT_ORAL_PROJECT: {' '.join(str(oral.get('project_understanding', '')).split())}")
    print(f"LEARN_READOUT_ORAL_CURRENT_FOCUS: {' '.join(str(oral.get('current_focus', '')).split())}")
    print(f"LEARN_READOUT_ANCHOR: {' '.join(str(anchor.get('question_id', '')).split())} | {' '.join(str(anchor.get('status', '')).split())}")
    print(f"LEARN_READOUT_ANCHOR_ACTION: {' '.join(str(anchor.get('return_to_mainline', '')).split())}")
    print(f"LEARN_READOUT_PRACTICE_COUNT: {int(practice.get('command_execution_count', 0))}")
    print("LEARN_READOUT_END")



# learn_tools_21 中文：把模型结果回写到 learn 主产物。
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
            f"- transport: `{plan_transport_effective}`",
            f"- status: `{model_sync_status}`",
            f"- reason: `{model_sync_reason}`",
            f"- prompt: `{model_prompt_file}`",
            f"- raw: `{model_raw_file}`",
            f"- parsed: `{model_json_file}`",
            f"- events: `{model_events_file}`",
            f"- stderr: `{model_stderr_file}`",
        ]
    )
    if model_sync_pass and isinstance(model_obj.get("result"), dict):
        result = model_obj["result"]
        guide_oral = result.get("guide_oral") or []
        lines.extend(
            [
                "",
                "## Guide Oral",
                f"- count: {len(guide_oral)}",
            ]
        )
        for item in guide_oral:
            if not isinstance(item, dict):
                continue
            lines.append(f"- {item.get('question_id')}: {item.get('question')}")
            lines.append(f"  - alignment: {item.get('standard_alignment')}")
    learn_md.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")



# learn_tools_22 中文：校验 learn 主文件是否满足门禁要求。
def learn_file_is_valid(learn_file: Path) -> bool:
    try:
        obj = read_json(learn_file)
    except Exception:
        return False
    if str(obj.get("schema", "")).strip() != "qf_learn.v3":
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
    if str(model_sync.get("plan_transport", "")).strip() != MODEL_TRANSPORT_PRIMARY:
        return False
    if str(model_sync.get("status", "")).strip() != "pass":
        return False
    if not bool(model_sync.get("passed")):
        return False
    model_result = model_sync.get("result")
    if not isinstance(model_result, dict):
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
    if not isinstance(context_files, list):
        context_files = []
    digest_lines = [f"ctx:{rel}:{file_sha(Path(str(rel)))}" for rel in context_files]
    digest_lines.sort()
    current = hashlib.sha256("\n".join(digest_lines).encode("utf-8")).hexdigest()
    return current == str(obj.get("context_digest", "")).strip()



# learn_tools_23 中文：检查 learn 文件是否属于当前项目。
def learn_file_matches_project(path: Path, project_id: str) -> bool:
    try:
        obj = read_json(path)
    except Exception:
        return False
    pid = str(obj.get("project_id") or "").strip() or DEFAULT_PROJECT_ID
    return pid == project_id



# learn_tools_24 中文：定位当前项目对应的 learn 文件。
def resolve_learn_file_for_project(project_id: str) -> str:
    learn_file = Path("learn") / f"{project_id}.json"
    if learn_file.is_file() and learn_file_is_valid(learn_file) and learn_file_matches_project(learn_file, project_id):
        return str(learn_file)
    return ""



# 2001 中文：第一步，锁定 learn 运行配置和当前项目上下文。
def learn_step_01_resolve_context(argv: list[str]) -> LearnContext:
    cfg = parse_cli(argv)
    project_id = resolve_project_id_for_cmd(cfg["explicit_project_id"], "learn")
    if os.environ.get("QF_LEARN_LOG_ACTIVE", "0") != "1":
        raise SystemExit(run_logged_self(project_id, cfg))
    state = read_state_snapshot()
    emit_step(1, 5, "resolve project context")
    print("LEARN_SCOPE_MODE: project-scoped")
    print(f"LEARN_PROJECT_ID: {project_id}")
    print(f"LEARN_CURRENT_RUN_ID: {state['current_run_id'] or '(none)'}")
    print("LEARN_SYNC_MODE: project-guide-driven-read")
    return LearnContext(cfg=cfg, project_id=project_id, state=state)


# 2002 中文：第二步，准备 learn 产物路径并清理旧的临时模型文件。
def learn_step_02_prepare_artifacts(context: LearnContext) -> LearnContext:
    emit_step(2, 5, "prepare learn artifact paths")
    learn_dir = Path("learn")
    learn_dir.mkdir(parents=True, exist_ok=True)
    context.learn_dir = learn_dir
    context.learn_file = learn_dir / f"{context.project_id}.json"
    context.learn_md = learn_dir / f"{context.project_id}.md"
    context.model_prompt_file = learn_dir / f"{context.project_id}.model.prompt.txt"
    context.model_raw_file = learn_dir / f"{context.project_id}.model.raw.txt"
    context.model_json_file = learn_dir / f"{context.project_id}.model.json"
    context.model_events_file = learn_dir / f"{context.project_id}.model.events.jsonl"
    context.model_stderr_file = learn_dir / f"{context.project_id}.model.stderr.log"
    for path in (
        context.model_prompt_file,
        context.model_raw_file,
        context.model_json_file,
        context.model_events_file,
        context.model_stderr_file,
    ):
        try:
            if path.exists():
                path.unlink()
        except Exception as exc:
            eprint(str(exc))
            raise SystemExit(1)
    return context


# 2003 中文：第三步，生成 learn 基础课程产物和主线锚点。
def learn_step_03_build_base_packet(context: LearnContext) -> LearnContext:
    emit_step(3, 5, "generate learn report (project guide + constitution + workflow)")
    assert context.learn_file is not None
    assert context.learn_md is not None
    try:
        build_base_learn(context.project_id, context.learn_file, context.learn_md, context.state)
    except Exception as exc:
        eprint(f"ERROR: build_base_learn failed: {exc}")
        raise SystemExit(1)
    print_base_anchors(context.learn_file)
    return context


# 2004 中文：第四步，执行模型同频并把模型结果回写到 learn 主产物。
def learn_step_04_run_model_sync(context: LearnContext) -> LearnContext:
    if shutil.which("codex") is None:
        eprint("ERROR: learn requires codex CLI (model sync is mandatory).")
        raise SystemExit(1)

    emit_step(4, 5, "run model sync and validate learn output")
    cfg = context.cfg
    assert context.learn_file is not None
    assert context.learn_md is not None
    assert context.model_prompt_file is not None
    assert context.model_raw_file is not None
    assert context.model_json_file is not None
    assert context.model_events_file is not None
    assert context.model_stderr_file is not None

    print(f"LEARN_MODEL_SYNC_MODE: {cfg['model_sync_mode']}")
    print(f"LEARN_MODEL_PLAN_MODE: {cfg['plan_mode']}")
    print(f"LEARN_MODEL_PLAN_TRANSPORT: {MODEL_TRANSPORT_PRIMARY}")
    print(f"LEARN_MODEL_PLAN_TRANSPORT_PRIMARY: {MODEL_TRANSPORT_PRIMARY}")
    print(f"LEARN_MODEL: {cfg['model_name']}")
    print(f"LEARN_MODEL_REASONING_PROFILE: {cfg['reasoning_profile']}")
    requested_effort = cfg["model_reasoning_effort"]
    effective_effort, effort_reason = runtime_reasoning_effort(requested_effort)
    if cfg.get("reasoning_alias") == "daily" and effort_reason == "as-requested":
        effort_reason = "daily-alias-to-medium"
    print(f"LEARN_MODEL_REASONING_EFFORT: {effective_effort}")
    print(f"LEARN_MODEL_REASONING_EFFORT_REQUESTED: {requested_effort}")
    print(f"LEARN_MODEL_REASONING_EFFORT_EFFECTIVE: {effective_effort}")
    print(f"LEARN_MODEL_REASONING_EFFORT_REASON: {effort_reason}")

    generate_prompt(context.learn_file, context.model_prompt_file, context.project_id, cfg["plan_mode"])
    transport_req = TransportRequest(
        model_name=cfg["model_name"],
        model_reasoning_effort=effective_effort,
        cwd=Path.cwd(),
    )
    transport_artifacts = TransportArtifacts(
        prompt_file=context.model_prompt_file,
        raw_file=context.model_raw_file,
        events_file=context.model_events_file,
        stderr_file=context.model_stderr_file,
    )
    transport_result = run_plan_sync(transport_req, transport_artifacts)
    print(f"LEARN_MODEL_SYNC_RC_{MODEL_TRANSPORT_PRIMARY}: {transport_result.primary_rc}")
    print(f"LEARN_MODEL_PLAN_TRANSPORT_EFFECTIVE: {transport_result.effective_transport}")
    print(f"LEARN_MODEL_SYNC_RC: {transport_result.final_rc}")

    model_sync_pass = False
    model_sync_status = "fail"
    model_sync_reason = "unknown"
    try:
        parsed = parse_model_output(
            context.model_raw_file,
            context.model_json_file,
            cfg["plan_mode"],
            context.learn_file,
            context.model_events_file,
        )
        print_model_anchors(parsed, cfg["plan_mode"])
        model_sync_pass = True
        model_sync_status = "pass"
        model_sync_reason = "ok"
    except Exception as exc:
        if transport_result.final_rc != 0:
            model_sync_reason = f"codex-exit-{transport_result.final_rc}"
        else:
            model_sync_reason = f"schema-parse-failed:{exc}"
        print("LEARN_MODEL_SYNC_STATUS: fail")
        print(f"LEARN_MODEL_SYNC_REASON: {model_sync_reason}")

    update_learn_with_model(
        context.learn_file,
        context.learn_md,
        cfg["model_sync_mode"],
        cfg["plan_mode"],
        transport_result.effective_transport,
        model_sync_status,
        model_sync_reason,
        model_sync_pass,
        context.model_prompt_file,
        context.model_raw_file,
        context.model_json_file,
        context.model_events_file,
        context.model_stderr_file,
    )

    if not model_sync_pass:
        eprint("ERROR: learn model sync strict mode failed.")
        eprint(f"Check: {context.model_stderr_file}")
        raise SystemExit(1)
    if not learn_file_is_valid(context.learn_file):
        eprint("ERROR: learn output validation failed.")
        eprint(f"Check: {context.learn_file}")
        raise SystemExit(1)
    return context


# 2005 中文：第五步，打印 learn 产物位置并给出下一步。
def learn_step_05_finalize(context: LearnContext) -> int:
    emit_step(5, 5, "print learn artifacts")
    assert context.learn_file is not None
    assert context.learn_md is not None
    assert context.model_prompt_file is not None
    assert context.model_raw_file is not None
    assert context.model_json_file is not None
    assert context.model_events_file is not None
    assert context.model_stderr_file is not None
    print(f"LEARN_FILE: {context.learn_file}")
    print(f"LEARN_MD: {context.learn_md}")
    print(f"LEARN_MODEL_PROMPT_FILE: {context.model_prompt_file}")
    print(f"LEARN_MODEL_RAW_FILE: {context.model_raw_file}")
    print(f"LEARN_MODEL_JSON_FILE: {context.model_json_file}")
    print(f"LEARN_MODEL_EVENTS_FILE: {context.model_events_file}")
    print(f"LEARN_MODEL_STDERR_FILE: {context.model_stderr_file}")
    print("LEARN_NEXT_COMMAND: python3 tools/ready.py")
    return 0


# 2006 中文：执行 learn 主流程，main 只负责分发五个业务步骤。
def main(argv: list[str]) -> int:
    context = learn_step_01_resolve_context(argv)
    context = learn_step_02_prepare_artifacts(context)
    context = learn_step_03_build_base_packet(context)
    context = learn_step_04_run_model_sync(context)
    return learn_step_05_finalize(context)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
