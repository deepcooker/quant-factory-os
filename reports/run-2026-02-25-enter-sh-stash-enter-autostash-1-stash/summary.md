# Summary

RUN_ID: `run-2026-02-25-enter-sh-stash-enter-autostash-1-stash`

## What changed
- Updated `tools/enter.sh` to support explicit autostash mode:
  - default behavior unchanged: dirty workspace still fails.
  - when `ENTER_AUTOSTASH=1`, script runs `git stash push -u` with
    `enter-wip-YYYYMMDD-HHMMSS`, prints stash reference and recovery commands,
    then continues pull/doctor flow.
- Updated `docs/WORKFLOW.md` with `ENTER_AUTOSTASH=1 tools/enter.sh` usage.
- Added static regression test `tests/test_enter_autostash_switch.py`.

## Commands / Outputs
- `make verify` -> `48 passed in 1.78s`

## Notes
- Autostash behavior is explicit opt-in; no change to safe default failure path.
