# TASK: project-guide-sync-first-handoff

RUN_ID: run-2026-02-27-project-guide-sync-first-handoff
OWNER: codex
PRIORITY: P1

## Goal
Refine `chatlogs/PROJECT_GUIDE.md` to make "sync-first + seamless handoff"
the primary operating logic, while preserving wealth/quant project appendix content.

## Scope (Required)
- `chatlogs/PROJECT_GUIDE.md`
- `TASKS/TASK-project-guide-sync-first-handoff.md`
- `reports/run-2026-02-27-project-guide-sync-first-handoff/`

## Non-goals
- Changing automation scripts or CLI behavior.
- Editing wealth/quant appendix technical roadmap content.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- User priority: 同频优先，不先纠结操作层。
- Constraint: 保留财富项目相关内容。

## Steps (Optional)
1. Add sync-first handoff protocol with explicit "latest conversation continuity".
2. Clarify init/readiness/handoff sequence for reconnect scenarios.
3. Preserve appendix A wealth/quant sections unchanged.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: wording update may conflict with old command descriptions.
- Rollback plan: revert this task diff.
