# Decision

RUN_ID: `run-2026-02-25-queue-add-next-auto-evidence`

## Why
- The queue includes a new unfinished item for auto-evidence-on-pick behavior and
  it must be formally submitted with task/evidence metadata before implementation.

## What
- Created `TASKS/TASK-queue-add-next-auto-evidence.md` with scope restricted to
  `TASKS/QUEUE.md`.
- Verified queue format consistency and confirmed the target item is already at
  queue top; kept `TASKS/QUEUE.md` unchanged to avoid duplication.
- Generated and updated evidence files for this run.

## Verify
- `make verify` -> `45 passed in 1.66s`

## Risks / Rollback
- Risk: concurrent queue edits can change top ordering before merge.
- Rollback: revert this run and resubmit with same minimal queue-add scope.
