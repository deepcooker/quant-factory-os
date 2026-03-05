#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import pty
import re
import select
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


STATE_FILE = Path(os.environ.get("QF_STATE_FILE", "TASKS/STATE.md"))
DEFAULT_PROJECT_ID = os.environ.get("QF_DEFAULT_PROJECT_ID", "project-0")


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
            "tool": "qf",
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


def parse_bool_01(name: str, raw: str, *, allow_true_default: bool = True) -> str:
    v = raw.strip().lower()
    if v in {"1", "true", "yes", "y"}:
        return "1"
    if v in {"0", "false", "no", "n"}:
        return "0"
    if allow_true_default and raw == "":
        return "1"
    eprint(f"ERROR: invalid {name}={raw} (expected 0|1).")
    raise SystemExit(2)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_cli(argv: list[str]) -> dict[str, Any]:
    explicit_project_id = os.environ.get("QF_PROJECT_ID", os.environ.get("PROJECT_ID", ""))
    ttl_days = os.environ.get("QF_LEARN_TTL_DAYS", "7")
    log_enabled = os.environ.get("QF_LEARN_LOG", "1")
    log_file = os.environ.get("QF_LEARN_LOG_FILE", "")
    model_sync_raw = os.environ.get("QF_LEARN_MODEL_SYNC", "1")
    plan_mode_raw = os.environ.get("QF_LEARN_PLAN_MODE", "strong")
    plan_transport_raw = os.environ.get("QF_LEARN_PLAN_TRANSPORT", "auto")
    plan_fallback_exec_raw = os.environ.get("QF_LEARN_PLAN_FALLBACK_EXEC", "0")
    model_timeout_sec = os.environ.get("QF_LEARN_MODEL_TIMEOUT_SEC", "300")
    model_name = os.environ.get("QF_LEARN_MODEL", os.environ.get("MODEL", ""))

    for token in argv:
        if not token:
            continue
        if token.startswith("PROJECT_ID="):
            explicit_project_id = token.split("=", 1)[1]
        elif token.startswith("TTL_DAYS="):
            ttl_days = token.split("=", 1)[1]
        elif token.startswith("MODEL_SYNC="):
            model_sync_raw = token.split("=", 1)[1]
        elif token.startswith("PLAN_MODE="):
            plan_mode_raw = token.split("=", 1)[1]
        elif token.startswith("PLAN_TRANSPORT="):
            plan_transport_raw = token.split("=", 1)[1]
        elif token.startswith("MODEL_TIMEOUT_SEC="):
            model_timeout_sec = token.split("=", 1)[1]
        elif token.startswith("MODEL="):
            model_name = token.split("=", 1)[1]
        elif token in {"-log", "--log"}:
            log_enabled = "1"
        elif token.startswith("LOG="):
            log_enabled = "1"
            log_file = token.split("=", 1)[1]
        elif token.startswith("AUTO_EXAM=") or token.startswith("REQUIRE_EXAM="):
            # Compatibility no-op.
            pass
        elif "=" in token:
            eprint(f"ERROR: unexpected learn arg: {token}")
            raise SystemExit(2)
        else:
            eprint("ERROR: learn does not accept positional args. Use PROJECT_ID=... or flags only.")
            raise SystemExit(2)

    if not ttl_days.isdigit() or int(ttl_days) < 1:
        eprint(f"ERROR: invalid TTL_DAYS={ttl_days} (expected positive integer).")
        raise SystemExit(2)
    if not model_timeout_sec.isdigit() or int(model_timeout_sec) < 1:
        eprint(f"ERROR: invalid MODEL_TIMEOUT_SEC={model_timeout_sec} (expected positive integer).")
        raise SystemExit(2)

    model_sync_mode = parse_bool_01("MODEL_SYNC", model_sync_raw, allow_true_default=False)
    if model_sync_mode != "1":
        eprint("ERROR: learn requires model sync. Use MODEL_SYNC=1 (or QF_LEARN_MODEL_SYNC=1).")
        raise SystemExit(2)

    plan_mode = plan_mode_raw.strip().lower()
    if plan_mode != "strong":
        eprint("ERROR: learn requires PLAN_MODE=strong (or QF_LEARN_PLAN_MODE=strong).")
        raise SystemExit(2)

    plan_transport = plan_transport_raw.strip().lower()
    if plan_transport not in {"auto", "slash", "exec"}:
        eprint(f"ERROR: invalid QF_LEARN_PLAN_TRANSPORT={plan_transport_raw} (expected auto|slash|exec).")
        raise SystemExit(2)

    plan_fallback_exec = parse_bool_01("QF_LEARN_PLAN_FALLBACK_EXEC", plan_fallback_exec_raw)
    log_mode = parse_bool_01("learn log flag", log_enabled)

    return {
        "explicit_project_id": explicit_project_id,
        "ttl_days": int(ttl_days),
        "log_enabled": log_mode,
        "log_file": log_file,
        "model_sync_mode": model_sync_mode,
        "plan_mode": plan_mode,
        "plan_transport": plan_transport,
        "plan_fallback_exec": plan_fallback_exec,
        "model_timeout_sec": int(model_timeout_sec),
        "model_name": model_name.strip(),
    }


