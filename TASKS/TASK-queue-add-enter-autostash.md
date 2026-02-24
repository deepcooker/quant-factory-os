# TASK: add queue item for enter autostash switch

RUN_ID: run-2026-02-25-queue-add-enter-autostash
OWNER: <you>
PRIORITY: P1

## Goal
Submit the newly added queue item for explicit `enter.sh` autostash support so it
can be picked and implemented in the next run.

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
- Do not implement `enter.sh` autostash behavior in this task.
- Do not modify tools/docs/tests beyond this queue-add submission.

## Acceptance
- [ ] Queue top contains unfinished item:
  `enter.sh 支持显式自动 stash（ENTER_AUTOSTASH=1）并打印 stash 名`.
- [ ] Command(s) pass: `make verify`.
- [ ] Evidence updated: `reports/{RUN_ID}/meta.json`,
  `reports/{RUN_ID}/summary.md`, and `reports/{RUN_ID}/decision.md`.
- [ ] No changes outside declared scope.

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Confirm queue format and top placement with `tools/view.sh`.
2. Create task and evidence files.
3. Run `make verify`.
4. Update summary and decision.
5. Ship via task workflow.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental changes to adjacent completed queue entries.
- Rollback plan: revert and resubmit with the same scope-only queue-add diff.
