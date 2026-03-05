# TASK: vnext release cleanup (reset task/report history)

RUN_ID: run-2026-03-05-ops-vnext-release
PROJECT_ID: project-0
STATUS: active

## Goal
清理历史 task/report 噪音，只保留最小开发设计阶段骨架，并提交新版本 PR。

## Scope
- `TASKS/`
- `reports/`
- `tools/`
- `tests/`
- `docs/`

## Acceptance
- [ ] 历史 `TASKS/TASK-*` 与 `reports/*` 已清理
- [ ] `TASKS/STATE.md`、`TASKS/QUEUE.md` 为新版本最小骨架
- [ ] 无单一主入口，直连脚本可用（至少 `python3 tools/ops_init.py -status` 可运行）
- [ ] 变更已提交并创建 PR
