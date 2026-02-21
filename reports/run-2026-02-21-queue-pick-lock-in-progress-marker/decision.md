# Decision

RUN_ID: `run-2026-02-21-queue-pick-lock-in-progress-marker`

## Why
- 

## Options considered
- 

## Risks / Rollback
- 

## Decision
- Add an in-progress marker `[>]` + `Picked:` metadata when picking the next queue item to prevent duplicate picks across sessions.

## Rationale
- Prevents repeated selection of the same queue item in parallel / restarted Codex sessions while keeping the audit trail in-repo.

