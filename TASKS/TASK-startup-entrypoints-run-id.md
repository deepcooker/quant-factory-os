# TASK: startup prints session entrypoints + active RUN_ID

RUN_ID: run-2026-02-21-startup-entrypoints-runid
OWNER: codex
PRIORITY: P0

## Goal
Ensure startup flow prints required session entrypoints and current RUN_ID per
queue requirement, with a minimal regression guardrail.

## Scope (Required)
- `tools/start.sh`
- `tools/enter.sh`
- `tests/`

## Non-goals
- No deep integration with external data, DB, or strategy logic.
- No workflow/gate behavior changes in `tools/ship.sh`.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `TASKS/QUEUE.md` top unfinished item
- `docs/WORKFLOW.md#Codex-session-startup-checklist`
- `tools/start.sh`
- `tools/enter.sh`

## Steps (Optional)
1. Create evidence via `make evidence RUN_ID=<RUN_ID>`.
2. Implement minimal change to satisfy startup entrypoint requirement.
3. Add/adjust regression test for required startup output contract.
4. Run `make verify`.
5. Update evidence docs and ship via `tools/task.sh`.

## Reading policy
Use `tools/view.sh` for repo file reads.

## Risks / Rollback
- Risks: overfitting tests to exact wording.
- Rollback plan: revert this task commit; runtime behavior remains as before.
