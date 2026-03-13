# FILE_INDEX.md

## 一句话定位
这是实验性的全量文件职责索引，用来帮助新 agent 在最短时间内定位“先看什么、为什么看、文件各自负责什么”。

## 使用方式
- 先看 owner docs 索引，再看 tools 索引，最后看 task / reports 索引。
- 这个文件不是流程文档，也不是设计白皮书；它只负责快速定位。
- 文件职责变化时，应同步更新这里的一句话说明。

## 1. Owner Docs

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `AGENTS.md` | 宪法与硬规则，定义门禁、允许命令、文档新鲜度和 PR 纪律。 | 每次 session 开始时 |
| `docs/PROJECT_GUIDE.md` | 学习课程、问题库、标准答案、主线回拉锚点。 | baseline 学习和主线漂移时 |
| `docs/PROJECT_BOOTSTRAP_PROTOCOL.md` | 陌生项目尚未接入基座时的最小学习与 owner docs 补齐协议。 | 承接新项目、只有杂乱文档和半截代码时 |
| `docs/WORKFLOW.md` | 状态机、阶段定义、主流程说明。 | 理解流程和阶段边界时 |
| `docs/ENTITIES.md` | 核心对象、状态和交付单元的词典。 | 理解 task/run/project/pr 等名词时 |
| `TOOLS_METHOD_FLOW_MAP.md` | 实验性主流程方法索引与调用图。 | 看主流程入口和方法调用时 |

## 2. Runtime / Config

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/project_config.json` | 项目最小配置数据源，含 required / git / runtime_state / session_registry；`current_summary` 也在这里落盘。 | 看项目接入最小字段、当前运行状态和 summary 回写时 |
| `TASKS/QUEUE.json` | 当前 queue 的机器真相源。 | 选择下一个 active/open task 时 |
| `TASKS/TASK-*.json` | 当前或历史 task 的机器真相源；现在也承载 `role_threads`、`test_gate` 和 task-level aggregate `task_summary`。 | 需要程序稳定读取 task 协作状态、test gate 或 task summary 时 |
| `tools/project_config.template.json` | 其他项目接入时可复用的最小配置模板。 | 新项目接入时 |
| `tools/project_config.py` | 统一配置出口；把 JSON 最小数据、系统常量和运行时状态拼成统一大配置视图。 | 任何脚本取配置时 |
| `tools/taskclient.py` | Python-first 的统一 task 入口；当前同时承担 task/queue JSON 读写、queue 选择、runtime 绑定、task bootstrap、`role_threads`、`test_gate`、`task_summary` 与 `run_main_resolution` 更新。 | 需要从 `QUEUE.json` 选择 task、读取 active task、新建 task 或更新 task 协作状态时 |
| `tools/evidence.py` | run evidence 的最小生成与维护入口；当前也提供 `run_summary.json` 的最小读写能力。 | 补 `meta/summary/decision` 或读取/更新 run summary 时 |
| `tools/result_schema.py` | 可组合流程方法统一返回协议：`err_code / err_desc / data`。 | 新增流程入口时 |

## 3. Prepare / Runtime / Git

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/init.py` | 环境准备、项目骨架补齐、Codex/Git 前置检查。 | 开工前环境准备时 |
| `tools/appserverclient.py` | Codex app-server runtime 核心；负责 baseline / fork / fork-role / role-turn / summarize-role / mark-test-gate / current-turn / summarize-current / refresh-baseline，并显式打印当前 active task JSON 摘要；`refresh-baseline` 现优先消费 `run_summary.json`，`summarize-role` 和 `mark-test-gate` 会自动刷新 task gap/escalation/resolution。 | 学习基线、当前 session 推进、role thread 绑定/执行/去噪、test gate 写回和 baseline 回灌时 |
| `tools/summarize_role_prompt.md` | role thread 去噪总结模板；用于把单个角色线程总结成可写入 task 机器层的 role summary。 | 调用 `appserverclient --summarize-role` 时 |
| `tools/taskclient.py` | task/queue 机器真相入口；负责 create/next、task summary 写回、role thread/role summary/test gate 更新，以及 `--merge-role-summaries` / `--refresh-task-gaps` / `--refresh-task-escalation` / `--refresh-run-main-resolution` 的 task-level 聚合、缺口刷新、升级判断和 run-main 确认闭环。 | 处理 task JSON truth、聚合 role summaries、刷新缺口/升级状态和绑定 active task 时 |
| `tools/gitclient.py` | Git 底层；负责 commit、PR、merge、rollback、main 同步，并优先从 task JSON 读取当前任务上下文。 | 收尾交付和回滚时 |

