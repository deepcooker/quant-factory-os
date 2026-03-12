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

### 4.3 `appserverclient --fork-current`

命令：
- `python3 tools/appserverclient.py --fork-current`

目标：
- 从 baseline 派生当前工作 session

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

说明：
- 这是当前正式主线的发展方向
- 角色 session 应互不干扰
- 每个角色 session 结束后要先做去噪总结，再考虑回灌 baseline
- 当前正式 task 入口是 `python3 tools/taskclient.py --next`，用于从 `TASKS/QUEUE.json` 选择并绑定下一个 active task
- 当前也可用 `python3 tools/taskclient.py --create ...` 生成新的 JSON-first task，并按需追加到 `TASKS/QUEUE.json` 或直接激活
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

### 4.7 `appserverclient --summarize-current`

命令：
- `python3 tools/appserverclient.py --summarize-current`

目标：
- 对当前 fork session 做一次去噪总结

输出：
- `session_registry.current_summary`

职责：
- `resume` current session
- 以最小 prompt 生成 run 级去噪摘要
- 读取最新 thread 内容并抽取最后一条 agent 结论
- 把 summary 文本和来源 thread 指针写回 `tools/project_config.json`

### 4.8 `appserverclient --refresh-baseline`

命令：
- `python3 tools/appserverclient.py --refresh-baseline`

目标：
- 只使用 `session_registry.current_summary` 中的有效增量更新 baseline

输入：
- `session_registry.learn_session_baseline`
- `session_registry.current_summary`

职责：
- `resume` baseline session
- 用 current summary 发起一次最小 baseline refresh
- 不重建 baseline，不回灌聊天噪音
- 把 baseline refresh 文本回写到 `session_registry.current_summary`

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
