# TASK: add QUEUE + startup checklist entrypoints to STATE

RUN_ID: run-2026-02-11-state-queue-startup-links
OWNER: codex
PRIORITY: P1

## Goal
Make `TASKS/STATE.md` explicitly include bootstrap entry references for queue and startup checklist.

## Non-goals
Do not modify workflow logic, tooling behavior, or files outside the scoped task/evidence paths.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-state-queue-startup-links/summary.md` and `reports/run-2026-02-11-state-queue-startup-links/decision.md`
- [ ] Scope respected: only `TASKS/STATE.md`, this task file, and `reports/run-2026-02-11-state-queue-startup-links/`

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/STATE.md`
- `TASKS/QUEUE.md`
- `docs/WORKFLOW.md#Codex-session-startup-checklist`

## Steps (Optional)
1. Create task file with RUN_ID.
2. Run `make evidence RUN_ID=run-2026-02-11-state-queue-startup-links`.
3. Update `TASKS/STATE.md` with explicit queue/startup checklist entrypoint references.
4. Run `make verify`.
5. Update evidence summary and decision with why/what/verify.
6. Ship using `RUN_ID=run-2026-02-11-state-queue-startup-links tools/task.sh TASKS/TASK-state-queue-startup-links.md`.

## Reading policy
Use `tools/view.sh` by default. If larger ranges are needed, provide explicit line ranges and reason.

## Risks / Rollback
- Risks: duplicate or unclear references in `TASKS/STATE.md`.
- Rollback plan: revert only this task's changes and keep previous `STATE` wording.
