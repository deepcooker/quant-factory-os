#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from tools.common_helpers import dedup_lines, normalize_scope, read_json
except Exception:  # pragma: no cover
    from common_helpers import dedup_lines, normalize_scope, read_json  # type: ignore
from ready import (
    append_conversation_checkpoint,
    append_execution_event,
    resolve_project_id_for_cmd,
    resolve_run_id_for_cmd,
    state_field_value,
    update_state_current,
)


@dataclass
class ArbiterContext:
    run_id: str
    project_id: str
    council_file: Path
    direction_contract: Path
    out_json: Path
    out_md: Path


# arbiter_tools_01 中文：解析 arbiter 的命令行参数。
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


# arbiter_tools_02 中文：根据 scope 推导本轮非目标。
def non_goals_from_scope(scope: list[str]) -> list[str]:
    base = [
        "不扩展到当前 selected direction 之外的其他流程层级",
        "不在本轮 contract 中引入新的业务项目范围",
        "不跳过 verify/review/docs freshness gate",
    ]
    if "tools/learn.py" in scope:
        base.append("不同时改造无关执行链脚本")
    if "tools/orient.py" in scope or "tools/council.py" in scope:
        base.append("不把 discussion artifacts 和 execution evidence 混写")
    return dedup_lines(base)


# 7001 中文：第一步，解析 arbiter 上下文并检查前置产物。
def arbiter_step_01_resolve_context(argv: list[str]) -> ArbiterContext:
    args = parse_args(argv)
    run_id = resolve_run_id_for_cmd(args["explicit_run_id"], "arbiter")
    if not run_id:
        print("ERROR: arbiter requires RUN_ID (explicit or TASKS/STATE.md CURRENT_RUN_ID).", file=sys.stderr)
        raise SystemExit(2)
    project_id = resolve_project_id_for_cmd(args["explicit_project_id"], "arbiter")

    council_file = Path(f"chatlogs/discussion/{run_id}/council.json")
    direction_contract = Path(f"reports/{run_id}/direction_contract.json")
    if not council_file.is_file():
        print("ERROR: council gate not satisfied.", file=sys.stderr)
        print(f"Run: python3 tools/council.py RUN_ID={run_id}", file=sys.stderr)
        print(f"Then: python3 tools/arbiter.py RUN_ID={run_id}", file=sys.stderr)
        raise SystemExit(1)
    if not direction_contract.is_file():
        print(f"ERROR: missing direction contract: {direction_contract}", file=sys.stderr)
        print(f"Run: python3 tools/choose.py RUN_ID={run_id} OPTION=<id>", file=sys.stderr)
        raise SystemExit(1)

    out_json = Path(f"reports/{run_id}/execution_contract.json")
    out_md = Path(f"reports/{run_id}/execution_contract.md")
    out_json.parent.mkdir(parents=True, exist_ok=True)
    return ArbiterContext(run_id, project_id, council_file, direction_contract, out_json, out_md)


