# WORKFLOW

本文件定义本仓当前的主流程状态机。

它回答的是：
- 当前流程分几层
- 每一层的目标是什么
- 每一层的输入、输出、门禁和下一跳是什么

它不负责重复解释所有命令参数。
对象定义以 `docs/ENTITIES.md` 为准，硬规则以 `AGENTS.md` 为准。

补充定位：
- 本文件描述的是 foundation repo 当前主流程。
- 当前主线不是业务项目模板，而是本仓 `tools` 自动化研发系统本身。
- `init` 只属于开工前准备层，不属于主业务流程。
- 真正自动化主线以项目为中心，由 `appserverclient` 驱动学习基线、run 级方向推进、fork 多角色 session、去噪回灌 baseline，并由 `gitclient` 完成交付收尾。
- 研发期主要通过 Codex CLI 调试和接管；长期正式运行应收敛到普通窗口中的 Python orchestrator + Codex app-server。
- 如果目标项目尚未接入本仓 owner docs 与自动化主线，先按 [PROJECT_BOOTSTRAP_PROTOCOL.md](/root/quant-factory-os/docs/PROJECT_BOOTSTRAP_PROTOCOL.md) 完成首轮项目学习与文档补齐，再进入本状态机。

## 1. 设计原则

### 1.1 流程分层
当前固定分为三层：

1. 准备层
   - `init`
2. 主流程层
   - `appserverclient`
   - `--learnbaseline`
   - `--fork-current`
   - `--current-turn`
   - `--summarize-current`
   - `--refresh-baseline`
3. 收尾层
   - `gitclient`
   - `--commit`
   - `--rollback-last`
   - `--rollback-commit`

旧的 `learn -> ready -> orient -> choose -> council -> arbiter -> slice -> do -> review -> ship`
链路现在视为研发期过渡流程和兼容材料，不再作为当前正式主线；对应旧 Python 与 shell 入口都已归档到 `tools/backup/`，不再占据正式 `tools/` 入口位。

### 1.2 边界原则
- `init` 只做环境准备、项目骨架补齐、Git/Codex 前置检查。
- `appserverclient` 承担项目级学习基线、run 级 session 推进、多 fork session 管理。
- `gitclient` 只承担提交、PR、合并、回滚、同步 main。
- baseline 只保留干净主认知，不直接承载日常噪音。
- 日常需求、讨论、验证应在 fork session 中推进，再将去噪结果回灌 baseline。

### 1.3 对象原则
- `project_id`：长期上下文
- `run_id`：一轮周期容器
- `task_id`：run 内最小执行切片
- discussion artifacts：方向到合同的中间对象

对象边界见：
- [docs/ENTITIES.md](/root/quant-factory-os/docs/ENTITIES.md)

## 2. 状态机总览

当前主线：

```text
project
  -> init (准备层，非主流程)
  -> appserverclient --learnbaseline
  -> 确定当前 run 的需求方向
  -> appserverclient --fork-current
  -> fork 多角色 session / 拆最小 task
  -> appserverclient --current-turn
  -> appserverclient --summarize-current
  -> appserverclient --refresh-baseline
  -> gitclient --commit / --rollback-*
  -> 回到 run 级同频继续推进
```

## 3. 准备层

### 3.1 `init`

命令：
- `python3 tools/init.py`
- `python3 tools/init.py -log`

目标：
- 用统一项目配置完成自动化开工前检查与项目骨架补齐

输入：
- 当前项目根目录
- `tools/project_config.json -> runtime_state`
- `tools/project_config.json -> task_registry`
- owner docs
- Codex / app-server 运行前提
- git 仓库 / 远端 / 账号 / 工作区状态

输出：
- 控制台状态打印
- 自动化是否允许继续的总判定

关键输出锚点：
- `INIT_PROJECT_ID`
- `INIT_PROJECT_ROOT`
- `INIT_RUN_ID`
- `INIT_TASK_FILE`
- `INIT_TASK_JSON_FILE`
- `INIT_PROJECT_GUIDE_STATUS`
- `INIT_CODEX_CLI_STATUS`
- `INIT_APP_SERVER_STATUS`
- `INIT_GIT_REPO_STATUS`
- `INIT_GIT_AUTH_STATUS`
- `INIT_BRANCH`
- `INIT_DIFF_SUMMARY`
- `INIT_STATUS`
- `INIT_REASON_CODES`
- `INIT_NEXT`

