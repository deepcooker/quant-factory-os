# TASK: vnext release baseline

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-vnext-release-baseline
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
扶正 `run` 为当前正式对象，移除 `TASKS/STATE.md` 这类过渡镜像，并让 `tools/project_config.json -> runtime_state` 成为唯一运行时真相源。

## Scope
- `tools/project_config.py`
- `tools/project_config.json`
- `tools/project_config.template.json`
- `tools/gitclient.py`
- `tools/evidence.py`
- `docs/`
- `AGENTS.md`
- `TASKS/`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写 `legacy.sh` 全链路。
- 不在本任务里完整重做新的 task 体系。
- 不扩 `appserverclient` 新命令。

## Acceptance
- [x] `runtime_state` 成为唯一运行时真相源，不再镜像到 `TASKS/STATE.md`
- [x] `runtime_state` 支持 `current_task_id`，并允许“有 run、无 task”状态
- [x] formal mainline 文档口径与新真相源一致
- [x] Command(s) pass: `python3 -m py_compile tools/project_config.py tools/gitclient.py tools/evidence.py tools/appserverclient.py`
- [x] Command(s) pass: `make verify`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `docs/PROJECT_GUIDE.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `tools/project_config.json`
- `TASKS/QUEUE.md`

## Risks / Rollback
- Risks: 历史兼容脚本仍可能保留 `TASKS/STATE.md` 旧引用。
- Rollback plan: 恢复 `tools/project_config.py` 镜像逻辑与 `TASKS/STATE.md` 文件，并回退 owner docs 口径。
