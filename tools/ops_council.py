#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ops_ready import (
    append_conversation_checkpoint,
    append_execution_event,
    resolve_project_id_for_cmd,
    resolve_run_id_for_cmd,
    state_field_value,
    update_state_current,
)


def parse_args(argv: list[str]) -> dict[str, str]:
    explicit_run_id = ""
    explicit_project_id = ""
    for token in argv:
        if not token:
            continue
        if token.startswith("RUN_ID="):
            explicit_run_id = token.split("=", 1)[1]
        elif token.startswith("PROJECT_ID="):
            explicit_project_id = token.split("=", 1)[1]
        else:
            if not explicit_run_id:
                explicit_run_id = token
    if not explicit_run_id:
        import os

        explicit_run_id = os.environ.get("RUN_ID", "")
    if not explicit_project_id:
        import os

        explicit_project_id = os.environ.get("QF_PROJECT_ID", os.environ.get("PROJECT_ID", ""))
    return {"explicit_run_id": explicit_run_id, "explicit_project_id": explicit_project_id}


def read_json(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_text(path: str) -> str:
    p = Path(path)
    if not p.is_file():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def normalize_scope(raw_scope: Any) -> list[str]:
    if not isinstance(raw_scope, list):
        return []
    out: list[str] = []
    for item in raw_scope:
        s = str(item).strip()
        if s:
            out.append(s.replace("`", ""))
    return out


def check_status(passed: bool, failed_level: str) -> str:
    return "pass" if passed else failed_level


def role_decision(status_by_id: dict[str, str], refs: list[str], concerns: list[str]) -> str:
    has_block = any(status_by_id.get(x) == "block" for x in refs)
    if has_block:
        return "reject_until_fixed"
    if concerns:
        return "accept_with_conditions"
    return "accept"


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    run_id = resolve_run_id_for_cmd(args["explicit_run_id"], "council")
    if not run_id:
        print("ERROR: council requires RUN_ID (explicit or TASKS/STATE.md CURRENT_RUN_ID).", file=sys.stderr)
        return 2
    project_id = resolve_project_id_for_cmd(args["explicit_project_id"], "council")

    choice_file = Path(f"reports/{run_id}/orient_choice.json")
    contract_json = Path(f"reports/{run_id}/direction_contract.json")
    if not choice_file.is_file():
        print("ERROR: direction gate not satisfied.", file=sys.stderr)
        print(f"Run: tools/ops orient RUN_ID={run_id}", file=sys.stderr)
        print(f"Then: tools/ops choose RUN_ID={run_id} OPTION=<id>", file=sys.stderr)
        print("Then retry: tools/ops do queue-next", file=sys.stderr)
        return 1
    if not contract_json.is_file():
        print(f"ERROR: missing direction contract: {contract_json}", file=sys.stderr)
        print(f"Run: tools/ops choose RUN_ID={run_id} OPTION=<id>", file=sys.stderr)
        return 1

    council_json = Path(f"chatlogs/discussion/{run_id}/council.json")
    council_md = Path(f"chatlogs/discussion/{run_id}/council.md")
    council_json.parent.mkdir(parents=True, exist_ok=True)

    contract = read_json(str(contract_json))
    title = str(contract.get("selected_title", "")).strip() or "confirmed direction"
    goal = str(contract.get("execution_goal", "")).strip()
    scope = normalize_scope(contract.get("scope_hint"))
    if not scope:
        scope = ["tools/ops", "tests/", "docs/WORKFLOW.md", "AGENTS.md", "TASKS/", "reports/{RUN_ID}/"]

    delivery_contract = contract.get("delivery_contract") or {}
    quality_gates = delivery_contract.get("quality_gates") or []
    if not isinstance(quality_gates, list):
        quality_gates = []
    steps = delivery_contract.get("steps") or []
    if not isinstance(steps, list):
        steps = []

    learn_obj = read_json(f"learn/{project_id}.json")
    ready_obj = read_json(f"reports/{run_id}/ready.json")
    queue_text = read_text("TASKS/QUEUE.md")
    queue_open_items = len(re.findall(r"^- \[ \] ", queue_text, flags=re.M))

    learn_passed = bool(learn_obj.get("learn_passed")) if learn_obj else False
    ready_passed = bool(ready_obj.get("restatement_passed")) if ready_obj else False
    goal_clear = len(goal) >= 24
    scope_present = len(scope) > 0
    scope_bounded = len(scope) <= 8 if scope_present else False
    verify_gate = any("verify" in str(x).lower() for x in quality_gates)
    docs_gate = any(("doc" in str(x).lower() or "owner docs" in str(x).lower()) for x in quality_gates)
    steps_bounded = len(steps) <= 8 if steps else True
    queue_pressure_ok = queue_open_items <= 20

    checks: list[dict[str, str]] = [
        {
            "id": "learn_gate",
            "label": "learn report is available and passed",
            "status": check_status(learn_passed, "block"),
            "detail": "learn.json missing or learn_passed=false" if not learn_passed else "ok",
        },
        {
            "id": "ready_gate",
            "label": "ready gate is passed",
            "status": check_status(ready_passed, "block"),
            "detail": "ready.json missing or restatement_passed=false" if not ready_passed else "ok",
        },
        {
            "id": "goal_clarity",
            "label": "direction goal clarity",
            "status": check_status(goal_clear, "warn"),
            "detail": "execution_goal is too short; refine expected business outcome" if not goal_clear else "ok",
        },
        {
            "id": "scope_present",
            "label": "scope is declared",
            "status": check_status(scope_present, "block"),
            "detail": "scope_hint is empty" if not scope_present else "ok",
        },
        {
            "id": "scope_bounded",
            "label": "scope remains bounded",
            "status": check_status(scope_bounded, "warn"),
            "detail": "scope paths are too broad (>8)" if not scope_bounded else "ok",
        },
        {
            "id": "verify_gate",
            "label": "delivery contract includes verify gate",
            "status": check_status(verify_gate, "warn"),
            "detail": "quality_gates missing make verify clause" if not verify_gate else "ok",
        },
        {
            "id": "docs_gate",
            "label": "delivery contract includes docs freshness gate",
            "status": check_status(docs_gate, "warn"),
            "detail": "quality_gates missing docs freshness clause" if not docs_gate else "ok",
        },
        {
            "id": "steps_bounded",
            "label": "delivery steps are operable",
            "status": check_status(steps_bounded, "warn"),
            "detail": "delivery steps are too many (>8)" if not steps_bounded else "ok",
        },
        {
            "id": "queue_pressure",
            "label": "queue pressure is manageable",
            "status": check_status(queue_pressure_ok, "warn"),
            "detail": f"open queue items={queue_open_items} (>20)" if not queue_pressure_ok else f"open queue items={queue_open_items}",
        },
    ]

    status_by_id = {c["id"]: c["status"] for c in checks}

    product_concerns: list[str] = []
    if not goal_clear:
        product_concerns.append("goal needs clearer user/business outcome statement")
    if queue_open_items > 30:
        product_concerns.append("queue backlog is high; prioritize minimal deliverable")
    if not docs_gate:
        product_concerns.append("missing docs freshness gate may cause acceptance drift")
    product_refs = ["goal_clarity", "queue_pressure", "docs_gate"]

    architect_concerns: list[str] = []
    if not learn_passed:
        architect_concerns.append("learn evidence missing; onboarding continuity risk")
    if not ready_passed:
        architect_concerns.append("ready gate missing; lifecycle invariant is broken")
    if not scope_present or not scope_bounded:
        architect_concerns.append("scope boundary is unclear or too broad")
    architect_refs = ["learn_gate", "ready_gate", "scope_present", "scope_bounded"]

    dev_concerns: list[str] = []
    if not steps_bounded:
        dev_concerns.append("delivery steps are too many; reduce friction for execution")
    if queue_open_items > 20:
        dev_concerns.append("queue pressure high; slice tasks should stay minimal")
    if not verify_gate:
        dev_concerns.append("verify gate missing; hard to keep deterministic feedback loop")
    dev_refs = ["steps_bounded", "queue_pressure", "verify_gate"]

    qa_concerns: list[str] = []
    if not verify_gate:
        qa_concerns.append("verify gate missing from quality contract")
    if not docs_gate:
        qa_concerns.append("docs freshness gate missing; regression in process docs likely")
    if not ready_passed:
        qa_concerns.append("ready gate missing; test baseline cannot be trusted")
    qa_refs = ["verify_gate", "docs_gate", "ready_gate"]

    roles: list[dict[str, Any]] = [
        {
            "role": "product",
            "independent_view": "Validate real user value and keep deliverable minimal before execution starts.",
            "decision": role_decision(status_by_id, product_refs, product_concerns),
            "concerns": product_concerns,
            "evidence_refs": product_refs,
        },
        {
            "role": "architect",
            "independent_view": "Verify lifecycle invariants, boundary clarity, and recoverability before build.",
            "decision": role_decision(status_by_id, architect_refs, architect_concerns),
            "concerns": architect_concerns,
            "evidence_refs": architect_refs,
        },
        {
            "role": "dev",
            "independent_view": "Keep implementation minimal, operable, and deterministic for fast iteration.",
            "decision": role_decision(status_by_id, dev_refs, dev_concerns),
            "concerns": dev_concerns,
            "evidence_refs": dev_refs,
        },
        {
            "role": "qa",
            "independent_view": "Independently enforce behavioral tests, failure paths, and documentation gates.",
            "decision": role_decision(status_by_id, qa_refs, qa_concerns),
            "concerns": qa_concerns,
            "evidence_refs": qa_refs,
        },
    ]

    decision_set = sorted({str(r["decision"]) for r in roles})
    disagreements: list[str] = []
    if len(decision_set) > 1:
        disagreements.append("role decisions are not uniform yet; arbiter must converge conditions.")
    warn_count = sum(1 for c in checks if c["status"] == "warn")
    block_count = sum(1 for c in checks if c["status"] == "block")
    if block_count:
        disagreements.append("blocking evidence checks exist and must be resolved before final execution.")
    elif warn_count:
        disagreements.append("warning-level concerns exist; execution must include guardrails.")

    created_at = datetime.now(timezone.utc).isoformat()
    obj: dict[str, Any] = {
        "project_id": project_id,
        "run_id": run_id,
        "created_at_utc": created_at,
        "source_contract": str(contract_json),
        "direction_title": title,
        "direction_goal": goal,
        "scope_hint": scope,
        "queue_open_items": queue_open_items,
        "evidence_summary": {
            "pass": sum(1 for c in checks if c["status"] == "pass"),
            "warn": warn_count,
            "block": block_count,
        },
        "evidence_checks": checks,
        "roles": roles,
        "disagreements": disagreements,
        "consensus_rule": "independent evidence review first, arbiter convergence second",
        "next_command": f"tools/ops arbiter RUN_ID={run_id}",
    }
    council_json.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Council Review (Discussion)",
        "",
        f"PROJECT_ID: `{project_id}`",
        f"RUN_ID: `{run_id}`",
        f"Generated At (UTC): {created_at}",
        f"Direction: {title}",
        f"Queue Open Items: {queue_open_items}",
        "",
        "## Evidence Checks",
    ]
    for c in checks:
        lines.append(f"- [{c['status']}] `{c['id']}`: {c['label']} | {c['detail']}")
    lines.extend(["", "## Independent Roles"])
    for role in roles:
        lines.append(f"- role: `{role['role']}`")
        lines.append(f"  - view: {role['independent_view']}")
        lines.append(f"  - decision: {role['decision']}")
        lines.append(f"  - evidence_refs: {', '.join(role['evidence_refs'])}")
        if role["concerns"]:
            lines.append("  - concerns:")
            for c in role["concerns"]:
                lines.append(f"    - {c}")
        else:
            lines.append("  - concerns: none")
    lines.extend(["", "## Disagreements"])
    if disagreements:
        for d in disagreements:
            lines.append(f"- {d}")
    else:
        lines.append("- none")
    lines.extend(["", "## Next Command", f"- `tools/ops arbiter RUN_ID={run_id}`", ""])
    council_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"COUNCIL_ROLES: {len(roles)}")
    print(f"COUNCIL_WARNINGS: {warn_count}")
    print(f"COUNCIL_BLOCKERS: {block_count}")
    print(f"COUNCIL_NEXT_COMMAND: tools/ops arbiter RUN_ID={run_id}")
    print(f"COUNCIL_PROJECT_ID: {project_id}")

    task_file = state_field_value("CURRENT_TASK_FILE")
    current_status = state_field_value("CURRENT_STATUS") or "active"
    append_execution_event(
        run_id,
        "council",
        "council_generated",
        "ok",
        f"tools/ops council RUN_ID={run_id}",
        f"choice_file={choice_file};council={council_json}",
        "",
    )
    append_conversation_checkpoint(run_id, "council", "council reviews generated; next step arbiter")
    update_state_current(run_id, task_file, current_status, project_id)
    print(f"COUNCIL_FILE_JSON: {council_json}")
    print(f"COUNCIL_FILE_MD: {council_md}")
    print(f"COUNCIL_PROJECT_ID: {project_id}")
    print(f"COUNCIL_RUN_ID: {run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
