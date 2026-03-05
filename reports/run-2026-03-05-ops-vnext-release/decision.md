# Decision

RUN_ID: `run-2026-03-05-ops-vnext-release`

## Why
- Current phase is development/design; old task/report history created noise and slowed execution.

## Decision
- Remove historical `TASKS/TASK-*` and previous `reports/*` content.
- Keep only minimal active pointers and one active task.
- Ship as a clean baseline version.

## Risk
- Historical audit trail is no longer available in-repo after this reset.

## Stop reason
- task_done
