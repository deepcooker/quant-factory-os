# TASK: add queue item for post-ship local main sync

RUN_ID: run-2026-02-25-queue-add-post-ship-sync-main
OWNER: <you>
PRIORITY: P1

## Goal
Submit the newly added queue item for post-ship local main sync so it is tracked
as the next executable shot.

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
- Do not implement post-ship sync behavior in this task.
- Do not modify tools/docs/tests beyond queue submission evidence.

## Acceptance
- [ ] Queue top contains unfinished item:
  `ship 成功后自动同步本地 main 到最新（无需手动 enter）`.
- [ ] Command(s) pass: `make verify`.
- [ ] Evidence updated: `reports/{RUN_ID}/meta.json`,
  `reports/{RUN_ID}/summary.md`, and `reports/{RUN_ID}/decision.md`.
- [ ] No changes outside declared scope.

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Confirm queue format and top-item placement with `tools/view.sh`.
2. Create this task and evidence files.
3. Run `make verify`.
4. Update summary and decision.
5. Ship with task metadata.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental edits to adjacent completed queue entries.
- Rollback plan: revert to prior queue and resubmit this minimal queue-add run.
