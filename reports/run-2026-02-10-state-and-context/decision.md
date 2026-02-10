# Decision

RUN_ID: `run-2026-02-10-state-and-context`

## Why
- Establish a durable, repo-resident handoff mechanism without storing full
  chat transcripts.

## Options considered
- Store transcripts in repo (rejected: violates memory rules and noise).
- Store only executable summaries and decisions (selected).

## Risks / Rollback
- Risk: missing context in handoffs. Mitigation: keep `TASKS/STATE.md` current.
- Rollback plan: revert `TASKS/STATE.md` and workflow section changes.
