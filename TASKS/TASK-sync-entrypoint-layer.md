# TASK: sync-entrypoint-layer

RUN_ID: run-2026-02-27-sync-entrypoint-layer
OWNER: codex
PRIORITY: P1

## Goal
Create a top-level `SYNC/` entrypoint layer so any model (Codex CLI or web GPT)
can align quickly with latest state, decisions, and handoff context.

## Scope (Required)
- `SYNC/`
- `chatlogs/PROJECT_GUIDE.md`
- `TASKS/TASK-sync-entrypoint-layer.md`
- `reports/run-2026-02-27-sync-entrypoint-layer/`

## Non-goals
- Modifying task execution automation logic.
- Rewriting wealth/quant project appendix content.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- User requirement: sync-first for both Codex CLI and web models, not docs-only scatter.

## Steps (Optional)
1. Add `SYNC/` folder with strict read order and latest handoff/state files.
2. Point `PROJECT_GUIDE.md` to `SYNC/` as first entrypoint.
3. Verify and capture evidence.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: stale sync files if maintenance discipline is weak.
- Rollback plan: revert this RUN diff.
