# TOOLS_REFACTOR_BLUEPRINT

本文件是 `tools` 体系后续重构的硬约束蓝图。

它不是评论，不是建议集，不是草稿。
它用于固定：

- 目标分层
- 公共能力抽离顺序
- 现有文件和方法归属
- 状态机契约
- `run_main.py` 最终边界
- 后续迁移顺序与验收标准

本蓝图先明确一个纠偏：

- 第一刀不是按 `init -> learn -> ready` 这些阶段拆。
- 第一刀必须先把阶段脚本里的非阶段职责拔干净。

因此，本蓝图采用如下重构顺序：

1. 先抽离流程无关的公共 helper
2. 再抽离 artifact / state 能力
3. 再统一 logging
4. 在前三者稳定后，才定义 workflow layer
5. 最后收缩 `run_main.py` 与 runtime layer

## 1. 目标分层定义

本蓝图保留 5 个正式目标层。

但在这 5 层之外，额外固定一个前置基础集合：

- `common helpers foundation`

它不是业务层，不算入正式 5 层。
它是所有正式层在重构前必须先清理出的公共基础。

### 1.0 Common Helpers Foundation

定义：
所有与具体流程阶段无关、与具体 artifact 真相源无关、与具体 runtime 协议无关的公共方法集合。

典型方法：
- `read_json`
- `read_text`
- `write_json`
- `file_sha`
- `normalize_scope`
- `dedup_lines`
- `dedup_acceptance`
- `split_scope`
- `short_text`
- `parse_bool_flag`
- `ordered_unique`
- `first_line`
- `count_lines`
- `list_lines`

职责：
- 提供纯函数或近纯函数的公共工具能力
- 提供通用文本、列表、hash、简单文件读取、参数标准化能力
- 不承载阶段语义

不负责什么：
- 不负责任何阶段推进
- 不负责 `TASKS/STATE.md` 真相读写
- 不负责 `reports/<RUN_ID>/` 产物定位
- 不负责日志 schema
- 不负责 app-server 协议

允许依赖：
- Python 标准库

禁止依赖：
- 禁止依赖 `workflow layer`
- 禁止依赖 `entry layer`
- 禁止依赖 `runtime layer`
- 禁止依赖任何当前 run/project 状态

硬约束：
- 任何“流程无关的方法”必须先归入这里，再谈阶段重构。
- 阶段脚本不得继续保留明显可复用的公共 helper。

### 1.1 Entry Layer

定义：
唯一对外 Python 主入口层。长期形态是普通窗口执行的总入口。

职责：
- 接收命令行参数
- 解析运行模式、目标项目、目标 run、目标阶段
- 建立一次 run 的入口上下文
- 调用 workflow layer

不负责什么：
- 不负责阶段内部规则
- 不负责真相源读写细节
- 不负责日志实现
- 不负责 app-server 协议细节

允许依赖：
- `workflow layer`
- `logging layer`
- `storage / artifact layer` 的最薄上下文读取接口

禁止依赖：
- 禁止直接依赖具体阶段脚本的内部 helper
- 禁止直接拼装 artifact 内容
- 禁止直接实现模型 transport

硬约束：
- `run_main.py` 最终只能是入口薄壳。

### 1.2 Workflow Layer

定义：
状态机推进层。只负责定义和执行阶段契约。

职责：
- 定义每个阶段的输入
- 定义每个阶段的输出
- 定义每个阶段的失败条件
- 定义每个阶段的恢复动作
- 定义合法下一跳

不负责什么：
- 不负责公共 helper 细节
- 不负责状态和 artifact 底层读写
- 不负责日志 schema
- 不负责 app-server 协议
- 不负责 CLI 参数解析

允许依赖：
- `common helpers foundation`
- `storage / artifact layer`
- `logging layer`
- `runtime layer`

禁止依赖：
- 禁止反向依赖 `entry layer`
- 禁止在阶段实现里散写路径规则
- 禁止在阶段实现里散写日志实现

硬约束：
- workflow 里只保留真正的阶段逻辑。
- 一切非阶段职责都必须先被拔走。

### 1.3 Runtime Layer

定义：
程序化 Codex 交互层。长期承接 `Python orchestrator + app-server`。

