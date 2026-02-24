# TASK: add queue item (Observer awareness digest) to enable --next

RUN_ID: run-2026-02-24-queue-add-awareness
OWNER: <you>
PRIORITY: P1

## Goal
Submit the newly added unfinished Observer awareness queue item so it is tracked
in a dedicated task/evidence run and can be picked by `tools/task.sh --next`.

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
- Do not implement the Observer/awareness feature in this task.
- Do not change queue item format or unrelated completed queue entries.
- Do not modify tooling, tests, or docs.

## Acceptance
- [ ] Queue top includes unfinished item:
  `TODO Title: 增加只读 Observer 周报（awareness digest）`.
- [ ] Command(s) pass: `make verify`.
- [ ] Evidence updated: `reports/<RUN_ID>/meta.json`, `reports/<RUN_ID>/summary.md`,
  and `reports/<RUN_ID>/decision.md`.
- [ ] No changes outside declared scope.

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Validate template and queue item format with `tools/view.sh`.
2. Create task file and evidence skeleton for this RUN_ID.
3. Keep queue item as-is at Queue top (no format drift).
4. Run `make verify`.
5. Write summary/decision and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental edits to completed queue history.
- Rollback plan: restore `TASKS/QUEUE.md` and resubmit this run with scope-only diff.
