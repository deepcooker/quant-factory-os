# TASK: add queue item (pick lock) to enable --next

RUN_ID: run-2026-02-21-queue-add-pick-lock
OWNER: codex
PRIORITY: P1

## Goal
Commit the new unfinished queue item (`queue pick lock`) so `tools/task.sh --next`
can discover a next-shot task across sessions.

## Scope (Required)
- `TASKS/QUEUE.md`

## Non-goals
- Do not implement queue locking behavior in scripts.
- Do not modify tools, tests, or other queue entries.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`
- [ ] `TASKS/QUEUE.md` contains the new `- [ ]` queue item and no unrelated edits

## Inputs
- `TASKS/QUEUE.md`
- `TASKS/_TEMPLATE.md`

## Steps (Optional)
1. Confirm template and queue entry contents.
2. Create evidence skeleton for this RUN_ID.
3. Verify queue file only includes the intended new unfinished item change.
4. Run `make verify`.
5. Update evidence files with why/what/verify.
6. Ship via `tools/task.sh`.

## Reading policy
Use `tools/view.sh` for file reads.

## Risks / Rollback
- Risks: committing accidental queue edits.
- Rollback plan: follow-up queue-only correction task.
