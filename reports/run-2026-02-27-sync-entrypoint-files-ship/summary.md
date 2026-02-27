# Summary

RUN_ID: `run-2026-02-27-sync-entrypoint-files-ship`

## What changed
- Added tracked top-level sync files under `SYNC/`:
  - `SYNC/README.md`
  - `SYNC/READ_ORDER.md`
  - `SYNC/CURRENT_STATE.md`
  - `SYNC/SESSION_LATEST.md`
  - `SYNC/DECISIONS_LATEST.md`
  - `SYNC/LINKS.md`
- Added follow-up task/evidence to ship these files as a dedicated PR.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-sync-entrypoint-files-ship`
- `make verify` -> `64 passed in 4.87s`

## Notes
- This is a recovery follow-up because previous ship did not stage untracked
  `SYNC/*` by default.
