# Decision

RUN_ID: `run-2026-02-25-ship-main-enter`

## Why
- Existing ship flow could sync local `main` before PR truly reached `MERGED`,
  which left local state stale and forced extra manual refresh steps.

## What
- Added `wait_for_pr_merged()` in `tools/ship.sh`, polling:
  `gh pr view "$pr_url" --json state -q .state`
  and waiting until state is exactly `MERGED`.
- Moved post-ship local main sync behind that merge wait gate.
- Added dirty-worktree guard right before sync; aborts with explicit error if not clean.
- Added sync confirmation output:
  `post-ship synced main@<sha> (origin/main@<sha>)`.
- Updated `docs/WORKFLOW.md` to state that ship now waits for merge then auto-syncs main.
- Added static regression test `tests/test_ship_wait_merge_then_sync.py`.

## Verify
- `make verify` -> `45 passed in 1.65s`

## Risks / Rollback
- Risk: if PR is blocked from merging, ship now waits instead of returning quickly.
- Rollback: revert this run commit; behavior is isolated to ship/docs/test paths.

## Evidence paths
- `reports/run-2026-02-25-ship-main-enter/meta.json`
- `reports/run-2026-02-25-ship-main-enter/summary.md`
- `reports/run-2026-02-25-ship-main-enter/decision.md`
