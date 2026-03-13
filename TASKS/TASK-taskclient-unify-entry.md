# TASK: taskclient unify entry

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskclient-unify-entry
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
直接弃用 tools/task.sh，并把 tools/taskstore.py 的公共方法合入 tools/taskclient.py，统一 task 对外入口。

## Scope
- `tools/taskclient.py`
- `tools/taskstore.py`
- `tools/task.sh`
- `tools/appserverclient.py`
- `tools/gitclient.py`
- `tools/evidence.py`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `AGENTS.md`
- `reports/run-2026-03-11-vnext-release-baseline/summary.md`
- `reports/run-2026-03-11-vnext-release-baseline/decision.md`

## Non-goals
- 不重构 gitclient 主线
- 不迁移其他 shell 职责

## Acceptance
- [x] taskclient 支持 --create 和 --next
- [x] taskstore 方法合入 taskclient
- [x] task.sh 直接弃用且不再回退 backup/task.sh
- [x] appserverclient/gitclient/evidence 不再从 taskstore 导入

## Inputs

## Risks / Rollback
- Risks: 
- Rollback plan:
