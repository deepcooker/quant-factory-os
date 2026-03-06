# Summary

RUN_ID: `run-2026-03-06-ship-pr-merge-resilience`

## What changed
- Added a merge-state check in `tools/ship.sh` before the direct `gh pr merge` call.
- Added a dedicated `pr_merge_blocked` failure path so non-clean PR merges exit early with an actionable resume state instead of blind retries.
- Updated docs and regression coverage for the new `pr_merge_blocked` contract.

## Commands / Outputs
- `bash -n tools/ship.sh` -> pass
- `make verify` -> `24 passed in 1.38s`

## Notes
- This task follows directly from the second real smoke on PR #167, where `pr_merge` failed because the merge commit could not be cleanly created.
