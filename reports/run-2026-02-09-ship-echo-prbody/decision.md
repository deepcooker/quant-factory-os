# Decision

RUN_ID: `run-2026-02-09-ship-echo-prbody`

## Why
- 避免再请求读取 PR body（自动输出摘要）

## Options considered
- 在 ship.sh 内部做最小解析与落盘，不改 PR body 结构

## Risks / Rollback
- 风险：PR body 标题改动会影响解析
- 回滚：移除摘录与测试

## Verify
- `make verify`（已通过）

## Mistakes
- 只读越界：曾读取超出 1-200 行范围（tools/ship.sh）。已纠正授权范围，后续超过范围先申请。
