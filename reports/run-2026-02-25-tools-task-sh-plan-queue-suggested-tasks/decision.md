# Decision

RUN_ID: `run-2026-02-25-tools-task-sh-plan-queue-suggested-tasks`

## Why
- `tools/task.sh --plan` previously produced only queue candidates + recent decisions.
- When queue candidates are empty, planning had no actionable output to enqueue, blocking the bootstrap flow.

## What
- Updated `tools/task.sh`:
  - Added `## Suggested tasks` generation in `--plan`.
  - Suggestions now draw from:
    - recent `reports/run-*/decision.md`
    - `TASKS/STATE.md`
    - optional `MISTAKES/*.md`
  - Each suggestion is emitted as a copy-paste-ready queue item skeleton:
    `TODO Title`, `Goal`, `Scope`, `Acceptance`.
  - Added fallback seeds so queue-empty planning still outputs at least 5 suggestions.
- Updated `docs/WORKFLOW.md` with queue-empty usage:
  choose one suggestion -> paste into `TASKS/QUEUE.md` -> run `--next/--pick queue-next`.
- Added regression test in `tests/test_task_plan_pick.py` for queue-empty suggested-task output.

## Verify
- `make verify`
- Result: `49 passed in 2.44s`

## Evidence paths
- `reports/run-2026-02-25-tools-task-sh-plan-queue-suggested-tasks/meta.json`
- `reports/run-2026-02-25-tools-task-sh-plan-queue-suggested-tasks/summary.md`
- `reports/run-2026-02-25-tools-task-sh-plan-queue-suggested-tasks/decision.md`

## Risks / Rollback
- Risk: heuristic suggestions may be generic if source signals are weak.
- Rollback: revert `tools/task.sh`, `tests/test_task_plan_pick.py`, and `docs/WORKFLOW.md` to previous commit.
