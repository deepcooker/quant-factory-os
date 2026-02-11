# TASK: add TASKS/QUEUE.md + codex startup checklist

RUN_ID: run-2026-02-11-bootstrap-queue
OWNER: codex
PRIORITY: P1

## Goal
Add a durable queue entrypoint and startup bootstrap checklist so new Codex
sessions can pick the next task from repo state without relying on chat memory.

## Non-goals
- No a9 main project integration.
- No changes outside task/workflow/state/evidence files required by this task.

## Acceptance
- [ ] New `TASKS/QUEUE.md` exists with usage notes and two TODO sample items.
- [ ] `docs/WORKFLOW.md` adds `Codex session startup checklist` with explicit 5-step bootstrap flow.
- [ ] `TASKS/STATE.md` adds entry references for queue and startup checklist paths.
- [ ] Command passes: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-bootstrap-queue/summary.md` and `reports/run-2026-02-11-bootstrap-queue/decision.md` with why/what/verify.

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/STATE.md`
- `docs/WORKFLOW.md`

## Steps (Optional)
1. Create evidence skeleton via `make evidence RUN_ID=run-2026-02-11-bootstrap-queue`.
2. Add `TASKS/QUEUE.md`.
3. Update workflow and state references.
4. Run `make verify` and update evidence docs.
5. Ship via `RUN_ID=run-2026-02-11-bootstrap-queue tools/task.sh`.

## Reading policy
Use `tools/view.sh` by default. If larger ranges are needed, specify the exact
line range and reason.

## Risks / Rollback
- Risks: Minor wording drift with existing conventions.
- Rollback plan: Revert this task's doc-only changes.
