# Decision

RUN_ID: `run-2026-02-22-queue-add-auto-mark-done`

## Why
- The new unfinished queue item for auto-mark-done is now the intended next shot
  and must be formally submitted with task/evidence so `--next` can pick it.

## Options considered
- Option A (chosen): submit the queue item as-is with minimal diff (task + evidence).
- Option B (not chosen): edit queue wording/ordering again, rejected to keep this
  task narrowly focused on submission only.

## Risks / Rollback
- Risk: unintended edits outside allowed files.
- Rollback: revert this run's task/evidence commit and resubmit with the same scope.
