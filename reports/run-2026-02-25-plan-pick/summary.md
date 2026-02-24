# Summary

RUN_ID: `run-2026-02-25-plan-pick`

## What changed
- Extended `tools/task.sh` with:
  - `--plan [N]`: generates `TASKS/TODO_PROPOSAL.md` (default N=20), including
    queue candidates (`queue-next` recommended) and recent decision paths.
  - `--pick queue-next`: requires existing proposal file and then performs queue
    top pick (equivalent to `--next`) while only printing `TASK_FILE`/`RUN_ID`.
- Updated `docs/WORKFLOW.md` startup checklist with plan/pick usage.
- Added tests in `tests/test_task_plan_pick.py` for `--plan` and `--pick`.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-25-plan-pick`
- `make verify` -> `44 passed in 1.62s`

## Notes
- `--plan` does not modify queue or ship anything; `--pick` only bootstraps task pick.
