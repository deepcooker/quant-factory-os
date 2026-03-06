# Execution Contract

PROJECT_ID: `project-0`
RUN_ID: `run-2026-03-06-automation-1-0-definition`
Generated At (UTC): 2026-03-06T15:51:49.114194+00:00
Direction: P2: 收敛执行链的人体工学
Arbiter Summary: blockers=1 warnings=0 conditions=2

## Convergence Input
- architect: ready gate missing; lifecycle invariant is broken
- qa: ready gate missing; test baseline cannot be trusted

## Disagreements
- role decisions are not uniform yet; arbiter must converge conditions.
- blocking evidence checks exist and must be resolved before final execution.

## Execution Goal
- 如果当前重点从讨论边界转向真正落地，那么最值得做的是把 do/review/ship 的提示、失败恢复和证据更新体验继续压顺。

## Non Goals
- 不扩展到当前 selected direction 之外的其他流程层级
- 不在本轮 contract 中引入新的业务项目范围
- 不跳过 verify/review/docs freshness gate

## Scope
- `tools/legacy.sh`
- `tools/task.sh`
- `tools/ship.sh`
- `docs/WORKFLOW.md`
- `reports/`

## Acceptance
- deliver selected direction option `execution-path-ergonomics` with bounded scope
- command(s) pass: make verify
- reports summary/decision updated for this run
- owner docs updated in same run when behavior/rules changed
- condition closed: architect: ready gate missing; lifecycle invariant is broken
- condition closed: qa: ready gate missing; test baseline cannot be trusted
- all blocker-level evidence checks are resolved
- bash tools/legacy.sh review STRICT=1 AUTO_FIX=1 passes
- decision records accepted tradeoffs and residual risks

## Next Command
- `python3 tools/slice_task.py RUN_ID=run-2026-03-06-automation-1-0-definition`
