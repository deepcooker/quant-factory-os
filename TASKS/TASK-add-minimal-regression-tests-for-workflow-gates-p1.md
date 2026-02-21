# TASK: add minimal regression tests for workflow gates (P1)

RUN_ID: run-2026-02-21-add-minimal-regression-tests-for-workflow-gates-p1
OWNER: <you>
PRIORITY: P1

## Goal
cover scope gate / expected-files gate / single-run guard with small

## Scope (Required)
- `tests/`
- `reports/`
- `TASKS/`


## Non-goals
What we explicitly do NOT do.

## Acceptance
- `make verify` passes.
- Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
- No changes outside declared scope.

## Inputs
- Links / files / references
- If data is needed, specify allowed sample constraints (max rows, time window)

## Steps (Optional)
Suggested approach, if you have one.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
- Rollback plan:
