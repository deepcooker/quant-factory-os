# TASK: add queue item for plan/pick auto task acquisition

RUN_ID: run-2026-02-25-queue-add-plan-pick
OWNER: <you>
PRIORITY: P1

## Goal
Submit the newly added queue item for automatic plan/pick task acquisition so it
can be picked and implemented in the next run.

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
- Do not implement `--plan` or `--pick` behavior in this task.
- Do not modify tooling/docs/tests beyond this queue submission run.

## Acceptance
- [ ] Queue top contains unfinished item:
  `自动生成任务候选清单（plan）并支持确认后领取（pick）`.
- [ ] Command(s) pass: `make verify`.
- [ ] Evidence updated: `reports/{RUN_ID}/meta.json`,
  `reports/{RUN_ID}/summary.md`, and `reports/{RUN_ID}/decision.md`.
- [ ] No changes outside declared scope.

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Confirm queue format and top item placement.
2. Create this task and evidence files.
3. Run `make verify`.
4. Update summary and decision.
5. Ship via task workflow.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental edits to completed queue history entries.
- Rollback plan: restore queue content and resubmit with minimal scope-only diff.
