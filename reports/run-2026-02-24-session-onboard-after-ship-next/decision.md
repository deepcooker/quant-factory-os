# Decision

RUN_ID: `run-2026-02-24-session-onboard-after-ship-next`

## Why
- Session startup quality depended on manual steps and inconsistent context checks.
  A lightweight, auditable onboard output plus a fixed post-ship next-shot hint
  reduces missed steps without auto-mutating queue/code.

## What
- Implemented `tools/onboard.sh` to print required onboarding entrypoints and
  recent decision paths, and to persist the result to
  `reports/run-2026-02-24-session-onboard-after-ship-next/onboard.md`.
- Appended a fixed next-shot suggestion block to successful ship output in
  `tools/ship.sh`.
- Added tests:
  - `tests/test_onboard_smoke.py`
  - `tests/test_ship_next_hint.py`

## Verify
- `bash tools/onboard.sh run-2026-02-24-session-onboard-after-ship-next`
- `make verify` -> `42 passed in 1.57s`

## Risks / Rollback
- Risk: onboard output references `PROJECT_GUIDE.md` as an entrypoint even when
  some environments may not provide that file.
- Rollback: revert this run commit; no data migration required.

## Evidence paths
- `reports/run-2026-02-24-session-onboard-after-ship-next/meta.json`
- `reports/run-2026-02-24-session-onboard-after-ship-next/summary.md`
- `reports/run-2026-02-24-session-onboard-after-ship-next/decision.md`
- `reports/run-2026-02-24-session-onboard-after-ship-next/onboard.md`
