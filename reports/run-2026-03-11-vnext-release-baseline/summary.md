# Summary

RUN_ID: `run-2026-03-11-vnext-release-baseline`

## What changed
- 绑定新的 active run/task，用于收敛 `run` 扶正与 `runtime_state` 唯一真相源。
- 删除 `TASKS/STATE.md` 镜像口径，改为只认 `tools/project_config.json -> runtime_state`。
- 给 `runtime_state` 增加 `current_task_id`，并允许后续过渡到“有 run、无 task”状态。
- 更新 formal mainline 文档，只保留 `project_config.json` 作为活动指针真相源。
- 调整 `tools/evidence.py` 和 `tools/gitclient.py`，不再依赖 `TASKS/STATE.md`。

## Commands / Outputs
- `python3 -m py_compile tools/project_config.py tools/gitclient.py tools/evidence.py tools/appserverclient.py` -> pass
- `python3 tools/project_config.py` -> pass; 新 `runtime_state` 输出包含 `current_task_id=task-vnext-release-baseline`
- `python3 tools/appserverclient.py --learnbaseline` -> pass; baseline 复用路径按新 `runtime_state` 工作
- `python3 tools/init.py` -> pass to completion; run/task 输出正确，最终仍因脏工作区返回 `INIT_STATUS: needs_fix`
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass
- `make verify` -> `VERIFY: no tests/task_*.py files present; skipping pytest`

## Notes
- 历史兼容脚本仍可能保留旧 `STATE.md` 引用，本轮只收 formal mainline。

## Follow-up task
- 新建 `task-compat-shell-archive`，把 `legacy.sh` / `task.sh` / `observe.sh` / `ship.sh` 归档到 `tools/backup/`，原路径改成转发 wrapper，避免旧引用立即断裂。

## Compatibility archive update
- 已创建 `tools/backup/`，并把 `legacy.sh` / `task.sh` / `observe.sh` / `ship.sh` 迁入归档目录。
- 原 `tools/*.sh` 路径现在只保留最小 wrapper，执行时先打印 deprecated 提示，再转发到 `tools/backup/`。
- formal mainline 文档已同步说明这些 shell 入口只是过渡兼容层。

## Task JSON bootstrap
- 新增 `TASKS/QUEUE.json` 作为 queue 机器真相源，当前只覆盖 active/open 工作项。
- 新增 `TASKS/TASK-vnext-release-baseline.json` 与 `TASKS/TASK-compat-shell-archive.json` 作为当前 run 下 task 真相源。
- `tools/project_config.json` 新增 `runtime_state.current_task_json_file` 和 `task_registry`，把 task/queue JSON 指针写死到运行时配置。
- `TASKS/*.md` 和 `TASKS/QUEUE.md` 现在只保留迁移期人类可读视图。

## Python archive update
- `tools/run_a9.py` 已归档到 `tools/backup/run_a9.py`；当前仓库未发现正式入口引用它。

## Active task shift
- 当前 active task 已切到 `task-task-queue-json-bootstrap`，用于承接 `task.json / queue.json` 机器真相源和 `runtime_state.current_task_json_file` 的引入。

## Taskstore bootstrap
- 新增 `tools/taskstore.py`，提供 active task、指定 task、queue 和 `run_id -> task_id` 的统一 JSON 读取入口。
- `tools/evidence.py` 已先切到 `taskstore.find_task_id_for_run()`，验证公共层可以服务现有主线工具。
- 当前 active task 已继续切到 `task-taskstore-bootstrap`。

## Active task shift
- 当前 active task 已切到 `task-gitclient-taskstore-integration`，用于承接 `gitclient` 对 task JSON 的接入。

## Gitclient taskstore integration
- `tools/gitclient.py` 的 `resolve_commit_message()` 现在优先读取 active task JSON。
- 当前优先级变为：显式 `--commit` message -> active task JSON 的 `title/task_id` -> `runtime_state.current_task_file/current_task_id` -> `current_run_id` -> 时间戳 fallback。

## Appserverclient taskstore integration
- `tools/appserverclient.py` 现在会通过 `taskstore` 读取 active task JSON。
- `APP_RUNTIME_STATE_*` 之后会追加 `APP_ACTIVE_TASK_*` 日志块，显式打印当前 `task_id/title/status/run_id`。
- 这一步只补 task 上下文感知，不改 learn/fork/current-turn 的 app-server 调用顺序。

## Taskclient bootstrap
- 新增 `tools/taskclient.py --pick-next`，先承担 Python-first 的 queue 选择和 runtime 绑定职责。
- `tools/taskstore.py` 新增 queue 写回和 active task 绑定能力，供 `taskclient` 复用。
- 这一步只替代旧 `task.sh` 的最小核心职责，不接 ship/PR。

## Taskclient create-task
- `tools/taskclient.py` 新增 `--create-task`，可以直接生成 `TASKS/TASK-*.json` 和兼容 `md` 视图。
- 新入口支持可选 `--queue`，把新 task 追加进 `TASKS/QUEUE.json`。
- 这一步仍保持最小参数模型：`title / goal / scope / run_id`。
- 为验证路径已实际生成 `TASKS/TASK-bootstrap-sample-task.json` / `TASKS/TASK-bootstrap-sample-task.md`，并追加 `queue-bootstrap-sample-task` 到 `TASKS/QUEUE.json`。

