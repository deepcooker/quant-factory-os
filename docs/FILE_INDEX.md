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
| `docs/TOOLS_METHOD_FLOW_MAP.md` | 实验性主流程方法索引与调用图。 | 看主流程入口和方法调用时 |

## 2. Runtime / Config

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/project_config.json` | 项目最小配置数据源，含 required / git / runtime_state / session_registry；`current_summary` 也在这里落盘。 | 看项目接入最小字段、当前运行状态和 summary 回写时 |
| `TASKS/QUEUE.json` | 当前 queue 的机器真相源。 | 选择下一个 active/open task 时 |
| `TASKS/TASK-*.json` | 当前或历史 task 的机器真相源；现在也承载 `role_threads`、`test_gate` 和 task-level aggregate `task_summary`。 | 需要程序稳定读取 task 协作状态、test gate 或 task summary 时 |
| `tools/project_config.template.json` | 其他项目接入时可复用的最小配置模板。 | 新项目接入时 |
| `tools/project_config.py` | 统一配置出口；把 JSON 最小数据、系统常量和运行时状态拼成统一大配置视图。 | 任何脚本取配置时 |
| `tools/taskclient.py` | Python-first 的统一 task 入口；当前同时承担 task/queue JSON 读写、queue 选择、runtime 绑定、task bootstrap、`role_threads`、`test_gate`、`task_summary` 与 `run_main_resolution` 更新。 | 需要从 `QUEUE.json` 选择 task、读取 active task、新建 task 或更新 task 协作状态时 |
| `tools/evidence.py` | run evidence 的最小生成与维护入口；当前也提供 `run_summary.json` 的最小读写、带 `merge_policy` 的 `task summary -> run summary` 聚合、少量高频模式的 run-level 规则化归并、`cross_task_risks` 的近义 blocked-gate 风险去重、按同一 run 下 task JSON 真相源重算 `active/completed/source tasks`、显式 `normalize-run-summary` 渐进清理，以及生成供 baseline refresh 使用的 `baseline_ready_summary`。 | 补 `meta/summary/decision`、读取/更新 run summary、按字段类别聚合稳定 task summary、提升 run-level 表达质量、对齐 run/task 真相、做显式历史清理，或压缩 baseline refresh 输入时 |
| `tools/result_schema.py` | 可组合流程方法统一返回协议：`err_code / err_desc / data`。 | 新增流程入口时 |

## 3. Prepare / Runtime / Git

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/init.py` | 环境准备、项目骨架补齐、Codex/Git 前置检查。 | 开工前环境准备时 |
| `tools/appserverclient.py` | Codex app-server runtime 核心；负责 baseline / fork / fork-role / role-turn / summarize-role / mark-test-gate / current-turn / summarize-current / refresh-baseline，并显式打印当前 active task JSON 摘要；`refresh-baseline` 现优先消费 `run_summary.json`，`summarize-role` 会自动 merge role summaries 并刷新 task gap/escalation/resolution，`mark-test-gate` 会继续联动刷新。当前风险是它已经同时看见 runtime 与部分 task gate 规则，后续应继续保持“真实线程生命周期 + 必要写回”的边界，避免演化成总控脚本。 | 学习基线、当前 session 推进、role thread 绑定/执行/去噪、test gate 写回和 baseline 回灌时 |
| `tools/view.sh` | 稳定的分段文件读取工具；支持直接执行和 `python3 tools/view.sh ...`，兼容历史 `--lines START:END` 用法，并内置 repo 边界与 denylist 检查。 | 读取长文件、按范围查看、查找命中行或验证读取边界时 |
| `tools/prompts/summarize_role_prompt.md` | role thread 去噪总结模板；用于把单个角色线程总结成可写入 task 机器层的 role summary。 | 调用 `appserverclient --summarize-role` 时 |
| `tools/taskclient.py` | task/queue 机器真相入口；负责 create/next、task summary 写回、role thread/role summary/test gate 更新，以及 `--merge-role-summaries` / `--refresh-task-gaps` / `--refresh-task-escalation` / `--refresh-run-main-resolution` 的 task-level 聚合、缺口刷新、升级判断和 run-main 确认闭环。当前还提供内部统一刷新入口 `refresh_task_coordination()`，以及 `update_role_summary_with_task_links()`、`update_test_gate_from_test_summary()` 这类 task-side 联动 helper，供 runtime 在不理解具体 task 规则细节的前提下完成 task 层联动。它是 task 级规则的优先归属层，后续新增 task policy 应优先落在这里，而不是回流到 runtime。 | 处理 task JSON truth、聚合 role summaries、刷新缺口/升级状态和绑定 active task 时 |
| `tools/gitclient.py` | Git 底层；负责 commit、PR、merge、rollback、main 同步，并优先从 task JSON 读取当前任务上下文。当前保持独立性较好，后续应继续避免把 runtime 或 task/run 聚合逻辑重新耦合回这里。 | 收尾交付和回滚时 |

