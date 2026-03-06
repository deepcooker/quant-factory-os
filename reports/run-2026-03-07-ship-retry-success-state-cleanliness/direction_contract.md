# Direction Contract

PROJECT_ID: `project-0`
RUN_ID: `run-2026-03-07-ship-retry-success-state-cleanliness`
Generated At (UTC): 2026-03-06T16:20:20.147452+00:00
Selected Option: `execution-path-ergonomics`
Title: P2: 收敛执行链的人体工学

## Why
- 当前证据已经反复触及 verify/review/ship 约束；如果要往执行层推进，最合理的是优先压顺执行链的人体工学与失败恢复。

## Scope Hint
- `tools/legacy.sh`
- `tools/task.sh`
- `tools/ship.sh`
- `docs/WORKFLOW.md`
- `reports/`

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
- `python3 tools/council.py RUN_ID=run-2026-03-07-ship-retry-success-state-cleanliness`
