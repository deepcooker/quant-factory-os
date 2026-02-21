# TASK: mark queue item done (workflow gates tests) with PR#81 + RUN_ID

RUN_ID: run-2026-02-21-queue-mark-done-pr81
OWNER: codex
PRIORITY: P1

## Goal
Mark the completed queue item for workflow gates regression tests as done and
record PR #81 and its RUN_ID to prevent future sessions from picking it again.

## Scope (Required)
- `TASKS/QUEUE.md`

## Non-goals
- Do not modify tools, code, or tests.
- Do not change other queue items.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`
- [ ] Queue item is checked and includes Done note with PR #81 and RUN_ID

## Inputs
- `TASKS/QUEUE.md`
- Completed work reference: PR #81
- Completed run reference: `run-2026-02-21-add-minimal-regression-tests-for-workflow-gates-p1`

## Steps (Optional)
1. Create evidence skeleton for this RUN_ID.
2. Update queue item status and add Done note.
3. Run verification.
4. Update summary and decision evidence with why/what/verify.
5. Ship via `tools/task.sh`.

## Reading policy
Use `tools/view.sh` for file reads.

## Risks / Rollback
- Risks: marking wrong queue item.
- Rollback plan: revert only the `TASKS/QUEUE.md` change in a follow-up task.
