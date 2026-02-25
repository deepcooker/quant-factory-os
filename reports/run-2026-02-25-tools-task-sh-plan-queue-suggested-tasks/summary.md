# Summary

RUN_ID: `run-2026-02-25-tools-task-sh-plan-queue-suggested-tasks`

## What changed
- Enhanced `tools/task.sh --plan` to generate a new `## Suggested tasks` section.
- Added copy-paste-ready queue item snippets per suggestion:
  `TODO Title` / `Goal` / `Scope` / `Acceptance`.
- Added signal sources for suggestions:
  recent `reports/run-*/decision.md`, `TASKS/STATE.md`, and optional `MISTAKES/*.md`.
- Ensured queue-empty scenario still yields at least 5 suggested tasks.
- Updated workflow guidance for queue-empty pickup from suggested tasks.
- Added regression test for queue-empty plan output.

## Commands / Outputs
- `make verify`
- Output: `49 passed in 2.44s`

## Notes
- Evidence directory is present at `reports/run-2026-02-25-tools-task-sh-plan-queue-suggested-tasks/`.
