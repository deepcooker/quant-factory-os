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

## Run-main escalation resolution
- task 机器层新增：
  - `task_summary.run_main_resolution_policy`
  - `task_summary.run_main_resolution`
- `tools/taskclient.py` 新增最小入口：
  - `--run-main-resolution`
  - `--set-run-main-resolution`
  - `--refresh-run-main-resolution`
- 当前最小状态约定是：
  - `not_needed`
  - `pending_ack`
  - `acknowledged`
  - `closed`
- 当前最小关闭条件是：
  - 已存在 `run-main` summary
  - `test_gate` 已通过
  - 没有 blocking issue
- 已用 `TASKS/TASK-run-main-escalation-resolution.json` 做真实验证，确认：
  - 初始升级状态可刷新为 `pending_ack`
  - 在 `run-main` summary 存在且 `test_gate=passed` 后，可手动写回 `close_escalation=true`

## Commands / Outputs (run-main escalation resolution)
- `python3 -m py_compile tools/taskclient.py` -> pass
- `python3 tools/taskclient.py --refresh-task-gaps --task-json-file TASKS/TASK-run-main-escalation-resolution.json` -> pass
- `python3 tools/taskclient.py --refresh-task-escalation --task-json-file TASKS/TASK-run-main-escalation-resolution.json` -> pass
- `python3 tools/taskclient.py --refresh-run-main-resolution --task-json-file TASKS/TASK-run-main-escalation-resolution.json` -> pass; 首次返回 `status=pending_ack`
- `python3 tools/taskclient.py --set-role-summary --task-json-file TASKS/TASK-run-main-escalation-resolution.json --role run-main ...` -> pass
- `python3 tools/taskclient.py --set-test-gate --task-json-file TASKS/TASK-run-main-escalation-resolution.json --gate-status passed --gate-evidence "manual verification demo"` -> pass
- `python3 tools/taskclient.py --set-run-main-resolution --task-json-file TASKS/TASK-run-main-escalation-resolution.json --resolution-status closed --resolution-note "run-main manually closed resolved escalation." --close-escalation` -> pass
- `python3 tools/taskclient.py --run-main-resolution --task-json-file TASKS/TASK-run-main-escalation-resolution.json` -> pass; 最终返回 `status=closed`、`close_escalation=true`
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

## Entity layering clarifications
- 新建并完成 `task-entity-layering-clarifications`，只做 owner docs 最小口径收紧，不改代码结构。
- `docs/ENTITIES.md` 现在显式引入 `baseline` 和 `thread summary` 两层，明确推荐链路是 `thread summary -> task summary -> run evidence / run summary -> baseline refresh`。
- 当前实现被明确标注为过渡态：
  - `session_registry.current_summary` 是 thread-level transitional summary
  - `reports/<RUN_ID>/summary.md` 和 `decision.md` 目前仍偏 active task evidence，属于 run 容器下的 task-focused 表达
- `docs/WORKFLOW.md` 现在也明确：
  - `--summarize-current` 产出当前 thread 的去噪摘要
  - `--refresh-baseline` 当前直接消费 `current_summary`
  - 长期 baseline 应优先吸收 run-level stable summaries，而不是直接吸收原始 thread 噪音

## Task summary bootstrap
- 新建并完成 `task-task-summary-bootstrap`，把 task-level aggregate summary 收为 `TASKS/TASK-*.json` 内的稳定对象 `task_summary`，不额外拆独立文件。
- `TASKS/_SCHEMA.task.json` 已新增 `task_summary.status/key_updates/decisions/risks/verification/next_steps/source_threads/updated_at`。
- `tools/taskclient.py` 已新增：
  - `--task-summary`
  - `--set-task-summary`
- `write_task_md()` 现在会把 `task_summary` 渲染到 `TASKS/TASK-*.md` 的 `## Task Summary` 区块，保持 `json truth + md view`。
- 真实验证已通过：
  - `python3 -m py_compile tools/taskclient.py`
  - `python3 tools/taskclient.py --set-task-summary ...`
  - `python3 tools/taskclient.py --task-summary`

