# Decision

RUN_ID: `run-2026-02-21-task-bootstrap-next`

## Why
- AGENTS rule requires creating a TASK from queue when no task is provided.
- Existing `tools/task.sh` only wrapped ship; it did not bootstrap new tasks
  from `TASKS/QUEUE.md`.
- Adding `--next/next` reduces manual task authoring friction while keeping the
  existing shipping flow unchanged.

## Options considered
- Add bootstrap as a new standalone script.
  - Rejected: increases surface area and duplicates task workflow entrypoint.
- Extend `tools/task.sh` with a `--next/next` mode.
  - Chosen: minimal change with backward compatibility.

## Risks / Rollback
- Risks:
  - Queue parser assumes current bullet-field format.
  - Scope extraction keeps one-line scope text; some generated tasks may still
    need manual refinement before ship.
- Rollback plan:
  - Revert this run commit to restore previous `tools/task.sh` behavior.
