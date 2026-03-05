#!/usr/bin/env python3
from __future__ import annotations

import sys
import os
from pathlib import Path

from ops_ready import (
    append_conversation_checkpoint,
    append_execution_event,
    generate_orient_draft,
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
        f"tools/ops orient RUN_ID={run_id}",
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
