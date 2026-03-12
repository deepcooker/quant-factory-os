# TASK: taskclient pick next

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskclient-pick-next
PROJECT_ID: quant-factory-os
STATUS: done
PRIORITY: P1

## Goal
新增一个 Python-first 的 task picker，先替代旧 `task.sh` 中“从 queue 选择下一个 task 并绑定 runtime_state”的核心职责。

## Scope
- `tools/taskclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `AGENTS.md`
- `docs/FILE_INDEX.md`
- `docs/WORKFLOW.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写旧 `task.sh` 的 task 模板生成逻辑。
- 不接 ship / PR / merge 流程。
- 不全量迁移历史 `QUEUE.md` 内容。

## Acceptance
- [x] 新增 `python3 tools/taskclient.py --pick-next`
- [x] picker 读取 `TASKS/QUEUE.json` 并绑定 active task 到 `runtime_state`
- [x] picker 会把 queue item 状态写回 JSON
- [x] Command(s) pass: `python3 tools/taskclient.py --pick-next`
- [x] Command(s) pass: `python3 -m py_compile tools/taskclient.py tools/taskstore.py tools/project_config.py`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `tools/taskstore.py`
- `tools/project_config.py`
- `TASKS/QUEUE.json`
- `TASKS/TASK-appserverclient-taskstore-integration.json`

## Risks / Rollback
- Risks: 当前 queue 仍是部分回填，picker 只能稳定服务已进入 JSON 的工作项。
- Rollback plan: 移除 `tools/taskclient.py`，恢复人工直接更新 `runtime_state`。
