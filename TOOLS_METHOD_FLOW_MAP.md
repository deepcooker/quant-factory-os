# TOOLS_METHOD_FLOW_MAP

这份文档现在按新的整理顺序来写：

1. 先看和业务流程无关的公共 helper
2. 再看各阶段脚本剩下的真正阶段方法
3. 最后看阶段流程调用链

这份文档不再把“公共能力”和“阶段逻辑”混在一起。

## 1. 编号分段

| 编号段 | 文件 | 归类 | 说明 |
| --- | --- | --- | --- |
| `0001-0099` | `tools/common_helpers.py` | 公共 helper | 与具体流程阶段无关的通用能力 |
| `1001-1099` | `tools/init.py` | 阶段逻辑 | 初始化诊断 |
| `2001-2099` | `tools/learn.py` | 阶段逻辑 | 学习同频 |
| `3001-3099` | `tools/ready.py` | 阶段逻辑 | 开工门禁 |
| `4001-4099` | `tools/orient.py` | 阶段逻辑 | 方向草案 |
| `5001-5099` | `tools/choose.py` | 阶段逻辑 | 方向确认 |
| `6001-6099` | `tools/council.py` | 阶段逻辑 | 多角色评审 |
| `7001-7099` | `tools/arbiter.py` | 阶段逻辑 | 合同收敛 |
| `8001-8099` | `tools/slice_task.py` | 阶段逻辑 | 任务切片 |
| `9001-9099` | `tools/run_main.py` | 入口/待收缩 | Python 总入口 |

## 2. 方法总表

### 2.1 `tools/common_helpers.py`

文件职责：承接从阶段脚本中抽出的流程无关公共能力。

| 编号 | 方法名 | 中文解释 |
| --- | --- | --- |
| `0001` | `read_json` | 读取 JSON 文件，缺失或解析失败时返回空字典。 |
| `0002` | `read_text` | 读取文本文件，缺失时返回空字符串。 |
| `0003` | `write_json` | 把对象写入 JSON 文件。 |
| `0004` | `file_sha` | 计算文件 SHA256 摘要，缺失或出错时返回标记值。 |
| `0005` | `ordered_unique` | 按原顺序去重并过滤空项。 |
| `0006` | `normalize_block` | 标准化多行文本块内容。 |
| `0007` | `normalize_list` | 标准化多行列表条目。 |
| `0008` | `normalize_scope` | 标准化 scope 路径列表。 |
| `0009` | `dedup_lines` | 按大小写不敏感方式去重文本行。 |
| `0010` | `dedup_acceptance` | 去重 acceptance 条目并压缩空白。 |
| `0011` | `split_scope` | 把逗号分隔的 scope 文本拆成列表。 |
| `0012` | `short_text` | 把长文本压缩成短句。 |
| `0013` | `parse_bool_flag` | 解析布尔型命令行标志。 |
| `0014` | `first_line` | 提取文本中的第一条非空行。 |

### 2.2 `tools/init.py`

文件职责：初始化前置检查入口。当前主线已经收成“固定配置 + 5 个业务步骤”，其余方法都是支撑能力。

| 编号 | 方法名 | 中文解释 |
| --- | --- | --- |
| `1001` | `parse_args` | 解析 `init` 的唯一附加开关，当前只允许 `-log`。 |
| `1002` | `run_cmd` | 执行直接命令并返回结构化结果。 |
| `1003` | `run_shell` | 通过 shell 执行命令字符串并返回结构化结果。 |
| `1004` | `load_project_config` | 读取固定项目常量配置。 |
| `1005` | `check_project_files` | 检查项目路径和关键 owner docs。 |
| `1006` | `check_codex_runtime` | 检查 Codex、app-server 和 session 前提。 |
| `1007` | `check_git_runtime` | 检查 git 仓库、远端、认证和工作区状态。 |
| `1008` | `finalize_init` | 汇总前四步检查结果，输出总状态、原因代码和下一步。 |
| `1009` | `main` | 按 5 个业务步骤执行 `init`。 |

### 2.3 `tools/learn.py`

文件职责：学习同频入口。公共文本、IO、hash helper 已抽出，当前保留学习阶段规则与模型交互逻辑。