职责：
- 管理 thread / session
- 管理 turn 生命周期
- 管理 model / reasoning / collaboration mode
- 接收和标准化 agent events
- 将运行时结果返回给 workflow

不负责什么：
- 不负责状态机跳转
- 不负责 artifact 真相写入
- 不负责日志 schema
- 不负责 CLI 参数解析

允许依赖：
- `logging layer`
- `common helpers foundation`

禁止依赖：
- 禁止依赖 `entry layer`
- 禁止直接写 `TASKS/STATE.md`
- 禁止直接写 `reports/*.md`

硬约束：
- 所有程序化 Codex 交互最终都要进 runtime layer。

### 1.4 Storage / Artifact Layer

定义：
状态与产物真相层。只负责 `TASKS/`、`reports/`、`learn/` 等真相源的访问和定位。

职责：
- 读取和更新 `TASKS/STATE.md`
- 读取和写入 `TASKS/TASK-*.md`
- 读取和写入 `reports/<RUN_ID>/...`
- 读取和写入 `learn/<project_id>.*`
- 提供统一 `resolve_*_for_run/project`
- 提供统一 artifact path policy

不负责什么：
- 不负责阶段业务判断
- 不负责日志 schema
- 不负责 app-server 协议
- 不负责 CLI 参数解析

允许依赖：
- `common helpers foundation`
- `logging layer`

禁止依赖：
- 禁止依赖 `workflow layer`
- 禁止依赖 `runtime layer`
- 禁止依赖 `entry layer`

硬约束：
- 所有 `resolve_*_for_run/project`
- 所有 `update_state_current`
- 所有 run evidence / state 读写
必须收敛到这一层。

### 1.5 Logging Layer

定义：
统一日志与事件层。只负责日志 schema、日志路由、事件落盘。

职责：
- 定义统一日志 schema
- 输出 step/event/error/audit 日志
- 提供 stdout/stderr line capture
- 提供 run-scoped logging context

不负责什么：
- 不负责阶段决策
- 不负责 artifact 真相判断
- 不负责 app-server 协议
- 不负责 CLI 参数解析

允许依赖：
- `common helpers foundation`

禁止依赖：
- 禁止依赖 `workflow layer`
- 禁止依赖 `runtime layer`
- 禁止依赖 `entry layer`
- 禁止依赖 artifact 业务规则

硬约束：
- 所有脚本日志实现最终必须统一进入 logging layer。

## 2. 现有文件 -> 目标层映射表

### 2.1 文件级映射

| 文件名 | 当前职责 | 目标归属层 | 是否需要拆分 | 第一轮是否迁移 | 迁移理由 |
| --- | --- | --- | --- | --- | --- |
| `tools/run_main.py` | 参数解析、步骤选择、状态读取、子进程编排、日志实现 | `entry layer`，并剥离 `storage/logging/workflow` 越界职责 | 必须拆分 | 否 | 它不是第一刀；必须在 helpers/artifact/logging 稳定后再收缩 |
| `tools/init.py` | 初始化诊断 + state 读取 + 输出日志 + 命令执行 + 文本处理 | `workflow layer`，并先抽 `helpers/storage/logging` | 必须拆分 | 是 | 有大量非阶段职责，适合作为第一批清理样本 |
| `tools/learn.py` | 学习阶段规则 + guide 解析 + 文件 IO + hash + state 读取 + model transport | `workflow layer` + `runtime layer`，并先抽 `helpers/storage` | 必须拆分 | 是 | 当前混合最严重，helper 和 artifact 逻辑过多 |
| `tools/ready.py` | 门禁规则 + state 更新 + run evidence 事件 + 文件 IO + 参数标准化 | `workflow layer`，并先抽 `helpers/storage/logging` | 必须拆分 | 是 | 这里聚集了大量 artifact/state 能力，必须尽早抽出 |
| `tools/orient.py` | 方向草案规则 + 读取 ready/evidence + 更新 state/事件 | `workflow layer`，并先抽 `helpers/storage` | 必须拆分 | 是 | 现阶段逻辑少，适合快速剥离出纯阶段逻辑 |
| `tools/choose.py` | 方向确认 + resolve orient 文件 + 更新 state/事件 | `workflow layer`，并先抽 `storage` | 必须拆分 | 是 | 当前大量依赖 `ready.py` 的状态能力，边界错误 |
| `tools/council.py` | 多角色评审 + 文件读取 + scope 标准化 | `workflow layer`，并先抽 `helpers/storage` | 必须拆分 | 是 | `normalize_scope` 明显是公共 helper，不应留在阶段脚本 |
| `tools/arbiter.py` | 合同收敛 + 文件读取 + scope 标准化 + 文本去重 | `workflow layer`，并先抽 `helpers/storage` | 必须拆分 | 是 | `normalize_scope/dedup_lines` 是公共能力，必须先拔 |
| `tools/slice_task.py` | 切片规则 + 合同读取 + acceptance 去重 + queue 更新 | `workflow layer`，并先抽 `helpers/storage` | 必须拆分 | 是 | `load_contract/dedup_acceptance` 不应粘在阶段壳上 |
| `tools/codex_transport.py` | 模型 transport / app-server 交互 | `runtime layer` | 需要标准化 | 否 | 要放在最后收敛，不可抢在 helper/artifact 之前改 |
| `tools/legacy.sh` | 兼容路由 | 临时兼容层 | 暂不处理 | 否 | 不属于第一轮重构主线 |

