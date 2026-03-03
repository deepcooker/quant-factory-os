# Execution Contract

PROJECT_ID: `project-0`
RUN_ID: `run-2026-03-02-qf-ready`
Generated At (UTC): 2026-03-03T04:51:38.143087+00:00
Direction: P1: ready 输出最强认知摘要与证据链
Arbiter Summary: blockers=0 warnings=0 conditions=0

## Convergence Input
- no unresolved role conditions

## Converged Task Slices
- task_id: `slice-1` | title: P1: ready 输出最强认知摘要与证据链 - core delivery
  - goal: ready 通过后立即给出项目理解、宪法解读、工作流和下一步建议。
  - scope: tools/qf, SYNC/, docs/WORKFLOW.md
  - acceptance:
    - deliver selected direction option `ready-strong-brief` with bounded scope
    - command(s) pass: make verify
    - reports summary/decision updated for this slice
- task_id: `slice-2` | title: P1: ready 输出最强认知摘要与证据链 - enforce guardrail tests
  - goal: Add or refine guardrail tests to lock behavior of the selected direction.
  - scope: tests/, tools/qf
  - acceptance:
    - critical path regression tests added or refreshed
    - failure-path assertions are explicit and actionable
- task_id: `slice-3` | title: P1: ready 输出最强认知摘要与证据链 - evidence and docs alignment
  - goal: Keep evidence and owner docs aligned with final behavior of this direction.
  - scope: AGENTS.md, docs/WORKFLOW.md, SYNC/, reports/{RUN_ID}/
  - acceptance:
    - owner docs updated in same run when behavior/rules changed
    - tools/qf review STRICT=1 AUTO_FIX=1 passes
    - decision records accepted tradeoffs and residual risks

## Next Command
- `tools/qf slice RUN_ID=run-2026-03-02-qf-ready`
