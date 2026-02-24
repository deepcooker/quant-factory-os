# TASK: add queue item for next auto evidence and next-step checklist

RUN_ID: run-2026-02-25-queue-add-next-auto-evidence
OWNER: <you>
PRIORITY: P1

## Goal
Submit the newly added queue item for auto evidence on task pick plus standardized
next-step checklist output.

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
- Do not implement auto-evidence or checklist logic in this task.
- Do not modify tools/docs/tests outside this queue-add submission.

## Acceptance
- [ ] Queue top contains unfinished item:
  `领取任务时自动 make evidence + 打印下一步清单（避免人肉步骤）`.
- [ ] Command(s) pass: `make verify`.
- [ ] Evidence updated: `reports/{RUN_ID}/meta.json`,
  `reports/{RUN_ID}/summary.md`, and `reports/{RUN_ID}/decision.md`.
- [ ] No changes outside declared scope.

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Confirm queue item format and top placement.
2. Create task + evidence files.
3. Run `make verify`.
4. Update summary and decision.
5. Ship via task workflow.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental queue history edits outside target scope.
- Rollback plan: revert and resubmit with same scope-only changes.
