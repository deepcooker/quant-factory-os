# Decision

RUN_ID: `run-2026-02-25-queue-add-plan-pick`

## Why
- The new plan/pick queue item must be submitted via a dedicated task/evidence run
  before implementation, so it is auditable and can be picked as next shot.

## What
- Created `TASKS/TASK-queue-add-plan-pick.md` with scope restricted to
  `TASKS/QUEUE.md`.
- Validated queue format and confirmed the target item was already present at
  queue top; no additional queue edit was needed.
- Generated and updated run evidence files.

## Verify
- `make verify` -> `42 passed in 1.55s`

## Risks / Rollback
- Risk: concurrent queue edits may reorder items before merge.
- Rollback: revert this run and re-submit with the same minimal scope.
