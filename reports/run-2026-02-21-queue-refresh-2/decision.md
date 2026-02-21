# Decision

RUN_ID: `run-2026-02-21-queue-refresh-2`

## Why
- New sessions pick the top unfinished queue item; stale `[ ]` marks caused
  repeated picks of already completed work.
- Queue must reflect current completion status and a clear next-shot top item.

## Options considered
- Minimal refresh only (mark done + reorder + optional Done notes).
  - Chosen: directly addresses repeated-pick risk with smallest diff.
- Broader queue rewrite/reprioritization.
  - Not chosen: outside requested scope.

## Risks / Rollback
- Risks:
  - Completion metadata for older historical done items remains implicit.
- Rollback plan:
  - Revert this run commit to restore previous queue ordering/marks.
