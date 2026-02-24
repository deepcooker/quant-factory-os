# Summary

RUN_ID: `run-2026-02-25-ship-main-enter`

## What changed
- Updated `tools/ship.sh` to wait until PR state is `MERGED` before post-ship
  local main sync.
- Added post-ship sync guard:
  - if working tree is not clean, abort with explicit error.
- Kept sync steps explicit and auditable:
  - `git checkout main`
  - `git pull --rebase origin main`
  - print `post-ship synced main@... (origin/main@...)`
- Updated `docs/WORKFLOW.md` to document merged-then-sync behavior.
- Added static regression test: `tests/test_ship_wait_merge_then_sync.py`.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-25-ship-main-enter`
- `make verify` -> `45 passed in 1.65s`

## Notes
- `tools/task.sh --next` produced:
  - `TASK_FILE: TASKS/TASK-ship-main-enter.md`
  - `RUN_ID: run-2026-02-25-ship-main-enter`
