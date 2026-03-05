#!/usr/bin/env python3
from __future__ import annotations

import json
import os
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


def resolve_orient_file_for_run(run_id: str) -> str:
    if not run_id:
        return ""
    draft_file = Path(f"chatlogs/discussion/{run_id}/orient.json")
    if draft_file.is_file():
        return str(draft_file)
    legacy_file = Path(f"reports/{run_id}/orient.json")
    if legacy_file.is_file():
        return str(legacy_file)
    return ""


def parse_args(argv: list[str]) -> dict[str, str]:
    explicit_run_id = ""
    explicit_project_id = os.environ.get("QF_PROJECT_ID", os.environ.get("PROJECT_ID", ""))
    option = os.environ.get("QF_ORIENT_OPTION", "")
    for token in argv:
        if not token:
            continue
        if token.startswith("RUN_ID="):
            explicit_run_id = token.split("=", 1)[1]
        elif token.startswith("PROJECT_ID="):
            explicit_project_id = token.split("=", 1)[1]
        elif token.startswith("OPTION="):
            option = token.split("=", 1)[1]
        else:
            if not option:
                option = token
    if not explicit_run_id and os.environ.get("RUN_ID"):
        explicit_run_id = os.environ["RUN_ID"]
    return {"explicit_run_id": explicit_run_id, "explicit_project_id": explicit_project_id, "option": option}


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    run_id = resolve_run_id_for_cmd(args["explicit_run_id"], "choose")
    if not run_id:
        print("ERROR: choose requires RUN_ID (explicit or TASKS/STATE.md CURRENT_RUN_ID).", file=sys.stderr)
        return 2
    project_id = resolve_project_id_for_cmd(args["explicit_project_id"], "choose")
    option = args["option"].strip()

    orient_file = resolve_orient_file_for_run(run_id)
    choice_file = Path(f"reports/{run_id}/orient_choice.json")
    contract_json = Path(f"reports/{run_id}/direction_contract.json")
    contract_md = Path(f"reports/{run_id}/direction_contract.md")
    if not orient_file or not Path(orient_file).is_file():
        print(f"ERROR: missing orientation file for run: {run_id}", file=sys.stderr)
        print(f"Run: tools/ops orient RUN_ID={run_id}", file=sys.stderr)
        return 1

    obj = json.loads(Path(orient_file).read_text(encoding="utf-8"))
    directions = obj.get("directions", [])
    if not directions:
        print("ERROR: orient report has no direction options.", file=sys.stderr)
        return 1

    ids: dict[str, dict[str, Any]] = {x.get("id"): x for x in directions if isinstance(x, dict) and x.get("id")}
    selected = option or str(obj.get("recommended_option", "")).strip()
    if selected not in ids:
        known = ", ".join(sorted(ids))
        print(f"ERROR: invalid OPTION={selected!r}. valid: {known}", file=sys.stderr)
        return 1

    picked = ids[selected]
    scope_hint = picked.get("scope_hint", [])
    if not isinstance(scope_hint, list):
        scope_hint = []
    role_reviews = [
        {
            "role": "product",
            "focus": "value and scope relevance",
            "independent_view": "确认方向是否解决真实问题，并限制在最小可交付范围内。",
            "must_hold": ["目标可验证", "非目标明确", "不做伪需求扩张"],
        },
        {
            "role": "architect",
            "focus": "boundary and extensibility",
            "independent_view": "检查状态机边界、证据边界、兼容迁移路径是否明确。",
            "must_hold": ["讨论态与执行态边界清晰", "旧流程兼容/迁移说明完整", "失败可恢复"],
        },
        {
            "role": "dev",
            "focus": "minimal diff and operability",
            "independent_view": "优先小步改动，确保命令链可重复执行并便于调试。",
            "must_hold": ["最小差异实现", "命令输出可操作", "错误提示可恢复"],
        },
        {
            "role": "qa",
            "focus": "behavioral regression and gates",
            "independent_view": "独立验证门禁和回归，不受开发路径影响。",
            "must_hold": ["关键路径有回归测试", "失败路径有断言", "文档门禁可验证"],
        },
    ]

    created_at = datetime.now(timezone.utc).isoformat()
    contract = {
        "project_id": project_id,
        "run_id": obj.get("run_id"),
        "created_at_utc": created_at,
        "selected_option": selected,
        "selected_title": picked.get("title", ""),
        "execution_goal": picked.get("why", ""),
        "scope_hint": scope_hint,
        "priority": picked.get("priority", ""),
        "delivery_contract": {
            "steps": [
                "council-review",
                "arbiter-contract",
                "slice-into-tasks",
                "implement",
                "verify",
                "review-and-align",
                "reports-and-ship",
            ],
            "quality_gates": [
                "make verify green",
                "scope remains bounded",
                "owner docs updated in same run",
                "reports evidence updated",
            ],
        },
        "role_reviews": role_reviews,
        "next_command": f"tools/ops council RUN_ID={obj.get('run_id') or ''}",
    }
    out = {
        "project_id": project_id,
        "run_id": obj.get("run_id"),
        "created_at_utc": created_at,
        "selected_option": selected,
        "selected_title": picked.get("title", ""),
        "priority": picked.get("priority", ""),
        "reason": picked.get("why", ""),
        "source_orient_file": orient_file,
        "discussion_confirmed": True,
        "contract_json": str(contract_json),
        "contract_md": str(contract_md),
        "next_command": f"tools/ops council RUN_ID={obj.get('run_id')}",
    }
    choice_file.parent.mkdir(parents=True, exist_ok=True)
    choice_file.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    contract_json.write_text(json.dumps(contract, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = [
        "# Direction Contract",
        "",
        f"PROJECT_ID: `{project_id}`",
        f"RUN_ID: `{out.get('run_id', '')}`",
        f"Generated At (UTC): {created_at}",
        f"Selected Option: `{selected}`",
        f"Title: {picked.get('title', '')}",
        "",
        "## Why",
        f"- {picked.get('why', '')}",
        "",
        "## Scope Hint",
    ]
    if scope_hint:
        for x in scope_hint:
            lines.append(f"- `{x}`")
    else:
        lines.append("- `(empty)`")
    lines.extend(["", "## Multi-Role Independent Reviews"])
    for rv in role_reviews:
        lines.append(f"- role: `{rv['role']}` | focus: {rv['focus']}")
        lines.append(f"  - view: {rv['independent_view']}")
        lines.append("  - must_hold:")
        for gate in rv["must_hold"]:
            lines.append(f"    - {gate}")
    lines.extend(["", "## Delivery Contract"])
    for st in contract["delivery_contract"]["steps"]:
        lines.append(f"- step: {st}")
    for gate in contract["delivery_contract"]["quality_gates"]:
        lines.append(f"- gate: {gate}")
    lines.extend(["", "## Next Command", f"- `tools/ops council RUN_ID={obj.get('run_id')}`", ""])
    contract_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"CHOOSE_OPTION: {selected}")
    print(f"CHOOSE_TITLE: {picked.get('title', '')}")
    print(f"CHOOSE_NEXT_COMMAND: tools/ops council RUN_ID={obj.get('run_id')}")
    print(f"CHOOSE_CONTRACT_JSON: {contract_json}")
    print(f"CHOOSE_CONTRACT_MD: {contract_md}")
    print(f"CHOOSE_PROJECT_ID: {project_id}")

    task_file = state_field_value("CURRENT_TASK_FILE")
    current_status = state_field_value("CURRENT_STATUS") or "active"
    append_execution_event(
        run_id,
        "orient",
        "orient_chosen",
        "ok",
        f"tools/ops choose RUN_ID={run_id} OPTION={option}",
        f"choice_file={choice_file};contract={contract_json}",
        "",
    )
    append_conversation_checkpoint(run_id, "choose", "direction selected and contract written; next step council")
    update_state_current(run_id, task_file, current_status, project_id)
    print(f"CHOOSE_FILE: {choice_file}")
    print(f"CHOOSE_CONTRACT_JSON: {contract_json}")
    print(f"CHOOSE_CONTRACT_MD: {contract_md}")
    print(f"CHOOSE_PROJECT_ID: {project_id}")
    print(f"CHOOSE_RUN_ID: {run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
