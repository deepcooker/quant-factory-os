# Summary

RUN_ID: `run-2026-03-06-ship-post-commit-state-cleanliness`

## What changed
- Tightened `tools/ship.sh` again so success-path `ship_state.json` rewrites stop after the initial pre-commit/runtime stage.
- Removed post-commit success-state rewrites for:
  - `committed`
  - `pr_created`
  - `merged`
  - `synced`
- Kept failure-path and recovery-path ship-state writes unchanged.
- Extended `tests/task_ship.py` to lock the full post-commit success-path behavior.
- Updated `docs/WORKFLOW.md` to document that success-path ship-state rewrites must stop after local commit.

## Commands / Outputs
- `make verify` -> `29 passed in 1.64s`
- Root cause confirmed from real ship runs:
  - PR #169 and PR #170 both merged
  - local continuity still failed because success-path `ship_state.json` rewrites after commit dirtied the tracked file again

## Notes
- This run supersedes the narrower post-merge-only hypothesis.
- The stable rule is now: success path should not mutate tracked ship-state evidence after a local commit exists.
