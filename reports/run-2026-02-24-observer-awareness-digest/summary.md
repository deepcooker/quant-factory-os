# Summary

RUN_ID: `run-2026-02-24-observer-awareness-digest`

## What changed
- Added `tools/observe.sh` to generate a read-only awareness digest by scanning:
  `reports/run-*/decision.md`, `reports/run-*/summary.md`, `TASKS/STATE.md`, and optional `MISTAKES/*.md`.
- Added tests in `tests/test_observe_awareness.py` for happy path and empty-input behavior.
- Stabilized `tests/test_ship_guard.py` to avoid dependence on ambient staged files.
- Generated `reports/run-2026-02-24-observer-awareness-digest/awareness.md`.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-24-observer-awareness-digest`
- `make awareness RUN_ID=run-2026-02-24-observer-awareness-digest`
  - `AWARENESS_FILE: ./reports/run-2026-02-24-observer-awareness-digest/awareness.md`
- `make verify`
  - `38 passed in 1.81s`

## Notes
- The digest is read-only and degrades safely when `MISTAKES/` or `TASKS/STATE.md` is absent.