### 2.2 公共 helper 候选方法映射

以下方法必须先从阶段脚本中抽出，进入 `common helpers foundation`。

| 当前方法 | 现所在文件 | 说明 | 第一轮是否迁移 |
| --- | --- | --- | --- |
| `read_json` | `learn.py` / `ready.py` / `orient.py` / `council.py` / `arbiter.py` | 通用 JSON 读取，不属于具体阶段 | 必须 |
| `read_text` | `learn.py` / `ready.py` / `council.py` | 通用文本读取，不属于具体阶段 | 必须 |
| `write_json` | `learn.py` | 通用 JSON 写入，不属于具体阶段 | 必须 |
| `file_sha` | `learn.py` / `ready.py` | 通用摘要计算 | 必须 |
| `normalize_scope` | `council.py` / `arbiter.py` | 公共 scope 标准化 | 必须 |
| `dedup_lines` | `arbiter.py` | 通用去重 | 必须 |
| `dedup_acceptance` | `slice_task.py` | 通用 acceptance 去重 | 必须 |
| `split_scope` | `orient.py` | 通用文本拆 scope | 必须 |
| `short_text` | `orient.py` | 通用短文本压缩 | 必须 |
| `parse_bool_flag` | `ready.py` | 通用布尔参数标准化 | 必须 |
| `ordered_unique` | `learn.py` | 通用去重 | 必须 |
| `normalize_block` / `normalize_list` | `learn.py` | 通用文本归一化 | 必须 |
| `first_line` / `count_lines` / `list_lines` | `init.py` | 通用命令结果整理 | 必须 |

### 2.3 Artifact / State 能力映射

以下能力必须从阶段脚本中抽出，进入 `storage / artifact layer`。

| 当前方法/能力 | 现所在文件 | 说明 | 第一轮是否迁移 |
| --- | --- | --- | --- |
| `state_field_value` | `init.py` / `learn.py` / `ready.py` / `run_main.py` | 读取 `TASKS/STATE.md` | 必须 |
| `resolve_state_current_run_id` / `resolve_state_current_project_id` | `init.py` / `ready.py` | 当前 active 指针解析 | 必须 |
| `read_state_snapshot` | `learn.py` | 当前状态快照 | 必须 |
| `resolve_project_id_for_cmd` / `resolve_run_id_for_cmd` | `learn.py` / `ready.py` 及被其他文件引用 | 运行上下文解析 | 必须 |
| `resolve_latest_report_run_id` | `ready.py` | run fallback 解析 | 必须 |
| `resolve_learn_file_for_project` | `learn.py` / `ready.py` | learn artifact 定位 | 必须 |
| `resolve_sync_file_for_run` | `ready.py` | sync artifact 定位 | 必须 |
| `resolve_ready_prior_decision_for_run` | `ready.py` | 历史 ready 决策定位 | 必须 |
| `resolve_orient_file_for_run` | `choose.py` | orient artifact 定位 | 必须 |
| `load_contract` | `slice_task.py` | execution contract 读取 | 必须 |
| `update_state_current` | `ready.py` 及被多阶段引用 | 状态回写 | 必须 |
| `append_execution_event` | `ready.py` 及被多阶段引用 | 运行事件记录 | 必须 |
| `append_conversation_checkpoint` | `ready.py` 及被多阶段引用 | 会话检查点记录 | 必须 |

