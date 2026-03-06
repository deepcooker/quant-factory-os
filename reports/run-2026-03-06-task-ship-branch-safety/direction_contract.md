# Direction Contract

RUN_ID: `run-2026-03-06-task-ship-branch-safety`

Selected Option: `task-ship-branch-safety`
Title: `P0: keep active run branch on task/ship handoff`

## Execution Goal
- 修复 `tools/task.sh` / `tools/ship.sh` 在收尾时强制切到 `main` 导致活跃 run 分支和 Python-first 基线错位的问题。

## Scope Hint
- `tools/task.sh`
- `tools/ship.sh`
- `tests/`
- `TASKS/`
- `reports/`
- `docs/`
