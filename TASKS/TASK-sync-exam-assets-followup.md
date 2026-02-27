# TASK: sync-exam-assets-followup

RUN_ID: run-2026-02-28-sync-exam-assets-followup
OWNER: codex
PRIORITY: P0

## Goal
Ship missing `SYNC/EXAM_*` assets that were left untracked by ship allowlist during the previous sync exam run.

## Scope (Required)
- `SYNC/EXAM_PLAN_PROMPT.md`
- `SYNC/EXAM_ANSWER_TEMPLATE.md`
- `SYNC/EXAM_RUBRIC.json`
- `SYNC/EXAM_WORKFLOW.md`
- `SYNC/SESSION_LATEST.md`
- `TASKS/STATE.md`
- `TASKS/TASK-sync-exam-assets-followup.md`
- `reports/run-2026-02-28-sync-exam-assets-followup/`

## Non-goals
- No behavior change to grader logic.
- No workflow redesign beyond shipping missing assets.

## Acceptance
- [x] All `SYNC/EXAM_*` files are tracked on `main`.
- [x] `make verify` passes.
- [x] Evidence updated under `reports/{RUN_ID}/`.

## Inputs
- Previous run merged without these files due ship untracked allowlist boundaries.

## Risks / Rollback
- Risk: none beyond normal documentation sync.
- Rollback: revert this RUN.
