# TASK: add queue item (auto-mark done) to enable --next

RUN_ID: run-2026-02-22-queue-add-auto-mark-done
OWNER: <you>
PRIORITY: P1

## Goal
Submit the newly added unfinished queue item for auto-mark-done so `--next` can
pick it in the next session flow.

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
Do not change existing completed queue items or tooling behavior in this task.

## Acceptance
- [ ] Queue contains unfinished item: `auto-mark queue done on successful ship`.
- [ ] `make verify` passes.
- [ ] Evidence updated: `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Confirm template and queue content with `tools/view.sh`.
2. Create task and evidence files.
3. Run `make verify`.
4. Update summary and decision.
5. Ship with task metadata.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental queue edits beyond the intended item.
- Rollback plan: restore prior queue content and resubmit with minimal diff.
