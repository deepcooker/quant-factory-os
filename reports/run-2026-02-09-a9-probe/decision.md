# Decision

RUN_ID: `run-2026-02-09-a9-probe`

## Why
- Provide a real entrypoint probe (`main_controller.py --help`) while retaining
  the existing dry-run behavior.

## Options considered
- Keep only dry-run (rejected: no real entrypoint validation).
- Run full backtest in probe (rejected: too heavy for initial check).

## Risks / Rollback
- Risks: probe fails if a9 entrypoint or flags change.
- Rollback: remove probe mode and tests.