| 编号 | 方法名 | 中文解释 |
| --- | --- | --- |
| `2001` | `eprint` | 向标准错误输出 `learn` 错误信息。 |
| `2002` | `normalize_project_id` | 规范化 `project_id`。 |
| `2003` | `state_field_value` | 从 `TASKS/STATE.md` 读取字段。 |
| `2004` | `read_state_snapshot` | 读取当前 `project/run/task/status` 快照。 |
| `2005` | `resolve_project_id_for_cmd` | 校验并确定本次 `learn` 使用的 `project_id`。 |
| `2006` | `should_emit_json_stream` | 判断是否输出 JSON 事件流。 |
| `2007` | `emit_step` | 输出 `learn` 的步骤锚点日志。 |
| `2008` | `parse_north_star` | 解析 `PROJECT_GUIDE` 北极星。 |
| `2009` | `resolve_dynamic_path` | 解析带占位符的动态路径。 |
| `2010` | `parse_project_guide` | 解析题目、答案、必查文件、主线信息。 |
| `2011` | `parse_cli` | 解析 `learn` 命令行参数。 |
| `2012` | `run_logged_self` | 以镜像日志模式重启 `learn`。 |
| `2013` | `build_base_learn` | 生成基础 `learn` 产物骨架。 |
| `2014` | `print_base_anchors` | 打印 `learn` 基础锚点。 |
| `2015` | `generate_prompt` | 生成发给 Codex 的学习提示词。 |
| `2016` | `path_reference_matches` | 检查模型输出里的路径引用是否合规。 |
| `2017` | `extract_first_learn_json_dict` | 从原始文本里抽取首个合法 `learn` JSON。 |
| `2018` | `extract_learn_json_from_events` | 从事件流中恢复 `learn` JSON。 |
| `2019` | `parse_model_output` | 解析模型输出。 |
| `2020` | `print_model_anchors` | 打印模型侧锚点。 |
| `2021` | `update_learn_with_model` | 将模型结果回写到主 `learn` 产物。 |
| `2022` | `learn_file_is_valid` | 校验 `learn` 文件是否达标。 |
| `2023` | `learn_file_matches_project` | 检查 `learn` 文件是否属于当前项目。 |
| `2024` | `resolve_learn_file_for_project` | 定位当前项目的 `learn` 文件。 |
| `2025` | `main` | 执行 `learn` 主流程。 |

### 2.4 `tools/ready.py`

文件职责：开工前门禁。公共文件 IO、布尔解析、hash helper 已抽出，当前仍保留较多 state/artifact 能力。

| 编号 | 方法名 | 中文解释 |
| --- | --- | --- |
| `3001` | `eprint` | 向标准错误输出 `ready` 错误信息。 |
| `3002` | `should_emit_json_stream` | 判断是否需要输出 JSON 事件流。 |
| `3003` | `emit_json_event` | 输出 `ready` 结构化 JSON 事件。 |
| `3004` | `emit_step` | 输出 `ready` 步骤锚点。 |
| `3005` | `run_cmd` | 直接执行命令。 |
| `3006` | `run_shell` | 通过 shell 执行命令。 |
| `3007` | `state_field_value` | 从 `TASKS/STATE.md` 读取字段。 |
| `3008` | `normalize_project_id` | 规范化 `project_id`。 |
| `3009` | `resolve_state_current_project_id` | 读取当前 active `project_id`。 |
| `3010` | `resolve_state_current_run_id` | 读取当前 active `run_id`。 |
| `3011` | `resolve_latest_report_run_id` | 回退定位最近的 report run。 |
| `3012` | `resolve_run_id_for_cmd` | 解析本次 `ready` 使用的 `run_id`。 |
| `3013` | `resolve_project_id_for_cmd` | 解析本次 `ready` 使用的 `project_id`。 |
| `3014` | `learn_file_is_valid` | 校验 `learn` 文件是否可用。 |
| `3015` | `learn_file_matches_project` | 检查 `learn` 文件是否属于当前项目。 |
| `3016` | `resolve_learn_file_for_project` | 定位当前项目的 `learn` 文件。 |
| `3017` | `sync_file_is_valid` | 校验同步文件是否有效。 |
| `3018` | `resolve_sync_file_for_run` | 定位指定 `run` 的同步文件。 |
| `3019` | `resolve_ready_prior_decision_for_run` | 读取历史 `ready` 决策。 |
| `3020` | `extract_task_goal_default` | 从 task 文件提取默认目标。 |
| `3021` | `extract_task_scope_default` | 从 task 文件提取默认 scope。 |
| `3022` | `extract_task_acceptance_default` | 从 task 文件提取默认 acceptance。 |
| `3023` | `resolve_ready_field` | 解析 `ready` 字段值。 |
| `3024` | `update_state_current` | 回写 `TASKS/STATE.md` 当前状态。 |
| `3025` | `is_dirty` | 判断工作区是否脏。 |
| `3026` | `append_execution_event` | 追加执行事件。 |
| `3027` | `append_conversation_checkpoint` | 记录会话检查点。 |
| `3028` | `parse_args` | 解析 `ready` 命令行参数。 |
| `3029` | `main` | 执行 `ready` 主流程。 |

### 2.5 `tools/orient.py`

文件职责：基于 `ready` 结果生成候选方向。公共 helper 已抽出后，当前只剩方向草案相关逻辑。

