#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from tools.common_helpers import dedup_acceptance
except Exception:  # pragma: no cover
    from common_helpers import dedup_acceptance  # type: ignore
from ready import (
    append_conversation_checkpoint,
    append_execution_event,
    resolve_project_id_for_cmd,
    resolve_run_id_for_cmd,
    state_field_value,
    update_state_current,
)


@dataclass
class SliceContext:
    run_id: str
    project_id: str
    execution_contract: Path
    queue_file: Path
    out_json: Path


# slice_tools_01 中文：解析 slice_task 的命令行参数。
def parse_args(argv: list[str]) -> dict[str, str]:
    explicit_run_id = ""
    explicit_project_id = os.environ.get("QF_PROJECT_ID", os.environ.get("PROJECT_ID", ""))
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
    if not explicit_run_id and os.environ.get("RUN_ID"):
        explicit_run_id = os.environ["RUN_ID"]
    return {"explicit_run_id": explicit_run_id, "explicit_project_id": explicit_project_id}


# slice_tools_02 中文：加载 execution contract。
def load_contract(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


# slice_tools_03 中文：根据 contract 自动生成最小任务切片。
def build_tasks_from_contract(contract: dict[str, Any]) -> list[dict[str, Any]]:
    direction = contract.get("direction") or {}
    title = str(direction.get("selected_title", "")).strip() or "execution contract"
    goal = str(contract.get("execution_goal", "")).strip() or str(direction.get("goal", "")).strip() or "Execute the selected direction."
    scope = contract.get("scope") or []
    if not isinstance(scope, list):
        scope = []
    scope = [str(x).strip().replace("`", "") for x in scope if str(x).strip()]
    if not scope:
        scope = ["tools/*.py", "tests/", "docs/WORKFLOW.md", "AGENTS.md", "TASKS/", "reports/{RUN_ID}/"]

    acceptance = contract.get("acceptance") or []
    if not isinstance(acceptance, list):
        acceptance = []
    acceptance = [str(x).strip() for x in acceptance if str(x).strip()]

    blockers = contract.get("blockers") or []
    warnings = contract.get("warnings") or []
    role_conditions = contract.get("role_conditions") or []
    if not isinstance(role_conditions, list):
        role_conditions = []

    tasks: list[dict[str, Any]] = [
        {
            "task_id": "slice-1",
            "title": f"{title} - core delivery",
            "goal": goal,
            "scope": scope,
            "acceptance": acceptance or [
                "deliver selected direction with bounded scope",
                "command(s) pass: make verify",
                "reports summary/decision updated for this run",
            ],
        }
    ]

    if blockers or warnings or role_conditions:
        concern_acceptance: list[str] = []
        for item in role_conditions[:5]:
            concern_acceptance.append(f"condition closed: {item}")
        if blockers:
            concern_acceptance.append("all blocker-level evidence checks are resolved")
        if warnings:
            concern_acceptance.append("warning-level checks are either resolved or explicitly accepted in decision.md")
        tasks.append(
            {
                "task_id": "slice-2",
                "title": f"{title} - close council conditions",
                "goal": "Resolve cross-role concerns raised by council before or during execution.",
                "scope": list(dict.fromkeys(scope + ["reports/{RUN_ID}/"])),
                "acceptance": concern_acceptance or ["no open council conditions"],
            }
        )

    return tasks


# 8001 中文：第一步，解析 slice 上下文并检查 execution contract。
def slice_step_01_resolve_context(argv: list[str]) -> SliceContext:
    args = parse_args(argv)
    run_id = resolve_run_id_for_cmd(args["explicit_run_id"], "slice")
    if not run_id:
        print("ERROR: slice requires RUN_ID (explicit or TASKS/STATE.md CURRENT_RUN_ID).", file=sys.stderr)
        raise SystemExit(2)
    project_id = resolve_project_id_for_cmd(args["explicit_project_id"], "slice")

    execution_contract = Path(f"reports/{run_id}/execution_contract.json")
    if not execution_contract.is_file():
        print("ERROR: execution-contract gate not satisfied.", file=sys.stderr)
        print(f"Run: python3 tools/arbiter.py RUN_ID={run_id}", file=sys.stderr)
        print(f"Then: python3 tools/slice_task.py RUN_ID={run_id}", file=sys.stderr)
        print("Then retry: bash tools/legacy.sh do queue-next", file=sys.stderr)
        raise SystemExit(1)
    return SliceContext(run_id, project_id, execution_contract, Path("TASKS/QUEUE.md"), Path(f"reports/{run_id}/slice_state.json"))


# 8002 中文：第二步，把 execution contract 切成 queue 任务并写入 slice_state。
def slice_step_02_build_queue(context: SliceContext) -> tuple[SliceContext, int, int, int]:
    contract = load_contract(context.execution_contract)
    tasks = contract.get("tasks") or []
    if not isinstance(tasks, list) or not tasks:
        tasks = build_tasks_from_contract(contract)

    if context.queue_file.exists():
        text = context.queue_file.read_text(encoding="utf-8")
    else:
        text = "# QUEUE\n\n## Queue\n\n"
    lines = text.splitlines()
    if not lines:
        lines = ["# QUEUE", "", "## Queue", ""]

    try:
        queue_idx = next(i for i, line in enumerate(lines) if line.strip() == "## Queue")
    except StopIteration:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(["## Queue", ""])
        queue_idx = len(lines) - 2

    insert_at = queue_idx + 1
    while insert_at < len(lines) and lines[insert_at].strip() == "":
        insert_at += 1

    existing = 0
    inserted = 0
    blocks: list[list[str]] = []
    for raw in tasks:
        if not isinstance(raw, dict):
            continue
        task_id = str(raw.get("task_id", "")).strip() or f"slice-{len(blocks) + 1}"
        title = str(raw.get("title", "")).strip() or f"Slice task {task_id}"
        goal = str(raw.get("goal", "")).strip() or "Execute task slice."
        scope = raw.get("scope") or []
        if not isinstance(scope, list):
            scope = []
        scope = [str(x).strip().replace("`", "") for x in scope if str(x).strip()]
        if not scope:
            scope = ["tools/*.py", "tests/", "docs/WORKFLOW.md", "AGENTS.md", "TASKS/", "reports/{RUN_ID}/"]
        scope_line = ", ".join(f"`{x}`" for x in scope)
        acceptance = raw.get("acceptance") or []
        if not isinstance(acceptance, list):
            acceptance = []
        acceptance = [str(x).strip() for x in acceptance if str(x).strip()]
        if not acceptance:
            acceptance = ["slice acceptance placeholder"]
        normalized = [a.lower().replace("`", "") for a in acceptance]
        if not any("make verify" in a or "command(s) pass" in a for a in normalized):
            acceptance.append("Command(s) pass: `make verify`")
        if not any("summary.md" in a or "decision.md" in a or "evidence updated" in a for a in normalized):
            acceptance.append("Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`")
        acceptance = dedup_acceptance(acceptance)

        marker = f"Slice: run_id={run_id} task_id={task_id}"
        if marker in text:
            existing += 1
            continue
        inserted += 1
        block = [
            f"- [ ] TODO Title: slice-next: {title}",
            f"  Goal: {goal}",
            f"  Scope: {scope_line}",
            "  Acceptance:",
        ]
        for a in acceptance:
            block.append(f"  - [ ] {a}")
        block.append(f"  {marker}")
        block.append("")
        blocks.append(block)

    if blocks:
        flat: list[str] = []
        for block in blocks:
            flat.extend(block)
        lines = lines[:insert_at] + flat + lines[insert_at:]
        context.queue_file.parent.mkdir(parents=True, exist_ok=True)
        context.queue_file.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    state = {
        "project_id": context.project_id,
        "run_id": context.run_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_contract": str(context.execution_contract),
        "tasks_total": len(tasks),
        "queue_inserted": inserted,
        "queue_existing": existing,
        "next_command": "bash tools/legacy.sh do queue-next",
    }
    context.out_json.parent.mkdir(parents=True, exist_ok=True)
    context.out_json.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"SLICE_TASKS_TOTAL: {len(tasks)}")
    print(f"SLICE_QUEUE_INSERTED: {inserted}")
    print(f"SLICE_QUEUE_EXISTING: {existing}")
    print("SLICE_NEXT_COMMAND: bash tools/legacy.sh do queue-next")
    print(f"SLICE_PROJECT_ID: {context.project_id}")
    return context, len(tasks), inserted, existing


