# Decision

RUN_ID: `run-2026-02-10-track-docs`

## Why
- 

## Options considered
- 

## Risks / Rollback
- 
# Decision
- Track the required docs files in git with no content changes.

# Why
- `docs/` was untracked, causing start/enter failures and test expectations to miss required files.

# Verify
- `make verify`
