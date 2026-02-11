# Summary

RUN_ID: `run-2026-02-11-ship-scope-gate`

## What changed
- Added scope gate to `tools/ship.sh`:
  - Parses `## Scope` bullets from task file.
  - Validates staged files are within task scope plus built-in allowlist:
    - task file itself
    - `reports/<RUN_ID>/...`
    - `TASKS/STATE.md`, `TASKS/QUEUE.md`, `docs/WORKFLOW.md`
  - Rejects out-of-scope files by default with explicit file list and fix guidance.
  - Added escape hatch `SHIP_ALLOW_OUT_OF_SCOPE=1`.
- Added test mode `SHIP_SCOPE_GATE_ONLY=1` for parse/validate-only checks without git push/PR side effects.
- Added regression tests in `tests/test_ship_scope_gate.py`:
  - in-scope files pass
  - out-of-scope file fails with `out-of-scope` output
- Updated `TASKS/_TEMPLATE.md` with required `## Scope` section guidance.
- Updated `docs/WORKFLOW.md` with scope gate workflow rule.
- Added task definition: `TASKS/TASK-ship-scope-gate.md`.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-11-ship-scope-gate`
  - created `meta.json`, initialized summary/decision files
- `make verify`
  - `25 passed in 1.11s`

## Notes
- Scope gate is default-on; users can still override explicitly with `SHIP_ALLOW_OUT_OF_SCOPE=1`.
