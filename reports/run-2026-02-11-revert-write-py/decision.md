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
- Keep PR #61 open and add a follow-up commit on the same branch to complete
  the `write.py` revert and evidence updates.

# Why
- PR #60 was merged with a non-task-related `write.py` modification that violates minimal-diff rules.
- Minimizes noise while preserving a single audit trail in PR #61.

# Verify
- `make verify`
