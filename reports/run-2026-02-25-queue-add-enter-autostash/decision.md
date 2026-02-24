# Decision

RUN_ID: `run-2026-02-25-queue-add-enter-autostash`

## Why
- The queue now includes a new explicit-autostash enter item and it must be
  submitted as a standalone task/evidence run before implementation.

## What
- Created `TASKS/TASK-queue-add-enter-autostash.md` with scope restricted to
  `TASKS/QUEUE.md`.
- Validated queue format and confirmed target item was already at queue top.
- Kept queue content unchanged to avoid duplicate insertion and generated run evidence.

## Verify
- `make verify` -> `47 passed in 1.95s`

## Risks / Rollback
- Risk: concurrent queue edits may alter top ordering before merge.
- Rollback: revert this run and resubmit with identical scope-only changes.
