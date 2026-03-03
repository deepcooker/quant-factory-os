# Orientation Draft

PROJECT_ID: `project-0`
RUN_ID: `run-2026-03-02-qf-ready`
Generated At (UTC): 2026-03-03T16:36:19.372873+00:00
Mode: discussion-only (not execution evidence)
Open Queue Items: 0

## Direction Options
- id=`ready-exit-resolution` | priority=`P0` | score=1738
  - title: P0: ready 先处理未收尾 run（收尾/抛弃）
  - why: 避免把历史中断状态混入新需求，先做生命周期分流。
  - benefit: 减少混乱上下文和重复执行。
  - risk: 增加一次显式确认步骤。
  - cost: S
  - dependencies: TASKS/STATE.md, reports/<RUN_ID>/ship_state.json
- id=`ready-strong-brief` | priority=`P1` | score=1080
  - title: P1: ready 输出最强认知摘要与证据链
  - why: ready 通过后立即给出项目理解、宪法解读、工作流和下一步建议。
  - benefit: 降低同频误差，提升决策速度。
  - risk: 摘要质量受输入文档完整性影响。
  - cost: S
  - dependencies: SYNC/READ_ORDER.md, reports/<RUN_ID>/sync_report.json
- id=`discussion-execution-split` | priority=`P2` | score=930
  - title: P1: 讨论态与执行态证据分层
  - why: 未确认方案只写讨论区，确认后再写 reports 执行证据。
  - benefit: 保持 report 可审计且低噪声。
  - risk: 需要清晰迁移边界。
  - cost: M
  - dependencies: SYNC/discussion/, reports/<RUN_ID>/
- id=`post-exec-drift-review` | priority=`P3` | score=666
  - title: P2: 执行后偏差审计与自动修复
  - why: 需求完成后自动检查目标/实现/测试/文档偏差并回补。
  - benefit: 形成闭环，减少累计偏差。
  - risk: 规则过严会增加时间成本。
  - cost: M
  - dependencies: reports/<RUN_ID>/summary.md, reports/<RUN_ID>/decision.md
- id=`council-contract` | priority=`P4` | score=302
  - title: P2: 多角色评审博弈 -> 统一执行契约
  - why: 产品/架构/研发/测试独立评审，再收敛成单一 contract。
  - benefit: 减少单视角偏差，提高执行稳定性。
  - risk: 初期输出可能偏模板化。
  - cost: M
  - dependencies: orient choice, task contract

## Recommended
- `ready-exit-resolution`

## Next Command
- `tools/qf choose RUN_ID=run-2026-03-02-qf-ready OPTION=ready-exit-resolution`
