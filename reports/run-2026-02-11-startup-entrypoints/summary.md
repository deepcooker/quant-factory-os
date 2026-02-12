# Summary

RUN_ID: `run-2026-02-11-startup-entrypoints`

## What changed
- Added a startup entrypoint block in `tools/enter.sh` after all checks pass:
- `Entry points:`
- `TASKS/STATE.md`
- `TASKS/QUEUE.md`
- `docs/WORKFLOW.md#Codex-session-startup-checklist`
- Added `RUN_ID` output in `tools/enter.sh`:
- prints `RUN_ID: <value>` when env var exists
- prints `RUN_ID: (not set)` when env var is absent
- Added regression tests in `tests/test_enter_entrypoints.py`:
- subprocess runs `bash tools/enter.sh` in an isolated temporary repo
- validates entrypoint lines are printed
- validates injected `RUN_ID=run-test` is printed

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-11-startup-entrypoints`
- `make verify`
- Output: `27 passed in 1.19s`

## Notes
- Kept `tools/start.sh` unchanged because it already calls `bash tools/enter.sh`.
