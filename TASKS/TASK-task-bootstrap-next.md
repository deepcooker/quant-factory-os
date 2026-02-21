# TASK: tools/task.sh bootstrap next task from QUEUE

RUN_ID: run-2026-02-21-task-bootstrap-next
OWNER: codex
PRIORITY: P1

## Goal
Add a backward-compatible `next/bootstrap` mode in `tools/task.sh` that reads
`TASKS/QUEUE.md`, generates a complete runnable `TASKS/TASK-*.md`, and outputs
the generated task path plus RUN_ID.

## Scope (Required)
- `tools/task.sh`
- `tests/`

## Non-goals
- Do not auto-ship in bootstrap mode.
- Do not modify core ship gate logic.
- Do not expand queue semantics beyond minimum parser needed for current format.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `AGENTS.md`
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`
- `tools/task.sh`

## Steps (Optional)
1. Add `--next` / `next` mode in `tools/task.sh`.
2. Parse first unchecked queue item for Title/Goal/Scope/Acceptance.
3. Generate non-placeholder RUN_ID and task markdown from template.
4. Add pytest coverage for bootstrap generation behavior.
5. Verify with `make verify`, update evidence, then ship with task file.

## Reading policy
Use `tools/view.sh` for file reads.

## Risks / Rollback
- Risks: queue parsing edge cases if queue format changes.
- Rollback plan: revert this run commit.
