# Decision

RUN_ID: `run-2026-02-09-enter`

## Why
- 减少每次进入 codex 的手工步骤（统一入口检查）

## Options considered
- 仅新增 enter.sh，不修改现有通过路径

## Risks / Rollback
- 风险：对不干净工作区的失败可能阻断使用
- 回滚：移除 enter.sh 与 Allowed Commands 更新

## Verify
- `make verify`（已通过）
