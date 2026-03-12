# TASK: taskclient schema tightening

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskclient-schema-tightening
PROJECT_ID: quant-factory-os
STATUS: done
PRIORITY: P1

## Goal
把 `taskclient --create-task` 和 `TASKS/_SCHEMA.task.json` 收到一版更稳定的字段口径，补齐必要字段、默认值和最小校验。

## Scope
- `tools/taskclient.py`
- `tools/taskstore.py`
- `TASKS/_SCHEMA.task.json`
- `docs/FILE_INDEX.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不做复杂交互式 wizard。
- 不做完整 JSON schema 校验器。
- 不清理本轮之前生成的样例 task。

## Acceptance
- [x] `TASKS/_SCHEMA.task.json` 与当前 task payload 字段对齐
- [x] `taskclient --create-task` 支持 priority/non-goal/input/acceptance/risks/rollback-plan
- [x] create-task 有最小字段校验与重复文件保护
- [x] `save_queue()` 会刷新 `updated_at`
- [x] Command(s) pass: `python3 tools/taskclient.py --create-task --title "schema sample task" --goal "验证 schema 收紧。" --scope docs/ --run-id run-2026-03-11-vnext-release-baseline --priority P2 --non-goal "不改运行时" --input AGENTS.md --acceptance "owner docs updated" --queue`
- [x] Command(s) pass: `python3 -m py_compile tools/taskclient.py tools/taskstore.py`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `TASKS/_SCHEMA.task.json`
- `tools/taskclient.py`
- `tools/taskstore.py`

## Risks / Rollback
- Risks: 当前仍是约定式校验，不是完整 schema engine。
- Rollback plan: 回退新增参数和校验，只保留最初最小 create-task 入口。
