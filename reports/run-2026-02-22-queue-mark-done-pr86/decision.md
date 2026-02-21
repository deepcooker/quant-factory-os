# Decision

RUN_ID: `run-2026-02-22-queue-mark-done-pr86`

## Why
- The scope-normalization task was completed and merged as PR #86, so its queue
  lifecycle must be finalized by converting `[>]` to `[x]` and recording Done metadata.

## Options considered
- Option A (chosen): update the existing in-progress entry in place.
- Option B (not chosen): append a new completed duplicate entry, rejected to avoid
  duplicate history for one queue item.

## Risks / Rollback
- Risk: touching adjacent queue blocks unintentionally.
- Rollback: restore previous `TASKS/QUEUE.md` and re-apply only target status and Done line.
