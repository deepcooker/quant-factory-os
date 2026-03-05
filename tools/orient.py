#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ready import (
    append_conversation_checkpoint,
    append_execution_event,
    read_text,
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
        explicit_run_id = os.environ.get("RUN_ID", "")
    if not explicit_project_id:
        explicit_project_id = os.environ.get("QF_PROJECT_ID", os.environ.get("PROJECT_ID", ""))
    return {"explicit_run_id": explicit_run_id, "explicit_project_id": explicit_project_id}


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
        f"reports/{run_id}/ready.json",
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


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    run_id = resolve_run_id_for_cmd(args["explicit_run_id"], "orient")
    if not run_id:
        print("ERROR: orient requires RUN_ID (explicit or TASKS/STATE.md CURRENT_RUN_ID).", file=sys.stderr)
        return 2
    project_id = resolve_project_id_for_cmd(args["explicit_project_id"], "orient")

    task_file = state_field_value("CURRENT_TASK_FILE")
    current_status = state_field_value("CURRENT_STATUS") or "active"

    orient_file = f"chatlogs/discussion/{run_id}/orient.json"
    orient_md = f"chatlogs/discussion/{run_id}/orient.md"
    Path(f"chatlogs/discussion/{run_id}").mkdir(parents=True, exist_ok=True)
    try:
        generate_orient_draft(run_id, project_id, task_file, orient_file, orient_md)
    except Exception:
        print("ERROR: orient generation failed.", file=sys.stderr)
        return 1

    append_execution_event(
        run_id,
        "orient",
        "orient_generated",
        "ok",
        f"python3 tools/orient.py RUN_ID={run_id}",
        f"orient_file={orient_file};orient_md={orient_md}",
        "",
    )
    append_conversation_checkpoint(
        run_id,
        "orient",
        "orientation draft updated in chatlogs/discussion; recommended option ready for choose",
    )
    update_state_current(run_id, task_file, current_status, project_id)
    print(f"ORIENT_FILE: {orient_file}")
    print(f"ORIENT_MD: {orient_md}")
    print(f"ORIENT_PROJECT_ID: {project_id}")
    print(f"ORIENT_RUN_ID: {run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
