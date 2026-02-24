# Decision

RUN_ID: `run-2026-02-25-enter-sh-stash-enter-autostash-1-stash`

## Why
- `tools/enter.sh` default strict-fail on dirty workspace is safe but creates
  friction in single-user flows. We need an explicit opt-in path that stashes
  and continues without weakening default safety.

## What
- In `tools/enter.sh`:
  - kept default dirty-workspace failure unchanged.
  - added `ENTER_AUTOSTASH=1` branch:
    - `git stash push -u -m "enter-wip-YYYYMMDD-HHMMSS"`
    - prints stash line (`git stash list -1`) and recovery commands
      (`git stash list`, `git stash pop stash@{0}`)
    - continues existing `git pull --rebase` and `doctor` flow.
- Updated `docs/WORKFLOW.md` to document explicit autostash usage.
- Added static test `tests/test_enter_autostash_switch.py` asserting presence of
  `ENTER_AUTOSTASH`, `git stash push -u`, and `enter-wip-` marker.

## Verify
- `make verify` -> `48 passed in 1.78s`

## Risks / Rollback
- Risk: users may forget they have stashed changes after autostash flow.
- Rollback: revert this run commit; changes are isolated to enter/docs/test/report.

## Evidence paths
- `reports/run-2026-02-25-enter-sh-stash-enter-autostash-1-stash/meta.json`
- `reports/run-2026-02-25-enter-sh-stash-enter-autostash-1-stash/summary.md`
- `reports/run-2026-02-25-enter-sh-stash-enter-autostash-1-stash/decision.md`
