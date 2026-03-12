# TASK: taskstore bootstrap

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskstore-bootstrap
PROJECT_ID: quant-factory-os
STATUS: done
PRIORITY: P1

## Goal
新增一个最小 `tools/taskstore.py`，统一读写 `TASKS/QUEUE.json` 与 `TASKS/TASK-*.json`，并先让 `evidence.py` 依赖这层读取运行态 task。

## Scope
- `tools/taskstore.py`
- `tools/evidence.py`
- `tools/project_config.json`
- `docs/FILE_INDEX.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写全部 task/queue 调用方。
- 不实现完整 task picker。
- 不删除现有 md 兼容视图。

## Acceptance
- [x] 新增 `tools/taskstore.py`
- [x] `taskstore` 可读取 active task、指定 task 和 queue
- [x] `tools/evidence.py` 通过 `taskstore` 解析当前 run 的 task_id
- [x] Command(s) pass: `python3 tools/taskstore.py --active-task`
- [x] Command(s) pass: `python3 -m py_compile tools/taskstore.py tools/evidence.py tools/project_config.py`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `tools/project_config.json`
- `TASKS/QUEUE.json`
- `TASKS/TASK-task-queue-json-bootstrap.json`
- `TASKS/TASK-compat-shell-archive.json`

## Risks / Rollback
- Risks: 当前 queue 仍是部分回填，`taskstore` 只能稳定服务已迁移的 JSON 任务。
- Rollback plan: 恢复 `evidence.py` 直接读取 runtime_state，并移除 `tools/taskstore.py`。
