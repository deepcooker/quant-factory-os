# TASK: sync-filename-rollback-keep-chinese-content

RUN_ID: run-2026-02-27-sync-filename-rollback-keep-chinese-content
OWNER: codex
PRIORITY: P1

## Goal
Restore SYNC filenames back to the original English names while keeping Chinese
content/notes inside files. Remove naming drift introduced in prior run.

## Scope (Required)
- `SYNC/`
- `README.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/CODEX_ONBOARDING_CONSTITUTION.md`
- `docs/PROJECT_GUIDE.md`
- `TASKS/STATE.md`
- `TASKS/TASK-sync-filename-rollback-keep-chinese-content.md`
- `reports/run-2026-02-27-sync-filename-rollback-keep-chinese-content/`

## Non-goals
- No change to qf/task/ship automation behavior.
- No change to wealth/quant strategy content.

## Acceptance
- [x] Command(s) pass: `make verify`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [x] Regression guardrail added/updated if applicable (N/A: naming/reference correction only)

## Inputs
- User clarification: only notes/content should be Chinese; SYNC filenames should
  remain unchanged.

## Steps (Optional)
1. Rename SYNC filenames back to original English names.
2. Update all references from Chinese SYNC paths to original paths.
3. Verify and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: stale references in docs.
- Rollback plan: revert this RUN diff.
