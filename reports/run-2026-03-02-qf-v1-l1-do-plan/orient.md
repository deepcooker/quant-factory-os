# Orientation Report

RUN_ID: `run-2026-03-02-qf-v1-l1-do-plan`
Generated At (UTC): 2026-03-02T04:24:55.045632+00:00
Open Queue Items: 0

## Direction Options
- id=`stability-do-plan` | priority=`P0` | score=746
  - title: P0: qf do/plan 稳定性硬化
  - why: 降低执行摩擦，优先修复 do/plan 断链与脏工作区冲突。
  - scope_hint: tools/qf, tests/
- id=`l1-direction-layer` | priority=`P1` | score=272
  - title: P1: L1 方向层（orient/choose）
  - why: 在执行前先做方向确认与优先级选择，建立两层任务模型。
  - scope_hint: tools/qf, TASKS/, docs/WORKFLOW.md, SYNC/
- id=`council-review-loop` | priority=`P2` | score=144
  - title: P2: 多角色评审博弈（architect/qa/dev/product）
  - why: 通过独立思考与冲突收敛提高方案质量，避免单视角偏差。
  - scope_hint: tools/qf, docs/WORKFLOW.md, reports/

## Recommended
- `stability-do-plan`

## Next Command
- `tools/qf choose RUN_ID=run-2026-03-02-qf-v1-l1-do-plan OPTION=stability-do-plan`
