# Summary

RUN_ID: `run-2026-02-10-view-find`

## What changed
- Added `--find`/`--context` support to `tools/view.sh` with friendly no-match
  messaging.
- Added pytest coverage for find hit/miss cases.

## Commands / Outputs
- `make verify`
  - `20 passed in 0.94s`

## Notes
- Evidence: `tools/view.sh`, `tests/test_view_find.py`
