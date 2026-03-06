# Summary

RUN_ID: `run-2026-03-06-ship-pr-merge-recovery-guidance`

## What changed
- Created a bounded follow-up task/run for the PR merge recovery gap exposed by PR #168.
- Hardened `tools/ship.sh` `pr_merge_blocked` handling so it now:
  - writes `recovery_cmd` into `ship_state.json`
  - prints explicit base-into-head recovery steps
  - includes `pr_url`, `base_branch`, and `head_branch` in the failure output
- Added regression coverage in `tests/task_ship.py`.
- Synced the minimal owner-doc wording in `docs/WORKFLOW.md` and `docs/PROJECT_GUIDE.md`.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-03-06-ship-pr-merge-recovery-guidance`
- `make verify` -> `28 passed in 2.07s`

## Notes
- This slice intentionally does not auto-merge the base branch into the PR branch.
- The goal is guidance and recoverability, not adding a destructive or overly magical repair path.
