#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from tools.project_config import load_project_config_json, save_project_config_json, update_runtime_state
except Exception:  # pragma: no cover
    from project_config import load_project_config_json, save_project_config_json, update_runtime_state  # type: ignore


REPO_ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = REPO_ROOT / "TASKS"


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _resolve_repo_path(raw_path: str) -> Path:
    candidate = Path(str(raw_path).strip())
    if candidate.is_absolute():
        return candidate
    return REPO_ROOT / candidate


def get_task_registry() -> dict[str, Any]:
    config = load_project_config_json()
    return dict(config.get("task_registry", {}) or {})


def get_runtime_state() -> dict[str, Any]:
    config = load_project_config_json()
    return dict(config.get("runtime_state", {}) or {})


def get_queue_path() -> Path:
    registry = get_task_registry()
    raw_path = str(registry.get("queue_json_file", "TASKS/QUEUE.json")).strip()
    return _resolve_repo_path(raw_path)


def load_queue() -> dict[str, Any]:
    return _read_json(get_queue_path())


def save_queue(payload: dict[str, Any]) -> None:
    path = get_queue_path()
    payload["updated_at"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(value: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", str(value).strip().lower()).strip("-")
    return text or "task"


def load_task(task_json_file: str) -> dict[str, Any]:
    return _read_json(_resolve_repo_path(task_json_file))


def save_task(task_json_file: str, payload: dict[str, Any]) -> None:
    path = _resolve_repo_path(task_json_file)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def get_active_task_path() -> Path:
    runtime_state = get_runtime_state()
    task_json_file = str(runtime_state.get("current_task_json_file", "")).strip()
    if task_json_file:
        return _resolve_repo_path(task_json_file)
    registry = get_task_registry()
    fallback = str(registry.get("active_task_json_file", "")).strip()
    if not fallback:
        raise FileNotFoundError("active task json file is not configured")
    return _resolve_repo_path(fallback)


def load_active_task() -> dict[str, Any]:
    return _read_json(get_active_task_path())


def set_active_task(task_json_file: str, task_id: str, task_md_file: str, run_id: str, status: str = "active") -> None:
    config = load_project_config_json()
    task_registry = config.setdefault("task_registry", {})
    task_registry["active_task_json_file"] = task_json_file
    save_project_config_json(config)
    required = dict(config.get("required", {}) or {})
    project_id = str(required.get("project_id", config.get("project_id", ""))).strip()
    update_runtime_state(project_id, run_id, task_md_file, status, task_id, task_json_file)


def find_queue_item_by_run_id(run_id: str) -> dict[str, Any] | None:
    for item in list(load_queue().get("items", []) or []):
        if str(item.get("run_id", "")).strip() == run_id:
            return dict(item)
    return None


def find_next_open_queue_item() -> dict[str, Any] | None:
    for item in list(load_queue().get("items", []) or []):
        status = str(item.get("status", "")).strip().lower()
        if status in {"pending", "open", ""}:
            return dict(item)
    return None


def mark_queue_item_status(queue_id: str, status: str, picked_at: str | None = None) -> dict[str, Any]:
    queue_payload = load_queue()
    for item in list(queue_payload.get("items", []) or []):
        if str(item.get("queue_id", "")).strip() != queue_id:
            continue
        item["status"] = status
        item["picked_at"] = picked_at
        save_queue(queue_payload)
        return dict(item)
    raise KeyError(f"queue_id not found: {queue_id}")


def append_queue_item(item: dict[str, Any]) -> dict[str, Any]:
    queue_payload = load_queue()
    items = list(queue_payload.get("items", []) or [])
    queue_id = str(item.get("queue_id", "")).strip()
    if queue_id and any(str(existing.get("queue_id", "")).strip() == queue_id for existing in items):
        raise ValueError(f"queue_id already exists: {queue_id}")
    items.append(item)
    queue_payload["items"] = items
    save_queue(queue_payload)
    return item


def task_paths_for_slug(slug: str) -> tuple[str, str]:
    task_json_file = f"TASKS/TASK-{slug}.json"
    task_md_file = f"TASKS/TASK-{slug}.md"
    return task_json_file, task_md_file


def find_task_id_for_run(run_id: str) -> str:
    runtime_state = get_runtime_state()
    if str(runtime_state.get("current_run_id", "")).strip() == run_id:
        current_task_id = str(runtime_state.get("current_task_id", "")).strip()
        if current_task_id:
            return current_task_id
        current_task_json_file = str(runtime_state.get("current_task_json_file", "")).strip()
        if current_task_json_file:
            return str(load_task(current_task_json_file).get("task_id", "")).strip()
    queue_item = find_queue_item_by_run_id(run_id)
    if queue_item:
        task_id = str(queue_item.get("task_id", "")).strip()
        if task_id:
            return task_id
        task_json_file = str(queue_item.get("task_json_file", "")).strip()
        if task_json_file:
            return str(load_task(task_json_file).get("task_id", "")).strip()
    return ""


def pick_next() -> dict[str, Any]:
    item = find_next_open_queue_item()
    if not item:
        raise RuntimeError("no open queue item found in TASKS/QUEUE.json")
    queue_id = str(item.get("queue_id", "")).strip()
    task_id = str(item.get("task_id", "")).strip()
    task_json_file = str(item.get("task_json_file", "")).strip()
    task_md_file = str(item.get("task_md_file", "")).strip()
    run_id = str(item.get("run_id", "")).strip()
    if not task_id or not task_json_file or not task_md_file or not run_id:
        raise RuntimeError(f"queue item is incomplete: {queue_id or '(missing queue_id)'}")
    picked_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    updated_item = mark_queue_item_status(queue_id, "active", picked_at)
    set_active_task(task_json_file, task_id, task_md_file, run_id, "active")
    return {
        "action": "next",
        "queue_id": queue_id,
        "task_id": task_id,
        "task_json_file": task_json_file,
        "task_md_file": task_md_file,
        "run_id": run_id,
        "queue_status": str(updated_item.get("status", "")).strip(),
        "picked_at": str(updated_item.get("picked_at", "")).strip(),
    }


def write_task_md(task_md_file: str, payload: dict[str, Any]) -> None:
    path = Path(task_md_file)
    lines = [
        f"# TASK: {payload.get('title', '')}",
        "",
        f"RUN_ID: {payload.get('run_id', '')}",
        f"TASK_ID: {payload.get('task_id', '')}",
        f"PROJECT_ID: {payload.get('project_id', '')}",
        f"STATUS: {payload.get('status', '')}",
        f"PRIORITY: {payload.get('priority', '')}",
        "",
        "## Goal",
        str(payload.get("goal", "")).strip(),
        "",
        "## Scope",
    ]
    for item in list(payload.get("scope", []) or []):
        lines.append(f"- `{str(item).strip()}`")
    lines.extend(["", "## Non-goals"])
    for item in list(payload.get("non_goals", []) or []):
        lines.append(f"- {str(item).strip()}")
    lines.extend(["", "## Acceptance"])
    for item in list(payload.get("acceptance", []) or []):
        status = "x" if str(item.get("status", "")).strip() == "done" else " "
        lines.append(f"- [{status}] {str(item.get('text', '')).strip()}")
    lines.extend(["", "## Inputs"])
    for item in list(payload.get("inputs", []) or []):
        lines.append(f"- `{str(item).strip()}`")
    lines.extend(
        [
            "",
            "## Risks / Rollback",
            f"- Risks: {str(payload.get('risks', '')).strip()}",
            f"- Rollback plan: {str(payload.get('rollback_plan', '')).strip()}",
        ]
    )
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def normalize_list(items: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for item in items:
        raw = str(item).strip()
        if not raw:
            continue
        for part in raw.split(","):
            value = str(part).strip()
            if not value or value in seen:
                continue
            seen.add(value)
            result.append(value)
    return result


def validate_create_task_args(title: str, goal: str, scope: list[str], run_id: str, priority: str) -> None:
    if not title.strip():
        raise ValueError("title is required")
    if not goal.strip():
        raise ValueError("goal is required")
    if not normalize_list(scope):
        raise ValueError("at least one scope item is required")
    if not run_id.strip().startswith("run-"):
        raise ValueError("run_id must start with 'run-'")
    if priority.strip() not in {"P0", "P1", "P2", "P3"}:
        raise ValueError("priority must be one of: P0, P1, P2, P3")


def default_run_id(raw_run_id: str | None) -> str:
    candidate = str(raw_run_id or "").strip()
    if candidate:
        return candidate
    runtime_state = get_runtime_state()
    return str(runtime_state.get("current_run_id", "")).strip()


def create_task(
    title: str,
    goal: str,
    scope: list[str],
    run_id: str,
    queue: bool,
    activate: bool,
    priority: str,
    non_goals: list[str],
    inputs: list[str],
    acceptance_texts: list[str],
    risks: str,
    rollback_plan: str,
) -> dict[str, Any]:
    validate_create_task_args(title, goal, scope, run_id, priority)
    slug = slugify(title)
    task_id = f"task-{slug}"
    task_json_file, task_md_file = task_paths_for_slug(slug)
    if Path(task_json_file).exists() or Path(task_md_file).exists():
        raise FileExistsError(f"task already exists for slug: {slug}")
    acceptance_payload = [
        {"id": f"check-{idx+1}", "text": text, "status": "pending"}
        for idx, text in enumerate(normalize_list(acceptance_texts))
    ]
    if not acceptance_payload:
        acceptance_payload = [
            {"id": "verify", "text": "Command(s) pass: make verify", "status": "pending"},
            {"id": "evidence", "text": "reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated", "status": "pending"},
        ]
    payload = {
        "task_id": task_id,
        "run_id": run_id,
        "project_id": "quant-factory-os",
        "status": "active",
        "priority": priority,
        "title": title.strip(),
        "goal": goal.strip(),
        "scope": normalize_list(scope),
        "non_goals": normalize_list(non_goals),
        "acceptance": acceptance_payload,
        "inputs": normalize_list(inputs),
        "artifacts": {
            "task_md_file": task_md_file,
            "summary_file": f"reports/{run_id}/summary.md",
            "decision_file": f"reports/{run_id}/decision.md",
        },
        "updated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "risks": risks.strip(),
        "rollback_plan": rollback_plan.strip(),
    }
    save_task(task_json_file, payload)
    write_task_md(task_md_file, payload)
    result: dict[str, Any] = {
        "action": "create",
        "task_id": task_id,
        "task_json_file": task_json_file,
        "task_md_file": task_md_file,
        "run_id": run_id,
    }
    if queue:
        queue_item = {
            "queue_id": f"queue-{slug}",
            "title": title,
            "run_id": run_id,
            "task_id": task_id,
            "task_json_file": task_json_file,
            "task_md_file": task_md_file,
            "status": "pending",
            "picked_at": None,
            "goal": payload["goal"],
            "scope": list(payload["scope"]),
            "acceptance": list(payload["acceptance"]),
        }
        append_queue_item(queue_item)
        result["queue_id"] = queue_item["queue_id"]
    if activate:
        set_active_task(task_json_file, task_id, task_md_file, run_id, "active")
        result["activated"] = True
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--next", action="store_true")
    parser.add_argument("--pick-next", action="store_true")
    parser.add_argument("--create", action="store_true")
    parser.add_argument("--create-task", action="store_true")
    parser.add_argument("--active-task", action="store_true")
    parser.add_argument("--queue", action="store_true")
    parser.add_argument("--task-json-file")
    parser.add_argument("--run-id")
    parser.add_argument("--title")
    parser.add_argument("--goal")
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--activate", action="store_true")
    parser.add_argument("--priority", default="P1")
    parser.add_argument("--non-goal", action="append", default=[])
    parser.add_argument("--input", action="append", default=[])
    parser.add_argument("--acceptance", action="append", default=[])
    parser.add_argument("--risks", default="")
    parser.add_argument("--rollback-plan", default="")
    args = parser.parse_args()

    if args.next or args.pick_next:
        result = pick_next()
    elif args.create or args.create_task:
        if not args.title or not args.goal or not args.scope:
            parser.error("--create requires --title, --goal, and at least one --scope")
            return 2
        run_id = default_run_id(args.run_id)
        if not run_id:
            parser.error("--create requires --run-id or an active runtime run")
            return 2
        result = create_task(
            args.title,
            args.goal,
            list(args.scope),
            run_id,
            args.queue,
            args.activate,
            str(args.priority),
            list(args.non_goal),
            list(args.input),
            list(args.acceptance),
            str(args.risks),
            str(args.rollback_plan),
        )
    elif args.active_task:
        result = load_active_task()
    elif args.queue and not args.title:
        result = load_queue()
    elif args.task_json_file:
        result = load_task(args.task_json_file)
    elif args.run_id and not args.title:
        result = {"run_id": args.run_id, "task_id": find_task_id_for_run(args.run_id)}
    else:
        parser.error(
            "supported commands: --next, --create, --active-task, --queue, --task-json-file, or --run-id"
        )
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
