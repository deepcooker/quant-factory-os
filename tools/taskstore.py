#!/usr/bin/env python3
from __future__ import annotations

try:
    from tools.taskclient import (
        append_queue_item,
        find_next_open_queue_item,
        find_queue_item_by_run_id,
        find_task_id_for_run,
        get_active_task_path,
        get_queue_path,
        get_runtime_state,
        get_task_registry,
        load_active_task,
        load_queue,
        load_task,
        mark_queue_item_status,
        save_queue,
        save_task,
        set_active_task,
        slugify,
        task_paths_for_slug,
    )
except Exception:  # pragma: no cover
    from taskclient import (  # type: ignore
        append_queue_item,
        find_next_open_queue_item,
        find_queue_item_by_run_id,
        find_task_id_for_run,
        get_active_task_path,
        get_queue_path,
        get_runtime_state,
        get_task_registry,
        load_active_task,
        load_queue,
        load_task,
        mark_queue_item_status,
        save_queue,
        save_task,
        set_active_task,
        slugify,
        task_paths_for_slug,
    )
