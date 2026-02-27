# Decision

RUN_ID: `run-2026-02-27-p0-sync-state-machine-doc-gates`

## Why
- Sync quality was being hurt by ambiguous command semantics (`init/handoff/ready`)
  and stale documentation after process changes.
- User requirement is explicit: sync must reduce total workload and improve
  downstream automation, not add extra burden.
- Therefore P0 should first establish a single lifecycle model and hard doc
  update gates before any tool refactor.

## Options considered
- Refactor `tools/qf` immediately:
  - Pros: fast UX change.
  - Cons: high drift risk without stable governance baseline.
- Only update one doc (WORKFLOW or AGENTS):
  - Pros: low effort.
  - Cons: conflicting truth sources remain.
- P0 governance-first (chosen):
  - Pros: unifies owner docs, auditability, and acceptance criteria.
  - Cons: UX improvements in scripts deferred to next phase.

## Risks / Rollback
- Risks:
  - Duplicate wording may reappear if future changes skip owner-doc updates.
  - Runtime behavior still depends on current `tools/qf` implementation.
- Mitigation:
  - hard "no doc update, no ship" policy documented in AGENTS/WORKFLOW/SYNC.
  - maintained placeholder rendering rule (`{RUN_ID}` instead of `<RUN_ID>`) to keep tests green.
  - next phase (P1) can safely optimize script UX on top of this baseline.
- Rollback plan:
  - revert this RUN diff.
