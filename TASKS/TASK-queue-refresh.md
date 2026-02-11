# TASK: refresh QUEUE (mark done; set next real queue items)

RUN_ID: run-2026-02-11-queue-refresh
OWNER: codex
PRIORITY: P0

## Goal
Refresh `TASKS/QUEUE.md` so completed items are checked and the top of queue has
the next actionable P0/P1 tasks for a fresh Codex session.

## Scope (Required)
- `TASKS/QUEUE.md`
- `TASKS/STATE.md` (optional, only if a new convention note is needed)

## Non-goals
- No code/tooling changes.
- No workflow policy rewrites outside queue/state maintenance.

## Acceptance
- [ ] Queue completed items updated to `[x]` when already delivered.
- [ ] 2-3 new top queue candidates added with Title/Goal/Scope.
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-queue-refresh/summary.md` and `reports/run-2026-02-11-queue-refresh/decision.md`

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`
- `TASKS/STATE.md`

## Steps (Optional)
1. Read template, queue, and state.
2. Create evidence skeleton with `make evidence RUN_ID=run-2026-02-11-queue-refresh`.
3. Update queue checkboxes and prepend new P0/P1 next-shot items.
4. Run `make verify`.
5. Update evidence summary + decision.
6. Ship via `RUN_ID=run-2026-02-11-queue-refresh tools/task.sh TASKS/TASK-queue-refresh.md`.

## Reading policy
Use `tools/view.sh` for file reads.

## Risks / Rollback
- Risks: mistakenly marking unfinished work as done; ambiguous next-shot scope.
- Rollback plan: revert `TASKS/QUEUE.md` and rerun verify.
