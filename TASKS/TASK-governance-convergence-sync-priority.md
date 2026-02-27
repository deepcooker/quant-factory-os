# TASK: governance-convergence-sync-priority

RUN_ID: run-2026-02-27-governance-convergence-sync-priority
OWNER: codex
PRIORITY: P1

## Goal
Converge top-level governance to a single source-of-truth model and implement
`CURRENT_RUN_ID` as the default session/task handoff key in `tools/qf`.

## Scope (Required)
- `README.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/CODEX_ONBOARDING_CONSTITUTION.md`
- `docs/PROJECT_GUIDE.md`
- `chatlogs/PROJECT_GUIDE.md`
- `SYNC/`
- `TASKS/STATE.md`
- `tools/qf`
- `tests/`
- `TASKS/TASK-governance-convergence-sync-priority.md`
- `reports/run-2026-02-27-governance-convergence-sync-priority/`

## Non-goals
- Changing wealth/quant strategy content.
- Rewriting ship/task automation semantics unrelated to sync governance.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- Approved top-level plan: single truth owner model + `CURRENT_RUN_ID` defaultization.
- User decision: `PROJECT_GUIDE` canonical in `docs/`; run key source in `TASKS/STATE.md`.

## Steps (Optional)
1. P0 docs convergence (owner/reference only, no duplicate rules).
2. P1 `tools/qf` reads/writes `CURRENT_RUN_ID` by default.
3. Add tests for default run resolution and mismatch fail-fast behavior.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: behavior change for users relying on explicit RUN_ID everywhere.
- Rollback plan: revert this RUN diff.
