# TASK: vnext release cleanup (reset task/report history)

RUN_ID: run-2026-03-05-ops-vnext-release
PROJECT_ID: project-0
STATUS: active

## Goal
清理历史 task/report 噪音，并把开发设计阶段的核心流程收敛到最小可用骨架；当前增量重点是把 `learn` 重构为 `PROJECT_GUIDE` 驱动的真同频流程。

## Scope
- `TASKS/`
- `reports/`
- `tools/`
- `tests/`
- `docs/`

## Acceptance
- [ ] 历史 `TASKS/TASK-*` 与 `reports/*` 已清理
- [ ] `TASKS/STATE.md`、`TASKS/QUEUE.md` 为新版本最小骨架
- [ ] 无单一主入口，直连脚本可用（至少 `python3 tools/init.py -status` 可运行）
- [ ] `python3 tools/learn.py` 仅使用 app-server true plan mode，不再允许 exec fallback
- [ ] `docs/PROJECT_GUIDE.md` 作为 `learn` 主课程，按题驱动口述同频
- [ ] `learn` 去掉考试机制，改为全量逐题口述 + 证据 + 主线回拉
- [ ] 变更已提交并创建 PR
