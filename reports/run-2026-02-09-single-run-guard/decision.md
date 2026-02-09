# Decision

RUN_ID: `run-2026-02-09-single-run-guard`

## Why
- 防串单（单任务单 RUN_ID）

## Options considered
- 只在 ship.sh 里做轻量护栏 + pytest 保护

## Risks / Rollback
- 风险：少数路径可能未被文件列表覆盖
- 回滚：移除护栏与测试
## Verify
- `make verify`（已通过）
