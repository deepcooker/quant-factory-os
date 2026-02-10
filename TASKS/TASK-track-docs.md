# TASK: track docs directory

RUN_ID: run-2026-02-10-track-docs
OWNER: codex
PRIORITY: P1

## Goal
Ensure required docs files are tracked in git so start/enter and tests pass.

## Non-goals
No content changes to docs or unrelated files.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-10-track-docs/summary.md` and `reports/run-2026-02-10-track-docs/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/INTEGRATION_A9.md`

## Steps (Optional)
1) Create evidence skeleton.
2) Ensure docs files are tracked.
3) Run `make verify`.
4) Update evidence and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Missing tracked docs could keep start/enter/tests failing.
- Rollback plan: Revert docs tracking changes.
