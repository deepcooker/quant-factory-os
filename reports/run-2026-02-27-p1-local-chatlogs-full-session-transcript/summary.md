# Summary

RUN_ID: `run-2026-02-27-p1-local-chatlogs-full-session-transcript`

## What changed
- Added local full-session transcript fallback to startup flow:
  - `tools/start.sh` now records full Codex terminal session by default to
    `chatlogs/session-*.log` (local only, gitignored).
  - Transcript logging can be disabled with `START_SESSION_LOG=0`.
  - Explicit transcript path can be set with `START_SESSION_LOG_FILE=...`.
  - If `script` utility is unavailable, startup warns and falls back to plain `codex`.
- Updated governance docs to reflect new behavior:
  - `docs/WORKFLOW.md`
  - `SYNC/README.md`
  - `SYNC/SESSION_LATEST.md`
- Updated startup contract test:
  - `tests/test_startup_entrypoints_contract.py`

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-p1-local-chatlogs-full-session-transcript`
  - evidence skeleton created
- `make verify`
  - `71 passed in 7.20s`

## Notes
- This change keeps full transcripts local-only under `chatlogs/` and does not
  store complete chat transcripts in tracked repo files.