# 7002 中文：第二步，收敛 council 评审并生成 execution contract。
def arbiter_step_02_build_contract(context: ArbiterContext) -> ArbiterContext:
    direction = read_json(str(context.direction_contract))
    council = read_json(str(context.council_file))

    scope = normalize_scope(direction.get("scope_hint"))
    if not scope:
        scope = ["tools/*.py", "tests/", "docs/WORKFLOW.md", "AGENTS.md", "TASKS/", "reports/{RUN_ID}/"]

    title = str(direction.get("selected_title", "")).strip() or "confirmed direction"
    goal = str(direction.get("execution_goal", "")).strip() or "Deliver the confirmed direction with minimal safe tasks."
    priority = str(direction.get("priority", "")).strip()
    selected_option = str(direction.get("selected_option", "")).strip()

    checks = council.get("evidence_checks") or []
    if not isinstance(checks, list):
        checks = []
    roles = council.get("roles") or []
    if not isinstance(roles, list):
        roles = []
    disagreements = council.get("disagreements") or []
    if not isinstance(disagreements, list):
        disagreements = []

    blockers = [c for c in checks if isinstance(c, dict) and c.get("status") == "block"]
    warnings = [c for c in checks if isinstance(c, dict) and c.get("status") == "warn"]
    role_conditions: list[str] = []
    for role in roles:
        if not isinstance(role, dict):
            continue
        role_name = str(role.get("role", "role")).strip() or "role"
        concerns = role.get("concerns") or []
        if not isinstance(concerns, list):
            continue
        for concern in concerns:
            text = str(concern).strip()
            if text:
                role_conditions.append(f"{role_name}: {text}")
    role_conditions = dedup_lines(role_conditions)

    acceptance = [
        f"deliver selected direction option `{selected_option or 'unknown'}` with bounded scope",
        "command(s) pass: make verify",
        "reports summary/decision updated for this run",
        "owner docs updated in same run when behavior/rules changed",
    ]
    if blockers or warnings or role_conditions:
        concern_acceptance: list[str] = []
        for c in role_conditions[:5]:
            concern_acceptance.append(f"condition closed: {c}")
        if blockers:
            concern_acceptance.append("all blocker-level evidence checks are resolved")
        if warnings:
            concern_acceptance.append("warning-level checks are either resolved or explicitly accepted in decision.md")
        acceptance.extend(concern_acceptance or ["no open council conditions"])
    else:
        acceptance.extend(
            [
                "critical path regression tests added or refreshed",
                "failure-path assertions are explicit and actionable",
            ]
        )
    acceptance.append("bash tools/legacy.sh review STRICT=1 AUTO_FIX=1 passes")
    acceptance.append("decision records accepted tradeoffs and residual risks")

    created_at = datetime.now(timezone.utc).isoformat()
    obj: dict[str, Any] = {
        "project_id": context.project_id,
        "run_id": context.run_id,
        "created_at_utc": created_at,
        "direction": {
            "selected_option": selected_option,
            "selected_title": title,
            "goal": goal,
            "priority": priority,
        },
        "execution_goal": goal,
        "non_goals": non_goals_from_scope(scope),
        "scope": scope,
        "acceptance": dedup_lines(acceptance),
        "council_source": str(context.council_file),
        "arbiter_rule": "converge independent evidence-based reviews into one executable contract",
        "arbiter_summary": {
            "blockers": len(blockers),
            "warnings": len(warnings),
            "role_conditions": len(role_conditions),
            "disagreements": len(disagreements),
        },
        "blockers": blockers,
        "warnings": warnings,
        "role_conditions": role_conditions,
        "next_command": f"python3 tools/slice_task.py RUN_ID={context.run_id}",
    }
    context.out_json.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Execution Contract",
        "",
        f"PROJECT_ID: `{context.project_id}`",
        f"RUN_ID: `{context.run_id}`",
        f"Generated At (UTC): {created_at}",
        f"Direction: {title}",
        f"Arbiter Summary: blockers={len(blockers)} warnings={len(warnings)} conditions={len(role_conditions)}",
        "",
        "## Convergence Input",
    ]
    if role_conditions:
        for c in role_conditions:
            lines.append(f"- {c}")
    else:
        lines.append("- no unresolved role conditions")
    if disagreements:
        lines.append("")
        lines.append("## Disagreements")
        for d in disagreements:
            lines.append(f"- {d}")
    lines.extend(["", "## Execution Goal", f"- {goal}", "", "## Non Goals"])
    for item in obj["non_goals"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Scope"])
    for item in scope:
        lines.append(f"- `{item}`")
    lines.extend(["", "## Acceptance"])
    for item in obj["acceptance"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Command", f"- `python3 tools/slice_task.py RUN_ID={context.run_id}`", ""])
    context.out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"ARBITER_BLOCKERS: {len(blockers)}")
    print(f"ARBITER_WARNINGS: {len(warnings)}")
    print(f"ARBITER_NEXT_COMMAND: python3 tools/slice_task.py RUN_ID={context.run_id}")
    print(f"ARBITER_PROJECT_ID: {context.project_id}")
    return context


# 7003 中文：第三步，记录 arbiter 证据并打印结果。
def arbiter_step_03_finalize(context: ArbiterContext) -> int:
    task_file = state_field_value("CURRENT_TASK_FILE")
    current_status = state_field_value("CURRENT_STATUS") or "active"
    append_execution_event(
        context.run_id,
        "arbiter",
        "arbiter_generated",
        "ok",
        f"python3 tools/arbiter.py RUN_ID={context.run_id}",
        f"council_file={context.council_file};execution_contract={context.out_json}",
        "",
    )
    append_conversation_checkpoint(context.run_id, "arbiter", "execution contract generated; next step slice")
    update_state_current(context.run_id, task_file, current_status, context.project_id)
    print(f"EXECUTION_CONTRACT_JSON: {context.out_json}")
    print(f"EXECUTION_CONTRACT_MD: {context.out_md}")
    print(f"ARBITER_PROJECT_ID: {context.project_id}")
    print(f"ARBITER_RUN_ID: {context.run_id}")
    return 0


# 7004 中文：执行 arbiter 主流程，main 只负责分发三个业务步骤。
def main(argv: list[str]) -> int:
    context = arbiter_step_01_resolve_context(argv)
    context = arbiter_step_02_build_contract(context)
    return arbiter_step_03_finalize(context)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
