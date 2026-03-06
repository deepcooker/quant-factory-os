# Decision

RUN_ID: `run-2026-03-06-vnext-release-baseline`

## Why
- The next unchecked queue item was `vnext release baseline`, so the first move had to be selecting a valid task/run before any more implementation.
- Recent discussion established a stable boundary:
  - `task` owns implementation through ship-ready
  - `smoke` is release-prep checking
  - `ship` owns git / PR / merge / sync
- The smallest safe executable diff was:
  - record the boundary in owner docs
  - add a minimal `tools/smoke.sh`
  - keep `PROJECT_GUIDE` edits to one standard-answer line

## Options considered
- Keep the boundary only in chat and postpone documentation.
- Record the boundary in owner docs only, without a runnable command.
- Add a minimal `tools/smoke.sh` now, but keep it strictly as a local readiness gate and not a remote release tool.

## Risks / Rollback
- The new `smoke` command currently relies on `drift_review` as its authoritative pre-ship evidence source; if review semantics change, smoke checks must be kept aligned.
- This run's dedicated `ready.json` is still missing because project-scoped learn regeneration did not finish a valid model-sync packet under the current app-server behavior.
- Rollback is simple: revert `tools/smoke.sh`, `tests/task_smoke.py`, and the owner-doc/task-pointer updates.

## Stop Reason
- task_done
