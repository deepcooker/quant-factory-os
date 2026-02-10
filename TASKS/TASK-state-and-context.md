# TASK: add STATE and memory rules

RUN_ID: run-2026-02-10-state-and-context
OWNER: codex
PRIORITY: P1

## Goal
Add a state handoff entrypoint and codify memory/context retention rules in
workflow documentation.

## Non-goals
Do not store raw chat logs or external data inside the repo.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-10-state-and-context/summary.md`
  and `reports/run-2026-02-10-state-and-context/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `TASKS/_TEMPLATE.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`

## Steps (Optional)
- Create `TASKS/STATE.md` with current state, conventions, plans, and risks.
- Extend `docs/WORKFLOW.md` with Memory & Context handoff rules.
- Run `make evidence` and `make verify`, then update evidence.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: forgetting to capture handoff rules in evidence.
- Rollback plan: revert added docs and task files.