职责：
- 读取固定项目常量配置
- 识别当前项目与项目路径
- 检查关键 owner docs 是否齐备
- 检查 Codex / app-server 是否具备运行前提
- 检查 git 仓库、远端、账号和工作区状态
- 给出自动化是否允许继续的总判定

非职责：
- 不分 `-status` / `-main` 多模式
- 不创建业务 `RUN_ID`
- 不做项目同频
- 不生成讨论产物
- 不授权执行
- 不替代 app-server 运行时交互

下一跳：
- `init` 通过后，才进入主流程层
- `init` 不属于 run 主流程本体

## 4. 主流程层

### 4.1 `appserverclient --learnbaseline`

命令：
- `python3 tools/appserverclient.py --learnbaseline`
- `python3 tools/appserverclient.py --learnbaseline -new`

目标：
- 建立或重建项目级 baseline 学习 session

输入：
- `docs/PROJECT_GUIDE.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `tools/project_config.json`
- 动态 prompt 组装结果

输出：
- `session_registry.learn_session_baseline`
- baseline thread/session

职责：
- 以项目为中心完成一次重型 `plan` 同频
- 把主线、课程、问题、材料锚定进 baseline session
- baseline 已存在时直接复用；`-new` 时重建

### 4.2 确定需求方向（run 级）

目标：
- 由人给出当前 run 的方向意图
- 系统负责围绕这个方向推进 session 与 task

说明：
- 这个点是人工注入意图，不完全自动生成
- 人给方向，系统负责收敛、拆解、执行、验证
- 当前 task/queue 机器真相源优先使用 `TASKS/*.json`；`*.md` 只保留人类阅读兼容层

run 主线程在这一步至少要收敛出：
- 背景与目标：为什么做，这轮 run 想解决什么
- 范围边界：必须做 / 应该做 / 可以做，以及明确不做项
- 影响面：涉及哪些模块、数据、外部系统或角色
- 风险面：异常流、回退点、依赖与潜在冲突
- 非功能约束：性能、稳定性、安全、审计、环境前提
- 验收方式：后续 task 与 test 应如何判断完成
- 第一版 `Markdown intake draft`：先把客户杂乱材料整理成 run 级讨论草稿，再继续收敛

说明：
- 这里强调的是新主线下的 run 方向收敛，不是回到旧的 `orient/choose/council/arbiter`
- run 方向收敛后的稳定结论，才适合继续拆成 task 或沉淀到 run summary
- `Markdown intake draft` 只是协议层草稿，不是 `run summary`，也不是机器真相源

### 4.3 `appserverclient --fork-current`

命令：
- `python3 tools/appserverclient.py --fork-current`

目标：
- 从 baseline 派生当前工作 session

补充：
- 当前还支持 `python3 tools/appserverclient.py --fork-role <run-main|dev|test|arch>`
- 该入口会基于当前 `fork_current_session` 再派生一个 role thread，并回写到当前 task 的 `role_threads`
- 这一步只负责最小 role thread 绑定，不等于完整多 agent orchestration
- 已绑定的 role thread 之后可通过 `python3 tools/appserverclient.py --role-turn <role> [text...]` 执行真实 turn
- 已绑定的 role thread 还可通过 `python3 tools/appserverclient.py --summarize-role <role>` 生成去噪 role summary，并把结果写回当前 task 的 `role_summaries` 与 `task_summary.role_summary_evidence`
- `--summarize-role` 写回 `role_summaries.<role>` 以及 `task_summary.role_summary_evidence/source_threads` 的联动，现在也由 `taskclient` 统一承接
- `--summarize-role` 现在会调用 `taskclient.refresh_task_coordination(include_role_merge=True)`，由 task 层统一完成 role summary merge 与后续刷新
- 当 `test` 角色已给出真实 summary 后，可通过 `python3 tools/appserverclient.py --mark-test-gate <pending|blocked|passed> [evidence...]` 写回 `test_gate`；其中 test thread/turn 证据拼接现由 `taskclient` 统一承接，再调用 `taskclient.refresh_task_coordination(include_role_merge=False)` 刷新 `gap_summary / escalation_summary / run_main_resolution`
- 当一个 task 下已有多个 role summaries 时，可通过 `python3 tools/taskclient.py --merge-role-summaries` 把现有 `role_summaries` 按最小去重规则汇入 `task_summary`
- 当需要把多角色缺口和冲突优先级写回 task 机器层时，可通过 `python3 tools/taskclient.py --refresh-task-gaps` 刷新 `task_summary.conflict_policy` 与 `task_summary.gap_summary`
- 当需要判断当前 task 是否必须升级给 `run-main` 时，可通过 `python3 tools/taskclient.py --refresh-task-escalation` 刷新 `task_summary.escalation_policy` 与 `task_summary.escalation_summary`
- 当 task 已升级给 `run-main` 后，可通过 `python3 tools/taskclient.py --refresh-run-main-resolution` 刷新 `task_summary.run_main_resolution_policy` 与 `task_summary.run_main_resolution`
- 如需手动确认或关闭升级项，可通过 `python3 tools/taskclient.py --set-run-main-resolution ...` 写回 run-main 的确认状态与 closing note

输出：
- `session_registry.fork_current_session`

职责：
- `resume` baseline
- `fork` 出当前工作副本
- 保证 baseline 不直接承载日常工作噪音

### 4.4 多角色 fork / 最小 task 拆解

目标：
- 从 baseline 或 current session 再分叉多角色 session
- 把需求方向拆成最小 task 单元逐个完成

### 4.5 Formal Tool Boundaries
当前 formal mainline 的四个主工具边界如下：

- `python3 tools/appserverclient.py`
  - 负责 baseline / run-main / role threads 的真实 runtime
  - 负责 `fork-current / fork-role / role-turn / summarize-role / summarize-current / refresh-baseline`
  - 不应继续演化成 task truth 或 run evidence 的总控脚本

- `python3 tools/taskclient.py`
  - 负责 task machine truth
  - 负责 `role_threads / role_summaries / test_gate / gap_summary / escalation_summary / run_main_resolution`
  - 不应负责 runtime transport 或 baseline session lifecycle

- `python3 tools/evidence.py`
  - 负责 run evidence 骨架与 `run_summary.json`
  - 负责 `reconcile / compact / normalize / task->run merge`
  - 不应接管 task 机器层或 role runtime

- `python3 tools/gitclient.py`
  - 负责提交、回滚和 message fallback
  - 应保持与 runtime / task / run 聚合逻辑解耦

当前稳定化原则：
- 新能力先判断应落在 `runtime / task truth / run evidence / git delivery` 哪一层
- 避免把更多聚合规则直接堆进 `appserverclient`
- 避免把 `gitclient` 再次耦合回旧 `ship` 式总控

说明：
- 这是当前正式主线的发展方向

### 4.6 Shortest Stable Mainline
当前推荐的最短稳定主线，只保留必要动作：

1. `python3 tools/init.py`
2. `python3 tools/appserverclient.py --learnbaseline`
3. 明确本轮 `run` 方向
4. `python3 tools/appserverclient.py --fork-current`
5. 仅在 task 需要真实角色线程时，再使用：
   - `python3 tools/appserverclient.py --fork-role <run-main|dev|test|arch>`
   - `python3 tools/appserverclient.py --role-turn <role> [text...]`
   - `python3 tools/appserverclient.py --summarize-role <role>`
   - `python3 tools/appserverclient.py --mark-test-gate <status> [evidence...]`
6. `python3 tools/appserverclient.py --summarize-current`
7. `python3 tools/appserverclient.py --refresh-baseline`
8. `python3 tools/gitclient.py --commit`

当前冻结原则：
- 不为“更纯”继续拆出更多中间层
- 不把 task policy 重新放回 runtime
- 不把 runtime/task/run 逻辑重新耦合回 git 层
- 角色 session 应互不干扰
- 每个角色 session 结束后要先做去噪总结，再考虑回灌 baseline
- 推荐的最小角色结构是：run 主线程负责收敛与确认；task 下默认 `dev/test`，复杂任务按需增加 `arch`
- `test` 负责独立验证，不等同于开发自测；`dev` 负责实现与单元/最小集成自证；`arch` 负责复杂任务的边界与结构风险
- 当前最小协作链优先收敛为：`run-main -> dev/test -> thread summary -> task summary`
- 在这条最小链里，`test` 的独立结论应先进入 `test_gate`，再决定 task 是否可以进入更高层 summary
- 当前正式 task 入口是 `python3 tools/taskclient.py --next`，用于从 `TASKS/QUEUE.json` 选择并绑定下一个 active task
- 当前也可用 `python3 tools/taskclient.py --create ...` 生成新的 JSON-first task，并按需追加到 `TASKS/QUEUE.json` 或直接激活
- 当前也可用 `python3 tools/taskclient.py --set-task-summary ...` 把多个 thread 的稳定结论聚合回 task JSON 内的 `task_summary`
- `tools/task.sh` 已退出正式层，只保留历史版本于 `tools/backup/task.sh`

### 4.5 `appserverclient --current-turn`

命令：
- `python3 tools/appserverclient.py --current-turn "..." `

目标：
- 在当前工作 session 上继续推进 run 级交互

职责：
- `resume` current session
- 用普通 `default` 模式持续交互
- 不把日常 session 永久锁死在 `plan`

### 4.6 baseline 回灌

目标：
- 将 fork session 中去噪后的有效结论同步回 baseline

说明：
- 不是把所有工作噪音直接写回 baseline
- 只回灌已去噪的主线更新、结论、证据和下一步
- 当前过渡态下，人类可读 run 视图仍主要在 `reports/<RUN_ID>/summary.md` 和 `decision.md`
- 当前机器层的最小 run 聚合真相源已落在 `reports/<RUN_ID>/run_summary.json`
- 当前最小写回入口已落在 `python3 tools/evidence.py --set-run-summary --run-id <RUN_ID> ...`
- 当前还支持 `python3 tools/evidence.py --merge-task-summary --run-id <RUN_ID> --task-json-file TASKS/TASK-*.json`，把稳定的 task summary 提升进 run summary
- `run_summary.json` 当前显式保留 `merge_policy`，把字段分成三类：`reconcile_only`、`append_dedup`、`merge_rewrite`
- 当前规则表如下：
  - `active_tasks` / `completed_tasks`: `reconcile_only`
  - `source_tasks` / `verification_overview`: `append_dedup`
  - `key_updates` / `cross_task_decisions` / `cross_task_risks` / `next_run_or_next_tasks`: `merge_rewrite`
- 当前 `merge_rewrite` 仍是规则化轻归并，不做模型改写：它会去掉 task 前缀、做最小 humanize，并对少量高频模式做 run-level 归并
- 当前已显式归并的高频模式包括：
  - 多个 `<role> summary merged` -> `multi-role runtime summaries are now preserved at run level`
  - `test gate=blocked` -> `test gate remains blocked`
  - `all three real summaries are preserved ...` -> 更短的 multi-role run-level 结论
- 当前 `cross_task_risks` 还额外遵守一个窄规则：如果同时存在通用 `test gate remains blocked` 与更具体的 blocked-gate 解释句，则只保留更具体的 run-level 风险句；底层验证证据继续留在 `verification_overview`
- 当前还支持 `python3 tools/evidence.py --reconcile-run-summary --run-id <RUN_ID>`，按同一 run 下的 `TASKS/TASK-*.json` 真实状态重算 `active_tasks/completed_tasks/source_tasks`
- 当前还支持 `python3 tools/evidence.py --compact-run-summary --run-id <RUN_ID>`，为 baseline refresh 生成更短的 `baseline_ready_summary`
- 当前还支持 `python3 tools/evidence.py --normalize-run-summary --run-id <RUN_ID>`，对历史 `merge_rewrite` 字段中的旧 task 前缀条目做显式维护式清理
- `reconcile-run-summary` 的目标是减少 `run_summary.json` 与 task 真相源的手工漂移；它不会自动掩盖历史遗留的 active task
- `normalize-run-summary` 的目标不是批量重写历史，而是在 owner 明确触发维护动作时，只清理已经落在 run-level 语义字段中的旧 task 前缀表达；`verification_overview` 和 `source_tasks` 仍保留原有证据粒度

### 4.7 `appserverclient --summarize-current`

命令：
- `python3 tools/appserverclient.py --summarize-current`

目标：
- 对当前 fork session 做一次去噪总结

输出：
- `session_registry.current_summary`

职责：
- `resume` current session
- 以最小 prompt 生成当前 thread 的去噪摘要
- 读取最新 thread 内容并抽取最后一条 agent 结论
- 把 summary 文本和来源 thread 指针写回 `tools/project_config.json`

当前定位：
- `session_registry.current_summary` 是 thread-level transitional summary
- 当前只有单槽位实现，适合作为最小闭环，不代表最终 run summary
- 多角色场景下，应先有多个 thread summaries，再聚合成 task summary / run summary
- 当前机器层的最小落点是 `TASKS/TASK-*.json -> role_threads / test_gate / task_summary`

### 4.8 `appserverclient --refresh-baseline`

命令：
- `python3 tools/appserverclient.py --refresh-baseline`

目标：
- 优先使用 `run_summary.json` 中的有效增量更新 baseline；缺失时再回退 `session_registry.current_summary`

输入：
- `session_registry.learn_session_baseline`
- `reports/<RUN_ID>/run_summary.json`
- `session_registry.current_summary`（fallback）

职责：
- `resume` baseline session
- 优先用 run summary 发起一次最小 baseline refresh；若 `baseline_ready_summary` 存在，则优先使用其压缩表达
- 不重建 baseline，不回灌聊天噪音
- 把 baseline refresh 文本回写到 `session_registry.current_summary`
- 显式记录本次 refresh 实际消费的是 `run_summary` 还是 `current_summary`

当前与长期边界：
- 当前实现优先消费 `run_summary.json`，仅在缺失时回退 `session_registry.current_summary`
- 当前 `session_registry.current_summary` 还会记录 `baseline_refresh_input_type` 和 `baseline_refresh_input_ref`，用于追踪 baseline refresh 的真实输入来源
- 长期推荐链路应为 `thread summary -> task summary -> run summary -> baseline refresh`
- baseline 长期应优先吸收 run-level stable summaries，而不是直接吸收原始 thread 噪音

## 5. 收尾层

### 5.1 `gitclient --commit`

命令：
- `tools/gitclient.py --commit`
- `tools/gitclient.py --commit "说明"`

目标：
- 完成提交、PR、合并、main 同步

职责：
- 从当前工作面建分支
- commit / push / PR
- 处理直接 merge 和 `--auto` merge
- 等待真正 `MERGED`
- 自动同步本地 `main`

### 5.2 `gitclient --rollback-last`

目标：
- 回滚主线最近一次提交

### 5.3 `gitclient --rollback-commit`

目标：
- 回滚指定提交

## 6. 历史兼容链路

以下链路保留为研发期过渡材料或兼容实现，不再作为当前正式主线：
- `learn`
- `ready`
- `orient`
- `choose`
- `council`
- `arbiter`
- `slice`
- `do`
- `verify`
- `review`
- archived shell entrypoints in `tools/backup/`
- `ship`

条件：
- 当前 run 下 task 全部完成
- 或明确终止

输出：
- `tools/project_config.json -> runtime_state` 更新
- `decision.md` 记录 stop reason

## 8. 正式主线

当前正式主线已经收敛成三层：

1. 准备层
- `python3 tools/init.py`

2. 主流程层
- `python3 tools/appserverclient.py --learnbaseline`
- 明确 run 级需求方向
- `python3 tools/appserverclient.py --fork-current`
- 在 current session 或多角色 fork session 中拆最小 task 并逐个推进
- 阶段结束后把去噪结论回灌 baseline

3. 收尾层
- `python3 tools/gitclient.py --commit`
- `python3 tools/gitclient.py --rollback-last`
- `python3 tools/gitclient.py --rollback-commit <sha>`

说明：
- `init` 是准备层，不属于主业务流程。
- baseline 学习使用 `plan`；日常 session 推进使用 `default`。
- `gitclient` 负责提交、PR、auto merge、回滚和本地同步 `main`。

## 9. 默认日常流程

推荐日常顺序：

1. `python3 tools/init.py`
2. `python3 tools/appserverclient.py --learnbaseline`
3. 人工注入当前 run 的需求方向
4. `python3 tools/appserverclient.py --fork-current`
5. 用 `python3 tools/appserverclient.py --current-turn "..."` 推进当前 session
6. 必要时 fork 多角色 session 做最小 task 处理
7. 去噪后把有效结论回灌 baseline
8. `python3 tools/gitclient.py --commit`

说明：
- baseline 只负责项目级主认知，不直接承载日常噪音讨论。
- 旧的 `learn / ready / orient / choose / council / arbiter / slice_task / run_main / ship.sh` 仍可作为 `tools/backup/` 下的参考资产，但不再是默认正式主线。
- `runtime_state` 允许“当前已有 run，但 task 尚未切出”的中间状态。

## 10. Pause / Resume

当 run 中断时：
- 优先依赖 `tools/project_config.json -> runtime_state`、`session_registry` 和 run evidence 恢复上下文
- `legacy.sh` 只保留历史版本于 `tools/backup/legacy.sh`，不再是正式恢复入口

停止原因统一记录到：
- `reports/<RUN_ID>/decision.md`

标准 stop reason：
- `task_done`
- `needs_human_decision`
- `infra_network`
- `infra_quota_or_auth`
- `tool_or_script_error`
- `verify_failed`
- `external_blocked`

## 11. Documentation Freshness Gate

流程、规则、工具行为变化时，必须在同一 run 更新：
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`（若对象定义变化）
- `docs/PROJECT_GUIDE.md`（若学习语义变化）
- `reports/<RUN_ID>/summary.md`
- `reports/<RUN_ID>/decision.md`

没有文档同步，不得 ship。
