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

# Why
- Prevents reliance on local-only context and clarifies the evidence path.

# Verify
- `make verify`
