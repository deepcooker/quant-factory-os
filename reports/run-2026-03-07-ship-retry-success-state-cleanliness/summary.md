# Summary

RUN_ID: `run-2026-03-07-ship-retry-success-state-cleanliness`

## What changed
- Added a success-state write gate to `tools/ship.sh` so `run_with_retry_capture()` no longer rewrites tracked `ship_state.json` after a local commit exists.
- Kept failure-path and recovery-path state writes intact; only success-path helper writes are suppressed after `git commit`.
- Refreshed `tests/task_ship.py` to lock the helper-level behavior.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-03-07-ship-retry-success-state-cleanliness`
- `make verify`

## Notes
- Root cause came from real ship runs: even after removing explicit `committed/pr_created/merged/synced` writes, the helper `run_with_retry_capture()` still wrote success-state ship markers for later steps like `push`, `pr_state`, and `sync_checkout_base`.
- This run fixes the helper, which was the remaining source of self-dirty ship-state rewrites on the success path.