# 8003 中文：第三步，记录 slice 证据并打印结果。
def slice_step_03_finalize(context: SliceContext, tasks_total: int, inserted: int, existing: int) -> int:
    task_file = state_field_value("CURRENT_TASK_FILE")
    current_status = state_field_value("CURRENT_STATUS") or "active"
    append_execution_event(
        context.run_id,
        "slice",
        "slice_generated",
        "ok",
        f"python3 tools/slice_task.py RUN_ID={context.run_id}",
        f"execution_contract={context.execution_contract};slice_state={context.out_json}",
        "",
    )
    append_conversation_checkpoint(context.run_id, "slice", "execution contract sliced into queue tasks; next step do")
    update_state_current(context.run_id, task_file, current_status, context.project_id)
    print(f"SLICE_STATE_FILE: {context.out_json}")
    print(f"SLICE_QUEUE_FILE: {context.queue_file}")
    print(f"SLICE_PROJECT_ID: {context.project_id}")
    print(f"SLICE_RUN_ID: {context.run_id}")
    return 0


# 8004 中文：执行 slice 主流程，main 只负责分发三个业务步骤。
def main(argv: list[str]) -> int:
    context = slice_step_01_resolve_context(argv)
    context, tasks_total, inserted, existing = slice_step_02_build_queue(context)
    return slice_step_03_finalize(context, tasks_total, inserted, existing)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
