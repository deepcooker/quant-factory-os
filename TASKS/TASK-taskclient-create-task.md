# TASK: taskclient create task

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskclient-create-task
PROJECT_ID: quant-factory-os
STATUS: done
PRIORITY: P1

## Goal
给 `tools/taskclient.py` 增加一个最小 JSON-first task bootstrap 入口，用来创建新的 `TASKS/TASK-*.json` 和兼容 `md` 视图，并可选追加到 `TASKS/QUEUE.json`。

## Scope
- `tools/taskclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `AGENTS.md`
- `docs/FILE_INDEX.md`
- `docs/WORKFLOW.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不复刻旧 `task.sh` 的交互式模板流程。
- 不实现复杂的 queue 规划或批量切片。
- 不改 ship / PR 链。

## Acceptance
- [x] `tools/taskclient.py` 支持创建新的 task JSON/MD
- [x] 创建入口支持可选写入 `TASKS/QUEUE.json`
- [x] Command(s) pass: `python3 tools/taskclient.py --create-task --title "..." --goal "..." --scope tools/`
- [x] Command(s) pass: `python3 -m py_compile tools/taskclient.py tools/taskstore.py tools/project_config.py`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `tools/taskclient.py`
- `tools/taskstore.py`
- `TASKS/QUEUE.json`
- `TASKS/_SCHEMA.task.json`
- `TASKS/_SCHEMA.queue.json`

## Risks / Rollback
- Risks: 目前 create-task 仍是最小参数版，后续还需要更严格的字段校验和 title/slug 规范。
- Rollback plan: 移除 `taskclient` 的 create-task 分支，继续只保留 pick-next。
