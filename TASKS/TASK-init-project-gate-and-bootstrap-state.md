# TASK-init-project-gate-and-bootstrap-state

## Goal
增加 `bootstrap_state.is_inited` 门禁，并在 `appserverclient` 中引入 `--init-project` 预检入口，禁止未初始化项目直接进入 baseline 主线。

## Scope
- `tools/project_config.json`
- `tools/project_config.template.json`
- `tools/project_config.py`
- `tools/appserverclient.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `AGENTS.md`

## Acceptance
- project_config 引入 `bootstrap_state.is_inited`
- 未初始化项目无法直接执行 baseline 主线
- `--init-project` 只有在 `is_inited` 不是 `Y` 且 owner docs 全为空时才允许进入下一步