## Taskclient schema tightening
- `TASKS/_SCHEMA.task.json` 已补齐 `risks` / `rollback_plan`，与当前 task payload 对齐。
- `taskclient --create-task` 现在支持 `--priority --non-goal --input --acceptance --risks --rollback-plan`，并带最小字段校验与重复 slug 保护。
- `taskstore.save_queue()` 现在会自动刷新 `QUEUE.json.updated_at`。

## Taskclient create-task UX
- `create-task` 现在默认复用当前 runtime run，不再强制每次显式传 `--run-id`。
- `--scope --input --non-goal --acceptance` 现在支持重复传参和逗号分隔。
- 新增 `--activate`，创建后可以直接把新 task 绑定成 active task。
- 已用 `TASKS/TASK-ux-sample-task.json` 做真实验证，确认 `--activate` 生效；验证后已把 runtime 指针切回本轮正式任务，避免后续上下文漂移。

## Task wrapper reroute
- `tools/task.sh --next` 和 `tools/task.sh --pick queue-next` 现在直接转到 `python3 tools/taskclient.py --pick-next`。
- 其他参数仍会回退到 `tools/backup/task.sh`，所以这一刀只是把主线路径从 shell wrapper 上移开，不是一次性硬删兼容链。
- 已用真实 `bash tools/task.sh --next` 验证 reroute 生效；验证后把样例 queue item 恢复到 `pending`，并把 runtime 指针切回本轮正式任务，避免样例任务继续占住上下文。

## Taskclient unify entry
- 当前 active task 已切到 `task-taskclient-unify-entry`，用于承接 `taskstore -> taskclient` 合并和 `task.sh` 直接弃用。
- `tools/taskclient.py` 现在同时承接 task/queue JSON 的公共读写、queue 选择、active task 读取与 task bootstrap；对外主命令收口为 `--next` 和 `--create`。
- `tools/appserverclient.py`、`tools/gitclient.py`、`tools/evidence.py` 已改为直接从 `taskclient` 导入 task 读取能力，不再依赖独立 `taskstore` 入口。
- `tools/taskstore.py` 已降级成兼容转发模块，历史实现归档到 `tools/backup/taskstore.py`；`tools/task.sh` 现在直接报废弃并退出，不再回退到 `tools/backup/task.sh`。
- 本轮 gate 中 `python3 tools/appserverclient.py --fork-current` 仍被 `/root/.codex/sessions` 权限阻塞，错误为 `permission denied`；这次本地重构未依赖该步骤。

## Commands / Outputs (compatibility archive)
- `bash tools/legacy.sh --help || true` -> pass; wrapper 生效并转发到 `tools/backup/legacy.sh`
- `python3 tools/project_config.py` -> pass; `runtime_state.current_task_id=task-compat-shell-archive`，`current_task_file=TASKS/TASK-compat-shell-archive.md`
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline` -> pass

## Legacy entrypoint archive cleanup
- 当前 active task 已切到 `task-archive-legacy-tool-entrypoints`，只做正式 `tools/` 白名单清理。
- 旧入口已从 `tools/` 顶层移出并归档到 `tools/backup/`：
  - `learn.py`
  - `ready.py`
  - `orient.py`
  - `choose.py`
  - `council.py`
  - `arbiter.py`
  - `slice_task.py`
  - `run_main.py`
- 旧 shell 顶层入口也已移出正式层，wrapper 版本归档到：
  - `tools/backup/legacy.wrapper.sh`
  - `tools/backup/observe.wrapper.sh`
  - `tools/backup/ship.wrapper.sh`
  - `tools/backup/task.wrapper.sh`
- 正式主流程现阶段只保留：
  - `tools/init.py`
  - `tools/appserverclient.py`
  - `tools/gitclient.py`
  - `tools/taskclient.py`
  - `tools/project_config.py`
- owner docs 已同步到这条主流程白名单，`AGENTS.md`、`docs/WORKFLOW.md`、`docs/FILE_INDEX.md` 不再把上述旧入口放在正式工具面。

## Commands / Outputs (legacy entrypoint archive)
- `python3 tools/taskclient.py --create --title "archive legacy tool entrypoints" ... --activate` -> pass
- `python3 tools/taskclient.py --active-task` -> pass; active task 切到 `task-archive-legacy-tool-entrypoints`
- `python3 tools/project_config.py` -> pass; `runtime_state.current_status=completed`

## Appserverclient summarize / refresh loop
- 当前 active task 已切到 `task-appserverclient-summarize-refresh-baseline-loop`，目标是补齐 current summary 与 baseline refresh 的正式入口。
- `tools/appserverclient.py` 现已新增：
  - `--summarize-current`
  - `--refresh-baseline`
- `tools/project_config.py` 新增 `update_current_summary()`，把 current summary 的来源 thread、摘要正文和 baseline refresh 结果统一写回 `session_registry.current_summary`。
- 真实链路已打通：
  - `--summarize-current` 会在 current fork 上发 summarize prompt，抽取最后一条 agent message，并写回 `session_registry.current_summary.summary_text`
  - `--refresh-baseline` 会只消费 `session_registry.current_summary`，在 baseline thread 上做增量 refresh，并把结果写回 `baseline_refresh_text`

## Commands / Outputs (appserverclient summarize / refresh)
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py` -> pass
- `python3 tools/appserverclient.py --summarize-current` -> pass; 输出 `current_summary_text_start ... current_summary_text_end`
- `python3 tools/appserverclient.py --refresh-baseline` -> pass; 输出 `baseline_refresh_text_start ... baseline_refresh_text_end`
- `python3 tools/project_config.py` -> pass; `session_registry.current_summary` 已包含 `thread_id/thread_path/status/source/model/effort`
