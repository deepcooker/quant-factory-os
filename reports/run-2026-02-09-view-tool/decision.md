# Decision

RUN_ID: `run-2026-02-09-view-tool`

## Why
- 降低只读查看权限摩擦（统一使用受控 viewer），并避免护栏因遗留文件误拦截

## Options considered
- 只新增受控 `tools/view.sh`，不扩展 sed/cat/rg；护栏改为仅检查 staged 列表

## Risks / Rollback
- 风险：路径/行数限制过严导致需要频繁分段
- 回滚：移除 view.sh 与政策变更

## Verify
- `make verify`（已通过）
