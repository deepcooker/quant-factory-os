# TASK: sync-learning-exam-cli-web

RUN_ID: run-2026-02-27-sync-learning-exam-cli-web
OWNER: codex
PRIORITY: P0

## Goal
Build a cross-surface sync learning exam flow (Codex CLI + web GPT) using `/plan` prompt packs, fixed answer templates, and an auto-grader so onboarding quality is measurable.

## Scope (Required)
- `SYNC/`
- `tools/sync_exam.py`
- `tests/test_sync_exam.py`
- `docs/WORKFLOW.md`
- `TASKS/STATE.md`
- `TASKS/TASK-sync-learning-exam-cli-web.md`
- `reports/run-2026-02-27-sync-learning-exam-cli-web/`

## Non-goals
- No business strategy changes.
- No changes to trading or data pipeline code.
- No replacement of existing `init/handoff/ready` execution gates.

## Acceptance
- [x] Provide one `/plan` exam prompt that works for both CLI and web GPT.
- [x] Provide one fixed answer template focused on learning core context and skills.
- [x] Auto-grader returns pass/fail + score + failed checks and writes auditable output.
- [x] `make verify` passes.
- [x] Evidence updated under `reports/{RUN_ID}/`.

## Inputs
- User requirement: exam must teach/align thought layer, not just ask questions; include dedicated judgement program.

## Risks / Rollback
- Risk: rubric too rigid and over-fits wording.
- Rollback: revert this RUN and keep manual review workflow.
