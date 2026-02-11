# Decision

RUN_ID: `run-2026-02-11-handoff-rule-fix-placeholder`

## Why
- Prior delivery introduced a placeholder RUN_ID token into task/evidence naming.
- Placeholder naming breaks traceability expectations for relay handoff and audit lookup, so reports and task references must use the concrete run identifier.

## Options considered
- Option 1: keep placeholder-named directory and only document it.
  - Rejected: leaves long-term audit pollution and ambiguous run identity.
- Option 2: copy evidence content into correctly named `reports/run-2026-02-11-handoff-rule/`, then delete legacy placeholder files and update task references.
  - Selected: minimal and deterministic normalization with clear file-level history.

## Risks / Rollback
- Risk: ship may miss newly created reports files if staging behavior is incomplete.
- Mitigation: explicitly verified target files exist and legacy files are gone before verify/ship.
- Verify: `make verify` (`20 passed in 0.87s`).
- Rollback: revert this task commit and re-run placeholder fix with same RUN_ID scope.
