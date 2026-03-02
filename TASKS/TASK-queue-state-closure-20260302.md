# TASK: queue/state closure cleanup

RUN_ID: run-2026-03-02-queue-state-closure
OWNER: <you>
PRIORITY: P1

## Goal
Close stale queue in-progress/unchecked leftovers and set session state to done.

## Scope (Required)
- `TASKS/QUEUE.md`
- `TASKS/STATE.md`
- `reports/{RUN_ID}/`

## Non-goals
- Modify runtime workflow logic.
- Touch unrelated task history content.

## Acceptance
- [ ] All stale `slice-next: ... ready 先处理未收尾 run` leftover items are no longer `[ ]`/`[>]`.
- [ ] `TASKS/STATE.md` status is `done` for the current run snapshot.
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- Current `TASKS/QUEUE.md`
- Current `TASKS/STATE.md`

## Steps (Optional)
- Normalize stale queue item states to closed.
- Mark state as done.
- Verify and ship.

## Reading policy
Use `tools/view.sh` by default.

## Risks / Rollback
- Risks: accidental closure of still-active queue items.
- Rollback plan: revert `TASKS/QUEUE.md` and `TASKS/STATE.md` to previous commit.
