# Decision

RUN_ID: `run-2026-02-10-handoff-rule`

## Why
- 

## Options considered
- 

## Risks / Rollback
- 
# Decision
- Enforce a documented handoff rule: uncommitted changes do not exist for other agents; handoff is via PR/commit.
- Fix the PR by reverting unintended `write.py` edits to satisfy minimal-diff constraints.

# Why
- Prevents reliance on local-only context and clarifies the evidence path.
- Ensures PR scope matches the task by removing unrelated changes.

# Verify
- `make verify`
