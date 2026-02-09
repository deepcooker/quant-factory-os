# Decision

RUN_ID: `run-2026-02-09-integrate-a9`

## Why
- 打通 a9quant 的最小 dry-run E2E（不跑真实回测）

## Options considered
- 仅用 Python 自检命令验证目录可用并记录日志

## Risks / Rollback
- 风险：dry-run 与真实流程覆盖有限
- 回滚：移除 run_a9 与测试

## Verify
- `make verify`（已通过）

## Evidence paths (additional)
- `reports/run-2026-02-09-integrate-a9/a9_stdout.log`
