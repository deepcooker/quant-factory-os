# Decision

RUN_ID: `run-2026-02-24-observer-awareness-digest`

## Why
- We need a reproducible, read-only weekly awareness artifact built from repo
  evidence so each run can inherit auditable context and next-step suggestions.

## What
- Implemented `tools/observe.sh` to produce
  `reports/<RUN_ID>/awareness.md` with required sections:
  shipped runs, repeated failure patterns, current risks, and next-shot suggestions.
- Added `make awareness RUN_ID=<RUN_ID>` in `Makefile` as the entrypoint.
- Added `tests/test_observe_awareness.py` covering:
  - happy path with sample reports/state/mistakes
  - empty inputs with graceful output generation
- Hardened `tests/test_ship_guard.py` to avoid false failures from unrelated staged files.
- Generated awareness output for this run:
  `reports/run-2026-02-24-observer-awareness-digest/awareness.md`

## Verify
- `make awareness RUN_ID=run-2026-02-24-observer-awareness-digest`
- `make verify` -> `38 passed in 1.81s`

## Risks
- Heuristic text extraction may miss some non-standard report formats.
- Week bucketing uses run-id date prefix; malformed run IDs are ignored.

## Evidence paths
- `reports/run-2026-02-24-observer-awareness-digest/meta.json`
- `reports/run-2026-02-24-observer-awareness-digest/summary.md`
- `reports/run-2026-02-24-observer-awareness-digest/decision.md`
- `reports/run-2026-02-24-observer-awareness-digest/awareness.md`
