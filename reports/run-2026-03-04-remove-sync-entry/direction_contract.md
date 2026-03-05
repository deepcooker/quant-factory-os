# Direction Contract

PROJECT_ID: `project-0`
RUN_ID: `run-2026-03-04-remove-sync-entry`
Generated At (UTC): 2026-03-05T13:14:05.157973+00:00
Selected Option: `ready-exit-resolution`
Title: P0: ready 先处理未收尾 run（收尾/抛弃）

## Why
- 避免把历史中断状态混入新需求，先做生命周期分流。

## Scope Hint
- `tools/qf`
- `tests/`

## Multi-Role Independent Reviews
- role: `product` | focus: value and scope relevance
  - view: 确认方向是否解决真实问题，并限制在最小可交付范围内。
  - must_hold:
    - 目标可验证
    - 非目标明确
    - 不做伪需求扩张
- role: `architect` | focus: boundary and extensibility
  - view: 检查状态机边界、证据边界、兼容迁移路径是否明确。
  - must_hold:
    - 讨论态与执行态边界清晰
    - 旧流程兼容/迁移说明完整
    - 失败可恢复
- role: `dev` | focus: minimal diff and operability
  - view: 优先小步改动，确保命令链可重复执行并便于调试。
  - must_hold:
    - 最小差异实现
    - 命令输出可操作
    - 错误提示可恢复
- role: `qa` | focus: behavioral regression and gates
  - view: 独立验证门禁和回归，不受开发路径影响。
  - must_hold:
    - 关键路径有回归测试
    - 失败路径有断言
    - 文档门禁可验证

## Delivery Contract
- step: council-review
- step: arbiter-contract
- step: slice-into-tasks
- step: implement
- step: verify
- step: review-and-align
- step: reports-and-ship
- gate: make verify green
- gate: scope remains bounded
- gate: owner docs updated in same run
- gate: reports evidence updated

## Next Command
- `tools/qf council RUN_ID=run-2026-03-04-remove-sync-entry`