def run_logged_self(project_id: str, cfg: dict[str, Any]) -> int:
    log_file = cfg["log_file"] or f"learn/{project_id}.stdout.log"
    print(f"LEARN_LOG_FILE: {log_file}")
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "bash",
        "tools/qf",
        "learn",
        f"PROJECT_ID={project_id}",
        f"TTL_DAYS={cfg['ttl_days']}",
        f"MODEL_SYNC={cfg['model_sync_mode']}",
        f"PLAN_MODE={cfg['plan_mode']}",
        f"PLAN_TRANSPORT={cfg['plan_transport']}",
        f"MODEL_TIMEOUT_SEC={cfg['model_timeout_sec']}",
    ]
    if cfg["model_name"]:
        cmd.append(f"MODEL={cfg['model_name']}")
    env = os.environ.copy()
    env["QF_LEARN_LOG_ACTIVE"] = "1"
    env["QF_LEARN_LOG"] = "0"
    env["QF_LEARN_LOG_FILE"] = log_file
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


def build_base_learn(project_id: str, ttl_days: int, learn_file: Path, learn_md: Path) -> None:
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
    expires = now + timedelta(days=max(ttl_days, 1))
    obj: dict[str, Any] = {
        "schema": "qf_learn.v2",
        "project_id": project_id,
        "scope": "project-session",
        "created_at_utc": now.isoformat(),
        "expires_at_utc": expires.isoformat(),
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
        "next_command": "tools/qf ready",
    }
    write_json(learn_file, obj)

    lines = [
        "# Learn Report",
        "",
        f"PROJECT_ID: `{project_id}`",
        f"Generated At (UTC): {obj['created_at_utc']}",
        f"Expires At (UTC): {obj['expires_at_utc']}",
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
        "Read the listed files with tools/view.sh and reply with JSON only.",
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
            "- Execute only minimal read/shell commands needed to gather evidence from the required files.",
            "- Do not call tools/qf init/learn/ready inside this model-sync pass.",
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
                "- plan_protocol fields are mandatory.",
                "- oral_restate fields are mandatory.",
                "- oral_exam must contain at least 3 QA items, each bound to PROJECT_GUIDE question ids (Q1..Q17).",
                "- anchor_realign must map to one PROJECT_GUIDE question id (Q1..Q17).",
                "",
            ]
        )
    lines.append("files_read must be a subset of the required files list above.")
    prompt_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_slash_transport(prompt_file: Path, raw_file: Path, events_file: Path, stderr_file: Path, timeout_sec: int, model_name: str) -> int:
    try:
        prompt_text = prompt_file.read_text(encoding="utf-8", errors="replace")
    except Exception as exc:
        stderr_file.write_text(f"read prompt failed: {exc}\n", encoding="utf-8")
        return 1

    cli_prompt = "/plan\n" + prompt_text
    cmd = ["codex", "--sandbox", "read-only", "--ask-for-approval", "never", "--search", "--no-alt-screen"]
    if model_name:
        cmd.extend(["-m", model_name])
    cmd.append(cli_prompt)
    try:
        master, slave = pty.openpty()
    except Exception as exc:
        stderr_file.write_text(f"interactive slash /plan unavailable: {exc}\n", encoding="utf-8")
        return 1

    start = time.time()
    buf = b""
    stderr_lines: list[str] = []
    submitted = False
    proc = subprocess.Popen(cmd, stdin=slave, stdout=slave, stderr=slave, close_fds=True)
    try:
        os.close(slave)
    except OSError:
        pass

    timed_out = False
    while True:
        if proc.poll() is not None:
            break
        if not submitted and (time.time() - start) > 1.0:
            try:
                os.write(master, b"\r")
                submitted = True
            except Exception:
                pass
        r, _, _ = select.select([master], [], [], 0.2)
        if r:
            try:
                chunk = os.read(master, 65536)
            except OSError:
                break
            if not chunk:
                break
            buf += chunk
        if (time.time() - start) > timeout_sec:
            timed_out = True
            try:
                proc.terminate()
            except Exception:
                pass
            break

    drain_deadline = time.time() + 2
    while time.time() < drain_deadline:
        r, _, _ = select.select([master], [], [], 0.1)
        if not r:
            if proc.poll() is not None:
                break
            continue
        try:
            chunk = os.read(master, 65536)
        except OSError:
            break
        if not chunk:
            break
        buf += chunk
    try:
        os.close(master)
    except OSError:
        pass

    raw_text = buf.decode("utf-8", errors="replace")
    events_file.write_text(raw_text, encoding="utf-8")
    plain = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", raw_text)
    plain = re.sub(r"\x1b\].*?(\x07|\x1b\\)", "", plain, flags=re.S)
    plain = plain.replace("\x1b", "")

    def collect_dict_candidates(text: str) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        dec = json.JSONDecoder()
        for i, ch in enumerate(text):
            if ch != "{":
                continue
            try:
                obj, _ = dec.raw_decode(text[i:])
            except Exception:
                continue
            if isinstance(obj, dict):
                out.append(obj)
        return out

    required_keys = {"mainline", "current_stage", "next_step", "files_read"}
    strong_keys = {"plan_protocol", "oral_restate", "oral_exam", "anchor_realign"}
    candidates: list[dict[str, Any]] = collect_dict_candidates(plain)
    compact = re.sub(r"\s+", "", plain)
    if compact and compact != plain:
        candidates.extend(collect_dict_candidates(compact))

    best_obj: dict[str, Any] | None = None
    for obj in candidates:
        if not required_keys.issubset(set(obj.keys())):
            continue
        if not strong_keys.issubset(set(obj.keys())):
            continue
        mainline = str(obj.get("mainline", "")).strip()
        goal = str((obj.get("plan_protocol") or {}).get("goal", "")).strip()
        files_read = obj.get("files_read") or []
        looks_placeholder = (
            mainline in {"", "<string>"}
            or goal in {"", "<string>"}
            or any("<" in str(x) and ">" in str(x) for x in files_read)
        )
        if looks_placeholder:
            continue
        best_obj = obj
        break

    if timed_out:
        stderr_lines.append("interactive slash /plan timed out (process terminated)\n")
    if proc.returncode not in (0, None):
        stderr_lines.append(f"interactive slash /plan rc={proc.returncode}\n")

    if best_obj is None:
        stderr_lines.append("no non-placeholder JSON object recovered from interactive /plan transcript\n")
        stderr_file.write_text("".join(stderr_lines), encoding="utf-8")
        return 1

    raw_file.write_text(json.dumps(best_obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    stderr_file.write_text("".join(stderr_lines), encoding="utf-8")
    return 0


def run_exec_transport(prompt_file: Path, raw_file: Path, events_file: Path, stderr_file: Path, timeout_sec: int, model_name: str) -> int:
    cmd = ["codex", "--search", "--ask-for-approval", "never"]
    if model_name:
        cmd.extend(["-m", model_name])
    cmd.extend(["exec", "--sandbox", "read-only", "--json", "--output-last-message", str(raw_file), "-"])
    prompt_text = prompt_file.read_text(encoding="utf-8", errors="replace")
    try:
        cp = subprocess.run(
            cmd,
            input=prompt_text,
            text=True,
            capture_output=True,
            timeout=timeout_sec,
            check=False,
        )
        events_file.write_text(cp.stdout or "", encoding="utf-8")
        stderr_file.write_text(cp.stderr or "", encoding="utf-8")
        return int(cp.returncode or 0)
    except subprocess.TimeoutExpired as exc:
        events_file.write_text((exc.stdout or ""), encoding="utf-8")
        stderr_file.write_text((exc.stderr or ""), encoding="utf-8")
        return 124


def slash_placeholder_valid(raw_file: Path) -> bool:
    try:
        obj = read_json(raw_file)
    except Exception:
        return False
    required = {"mainline", "current_stage", "next_step", "files_read", "plan_protocol", "oral_restate", "oral_exam", "anchor_realign"}
    if not required.issubset(set(obj.keys())):
        return False
    mainline = str(obj.get("mainline", "")).strip()
    goal = str((obj.get("plan_protocol") or {}).get("goal", "")).strip()
    files_read = obj.get("files_read") or []
    if mainline in {"", "<string>"}:
        return False
    if goal in {"", "<string>"}:
        return False
    if any("<" in str(x) and ">" in str(x) for x in files_read):
        return False
    return True


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
        m = re.search(r"\{.*\}", raw_text, flags=re.S)
        if m:
            maybe = json.loads(m.group(0))
            if isinstance(maybe, dict):
                obj = maybe
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

    practice_commands: list[str] = []
    if model_events_file.is_file():
        events_text = model_events_file.read_text(encoding="utf-8", errors="replace")
        for raw_line in events_text.splitlines():
            line = raw_line.strip()
            if not line:
                continue
            try:
                event_obj = json.loads(line)
            except Exception:
                continue
            item = event_obj.get("item")
            if not isinstance(item, dict):
                continue
            if item.get("type") != "command_execution":
                continue
            raw_cmd = item.get("raw_input") or item.get("command") or item.get("input")
            cmd = " ".join(str(raw_cmd or "").split()).strip()
            if cmd:
                practice_commands.append(cmd)
        if not practice_commands:
            plain_events = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", events_text)
            plain_events = re.sub(r"\x1b\].*?(\x07|\x1b\\)", "", plain_events, flags=re.S)
            plain_events = plain_events.replace("\x1b", "")
            for m in re.finditer(r"/bin/bash -lc [^\r\n]+", plain_events):
                cmd = " ".join(m.group(0).split()).strip()
                if cmd:
                    practice_commands.append(cmd)
            if not practice_commands and ("Ran " in plain_events or "command_execution" in plain_events):
                practice_commands.append("interactive_plan_tool_run_detected")
    if not practice_commands:
        raise ValueError("no practice command evidence")

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

    if os.environ.get("QF_READY_IGNORE_LEARN_TTL", "0") != "1":
        expires = str(obj.get("expires_at_utc", "")).strip()
        if not expires:
            return False
        try:
            exp = datetime.fromisoformat(expires.replace("Z", "+00:00"))
        except Exception:
            return False
        now = datetime.now(timezone.utc)
        if exp.tzinfo is None:
            exp = exp.replace(tzinfo=timezone.utc)
        if exp < now:
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


@dataclass
class ModelRunResult:
    rc: int
    status: str
    reason: str
    passed: bool
    plan_transport_effective: str


def main(argv: list[str]) -> int:
    cfg = parse_cli(argv)
    project_id = resolve_project_id_for_cmd(cfg["explicit_project_id"], "learn")

    if cfg["log_enabled"] == "1" and os.environ.get("QF_LEARN_LOG_ACTIVE", "0") != "1":
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
    for p in (model_prompt_file, model_raw_file, model_json_file, model_events_file, model_stderr_file):
        try:
            if p.exists():
                p.unlink()
        except Exception as exc:
            eprint(str(exc))
            return 1

    emit_step(3, 4, "generate learn report (project + constitution + workflow + skills)")
    build_base_learn(project_id, cfg["ttl_days"], learn_file, learn_md)
    print_base_anchors(learn_file)

    if shutil.which("codex") is None:
        eprint("ERROR: learn requires codex CLI (model sync is mandatory).")
        return 1

    print(f"LEARN_MODEL_SYNC_MODE: {cfg['model_sync_mode']}")
    print(f"LEARN_MODEL_PLAN_MODE: {cfg['plan_mode']}")
    print(f"LEARN_MODEL_PLAN_TRANSPORT: {cfg['plan_transport']}")
    print(f"LEARN_MODEL_TIMEOUT_SEC: {cfg['model_timeout_sec']}")

    pty_capable = False
    if cfg["plan_transport"] in {"auto", "slash"}:
        try:
            m, s = pty.openpty()
            os.close(m)
            os.close(s)
            pty_capable = True
        except Exception:
            pty_capable = False

    plan_transport_effective = cfg["plan_transport"]
    if cfg["plan_transport"] == "auto":
        if pty_capable:
            plan_transport_effective = "slash"
            print("LEARN_MODEL_PLAN_TRANSPORT_AUTO_REASON: pty_available")
        else:
            plan_transport_effective = "exec"
            print("LEARN_MODEL_PLAN_TRANSPORT_AUTO_REASON: no_pty_devices")
    elif cfg["plan_transport"] == "slash":
        plan_transport_effective = "slash"
    elif cfg["plan_transport"] == "exec":
        plan_transport_effective = "exec"

    generate_prompt(learn_file, model_prompt_file, project_id, cfg["plan_mode"])

    model_rc = 0
    if plan_transport_effective == "slash":
        model_rc = run_slash_transport(
            model_prompt_file,
            model_raw_file,
            model_events_file,
            model_stderr_file,
            cfg["model_timeout_sec"],
            cfg["model_name"],
        )
    else:
        model_rc = run_exec_transport(
            model_prompt_file,
            model_raw_file,
            model_events_file,
            model_stderr_file,
            cfg["model_timeout_sec"],
            cfg["model_name"],
        )

    if plan_transport_effective == "slash" and model_rc == 0 and not slash_placeholder_valid(model_raw_file):
        print("LEARN_MODEL_PLAN_SLASH_OUTPUT: invalid_or_placeholder")
        model_rc = 2

    if plan_transport_effective == "slash" and model_rc != 0 and cfg["plan_fallback_exec"] == "1":
        print("LEARN_MODEL_PLAN_FALLBACK: exec")
        model_rc = run_exec_transport(
            model_prompt_file,
            model_raw_file,
            model_events_file,
            model_stderr_file,
            cfg["model_timeout_sec"],
            cfg["model_name"],
        )
        plan_transport_effective = "exec-fallback"

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
        stderr_text = model_stderr_file.read_text(encoding="utf-8", errors="replace") if model_stderr_file.is_file() else ""
        if model_rc == 124:
            model_sync_reason = "timeout"
        elif model_rc == 2:
            model_sync_reason = "slash-output-invalid"
        elif model_rc != 0:
            if re.search(r"interactive slash /plan unavailable|out of pty devices|no pty", stderr_text, flags=re.I):
                model_sync_reason = "no-pty-for-slash"
            else:
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

    if cfg["model_sync_mode"] == "1" and not model_sync_pass:
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
    print("LEARN_NEXT_COMMAND: tools/qf ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
