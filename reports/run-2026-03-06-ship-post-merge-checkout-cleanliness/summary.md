# Summary

RUN_ID: `run-2026-03-06-ship-post-merge-checkout-cleanliness`

## What changed
- Tightened `tools/ship.sh` success-path behavior so it no longer rewrites tracked `ship_state.json` after PR merge and after base-branch sync.
- Preserved failure-path `ship_state.json` writes for recoverable blocked states.
- Added a regression assertion in `tests/task_ship.py` to lock the success-path behavior.
- Updated `docs/WORKFLOW.md` to document that successful post-merge sync must not dirty the tracked ship-state evidence file.

## Commands / Outputs
- `make verify` -> `29 passed in 2.05s`
- Root cause reproduced from real ship path:
  - PR merged successfully
  - local post-ship sync then failed at `sync_checkout_base`
  - blocker was the current run's rewritten `reports/<RUN_ID>/ship_state.json`

## Notes
- This run fixes a post-merge continuity bug in the shipping pipeline, not a business-feature bug.
- The change intentionally favors clean successful sync over writing extra runtime success states into a tracked evidence file.
