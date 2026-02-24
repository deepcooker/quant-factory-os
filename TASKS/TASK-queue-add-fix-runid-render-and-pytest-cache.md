# TASK: add queue item for fixing RUN_ID rendering and pytest cache hygiene

RUN_ID: run-2026-02-24-queue-add-fix-runid-render-and-pytest-cache
OWNER: <you>
PRIORITY: P1

## Goal
Submit the newly added queue item for fixing RUN_ID placeholder rendering and
pytest cache hygiene so it becomes the next executable queued task.

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
- Do not implement RUN_ID rendering fixes in this task.
- Do not implement pytest cache ignore changes in this task.
- Do not modify tooling/tests/docs outside queue submission evidence.

## Acceptance
- [ ] `TASKS/QUEUE.md` Queue-top unfinished item exists for:
  `修复 <RUN_ID> 占位符渲染 + 忽略 pytest 缓存确保工作区干净`.
- [ ] Command(s) pass: `make verify`.
- [ ] Evidence updated: `reports/<RUN_ID>/meta.json`,
  `reports/<RUN_ID>/summary.md`, and `reports/<RUN_ID>/decision.md`.
- [ ] No changes outside declared scope.

## Inputs
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Confirm queue item format and placement with `tools/view.sh`.
2. Create task + evidence files for this RUN_ID.
3. Run `make verify`.
4. Update summary/decision.
5. Ship task.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental edits to adjacent completed queue history items.
- Rollback plan: restore prior queue content and reship only the intended queue submission.
