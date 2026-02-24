# Decision

RUN_ID: `run-2026-02-24-queue-add-fix-runid-render-and-pytest-cache`

## Why
- The queue now contains a new unfinished fix item, and it must be recorded via a
  dedicated task/evidence run before execution in a later shot.

## What
- Created `TASKS/TASK-queue-add-fix-runid-render-and-pytest-cache.md` with scope
  restricted to `TASKS/QUEUE.md`.
- Verified `TASKS/QUEUE.md` already has the target queue item at Queue top with the
  required structure; kept queue content unchanged to avoid duplication.
- Generated and updated evidence files for this run.

## Verify
- `make verify` -> `38 passed in 1.51s`

## Risks / Rollback
- Risk: concurrent queue edits can reorder or modify the target item before merge.
- Rollback: revert this run and resubmit with the same minimal queue-submission scope.
