# Summary

RUN_ID: `run-2026-02-11-codex-read-denylist`

## What changed
- Added repo denylist file `.codex_read_denylist` with:
  - `project_all_files.txt`
  - comment documenting auditable override via `CODEX_READ_DENYLIST_ALLOW=1`
- Updated `tools/view.sh` to enforce denylist before file reads:
  - default deny with non-zero exit and matched pattern in error message
  - override allow when `CODEX_READ_DENYLIST_ALLOW=1`, with explicit notice
- Added minimal regression tests in `tests/test_codex_read_denylist.py`:
  - default deny for `project_all_files.txt`
  - override allow path with notice
- Added task definition: `TASKS/TASK-codex-read-denylist.md`
- `tools/find.sh` was not modified because it does not exist as a regular file in this repo.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-11-codex-read-denylist`
  - created `meta.json`, initialized `summary.md` and `decision.md`
- `make verify`
  - `23 passed in 1.09s`

## Notes
- `tools/view.sh` existing core behavior (`--from/--to`, line limits, `--find/--context`) remains unchanged.
