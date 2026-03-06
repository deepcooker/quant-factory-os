# Summary

RUN_ID: `run-2026-03-06-task-ship-smoke`

## What changed
- Prepared a minimal smoke run to exercise the real `tools/task.sh -> tools/ship.sh` path after the branch-continuity fix.
- Bound the smoke to `run-2026-03-06-task-ship-smoke` with a dedicated task and direction artifacts.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-03-06-task-ship-smoke` -> pass

## Notes
- This smoke is intentionally limited to harmless `TASKS/` + `reports/` updates and a real ship-path exercise.
