# TASK: sync-entrypoint-files-ship

RUN_ID: run-2026-02-27-sync-entrypoint-files-ship
OWNER: codex
PRIORITY: P1

## Goal
Ship recovered `SYNC/` top-level handoff files that were not included in the
previous PR due untracked-file staging behavior.

## Scope (Required)
- `SYNC/`
- `TASKS/TASK-sync-entrypoint-files-ship.md`
- `reports/run-2026-02-27-sync-entrypoint-files-ship/`

## Non-goals
- Tooling refactor for `tools/ship.sh`.
- Changes to wealth/quant roadmap docs.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- Recovered `SYNC/*` files from stash after PR #119 merge.

## Steps (Optional)
1. Track `SYNC/*` files in git.
2. Verify and ship as a dedicated follow-up PR.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: sync files can drift if not maintained.
- Rollback plan: revert this RUN diff.
