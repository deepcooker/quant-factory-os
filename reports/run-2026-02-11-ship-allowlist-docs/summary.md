# Summary

RUN_ID: `run-2026-02-11-ship-allowlist-docs`

## What changed
- Updated `tools/ship.sh` untracked allowlist in `stage_changes()`:
  - from: `tools/*|tests/*|TASKS/*|Makefile`
  - to: `tools/*|tests/*|TASKS/*|docs/*|Makefile`
- Added regression test `tests/test_ship_untracked_allowlist.py` to assert `docs/*` is present in the allowlist case line.
- Added task file `TASKS/TASK-ship-allowlist-docs.md`.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-11-ship-allowlist-docs`
  - created `meta.json`, initialized `summary.md` and `decision.md`
- `make verify`
  - `21 passed in 0.95s`

## Notes
- Minimal scope maintained: only `tools/ship.sh`, one pytest file, task file, and this run evidence files.
