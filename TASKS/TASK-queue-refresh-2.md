# TASK: refresh queue completion state and next-shot ordering

RUN_ID: run-2026-02-21-queue-refresh-2
OWNER: codex
PRIORITY: P1

## Goal
Refresh `TASKS/QUEUE.md` so completed items are marked done and startup pick
will select the true next unfinished task.

## Scope (Required)
- `TASKS/QUEUE.md`

## Non-goals
- No tooling, workflow script, or business logic changes.
- No queue expansion beyond minimal completion refresh and ordering cleanup.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `TASKS/QUEUE.md`
- recent merged PRs for completed queue items

## Steps (Optional)
1. Mark completed queue items as `[x]`.
2. Add `Done: PR #xx, RUN_ID=...` under completed items.
3. Ensure queue top first unchecked item is the real next shot.
4. Run verify and update evidence.

## Reading policy
Use `tools/view.sh` for repo file reads.

## Risks / Rollback
- Risks: wrong completion mapping between queue and delivered runs.
- Rollback plan: revert queue refresh commit.
