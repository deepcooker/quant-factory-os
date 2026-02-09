# Decision

RUN_ID: `run-2026-02-09-start-exec`

## Why
- `tools/start.sh` should be runnable directly via `./tools/start.sh`.

## Options considered
- Keep non-executable and require `bash tools/start.sh` (rejected: not one-step).

## Risks / Rollback
- Risks: none beyond permission change.
- Rollback: `chmod -x tools/start.sh`.