## 5. Prompt / Learning Assets

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/learnbaseline_prompt.md` | baseline 学习固定前言 prompt 文件。 | 调整 baseline 学习提示词时 |
| `tools/summarize_current_prompt.md` | current fork 去噪总结提示词。 | 调整 `--summarize-current` 时 |
| `tools/refresh_baseline_prompt.md` | baseline 增量回灌提示词。 | 调整 `--refresh-baseline` 时 |
| `tools/learn_prompt_compare.md` | `learn.py` 与 `appserverclient` baseline prompt 对比说明。 | 做提示词迁移时 |

## 6. Task / State / Evidence

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `TASKS/QUEUE.md` | queue 的遗留可读视图；迁移期保留。 | 需要人工快速扫历史 backlog 时 |
| `TASKS/TASK-*.md` | task 的遗留可读视图；迁移期保留。 | 需要人工快速浏览任务说明时 |
| `reports/_SCHEMA.run_summary.json` | run summary 的机器真相源 schema 模板。 | 设计或扩展 run-level aggregate summary 时 |
| `reports/<RUN_ID>/run_summary.json` | 当前 run 的机器真相源摘要。 | 需要程序稳定读取 run-level aggregate summary 时 |
| `reports/<RUN_ID>/summary.md` | 当前 run 的总结证据。 | 看最近做了什么时 |
| `reports/<RUN_ID>/decision.md` | 当前 run 的决策证据。 | 看为什么这么做时 |

## 7. Legacy / Compatibility

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/backup/legacy.sh` | 已归档的旧兼容入口路由。 | 追溯旧 shell 入口设计时 |
| `tools/backup/task.sh` | 已归档的旧 task shell 流程。 | 对照旧 shell task/ship 链时 |
| `tools/backup/taskstore.py` | 已归档的独立 taskstore 实现，保留作历史参考。 | 对照 taskclient 合并前的实现时 |
| `tools/backup/observe.sh` | 已归档的旧 observe shell 入口。 | 排查旧 shell 观察链时 |
| `tools/backup/ship.sh` | 已归档的旧 ship 实现。 | 对照旧发货逻辑时 |
| `tools/backup/legacy.wrapper.sh` | 已移出的旧顶层 `legacy.sh` wrapper。 | 追溯 wrapper 退场方式时 |
| `tools/backup/task.wrapper.sh` | 已移出的旧顶层 `task.sh` wrapper。 | 追溯 task shell 入口退场方式时 |
| `tools/backup/observe.wrapper.sh` | 已移出的旧顶层 `observe.sh` wrapper。 | 追溯 observe shell 入口退场方式时 |
| `tools/backup/ship.wrapper.sh` | 已移出的旧顶层 `ship.sh` wrapper。 | 追溯 ship shell 入口退场方式时 |
| `tools/backup/learn.py` | 已归档的历史 learn 工作流入口。 | 看 baseline 学习旧实现和迁移边界时 |
| `tools/backup/ready.py` | 已归档的历史 `learn` 后门禁与合同准备。 | 对照旧门禁链时 |
| `tools/backup/orient.py` | 已归档的历史方向草案生成。 | 对照旧讨论链时 |
| `tools/backup/choose.py` | 已归档的历史方向确认与合同生成。 | 对照旧讨论链时 |
| `tools/backup/council.py` | 已归档的历史多角色独立评审。 | 对照旧讨论链时 |
| `tools/backup/arbiter.py` | 已归档的历史 execution contract 收敛。 | 对照旧讨论链时 |
| `tools/backup/slice_task.py` | 已归档的历史最小 task 拆分入口。 | 对照旧 task 切片链时 |
| `tools/backup/run_main.py` | 已归档的历史 Python 总入口骨架。 | 看旧 orchestrator 设计时 |
| `tools/backup/run_a9.py` | 已归档的旧实验性 Python 入口。 | 排查历史实验入口时 |
| `tools/doctor.sh` | 辅助诊断脚本。 | 排查环境和 Git/Codex 体检时 |
| `tools/view.sh` | 分块读取长文件。 | 按仓库规则读长文件时 |

## 8. 当前建议阅读顺序

1. `AGENTS.md`
2. `docs/PROJECT_GUIDE.md`
3. `docs/WORKFLOW.md`
4. `docs/ENTITIES.md`
5. `TOOLS_METHOD_FLOW_MAP.md`
6. `tools/project_config.py`
7. `tools/appserverclient.py`
8. `tools/gitclient.py`
