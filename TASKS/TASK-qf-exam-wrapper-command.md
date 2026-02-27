# TASK: qf-exam-wrapper-command

RUN_ID: run-2026-02-28-qf-exam-wrapper-command
OWNER: codex
PRIORITY: P1

## Goal
Add `tools/qf exam` as a one-command wrapper to run sync exam grading and write auditable output under `reports/{RUN_ID}/`.

## Scope (Required)
- `tools/qf`
- `tests/test_qf_exam.py`
- `docs/WORKFLOW.md`
- `TASKS/STATE.md`
- `TASKS/TASK-qf-exam-wrapper-command.md`
- `reports/run-2026-02-28-qf-exam-wrapper-command/`

## Non-goals
- No changes to grading rubric logic.
- No changes to ship policy.
- No business strategy changes.

## Acceptance
- [x] `tools/qf exam` works with default paths based on `CURRENT_RUN_ID`.
- [x] `tools/qf exam` supports explicit `RUN_ID=...` and custom answer/rubric/output args.
- [x] `make verify` passes.
- [x] Evidence updated under `reports/{RUN_ID}/`.

## Inputs
- User requested one-command exam operation to reduce friction.

## Risks / Rollback
- Risk: wrapper argument parsing may conflict with existing qf subcommands.
- Rollback: revert this RUN diff.
