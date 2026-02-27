# Summary

RUN_ID: `run-2026-02-27-ship-runid-normalization`

## What changed
- Fixed RUN_ID parsing in `tools/ship.sh`:
  - Added `normalize_run_id` to trim whitespace and trailing punctuation.
  - Added `extract_run_id_from_msg` with stricter message regex.
  - Applied normalization to `SHIP_RUN_ID`, `RUN_ID`, and message-derived RUN_ID.
- Added parse-only test hook:
  - `SHIP_RUN_ID_PARSE_ONLY=1 SHIP_RUN_ID_PARSE_INPUT=... tools/ship.sh ...`
  - Outputs `PARSED_RUN_ID: ...` then exits.
- Added regression tests for trailing `:` and sentence-with-punctuation cases.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-ship-runid-normalization`
- `make verify` -> `58 passed in 3.55s`

## Notes
- This prevents path pollution like `reports/run-...:/ship_state.json`.
