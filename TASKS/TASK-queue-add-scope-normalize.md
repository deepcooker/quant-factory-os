# TASK: add queue item for scope normalization + move into Queue section

RUN_ID: run-2026-02-22-queue-add-scope-normalize
OWNER: <you>
PRIORITY: P1

## Goal
Add a new unfinished queue item for Scope normalization/self-check and place it at
the top of the `## Queue` section instead of before the `# QUEUE` title.

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
Do not change completed queue items or unrelated task/workflow logic.

## Acceptance
- [ ] New unfinished item exists under `## Queue` as the first queue entry.
- [ ] The same item no longer appears before the `# QUEUE` title.
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Read template and queue with `tools/view.sh`.
2. Create this task file and evidence skeleton.
3. Move the unfinished item into `## Queue` top (minimal edit).
4. Run `make verify`.
5. Update evidence files and ship with `tools/task.sh`.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental edits to completed queue items.
- Rollback plan: revert `TASKS/QUEUE.md` to prior content and re-apply only the move.
