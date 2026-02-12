# Summary

RUN_ID: `run-2026-02-12-codex-read-denylist-file`

## What changed
- Updated `tools/ship.sh` untracked allowlist in `stage_changes()` to explicitly
  include `.codex_read_denylist`.
- Added tracked repository file `.codex_read_denylist` with:
- deny pattern `project_all_files.txt`
- comment documenting temporary override via `CODEX_READ_DENYLIST_ALLOW=1` and
  evidence requirement
- This makes denylist config ship-safe and avoids lingering untracked `??` state.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-12-codex-read-denylist-file`
- `make verify`
- Output: `27 passed in 1.20s`

## Notes
- No changes to `tools/view.sh` logic were needed; tests passed with tracked denylist file.
