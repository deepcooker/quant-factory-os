# Decision

RUN_ID: `run-2026-02-25-plan-pick`

## Why
- Session-level serial handoff needed a lightweight, explicit plan/pick loop:
  propose tasks from current repo evidence, then let a human confirm and pick
  queue-next without auto-coding or auto-shipping.

## What
- Implemented `tools/task.sh --plan [N]` to generate `TASKS/TODO_PROPOSAL.md`
  with:
  - Queue candidates (top unfinished, with `id=queue-next` recommended)
  - Recent decisions (paths from `reports/run-*/decision.md`)
- Implemented `tools/task.sh --pick queue-next` to require a generated proposal
  and then run the existing queue-next bootstrap flow.
- Updated `docs/WORKFLOW.md` startup checklist to include optional plan/pick steps.
- Added `tests/test_task_plan_pick.py` covering `--plan` output and `--pick`
  `TASK_FILE/RUN_ID` emission.

## Verify
- `make verify` -> `44 passed in 1.62s`

## Risks / Rollback
- Risk: users may expect `--pick` to support ids beyond `queue-next`; currently
  intentionally constrained for minimal scope.
- Rollback: revert this run commit; plan/pick behavior is isolated to
  `tools/task.sh`, docs, and tests.

## Evidence paths
- `reports/run-2026-02-25-plan-pick/meta.json`
- `reports/run-2026-02-25-plan-pick/summary.md`
- `reports/run-2026-02-25-plan-pick/decision.md`
