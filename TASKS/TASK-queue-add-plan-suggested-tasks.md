# TASK: add queue item for plan suggested tasks when queue empty

RUN_ID: run-2026-02-25-queue-add-plan-suggested-tasks
OWNER: <you>
PRIORITY: P1

## Goal
Submit the newly added queue item for strengthening `--plan` suggested tasks when
queue candidates are empty.

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
- Do not implement suggested-task generation logic in this task.
- Do not modify tools/docs/tests outside queue-add submission evidence.

## Acceptance
- [ ] Queue top contains unfinished item:
  `强化 tools/task.sh --plan：Queue 为空时生成 Suggested tasks（可复制入队）`.
- [ ] Command(s) pass: `make verify`.
- [ ] Evidence updated: `reports/{RUN_ID}/meta.json`,
  `reports/{RUN_ID}/summary.md`, and `reports/{RUN_ID}/decision.md`.
- [ ] No changes outside declared scope.

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Confirm queue format and top placement.
2. Create task/evidence files for this RUN_ID.
3. Run `make verify`.
4. Update summary and decision.
5. Ship via task flow.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental queue history edits beyond target scope.
- Rollback plan: revert and resubmit with the same scope-only changes.