当前最短稳定操作面：
- `init -> learnbaseline -> 明确 run 方向 -> fork-current -> （按需 fork-role/role-turn/summarize-role/mark-test-gate） -> summarize-current -> refresh-baseline -> gitclient`
- 如果没有真实多角色需要，不要额外引入 role thread 步骤
- 如果在 Codex TUI 内做真实 session/runtime 调试，`Default` 权限模式可能拦住 workspace 外的 `/root/.codex/sessions`；此时应临时切 `/permissions -> Full Access`，避免把外层权限问题误判为主线逻辑问题

## 5. Prompt / Learning Assets

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/prompts/learnbaseline_prompt.md` | baseline 学习固定前言 prompt 文件。 | 调整 baseline 学习提示词时 |
| `tools/prompts/summarize_current_prompt.md` | current fork 去噪总结提示词。 | 调整 `--summarize-current` 时 |
| `tools/prompts/refresh_baseline_prompt.md` | baseline 增量回灌提示词；当前要求优先消费 `run_summary`，缺失时再回退 `current_summary`。 | 调整 `--refresh-baseline` 时 |
| `appserver_log/test_app*.jsonl/.log` | app-server Python 调试日志输出目录；默认承载 runtime 事件流和 stderr 记录。 | 排查 baseline / fork / role runtime 问题时 |
| `chatlogs/需求管理及分析工作指南.doc` | 传统需求分析参考材料，当前主要服务 run-main 的需求收敛方法提炼。 | 回看需求分析原则来源时 |
| `chatlogs/learn_prompt_compare.md` | `learn.py` 与 `appserverclient` baseline prompt 对比说明。 | 做提示词迁移时 |

## 6. Task / State / Evidence

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `TASKS/QUEUE.json` | queue 的唯一机器真相源。 | 读取、绑定或收口 task/queue 状态时 |
| `TASKS/TASK-*.md` | task 的遗留可读视图；迁移期保留。 | 需要人工快速浏览任务说明时 |
| `reports/_SCHEMA.run_summary.json` | run summary 的机器真相源 schema 模板；当前也声明 `merge_policy`、`legacy_cleanup_policy` 和 `audit_risks`，用于区分运行时归并规则、历史前缀渐进清理规则以及不应进入 baseline-ready compaction 的审计风险层。 | 设计或扩展 run-level aggregate summary 时 |
| `reports/<RUN_ID>/run_summary.json` | 当前 run 的机器真相源摘要。 | 需要程序稳定读取 run-level aggregate summary 时 |
| `reports/<RUN_ID>/summary.md` | 当前 run 的总结证据。 | 看最近做了什么时 |
| `reports/<RUN_ID>/decision.md` | 当前 run 的决策证据。 | 看为什么这么做时 |

## 7. 当前建议阅读顺序

1. `AGENTS.md`
2. `docs/PROJECT_GUIDE.md`
3. `docs/WORKFLOW.md`
4. `docs/ENTITIES.md`
5. `docs/TOOLS_METHOD_FLOW_MAP.md`
6. `tools/project_config.py`
7. `tools/appserverclient.py`
8. `tools/gitclient.py`
