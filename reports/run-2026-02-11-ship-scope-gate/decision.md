# Decision

RUN_ID: `run-2026-02-11-ship-scope-gate`

## Why
- Ship currently stages/commits files without validating declared task scope, allowing accidental mixed changes or missing expected files.
- Enforcing scope from task metadata improves delivery discipline and keeps PR content aligned with declared intent.

## Options considered
- Scope gate in `tools/ship.sh` with task-declared `## Scope` (chosen): centralized enforcement and immediate protection at ship time.
- Rely only on manual review/checklists: rejected due to inconsistency and higher miss risk.
- Hard-block with no override: rejected; operational escape hatch is needed for exceptional situations, so `SHIP_ALLOW_OUT_OF_SCOPE=1` is provided and auditable.

## Risks / Rollback
- Risk: malformed task files without `## Scope` will fail shipping until corrected.
- Risk: scope matching semantics (exact/prefix/glob) may need tuning for edge patterns.
- Rollback plan: revert `tools/ship.sh`, `TASKS/_TEMPLATE.md`, `docs/WORKFLOW.md`, and `tests/test_ship_scope_gate.py`.
