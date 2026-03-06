# Decision

RUN_ID: `run-2026-03-06-task-ship-smoke`

## Why
- The branch-continuity fix was validated by tests, but it still needs one real `tools/task.sh -> tools/ship.sh` smoke to prove the shipping path no longer jumps to the wrong base branch.

## Options considered
- Stop at `make verify` only.
- Run a real smoke with a minimal harmless task and evidence-only diff.

Chosen:
- Run the real smoke with a minimal harmless task and evidence-only diff.

## Risks / Rollback
- Risk: the real ship path can still fail due to external GitHub or branch state unrelated to the continuity fix.
- Rollback: keep the smoke diff minimal and record the exact failing step in this run if the path breaks again.
