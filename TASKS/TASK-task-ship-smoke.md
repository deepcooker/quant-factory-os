# TASK: task/ship smoke

RUN_ID: run-2026-03-06-task-ship-smoke
PROJECT_ID: project-0
STATUS: active

## Goal
用一个最小无害改动真实演练 `tools/task.sh -> tools/ship.sh`，验证新的 branch continuity 策略不会把会话带到错误基线。

## Scope
- `TASKS/`
- `reports/`
- `docs/`

## Acceptance
- [ ] 真实执行 `tools/task.sh -> tools/ship.sh`
- [ ] 发货前后 active branch continuity 符合预期
- [ ] `make verify` 通过
- [ ] 更新 `reports/run-2026-03-06-task-ship-smoke/summary.md`
- [ ] 更新 `reports/run-2026-03-06-task-ship-smoke/decision.md`

## Notes
- 这是 smoke task，不引入新的工具行为变更。
- 只允许最小无害改动，用于验证真实发货链路。