## Run summary bootstrap
- 新建并完成 `task-run-summary-bootstrap`，把 run-level aggregate machine truth 收到 `reports/<RUN_ID>/run_summary.json`，不去污染 `project_config.json`。
- 新增 [reports/_SCHEMA.run_summary.json](/root/quant-factory-os/reports/_SCHEMA.run_summary.json) 作为最小 schema 模板。
- `tools/evidence.py` 现在在 `make evidence RUN_ID=...` 时会自动确保 `run_summary.json` 存在。
- 当前设计已经明确分层：
  - `run_summary.json` 是机器真相源
  - `summary.md / decision.md` 继续是 run 级 md 视图
- 真实验证已通过：
  - `python3 -m py_compile tools/evidence.py`
  - `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline`
  - `reports/run-2026-03-11-vnext-release-baseline/run_summary.json` 已自动生成

## Run summary writeback entry
- 新建并完成 `task-run-summary-writeback-entry`，没有新增 `runclient`，而是把 `run_summary.json` 的最小读写入口直接落在 `tools/evidence.py`。
- 新增命令：
  - `python3 tools/evidence.py --run-id <RUN_ID> --run-summary`
  - `python3 tools/evidence.py --run-id <RUN_ID> --set-run-summary ...`
- 已用真实命令把 [run_summary.json](/root/quant-factory-os/reports/run-2026-03-11-vnext-release-baseline/run_summary.json) 写成一版稳定内容，并成功读回。
- 这一步只补 run-level machine truth 的写回，不改 baseline 仍然只消费 `current_summary` 的现状。

## Baseline prefers run summary
- 新建并完成 `task-baseline-prefers-run-summary`，把 `appserverclient --refresh-baseline` 的输入优先级改为：
  - `reports/<RUN_ID>/run_summary.json`
  - `session_registry.current_summary`（仅缺失时回退）
- 真实运行 `python3 tools/appserverclient.py --refresh-baseline` 后，`turn/start` 请求体中已经出现 `run_summary:` 段，而不是 `current_summary:` 段，说明输入优先级生效。
- 本轮没有改 baseline writeback 的输出落点，仍然回写到 `session_registry.current_summary.baseline_refresh_text`。

## Project guide requirement-analysis principles
- 新建并完成 `task-project-guide-requirement-analysis-principles`，把 [tools/需求管理及分析工作指南.doc](/root/quant-factory-os/tools/需求管理及分析工作指南.doc) 中适合 AI/Codex 的需求分析原则提炼进 owner docs。
- `docs/PROJECT_GUIDE.md` 的 Q9-Q12 现在更明确要求 run 方向收敛时至少确认：背景与目标、必须做/应该做/可以做、不做项、影响模块、异常流、非功能和验收方式。
- `docs/WORKFLOW.md` 现在把这些内容挂到新主线的 `确定需求方向（run 级）` 和 `多角色 fork / 最小 task 拆解`，没有回迁旧 `orient/choose/council/arbiter` 为正式流程。
- `docs/ENTITIES.md` 现在补了 run/task 的需求边界字段建议，并明确推荐角色是 `run-main/dev/test/arch`，其中 `test` 独立验证、`arch` 按需启用。

## Commands / Outputs (project-guide requirement-analysis principles)
- `python3 tools/taskclient.py --create --title "project-guide requirement-analysis principles" ... --activate` -> pass
- `python3 tools/init.py` -> pass to completion; 仍因脏工作区返回 `INIT_STATUS: needs_fix`
- `python3 tools/appserverclient.py --learnbaseline` -> pass; baseline 已复用
- `python3 tools/appserverclient.py --fork-current` -> pass; 当前 fork thread=`019ce5e2-50f1-7b20-aadf-4b746a1d1467`

## Project guide probing templates
- 新建并完成 `task-project-guide-probing-templates`，继续只增强 `PROJECT_GUIDE` 的学习协议层，不改题库结构。
- 在 Q9-Q12 下补了少量高质量追问模板，帮助 AI 面对杂乱需求材料时，先把 run 方向、角色分工、对象分层和 task 前置边界问清楚。
- 追问模板聚焦：背景与目标、必须做/应该做/可以做、不做项、影响模块、异常流、非功能、验收，以及哪些问题属于 run、task 或 thread summary。