### 2.4 Logging 能力映射

以下能力必须从脚本中抽出，进入 `logging layer`。

| 当前方法/能力 | 现所在文件 | 说明 | 第一轮是否迁移 |
| --- | --- | --- | --- |
| `Logger.__init__/close/_emit/info/error` | `run_main.py` | 当前总入口日志器实现 | 必须 |
| `stream_reader` | `run_main.py` | 子进程逐行日志采集 | 必须 |
| `emit_json_event` | `init.py` / `ready.py` | 阶段事件输出 | 必须 |
| `emit_step` | `init.py` / `learn.py` / `ready.py` | 阶段锚点输出 | 必须 |
| 统一日志 schema | 当前散落在多个脚本 | 无统一格式 | 必须 |

### 2.5 纯阶段逻辑保留映射

以下逻辑在前三类抽离完成后，才允许留在 `workflow layer`。

| 文件 | 保留为阶段逻辑的方法 |
| --- | --- |
| `init.py` | `main`，以及必要的初始化诊断规则 |
| `learn.py` | `parse_project_guide`、`parse_north_star`、`build_base_learn`、`generate_prompt`、`parse_model_output`、`update_learn_with_model`、`learn_file_is_valid`、`learn_file_matches_project`、`main` |
| `ready.py` | `learn_file_is_valid`、`learn_file_matches_project`、`sync_file_is_valid`、`extract_task_goal_default`、`extract_task_scope_default`、`extract_task_acceptance_default`、`resolve_ready_field`、`main` |
| `orient.py` | `generate_orient_draft`、`main` |
| `choose.py` | `main` |
| `council.py` | `check_status`、`role_decision`、`main` |
| `arbiter.py` | `non_goals_from_scope` 的阶段性部分、`main` |
| `slice_task.py` | `build_tasks_from_contract`、`main` |

## 3. 状态机契约

本节在“非阶段职责已抽离”的前提下定义。
也就是说，下面每个阶段只保留真正的阶段逻辑，不再夹带公共 helper、artifact 读写、日志实现。

### 3.1 `init`

输入：
- 当前仓库工作区
- 当前 state 快照
- git 诊断结果

输出：
- 初始化诊断结论
- 当前上下文可继续/需恢复判断

产物路径：
- 默认只要求日志和标准化阶段结果对象
- 可选产物：`reports/<RUN_ID>/init.json`

失败条件：
- 仓库上下文无法识别
- state 真相缺失且无法恢复
- git 诊断失败

恢复动作：
- 修复仓库位置或 state
- 重新运行 `init`

下一步允许进入：
- `learn`

### 3.2 `learn`

输入：
- owner docs
- 必查文件列表
- 当前 state 快照
- 当前 learn artifact
- runtime 返回的模型结果

输出：
- 项目同频结果
- 标准化 `learn` 产物

产物路径：
- `learn/<project_id>.json`
- `learn/<project_id>.md`
- `learn/<project_id>.stdout.log`
- `learn/<project_id>.model.*`

失败条件：
- owner docs 缺失
- `PROJECT_GUIDE` 解析失败
- model sync 未完成
- oral restatement 不完整
- learn 产物校验失败

恢复动作：
- 修复 docs / learn artifact
- 重新运行 `learn`

下一步允许进入：
- `ready`

### 3.3 `ready`

输入：
- 当前 state 快照
- 当前 task 合同
- `learn` 结果
- 当前 run evidence

输出：
- 开工许可
- 当前 run/task 最小合同

产物路径：
- `reports/<RUN_ID>/ready.json`

失败条件：
- `learn` 不合法
- 当前 task 合同缺字段
- run 状态不允许开工

恢复动作：
- 回到 `learn`
- 修复 task/state
- 重新运行 `ready`

