# TASK: slice-next: P0: 收敛 learn 的日常同频体验 - core delivery

RUN_ID: run-2026-03-06-slice-next-p0-learn-core-delivery
OWNER: <you>
PRIORITY: P1

## Goal
当前合同直接把 learn 和 PROJECT_GUIDE 同频列为增量重点；结合最新 learn focus，下一步最合理的是继续收敛强同频输出和主线回拉体验：继续围绕当前 active run 收敛 learn 主线、流程边界和日常使用体验。

## Scope (Required)
- `tools/learn.py`
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `AGENTS.md`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [ ] deliver selected direction option `learn-daily-ergonomics` with bounded scope
- [ ] command(s) pass: make verify
- [ ] reports summary/decision updated for this run
- [ ] owner docs updated in same run when behavior/rules changed
- [ ] critical path regression tests added or refreshed
- [ ] failure-path assertions are explicit and actionable
- [ ] bash tools/legacy.sh review STRICT=1 AUTO_FIX=1 passes
- [ ] decision records accepted tradeoffs and residual risks
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- Links / files / references
- If data is needed, specify allowed sample constraints (max rows, time window)

## Steps (Optional)
Suggested approach, if you have one.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
- Rollback plan:
