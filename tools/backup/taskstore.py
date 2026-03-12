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


REPO_ROOT = Path(__file__).resolve().parent.parent.parent
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--active-task", action="store_true")
    parser.add_argument("--queue", action="store_true")
    parser.add_argument("--task-json-file")
    parser.add_argument("--run-id")
    args = parser.parse_args()

    payload: dict[str, Any]
    if args.active_task:
        payload = load_active_task()
    elif args.queue:
        payload = load_queue()
    elif args.task_json_file:
        payload = load_task(args.task_json_file)
    elif args.run_id:
        payload = {"run_id": args.run_id, "task_id": find_task_id_for_run(args.run_id)}
    else:
        parser.error("one of --active-task, --queue, --task-json-file, --run-id is required")
        return 2

    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