## Project guide self-structuring skeleton
- 新建并完成 `task-project-guide-self-structuring-skeleton`，继续只在 `PROJECT_GUIDE` 里增强 AI 自我学习协议。
- 在 Q9-Q12 下补了最小“自我梳理输出骨架”，让 AI 读完客户杂乱材料后，先产出自己的 `run_goal/scope/non_goals/impacted_modules/risks/acceptance`、`role_plan`、`object_layer`、`task_ready` 等草稿结构。
- 这一步仍然不改题号、不新增独立实现层，只把高质量提问进一步压成可复用的结构化思考骨架。

## Project guide markdown draft template
- 新建并完成 `task-project-guide-markdown-draft-template`，继续只增强协议层，不碰任何运行时或自动化实现。
- 在 `docs/PROJECT_GUIDE.md` 的 Q12 下新增标准化 `Markdown intake draft` 模板，用于 AI 读完客户杂乱材料后的首轮结构化输出；模板覆盖 `Background / Run Goal / Scope / Non-Goals / Impacted Modules / Risks / Non-Functional Constraints / Acceptance / Role Plan / Task Candidates / Open Questions / Summary Target`。
- `docs/WORKFLOW.md` 与 `docs/ENTITIES.md` 同步明确：`Markdown intake draft` 只是 run 级协议层草稿，用于把客户材料先整理成讨论输入，不等于 `run summary`，也不是机器真相源。

## Project bootstrap learning protocol
- 新建并完成 `task-project-bootstrap-learning-protocol`，把“陌生项目尚未接入基座时如何先学习、再补 owner docs、最后再考虑自动化接入”沉淀成独立协议文档 [PROJECT_BOOTSTRAP_PROTOCOL.md](/root/quant-factory-os/docs/PROJECT_BOOTSTRAP_PROTOCOL.md)。
- 该协议明确：面对只有杂乱文档、半截代码、零散认知的新项目，先使用通用 `PROJECT_GUIDE` 题库做首轮学习，再补项目化 `PROJECT_GUIDE/WORKFLOW/ENTITIES/AGENTS`，而不是先复制 `tools/` 或直接开始实现。
- `docs/PROJECT_GUIDE.md`、`docs/WORKFLOW.md`、`docs/FILE_INDEX.md` 已同步引用这份 bootstrap 协议，口径上把“通用学习协议”和“项目化 owner docs”分清。

## Multi-thread collaboration minimum chain
- 新建并完成 `task-multi-thread-collaboration-minimum-chain`，把最小多线程协作链先收敛到 `run-main -> dev/test -> thread summary -> task summary`，不直接跳到完整多 agent orchestration。
- `TASKS/_SCHEMA.task.json` 现在新增 `role_threads` 和 `test_gate`；`role_threads` 固定最小角色位为 `run-main/dev/test/arch`，`test_gate` 承担 task 内独立验证门。
- `tools/taskclient.py` 现已支持：
  - `--role-threads`
  - `--set-role-thread`
  - `--test-gate`
  - `--set-test-gate`
- 真实验证已通过：当前 task 已写入 `dev` 角色线程样例和一个 `blocked` 的 `test_gate`，说明“实现侧”和“独立验证侧”的最小机器层已存在。

## Appserverclient fork role command
- 新建并完成 `task-appserverclient-fork-role-command`，把最小 role thread binding 接到真实 runtime。
- `tools/appserverclient.py` 现在支持 `python3 tools/appserverclient.py --fork-role <dev|test|arch>`：它会基于当前 `fork_current_session` fork 出真实 role thread，命名后回写到当前 task 的 `role_threads.<role>`。
- 真实验证已通过：本轮成功 fork 出 `test` role thread `019ce643-7e04-7d61-a980-bec20518d20b`，并写回 [TASKS/TASK-appserverclient-fork-role-command.json](/root/quant-factory-os/TASKS/TASK-appserverclient-fork-role-command.json)。

