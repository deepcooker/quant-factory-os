# Summary

RUN_ID: `run-2026-02-27-sync-entrypoint-layer`

## What changed
- Added top-level sync entry layer: `SYNC/`
  - `SYNC/README.md`
  - `SYNC/READ_ORDER.md`
  - `SYNC/CURRENT_STATE.md`
  - `SYNC/SESSION_LATEST.md`
  - `SYNC/DECISIONS_LATEST.md`
  - `SYNC/LINKS.md`
- Updated `chatlogs/PROJECT_GUIDE.md` header to explicitly route new sessions
  to `SYNC/READ_ORDER.md` before deeper docs.
- Preserved wealth/quant roadmap content (appendix sections not modified).

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-sync-entrypoint-layer`
- `make verify` -> `64 passed in 4.83s`

## Notes
- This change is sync/governance layer only; no automation logic was modified.
