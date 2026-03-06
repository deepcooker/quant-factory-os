# TASK: task/ship branch safety

RUN_ID: run-2026-03-06-task-ship-branch-safety
PROJECT_ID: project-0
STATUS: active

## Goal
修复 `tools/task.sh` / `tools/ship.sh` 在收尾时强制切到 `main` 导致活跃 run 分支和 Python-first 基线错位的问题。

## Scope
- `tools/task.sh`
- `tools/ship.sh`
- `tests/`
- `TASKS/`
- `reports/`
- `docs/`

## Acceptance
- [ ] `tools/task.sh` 在活跃 run 分支上不会把收尾流程带到错误基线
- [ ] `tools/ship.sh` 的分支切换策略与当前 run / branch continuity 一致
- [ ] 新增或刷新关键回归测试
- [ ] `make verify` 通过
- [ ] 更新 `reports/run-2026-03-06-task-ship-branch-safety/summary.md`
- [ ] 更新 `reports/run-2026-03-06-task-ship-branch-safety/decision.md`

## Notes
- 本任务直接基于本轮真实故障：`tools/task.sh` 把会话从 `run-2026-03-05-ops-vnext-release` 切到过旧 `main`，导致 `tools/codex_transport.py` 等基线文件缺失。
