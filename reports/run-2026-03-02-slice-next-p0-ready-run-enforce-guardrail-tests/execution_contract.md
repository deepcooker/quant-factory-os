# Execution Contract

RUN_ID: `run-2026-03-02-slice-next-p0-ready-run-enforce-guardrail-tests`
Generated At (UTC): 2026-03-02T08:04:01.869660+00:00
Direction: P0: ready 先处理未收尾 run（收尾/抛弃）
Arbiter Summary: blockers=0 warnings=0 conditions=0

## Convergence Input
- no unresolved role conditions

## Converged Task Slices
- task_id: `slice-1` | title: P0: ready 先处理未收尾 run（收尾/抛弃） - core delivery
  - goal: 避免把历史中断状态混入新需求，先做生命周期分流。
  - scope: tools/qf, tests/
  - acceptance:
    - deliver selected direction option `ready-exit-resolution` with bounded scope
    - command(s) pass: make verify
    - reports summary/decision updated for this slice
- task_id: `slice-2` | title: P0: ready 先处理未收尾 run（收尾/抛弃） - enforce guardrail tests
  - goal: Add or refine guardrail tests to lock behavior of the selected direction.
  - scope: tests/, tools/qf
  - acceptance:
    - critical path regression tests added or refreshed
    - failure-path assertions are explicit and actionable
- task_id: `slice-3` | title: P0: ready 先处理未收尾 run（收尾/抛弃） - evidence and docs alignment
  - goal: Keep evidence and owner docs aligned with final behavior of this direction.
  - scope: AGENTS.md, docs/WORKFLOW.md, SYNC/, reports/{RUN_ID}/
  - acceptance:
    - owner docs updated in same run when behavior/rules changed
    - tools/qf review STRICT=1 AUTO_FIX=1 passes
    - decision records accepted tradeoffs and residual risks

## Next Command
- `tools/qf slice RUN_ID=run-2026-03-02-slice-next-p0-ready-run-enforce-guardrail-tests`