下一步允许进入：
- `orient`
- 特殊直达执行通道未来单独定义，不作为当前默认主线

### 3.4 `orient`

输入：
- `ready` 结果
- 当前 run evidence
- 当前 learn 结果

输出：
- 候选方向集合

产物路径：
- `reports/<RUN_ID>/orient.json`

失败条件：
- `ready` 结果缺失
- 方向集合为空

恢复动作：
- 回到 `ready`
- 重新运行 `orient`

下一步允许进入：
- `choose`

### 3.5 `choose`

输入：
- `orient` 结果
- 用户选择的 option

输出：
- 选定方向
- 方向合同

产物路径：
- `reports/<RUN_ID>/orient_choice.json`
- `reports/<RUN_ID>/direction_contract.json`

失败条件：
- `orient` 缺失
- `OPTION` 非法

恢复动作：
- 回到 `orient`
- 重新运行 `choose`

下一步允许进入：
- `council`

### 3.6 `council`

输入：
- `direction_contract`
- 当前 scope 对应的核心材料

输出：
- 多角色评审结果

产物路径：
- 目标真相源：`reports/<RUN_ID>/council.json`

失败条件：
- direction contract 缺失
- 评审结果不完整
- blocker 未明确

恢复动作：
- 回到 `choose`
- 重新运行 `council`

下一步允许进入：
- `arbiter`

### 3.7 `arbiter`

输入：
- `council` 结果
- `direction_contract`

输出：
- `execution_contract`

产物路径：
- `reports/<RUN_ID>/execution_contract.json`
- `reports/<RUN_ID>/execution_contract.md`

失败条件：
- `council` 结果缺失
- `direction_contract` 缺失
- 无法收敛成单一执行边界

恢复动作：
- 回到 `council`
- 必要时回到 `choose`
- 重新运行 `arbiter`

下一步允许进入：
- `slice`

### 3.8 `slice`

输入：
- `execution_contract`

输出：
- 最小任务切片
- queue block

产物路径：
- `reports/<RUN_ID>/slice_state.json`
- `TASKS/QUEUE.md`

失败条件：
- execution contract 缺失
- 切片为空
- acceptance 无法落到 task 级

恢复动作：
- 回到 `arbiter`
- 重新运行 `slice`

下一步允许进入：
- `do`

### 3.9 `do`

输入：
- `slice_state`
- 当前 task 文件
- 当前项目代码与文档

输出：
- 实际改动
- 更新后的 run evidence

产物路径：
- 工作树变更
- `reports/<RUN_ID>/summary.md`
- `reports/<RUN_ID>/decision.md`

失败条件：
- 无有效 task
- 改动越界
- evidence 未更新

恢复动作：
- 回到 `slice`
- 缩 scope
- 重新运行 `do`

下一步允许进入：
- `review`
- `verify`

### 3.10 `review`

输入：
- `do` 后工作树
- verify 结果
- 当前 run evidence

输出：
- review 结论
- 风险与遗留问题

产物路径：
- `reports/<RUN_ID>/review.md`

失败条件：
- verify 未通过
- evidence 不完整
- 改动与合同不一致

恢复动作：
- 回到 `do`
- 修复问题后重跑 `review`

下一步允许进入：
- `ship`

### 3.11 `ship`

输入：
- review 通过
- verify 通过
- docs freshness 通过

输出：
- 正式交付动作

产物路径：
- `reports/<RUN_ID>/ship_state.json`

失败条件：
- review 未通过
- verify 未通过
- 文档未更新
- 远端操作失败

恢复动作：
- 回到 `review`
- 必要时回到 `do`

下一步允许进入：
- run close

## 4. `run_main.py` 的最终职责边界

### 4.1 它最终只允许负责什么

- 解析 CLI 参数
- 解析最小入口上下文
- 初始化 run 级 logging context
- 调用 workflow layer 的统一接口
- 返回统一退出码

### 4.2 它绝对不允许负责什么

- 不允许自己维护公共 helper
- 不允许自己读写 `TASKS/STATE.md`
- 不允许自己定位 `reports/learn` 产物
- 不允许自己拼阶段规则
- 不允许自己实现日志器
- 不允许自己持有 app-server 协议细节

