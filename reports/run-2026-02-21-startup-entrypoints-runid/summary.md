# Summary

RUN_ID: `run-2026-02-21-startup-entrypoints-runid`

## What changed
- Added task file `TASKS/TASK-startup-entrypoints-run-id.md` for the top
  unfinished queue item.
- Added regression test `tests/test_startup_entrypoints_contract.py` to enforce
  startup contract:
  - `tools/enter.sh` includes required entrypoints and `RUN_ID` output.
  - `tools/start.sh` delegates to `tools/enter.sh`.
- No runtime workflow script logic changes were needed; current implementation
  already satisfies the queue goal.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-21-startup-entrypoints-runid`
  - wrote/ensured `meta.json`, `summary.md`, `decision.md`.
- `make verify`
  - PASS: `29 passed in 1.41s`.

## Notes
- Scope kept minimal: task file, one test file, and evidence files.