| 编号 | 方法名 | 中文解释 |
| --- | --- | --- |
| `4001` | `parse_args` | 解析 `orient` 命令行参数。 |
| `4002` | `generate_orient_draft` | 生成方向草案。 |
| `4003` | `main` | 执行 `orient` 主流程。 |

### 2.6 `tools/choose.py`

文件职责：从方向草案里确认一个 option，形成当前轮次方向选择。

| 编号 | 方法名 | 中文解释 |
| --- | --- | --- |
| `5001` | `resolve_orient_file_for_run` | 定位当前 `run` 可用的 `orient` 文件。 |
| `5002` | `parse_args` | 解析 `choose` 命令行参数。 |
| `5003` | `main` | 执行 `choose` 主流程。 |

### 2.7 `tools/council.py`

文件职责：从多个角色视角评审当前方向。公共文件读写和 scope 标准化已抽出。

| 编号 | 方法名 | 中文解释 |
| --- | --- | --- |
| `6001` | `parse_args` | 解析 `council` 命令行参数。 |
| `6002` | `check_status` | 把布尔通过结果映射成门禁状态。 |
| `6003` | `role_decision` | 根据检查结果和关注点得出角色结论。 |
| `6004` | `main` | 执行 `council` 主流程。 |

### 2.8 `tools/arbiter.py`

文件职责：将多角色意见收敛成执行合同。公共 JSON、scope、去重 helper 已抽出。

| 编号 | 方法名 | 中文解释 |
| --- | --- | --- |
| `7001` | `parse_args` | 解析 `arbiter` 命令行参数。 |
| `7002` | `non_goals_from_scope` | 根据 scope 推导本轮非目标。 |
| `7003` | `main` | 执行 `arbiter` 主流程。 |

### 2.9 `tools/slice_task.py`

文件职责：把执行合同切成最小任务。公共 acceptance 去重 helper 已抽出。

| 编号 | 方法名 | 中文解释 |
| --- | --- | --- |
| `8001` | `parse_args` | 解析 `slice_task` 命令行参数。 |
| `8002` | `load_contract` | 加载 `execution_contract`。 |
| `8003` | `build_tasks_from_contract` | 从合同生成最小任务列表。 |
| `8004` | `main` | 执行 `slice_task` 主流程。 |

### 2.10 `tools/run_main.py`

文件职责：作为 Python 总入口，当前仍承担入口、日志和部分流程编排职责，后续还要继续收缩。

| 编号 | 方法名 | 中文解释 |
| --- | --- | --- |
| `9001` | `Logger.__init__` | 初始化日志器并打开日志文件。 |
| `9002` | `Logger.close` | 关闭日志文件句柄。 |
| `9003` | `Logger._emit` | 输出统一格式的单条日志。 |
| `9004` | `Logger.info` | 输出 `INFO` 日志。 |
| `9005` | `Logger.error` | 输出 `ERROR` 日志。 |
| `9006` | `state_field_value` | 从 `TASKS/STATE.md` 读取字段。 |
| `9007` | `resolve_run_id` | 解析总入口使用的 `run_id`。 |
| `9008` | `resolve_project_id` | 解析总入口使用的 `project_id`。 |
| `9009` | `parse_steps` | 解析要执行的步骤列表。 |
| `9010` | `build_step_specs` | 把逻辑步骤翻译成具体命令。 |
| `9011` | `stream_reader` | 逐行读取子进程输出并写日志。 |
| `9012` | `run_step` | 执行单个步骤。 |
| `9013` | `build_parser` | 构建命令行解析器。 |
| `9014` | `main` | 执行总入口主流程。 |

## 3. 流程调用链

本节只写阶段逻辑，不再把公共 helper 混进阶段编号。

### S0-common-01 公共 helper 先于阶段执行

- 阶段说明：所有与流程无关的文本、JSON、去重、hash、scope 处理都先进入 `tools/common_helpers.py`。
- 主调用方法：
  - `0001 read_json`
  - `0002 read_text`
  - `0003 write_json`
  - `0004 file_sha`
  - `0008 normalize_scope`
  - `0009 dedup_lines`
  - `0010 dedup_acceptance`
- 关键意义：
  - 阶段脚本先失去“公共工具箱”身份
  - 后续才能看清真正阶段逻辑

### S1-init-01 初始化入口

- 阶段说明：进入仓库后先读取固定项目常量配置和当前上下文。
- 主方法：
  - `1001 parse_args`
  - `1004 load_project_config`
  - `1009 main`
- 关键意义：
  - 先确认“这是哪个项目”
  - 再确认当前 `run/task`

### S1-init-02 初始化采集

- 阶段说明：检查项目材料、Codex/app-server 前提、git 前提，并最终汇总为自动化是否可继续。
- 主方法：
  - `1005 check_project_files`
  - `1006 check_codex_runtime`
  - `1007 check_git_runtime`
  - `1008 finalize_init`
