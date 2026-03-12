# TASK: gitclient taskstore integration

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-gitclient-taskstore-integration
PROJECT_ID: quant-factory-os
STATUS: done
PRIORITY: P1

## Goal
让 `tools/gitclient.py` 通过 `taskstore` 读取当前 active task，提交说明优先使用 task JSON 的结构化上下文，而不是继续依赖 `TASKS/*.md` 文件名。

## Scope
- `tools/gitclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `docs/FILE_INDEX.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写 commit / PR / merge 主流程。
- 不改更多 shell 兼容层。
- 不做完整 task title 规范化。

## Acceptance
- [x] `gitclient` 可通过 `taskstore` 读取 active task
- [x] `resolve_commit_message()` 优先使用 task JSON 的 `title/task_id`
- [x] `python3 -m py_compile tools/gitclient.py tools/taskstore.py tools/project_config.py` 通过
- [x] `python3 tools/taskstore.py --active-task` 通过
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `tools/gitclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `TASKS/TASK-taskstore-bootstrap.json`

## Risks / Rollback
- Risks: 当前 task title 仍是自由文本，提交说明格式短期内不会完全统一。
- Rollback plan: 恢复 `gitclient` 对 `runtime_state.current_task_file/current_task_id` 的直接回退逻辑。
