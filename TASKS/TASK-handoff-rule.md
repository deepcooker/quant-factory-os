# TASK: codify handoff rule (uncommitted does not exist)

RUN_ID: run-2026-02-10-handoff-rule
OWNER: codex
PRIORITY: P1

## Goal
Codify the handoff rule in workflow docs and reference it from STATE.

## Non-goals
No changes to main project code or deep a9 integration.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-10-handoff-rule/summary.md` and `reports/run-2026-02-10-handoff-rule/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `docs/WORKFLOW.md` (Memory & Context section)
- `TASKS/STATE.md`

## Steps (Optional)
1) Create evidence skeleton.
2) Update workflow/STATE text for handoff rule.
3) Run `make verify`.
4) Update evidence and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Inconsistent handoff behavior if rule is unclear.
- Rollback plan: Revert the documentation updates.
