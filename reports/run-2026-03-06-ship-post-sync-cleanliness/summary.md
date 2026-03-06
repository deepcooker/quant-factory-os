# Summary

RUN_ID: `run-2026-03-06-ship-post-sync-cleanliness`

## What changed
- Added a dirty-path filter in `tools/ship.sh` so post-ship sync ignores the current run's own `reports/<RUN_ID>/ship_state.json`.
- Added source-level regression coverage in `tests/task_ship.py` for both active-base continuity and self-dirty `ship_state` filtering.

## Commands / Outputs
- `bash -n tools/ship.sh` -> pass
- `make verify` -> `23 passed in 1.31s`
- `make evidence RUN_ID=run-2026-03-06-ship-post-sync-cleanliness` -> pass

## Notes
- This task follows directly from the real smoke on PR #166: branch continuity was fixed, but post-ship sync still blocked on the tool's own `ship_state.json`.
