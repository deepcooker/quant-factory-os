# Decision

RUN_ID: `run-2026-02-21-queue-add-pick-lock`

## Why
- `tools/task.sh --next` had no available unchecked queue item in the committed queue state. Adding and committing the `queue pick lock` item restores deterministic next-shot discovery.

## Options considered
- Commit only `TASKS/QUEUE.md` queue item addition with required evidence (chosen).
- Delay commit and keep item local/uncommitted (rejected: not visible to other sessions).

## Risks / Rollback
- Risk: queue item wording/scope could need refinement later.
- Rollback: update/remove only this queue item in a follow-up queue-only task.
