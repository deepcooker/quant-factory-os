# TASK: sync-chinese-entrypoint-naming

RUN_ID: run-2026-02-27-sync-chinese-entrypoint-naming
OWNER: codex
PRIORITY: P1

## Goal
Rename SYNC entry files to distinct Chinese names (to avoid confusion with root
`README.md`) and update all references consistently.

## Scope (Required)
- `SYNC/`
- `README.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/CODEX_ONBOARDING_CONSTITUTION.md`
- `docs/PROJECT_GUIDE.md`
- `TASKS/STATE.md`
- `TASKS/TASK-sync-chinese-entrypoint-naming.md`
- `reports/run-2026-02-27-sync-chinese-entrypoint-naming/`

## Non-goals
- Changing automation behavior in `tools/qf`.
- Modifying wealth/quant strategic content.

## Acceptance
- [x] Command(s) pass: `make verify`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [x] Regression guardrail added/updated if applicable (N/A: naming/docs-only change; existing suite remains green)

## Inputs
- User request: distinguish SYNC entry names from root README and switch to Chinese.

## Steps (Optional)
1. Rename SYNC canonical files to Chinese names.
2. Keep optional compatibility pointers only where needed.
3. Update all references in governance docs.
4. Verify and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: stale links from older notes.
- Rollback plan: revert this RUN diff.