## Appserverclient role-turn runtime
- 新建并完成 `task-appserverclient-role-turn-runtime`，把最小 role thread 执行面接到真实 runtime。
- `tools/appserverclient.py` 现在支持 `python3 tools/appserverclient.py --role-turn <dev|test|arch> [text...]`：它会恢复已绑定的 role thread，并在该线程上执行真实 turn。
- 为当前 task 先真实 fork 并绑定了 `test` role thread `019ce64a-8ad1-7733-a6e0-f8b0c15d22f2`，然后成功执行：
  - `python3 tools/appserverclient.py --role-turn test "请用一句话说明你当前作为 test 线程的职责。"`
- 本次真实返回的 `last_agent_message` 为：`我当前作为 test 线程的职责，是基于主线合同独立验证实现是否满足预期、暴露风险与回归缺口，并把可回灌的测试结论沉淀为 run 级证据。`
- 这一步只打通 role thread 的执行面，不做 thread summary 自动回收，也不做多角色调度器。

## Role thread summary to task summary
- 新建并完成 `task-role-thread-summary-to-task-summary`，把 `thread summary -> task summary` 的最小回收链接到真实 runtime。
- `TASKS/_SCHEMA.task.json` 新增 `role_summaries`，`task_summary` 新增 `role_summary_evidence`。
- `tools/appserverclient.py` 新增 `python3 tools/appserverclient.py --summarize-role <role>`，它会恢复已绑定的 role thread、发送 role summary prompt、抽取最后一条 agent message，并写回当前 task 的 `role_summaries.<role>`。
- 同时，task 机器层会追加：
  - `task_summary.source_threads`
  - `task_summary.role_summary_evidence`
- 真实验证已通过：
  - `python3 tools/appserverclient.py --fork-role test`
  - `python3 tools/appserverclient.py --role-turn test "请从独立测试视角给出这个 task 当前最关键的验证关注点。"`
  - `python3 tools/appserverclient.py --summarize-role test`
  - `python3 tools/taskclient.py --role-summaries`
  - `python3 tools/taskclient.py --active-task`

## Task role summary merge rules
- 新建并完成 `task-task-role-summary-merge-rules`，把多角色 role summaries 并存时的 task-level 最小聚合收进 `taskclient`。
- `tools/taskclient.py` 新增 `python3 tools/taskclient.py --merge-role-summaries`。
- 当前聚合规则只做最小去重追加：
  - `task_summary.source_threads`
  - `task_summary.role_summary_evidence`
  - `task_summary.key_updates` 中的 `<role> summary merged`
- 真实验证已通过：
  - `python3 tools/taskclient.py --merge-role-summaries --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
  - `python3 tools/taskclient.py --task-summary --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`

## Task role summary conflict rules
- 新建并完成 `task-task-role-summary-conflict-rules`，把 task 层的最小冲突优先级和缺口汇总规则落到机器层。
- `TASKS/_SCHEMA.task.json` 现在把这两块定义为：
  - `task_summary.conflict_policy`
  - `task_summary.gap_summary`
- `tools/taskclient.py` 新增 `python3 tools/taskclient.py --refresh-task-gaps`，会基于：
  - `role_summaries`
  - `test_gate`
  刷新 `missing_roles` 和 `open_gaps`
- 当前默认优先级顺序是：
  - `run-main -> test -> arch -> dev`
- 真实验证已通过：
  - `python3 tools/taskclient.py --refresh-task-gaps --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
  - `python3 tools/taskclient.py --task-summary --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`

## Run-main role runtime resolution link
- 新建并完成 `task-run-main-role-runtime-resolution-link`，把 `run-main` 的真实 role runtime 与 task resolution 自动刷新串起来。
- `appserverclient --fork-role` 现在正式支持 `run-main`，不再只限 `dev/test/arch`。
- 已真实验证：
  - `python3 tools/appserverclient.py --fork-role run-main`
  - `python3 tools/appserverclient.py --role-turn run-main "..."`
  - `python3 tools/appserverclient.py --summarize-role run-main`
