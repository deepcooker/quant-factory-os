# Decision

RUN_ID: `run-2026-02-21-queue-mark-done-pr81`

## Why
- The queue still listed the completed workflow-gates regression task as pending,
  which can cause future sessions to pick duplicate work.

## Options considered
- Update only `TASKS/QUEUE.md` status and annotate completion metadata (chosen).
- Leave queue unchanged and rely on memory/PR list (rejected: not deterministic).

## Risks / Rollback
- Risk: incorrect queue item bookkeeping.
- Rollback: submit a follow-up queue-only task to correct the checkbox/note.
