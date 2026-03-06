# Decision

RUN_ID: `run-2026-03-06-ship-post-sync-smoke`

## Why
- The first real smoke proved branch continuity but exposed `ship_state.json` self-dirty blocking post-ship sync. This second smoke validates the fix on the full merged-PR path.

## Options considered
- Stop at source-level tests and `make verify`.
- Run a second real smoke to validate the full merged-PR post-sync path.

Chosen:
- Run the second real smoke with a minimal harmless diff.

## Risks / Rollback
- Risk: the real path can still fail on an external GitHub step unrelated to the `ship_state.json` fix.
