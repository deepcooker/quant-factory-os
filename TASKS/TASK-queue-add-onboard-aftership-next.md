# TASK: add queue item for onboard + after-ship next flow

RUN_ID: run-2026-02-24-queue-add-onboard-aftership-next
OWNER: <you>
PRIORITY: P1

## Goal
Submit the newly added queue item for session onboard plus serial next-shot
handoff, so it can be picked and implemented in the next run.

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
- Do not implement onboard scripts or after-ship next-shot automation in this task.
- Do not modify tooling, tests, or docs outside queue submission evidence.

## Acceptance
- [ ] Queue top contains unfinished item:
  `Session 一键初始化（onboard）+ 串行接下一枪（after-ship next）`.
- [ ] Command(s) pass: `make verify`.
- [ ] Evidence updated: `reports/{RUN_ID}/meta.json`,
  `reports/{RUN_ID}/summary.md`, `reports/{RUN_ID}/decision.md`.
- [ ] No changes outside declared scope.

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Confirm queue format and top item placement with `tools/view.sh`.
2. Create task and evidence files for this RUN_ID.
3. Run `make verify`.
4. Update summary and decision.
5. Ship via task flow.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental edits to completed queue history entries.
- Rollback plan: restore queue content and resubmit only this task/evidence diff.