### 4.3 它现在有哪些越界职责

- `state_field_value`：越界到 artifact/state
- `build_step_specs`：越界到 workflow
- `Logger`：越界到 logging
- `stream_reader`：越界到 logging
- `run_step`：越界到 workflow + logging

### 4.4 这些越界职责未来应拆到哪一层

- `state_field_value` -> `storage / artifact layer`
- `build_step_specs` -> `workflow layer`
- `Logger` -> `logging layer`
- `stream_reader` -> `logging layer`
- `run_step` -> `workflow layer` 调用 `logging layer`

### 4.5 硬边界

- `run_main.py` 只能在最后阶段收缩。
- 在 helper / artifact / logging 还没抽离前，禁止直接重写成所谓“纯 orchestrator”。
- `run_main.py` 的收缩必须发生在 workflow 契约稳定之后。

## 5. 迁移顺序

迁移顺序必须固定如下，不允许跳步：

1. `common helpers foundation`
2. `storage / artifact layer`
3. `logging layer`
4. `workflow layer`
5. `entry layer` 收缩
6. `runtime layer`

### 5.1 第一步：Common Helpers Foundation

本轮迁移目标：
- 把所有流程无关的方法从阶段脚本中抽离出来。
- 让每个阶段脚本先失去“通用工具箱”身份。

需要动哪些文件：
- `tools/init.py`
- `tools/learn.py`
- `tools/ready.py`
- `tools/orient.py`
- `tools/council.py`
- `tools/arbiter.py`
- `tools/slice_task.py`
- 新增公共 helper 模块，例如 `tools/common_helpers.py`

风险是什么：
- 同名方法分布在多个文件里，抽离时可能行为不一致。
- 某些 helper 其实混入了阶段语义，需要谨慎裁剪。

如何验收：
- 上文 `2.2` 表中的 helper 全部迁出阶段脚本。
- 阶段脚本中不再保留明显通用的文本/列表/hash/简单 IO helper。
- 公共 helper 模块不依赖任何阶段语义和 state 真相。

完成后系统会获得什么边界收敛：
- 脚本先从“杂糅工具箱”变成“较纯的阶段壳”。

### 5.2 第二步：Storage / Artifact Layer

本轮迁移目标：
- 把所有 state/artifact 真相读写能力从阶段脚本里拔出来。

需要动哪些文件：
- `tools/run_main.py`
- `tools/init.py`
- `tools/learn.py`
- `tools/ready.py`
- `tools/orient.py`
- `tools/choose.py`
- `tools/council.py`
- `tools/arbiter.py`
- `tools/slice_task.py`
- 新增 artifact/state 模块，例如 `tools/state_store.py`、`tools/artifacts.py`

风险是什么：
- 当前很多阶段通过 `ready.py` 间接复用状态写入能力，拆开后会暴露更多边界错误。
- 历史兼容路径会和新真相源路径冲突。

如何验收：
- 上文 `2.3` 表中的能力全部迁出阶段脚本。
- 阶段脚本不再本地实现 `state_field_value`、`resolve_*_for_run/project`、`update_state_current`。
- `reports/`、`TASKS/`、`learn/` 访问统一通过 storage/artifact 接口完成。

完成后系统会获得什么边界收敛：
- 状态和证据真相源被集中。
- 阶段脚本不再自己碰状态真相。

### 5.3 第三步：Logging Layer

本轮迁移目标：
- 统一日志 schema、逐行采集、事件输出能力。

需要动哪些文件：
- `tools/run_main.py`
- `tools/init.py`
- `tools/learn.py`
- `tools/ready.py`
- 新增日志模块，例如 `tools/logging_runtime.py`

风险是什么：
- 关键锚点输出可能被破坏。
- CLI 现有可读性可能短期下降。

如何验收：
- 上文 `2.4` 表中的能力全部迁出脚本。
- `run_main.py` 不再内置 `Logger`。
- 阶段锚点与统一日志 schema 可以同时存在，并有清晰边界。

完成后系统会获得什么边界收敛：
- 日志实现从阶段逻辑中剥离。
- 后续 workflow 和 runtime 都可复用统一日志接口。

### 5.4 第四步：Workflow Layer

