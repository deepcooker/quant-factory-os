#!/usr/bin/env python3
from __future__ import annotations

import json
import os
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


def read_json(path: str) -> dict[str, Any]:
    p = Path(path)
    if not p.is_file():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def split_scope(scope_text: str) -> list[str]:
    out: list[str] = []
    for raw in str(scope_text).split(","):
        item = raw.strip().replace("`", "")
        if item:
            out.append(item)
    return out


def short_text(text: str, limit: int = 140) -> str:
    s = " ".join(str(text).split())
    if len(s) <= limit:
        return s
    return s[: limit - 3].rstrip() + "..."


def generate_orient_draft(run_id: str, project_id: str, task_file: str, orient_file: str, orient_md: str) -> None:
    ready_obj = read_json(f"reports/{run_id}/ready.json")
    summary_text = read_text(f"reports/{run_id}/summary.md")
    decision_text = read_text(f"reports/{run_id}/decision.md")
    state_text = read_text("TASKS/STATE.md")
    queue_text = read_text("TASKS/QUEUE.md")
    learn_obj = read_json(f"learn/{project_id}.json")

    contract = ready_obj.get("contract") or {}
    goal = str(contract.get("goal", "")).strip()
    acceptance = str(contract.get("acceptance", "")).strip()
    scope_hint = split_scope(str(contract.get("scope", "")).strip())
    if not scope_hint:
        scope_hint = ["tools/*.py", "tests/", "docs/", "TASKS/", "reports/"]

    open_items = queue_text.count("- [ ] ")
    learn_focus = ""
    model_sync = learn_obj.get("model_sync") if isinstance(learn_obj, dict) else {}
    if isinstance(model_sync, dict):
        result = model_sync.get("result") or {}
        if isinstance(result, dict):
            oral_summary = result.get("oral_summary") or {}
            if isinstance(oral_summary, dict):
                learn_focus = str(oral_summary.get("current_focus", "")).strip()
    if not learn_focus:
        learn_focus = "继续围绕当前 active run 收敛 learn 主线、流程边界和日常使用体验。"

    summary_lower = summary_text.lower()
    decision_lower = decision_text.lower()
    ready_lower = f"{goal} {acceptance}".lower()

    directions: list[dict[str, Any]] = []

    directions.append(
        {
            "id": "learn-daily-ergonomics",
            "title": "P0: 收敛 learn 的日常同频体验",
            "why": short_text(
                f"当前 ready 合同和 run 证据都把重点放在 learn 主线、PROJECT_GUIDE 驱动和流程降噪；下一轮最合理的方向是继续压输出噪音并稳住日常使用体验。"
            ),
            "risk": "如果只追求更短输出，可能削弱主线回拉和证据覆盖。",
            "scope_hint": ["tools/learn.py", "docs/PROJECT_GUIDE.md", "docs/WORKFLOW.md", "AGENTS.md"],
        }
    )

    directions.append(
        {
            "id": "discussion-chain-hardening",
            "title": "P1: 继续收敛讨论链边界",
            "why": short_text(
                "当前 run 已经把 ready 收成纯门禁、orient 从 ready 解耦；下一步自然是继续把 orient/choose/council/arbiter/slice 的对象边界和输出责任彻底理顺。"
            ),
            "risk": "如果只改边界不验证链路，可能出现流程看起来更清楚但真实执行断链。",
            "scope_hint": ["tools/orient.py", "tools/choose.py", "tools/council.py", "tools/arbiter.py", "tools/slice_task.py", "docs/WORKFLOW.md", "docs/ENTITIES.md"],
        }
    )

    directions.append(
        {
            "id": "execution-path-ergonomics",
            "title": "P2: 收敛执行链的人体工学",
            "why": short_text(
                "如果当前重点从讨论边界转向真正落地，那么最值得做的是把 do/review/ship 的提示、失败恢复和证据更新体验继续压顺。"
            ),
            "risk": "若过早进入执行链优化，可能掩盖讨论层对象模型仍未完全稳定的问题。",
            "scope_hint": ["tools/legacy.sh", "tools/task.sh", "tools/ship.sh", "docs/WORKFLOW.md", "reports/"],
        }
    )

    if "orient" in ready_lower or "council" in ready_lower or "arbiter" in ready_lower:
        directions[1]["why"] = short_text(
            "当前合同已经明确讨论链是下一阶段重点，所以优先方向应是继续把 orient/choose/council/arbiter/slice 的输入输出和状态边界彻底做稳。"
        )
    if "learn" in ready_lower or "project_guide" in ready_lower or "主线" in goal:
        directions[0]["why"] = short_text(
            f"当前合同直接把 learn 和 PROJECT_GUIDE 同频列为增量重点；结合最新 learn focus，下一步最合理的是继续收敛强同频输出和主线回拉体验：{learn_focus}"
        )
    if "ship" in summary_lower or "review" in decision_lower or "verify" in ready_lower:
        directions[2]["why"] = short_text(
            "当前证据已经反复触及 verify/review/ship 约束；如果要往执行层推进，最合理的是优先压顺执行链的人体工学与失败恢复。"
        )

    recommended_idx = 0
    if "learn" in ready_lower or "project_guide" in ready_lower or "主线" in goal:
        recommended_idx = 0
    elif "orient" in ready_lower or "council" in ready_lower or "arbiter" in ready_lower:
        recommended_idx = 1
    elif "ship" in ready_lower or "verify" in ready_lower or open_items > 3:
        recommended_idx = 2

    for idx, item in enumerate(directions):
        item["priority_rank"] = idx + 1
        item["priority"] = f"P{idx}"
        item["recommended"] = idx == recommended_idx

    recommended = directions[recommended_idx]["id"] if directions else ""
    next_cmd = f"python3 tools/choose.py RUN_ID={run_id} OPTION={recommended}" if recommended else f"python3 tools/choose.py RUN_ID={run_id} OPTION=<id>"
    obj = {
        "project_id": project_id,
        "run_id": run_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "discussion_mode": True,
        "task_file": task_file,
        "open_queue_items": open_items,
        "inputs": [
            "reports/<RUN_ID>/ready.json",
            "TASKS/STATE.md",
            "TASKS/QUEUE.md",
            "reports/<RUN_ID>/summary.md",
            "reports/<RUN_ID>/decision.md",
            "learn/<PROJECT_ID>.json",
        ],
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
        lines.append(f"- id=`{item['id']}` | priority=`{item['priority']}` | recommended=`{str(item['recommended']).lower()}`")
        lines.append(f"  - title: {item['title']}")
        lines.append(f"  - why: {item['why']}")
        lines.append(f"  - risk: {item['risk']}")
        lines.append(f"  - scope_hint: {', '.join(item['scope_hint'])}")
    lines.extend(["", "## Recommended", f"- `{recommended}`", "", "## Next Command", f"- `{next_cmd}`", ""])
    Path(orient_md).write_text("\n".join(lines), encoding="utf-8")

    print(f"ORIENT_OPTIONS: {len(directions)}")
    for idx, item in enumerate(directions[:3], start=1):
        print(
            f"ORIENT_OPTION_{idx}: id={item['id']} | priority={item['priority']} | "
            f"recommended={str(item['recommended']).lower()} | risk={item['risk']}"
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
