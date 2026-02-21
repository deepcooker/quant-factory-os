# Decision

RUN_ID: `run-2026-02-22-queue-add-scope-normalize`

## Why
- Queue discipline requires new unfinished work items to live inside the `## Queue`
  section. Leaving an item before `# QUEUE` breaks the queue source-of-truth layout.

## Options considered
- Option A (chosen): move the existing unfinished block into `## Queue` top with no
  content rewrite.
- Option B (not chosen): add a duplicate block inside `## Queue` and keep original
  pre-header block, rejected due to duplicated source-of-truth item.

## Risks / Rollback
- Risk: accidental edits to completed queue history entries.
- Rollback: restore previous `TASKS/QUEUE.md` and reapply only the single block move.
