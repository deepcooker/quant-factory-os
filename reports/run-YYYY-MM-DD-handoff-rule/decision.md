# Decision

RUN_ID: `run-YYYY-MM-DD-handoff-rule`

## Why
- Handoff behavior must be explicit and immutable at workflow level: local uncommitted state is non-transferable, and handoff artifacts must be PR/commit plus evidence.
- `TASKS/STATE.md` should directly point to the governing handoff hard rules for quick operator lookup.

## Options considered
- Option 1: keep existing wording only.
  - Rejected: rules existed but were not explicitly marked as handoff gates in wording.
- Option 2: minimal textual reinforcement in `docs/WORKFLOW.md` + add STATE entry.
  - Selected: satisfies hardening goal with smallest possible diff.

## Risks / Rollback
- Risk: over-editing outside allowed scope could be swept into ship by `git add -u`.
- Mitigation: touched only `docs/WORKFLOW.md`, `TASKS/STATE.md`, task file, and this RUN_ID evidence.
- Verify: `make verify` (`20 passed in 0.88s`).
- Rollback: revert this task PR if wording changes are not accepted.
