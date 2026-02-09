# Decision

RUN_ID: `run-2026-02-09-test`

## Why
- 

## Options considered
- 

## Risks / Rollback
- 
# Decision
- Prefer GH_TOKEN when present to enable non-interactive auth in tools/ship.sh.
- Keep existing behavior unchanged when GH_TOKEN is absent.
- Verify: `make verify` (after `source /root/policy/venv/bin/activate`).
