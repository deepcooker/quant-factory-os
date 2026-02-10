# Decision

RUN_ID: `run-2026-02-11-revert-write-py`

## Why
- 

## Options considered
- 

## Risks / Rollback
- 
# Decision
- Revert the unintended `write.py` change from merged PR #60.

# Why
- PR #60 was merged with a non-task-related `write.py` modification that violates minimal-diff rules.

# Verify
- `make verify`
