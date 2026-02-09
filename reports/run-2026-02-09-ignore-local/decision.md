# Decision

RUN_ID: `run-2026-02-09-ignore-local`

## Why
- 避免 enter/ship 被本地运行产物阻塞

## Options considered
- 仅确认 `.gitignore` 已包含所需规则，不再重复添加

## Risks / Rollback
- 风险：无
- 回滚：无（未改动 .gitignore）

## Verify
- `make verify`（已通过）
