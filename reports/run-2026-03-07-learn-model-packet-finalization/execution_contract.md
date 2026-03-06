# Execution Contract

PROJECT_ID: `project-0`
RUN_ID: `run-2026-03-07-learn-model-packet-finalization`
Generated At (UTC): 2026-03-06T17:05:56.466592+00:00
Direction: P0: 收敛 learn 的日常同频体验
Arbiter Summary: blockers=0 warnings=0 conditions=0

## Convergence Input
- no unresolved role conditions

## Execution Goal
- 当前合同直接把 learn 和 PROJECT_GUIDE 同频列为增量重点；结合最新 learn focus，下一步最合理的是继续收敛强同频输出和主线回拉体验：继续围绕当前 active run 收敛 learn 主线、流程边界和日常使用体验。

## Non Goals
- 不扩展到当前 selected direction 之外的其他流程层级
- 不在本轮 contract 中引入新的业务项目范围
- 不跳过 verify/review/docs freshness gate
- 不同时改造无关执行链脚本

## Scope
- `tools/learn.py`
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `AGENTS.md`

## Acceptance
- deliver selected direction option `learn-daily-ergonomics` with bounded scope
- command(s) pass: make verify
- reports summary/decision updated for this run
- owner docs updated in same run when behavior/rules changed
- critical path regression tests added or refreshed
- failure-path assertions are explicit and actionable
- bash tools/legacy.sh review STRICT=1 AUTO_FIX=1 passes
- decision records accepted tradeoffs and residual risks

## Next Command
- `python3 tools/slice_task.py RUN_ID=run-2026-03-07-learn-model-packet-finalization`