本轮迁移目标：
- 在前三类非阶段职责拔净后，正式固化阶段契约。

需要动哪些文件：
- `tools/init.py`
- `tools/learn.py`
- `tools/ready.py`
- `tools/orient.py`
- `tools/choose.py`
- `tools/council.py`
- `tools/arbiter.py`
- `tools/slice_task.py`
- 新增 workflow 模块，例如 `tools/workflow_steps.py`
- 同步更新 [docs/WORKFLOW.md](/root/quant-factory-os/docs/WORKFLOW.md)

风险是什么：
- 历史脚本壳和新 workflow 接口会双轨并存一段时间。
- 如果前三类没抽净，workflow 会再次被污染。

如何验收：
- 每个阶段只保留真正阶段逻辑。
- 每个阶段都对应本蓝图第 3 节的契约。
- workflow 接口成为阶段执行唯一正式入口。

完成后系统会获得什么边界收敛：
- 状态机从“脚本集合”收敛成“契约化阶段层”。

### 5.5 第五步：Entry Layer 收缩

本轮迁移目标：
- 在 workflow 稳定后，把 `run_main.py` 收缩成入口薄壳。

需要动哪些文件：
- `tools/run_main.py`
- workflow 入口接口
- logging 上下文接口
- storage 上下文读取接口

风险是什么：
- 现有直接脚本调用的灵活性会下降。
- 如果 workflow 接口未稳定，入口会反复返工。

如何验收：
- `run_main.py` 只剩参数解析、上下文解析、workflow 调用、退出码。
- 文件中不再有 `Logger`、`stream_reader`、`build_step_specs`、`state_field_value` 的实现。

完成后系统会获得什么边界收敛：
- 真正的单入口形成。

### 5.6 第六步：Runtime Layer

本轮迁移目标：
- 最后收敛 app-server 交互，让模型调用不再散落在阶段脚本里。

需要动哪些文件：
- `tools/learn.py`
- `tools/codex_transport.py`
- 新增 runtime 模块，例如 `tools/runtime_app_server.py`
- 必要时更新 [docs/WORKFLOW.md](/root/quant-factory-os/docs/WORKFLOW.md) 与 [docs/ENTITIES.md](/root/quant-factory-os/docs/ENTITIES.md)

风险是什么：
- 这是最靠近真实模型交互的一层，行为回归风险最高。
- 如果前五步没完成，runtime 接口会反复重做。

如何验收：
- `learn.py` 不再自己拼 transport 细节。
- workflow 只通过 runtime 标准接口拿模型结果。
- app-server 交互可独立审计。

完成后系统会获得什么边界收敛：
- `Python orchestrator + app-server` 的长期形态真正成立。

## 6. 当前边界

### 6.1 必须

- 必须先按 `helpers -> artifact/state -> logging -> workflow -> entry -> runtime` 的顺序推进。
- 必须先拔非阶段职责，再谈阶段层。
- 必须以后续所有重构都引用本蓝图。

### 6.2 禁止

- 禁止跳过 `common helpers foundation` 直接按阶段重写。
- 禁止在 state/artifact 未抽离前重写 workflow。
- 禁止在 logging 未统一前宣称已有正式 orchestrator。
- 禁止在前五步未完成前提前大改 runtime。

### 6.3 第一轮先做

- `common helpers foundation`
- `storage / artifact layer`
- `logging layer`

### 6.4 第二轮再做

- `workflow layer`
- `entry layer` 收缩
- `runtime layer`

### 6.5 验收标准

- 每一轮都必须给出明确文件清单。
- 每一轮都必须说明哪些能力被迁出。
- 每一轮都必须说明迁出后哪些阶段逻辑得以净化。
- 没有验收标准的迁移视为未开始。

## 7. 完成标准

本次蓝图任务是否完成，只看以下 4 条：

1. 是否给出完整目标分层定义，并明确 `common helpers foundation` 的前置地位。
2. 是否给出文件级、方法级映射，特别是公共 helper / artifact-state / logging 三类映射。
3. 是否给出状态机契约，并明确阶段只保留真正阶段逻辑。
4. 是否给出新的迁移顺序和每一步验收方法。

四条缺任意一条，都算未完成。
