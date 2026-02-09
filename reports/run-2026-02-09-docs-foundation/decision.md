# Decision

RUN_ID: `run-2026-02-09-docs-foundation`

## Why
- Onboarding and handoffs are faster when workflow, entities, and integration
  expectations are written in one place.

## Options considered
- Keep docs scattered in README only (rejected: hard to maintain and find).
- Skip guardrail tests (rejected: easy to regress).

## Risks / Rollback
- Risks: docs can drift if not updated with behavior changes.
- Rollback: revert docs and test updates.
