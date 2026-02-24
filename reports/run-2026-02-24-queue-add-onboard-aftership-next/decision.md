# Decision

RUN_ID: `run-2026-02-24-queue-add-onboard-aftership-next`

## Why
- The queue now includes a new onboarding + after-ship-next item, and it must be
  submitted with task/evidence so it becomes the next executable shot.

## What
- Created `TASKS/TASK-queue-add-onboard-aftership-next.md` with scope restricted
  to `TASKS/QUEUE.md`.
- Validated queue format and placement, and kept queue content unchanged because
  the target item was already present at `## Queue` top.
- Generated this run's evidence bundle.

## Verify
- `make verify` -> `40 passed in 1.51s`

## Risks / Rollback
- Risk: concurrent edits can reorder queue top before merge.
- Rollback: revert this run and re-submit with same minimal scope.