- `summarize-role run-main` 后，task 机器层会自动刷新：
  - `task_summary.gap_summary`
  - `task_summary.escalation_summary`
  - `task_summary.run_main_resolution`
- 本次真实结果中：
  - `role_threads.run-main.thread_id=019ce69a-7e4f-7aa3-b1f2-9e9299c70d61`
  - `role_summaries.run-main.summary_turn_id=019ce69c-2cfa-73a1-a821-25634ddbdc43`
  - `escalation_summary.needs_run_main=true`
  - `run_main_resolution.status=acknowledged`
  - 仍等待 `test_gate=passed` 才能关闭升级项

## Commands / Outputs (run-main role runtime resolution link)
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py` -> pass
- `python3 tools/appserverclient.py --fork-role run-main` -> pass
- `python3 tools/appserverclient.py --role-turn run-main "请从 run-main 视角确认当前 task 的升级项，并说明关闭升级前还缺什么。"` -> pass
- `python3 tools/appserverclient.py --summarize-role run-main` -> pass; 自动刷新 `gap_summary` / `escalation_summary` / `run_main_resolution`
- `python3 tools/taskclient.py --run-main-resolution --task-json-file TASKS/TASK-run-main-role-runtime-resolution-link.json` -> pass; 当前返回 `status=acknowledged`

## Test role gate runtime link
- 新建并完成 `task-test-role-gate-runtime-link`，把 `test` 真实 role thread、`test_gate` 写回和升级项关闭条件串起来。
- `appserverclient` 现在新增：
  - `--mark-test-gate <pending|blocked|passed> [evidence...]`
- 已真实验证：
  - `python3 tools/appserverclient.py --fork-role test`
  - `python3 tools/appserverclient.py --role-turn test "..."`
  - `python3 tools/appserverclient.py --summarize-role test`
  - `python3 tools/appserverclient.py --mark-test-gate passed "real test gate passed from runtime"`
- 为了把关闭链完整跑通，本轮还在同一 task 下补了：
  - `python3 tools/appserverclient.py --fork-role run-main`
  - `python3 tools/appserverclient.py --summarize-role run-main`
- 当前最终结果：
  - `test_gate.status=passed`
  - `escalation_summary.needs_run_main=false`
  - `run_main_resolution.status=not_needed`
  - `task_summary.role_summary_evidence` 已同时保留 `run-main` 与 `test` 的真实 summary turn 证据

## Commands / Outputs (test role gate runtime link)
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py` -> pass
- `python3 tools/appserverclient.py --fork-role test` -> pass
- `python3 tools/appserverclient.py --role-turn test "请从独立测试视角说明当前 task 关闭升级项前最关键的验证结论。"` -> pass
- `python3 tools/appserverclient.py --summarize-role test` -> pass
- `python3 tools/appserverclient.py --mark-test-gate passed "real test gate passed from runtime"` -> pass
- `python3 tools/appserverclient.py --fork-role run-main` -> pass
- `python3 tools/appserverclient.py --summarize-role run-main` -> pass
- `python3 tools/taskclient.py --run-main-resolution --task-json-file TASKS/TASK-test-role-gate-runtime-link.json` -> pass; 最终返回 `status=not_needed`

## Task escalation to run-main rules
- 新建并完成 `task-task-escalation-to-run-main-rules`，把“哪些冲突必须升级给 run-main”落到 task 机器层。
- `TASKS/_SCHEMA.task.json` 现在新增：
  - `task_summary.escalation_policy`
  - `task_summary.escalation_summary`
- `tools/taskclient.py` 新增 `python3 tools/taskclient.py --refresh-task-escalation`，会基于：
  - `gap_summary`
  - `test_gate`
  刷新当前是否必须升级给 `run-main`
- 当前最小必须升级条件是：
  - `run-main summary missing`
  - `test_gate` 未通过
  - 仍有 blocking issue
- 真实验证已通过：
  - `python3 tools/taskclient.py --refresh-task-gaps --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
  - `python3 tools/taskclient.py --refresh-task-escalation --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
  - `python3 tools/taskclient.py --task-summary --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
