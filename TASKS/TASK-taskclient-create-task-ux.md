# TASK: taskclient create-task ux

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskclient-create-task-ux
PROJECT_ID: quant-factory-os
STATUS: done
PRIORITY: P1

## Goal
优化 `taskclient --create-task` 的使用体验，在不破坏当前 JSON schema 的前提下，让它更适合日常直接使用。

## Scope
- `tools/taskclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `docs/FILE_INDEX.md`
- `docs/WORKFLOW.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不改 task JSON schema。
- 不做交互式 wizard。
- 不重写 pick-next 行为。

## Acceptance
- [x] `--run-id` 可省略，默认使用当前 runtime run
- [x] `--scope/--input/--non-goal/--acceptance` 支持重复传参和逗号分隔
- [x] 支持创建后立即绑定 active task
- [x] Command(s) pass: `python3 tools/taskclient.py --create-task --title "ux sample task" --goal "验证 create-task 体验优化。" --scope "tools/,docs/" --non-goal "不改 schema,不改 ship" --input "AGENTS.md,docs/WORKFLOW.md" --acceptance "docs updated,task json created" --activate`
- [x] Command(s) pass: `python3 -m py_compile tools/taskclient.py tools/taskstore.py`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `tools/taskclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`

## Risks / Rollback
- Risks: CLI 参数行为更灵活后，需要保持输出仍可预测。
- Rollback plan: 回退 `create-task` 的默认 run 和列表参数扩展，只保留严格单值模式。