- 支撑能力：
  - `1002 run_cmd`
  - `1003 run_shell`
  - `0014 first_line`

### S2-learn-01 学习入口

- 阶段说明：启动 `learn`，解析参数并确认项目上下文。
- 主方法：
  - `2011 parse_cli`
  - `2025 main`
- 关键辅助方法：
  - `2004 read_state_snapshot`
  - `2005 resolve_project_id_for_cmd`
  - `2007 emit_step`

### S2-learn-02 课程解析与基础产物

- 阶段说明：解析 `PROJECT_GUIDE`，生成基础 `learn` 产物。
- 主方法：
  - `2010 parse_project_guide`
  - `2013 build_base_learn`
  - `2014 print_base_anchors`
- 公共 helper：
  - `0003 write_json`
  - `0005 ordered_unique`
  - `0006 normalize_block`
  - `0007 normalize_list`
  - `0004 file_sha`

### S2-learn-03 模型提示词与结果回写

- 阶段说明：生成提示词、解析模型输出并回写结果。
- 主方法：
  - `2015 generate_prompt`
  - `2019 parse_model_output`
  - `2021 update_learn_with_model`
  - `2020 print_model_anchors`

### S3-ready-01 开工门禁

- 阶段说明：校验 `learn/run/task` 是否满足开工条件。
- 主方法：
  - `3028 parse_args`
  - `3029 main`
- 关键辅助方法：
  - `3012 resolve_run_id_for_cmd`
  - `3013 resolve_project_id_for_cmd`
  - `3004 emit_step`

### S3-ready-02 门禁校验

- 阶段说明：确认 `learn` 文件、sync 文件、历史决策和 task 合同是否可用。
- 主方法：
  - `3014 learn_file_is_valid`
  - `3015 learn_file_matches_project`
  - `3016 resolve_learn_file_for_project`
  - `3017 sync_file_is_valid`
  - `3018 resolve_sync_file_for_run`
  - `3019 resolve_ready_prior_decision_for_run`
  - `3020 extract_task_goal_default`
  - `3021 extract_task_scope_default`
  - `3022 extract_task_acceptance_default`
  - `3023 resolve_ready_field`
- 公共 helper：
  - `0001 read_json`
  - `0002 read_text`
  - `0004 file_sha`
  - `0013 parse_bool_flag`

### S4-orient-01 方向草案生成

- 阶段说明：基于 `ready` 结果生成候选方向。
- 主方法：
  - `4001 parse_args`
  - `4002 generate_orient_draft`
  - `4003 main`
- 公共 helper：
  - `0001 read_json`
  - `0002 read_text`
  - `0011 split_scope`
  - `0012 short_text`

### S5-choose-01 方向确认

- 阶段说明：从方向草案中选择本轮方向。
- 主方法：
  - `5002 parse_args`
  - `5003 main`
- 关键辅助方法：
  - `5001 resolve_orient_file_for_run`

### S6-council-01 多角色评审

- 阶段说明：从多角色视角审查当前方向。
- 主方法：
  - `6001 parse_args`
  - `6002 check_status`
  - `6003 role_decision`
  - `6004 main`
- 公共 helper：
  - `0001 read_json`
  - `0002 read_text`
  - `0008 normalize_scope`

### S7-arbiter-01 合同收敛

- 阶段说明：将 `council` 意见收敛成执行合同。
- 主方法：
  - `7001 parse_args`
  - `7002 non_goals_from_scope`
  - `7003 main`
- 公共 helper：
  - `0001 read_json`
  - `0008 normalize_scope`
  - `0009 dedup_lines`

### S8-slice-task-01 任务切片

- 阶段说明：把执行合同切成最小任务。
- 主方法：
  - `8001 parse_args`
  - `8002 load_contract`
  - `8003 build_tasks_from_contract`
  - `8004 main`
- 公共 helper：
  - `0010 dedup_acceptance`

### S9-run-main-01 总入口编排

- 阶段说明：`run_main.py` 仍负责单入口编排与统一日志。
- 主方法：
  - `9013 build_parser`
  - `9014 main`
  - `9010 build_step_specs`
  - `9012 run_step`
- 关键辅助方法：
  - `9006 state_field_value`
  - `9007 resolve_run_id`
  - `9008 resolve_project_id`
  - `9009 parse_steps`
  - `9011 stream_reader`

## 4. 当前观察

这次整理后的直接结论只有两条：

1. 第一批与业务流程无关的公共 helper 已经有独立归宿，不再应该留在阶段脚本里。
2. `ready.py` 和 `run_main.py` 仍然夹带大量非阶段职责，下一刀应该继续抽 `artifact/state` 和 `logging`。
