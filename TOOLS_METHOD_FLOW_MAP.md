# TOOLS_METHOD_FLOW_MAP

这份文档只按业务流程写。

阅读顺序固定为：
1. 先看每个阶段的业务目标
2. 再看每个阶段的主流程方法
3. 最后才看该阶段的 `xxx_tools_xx`

不允许再反过来把支撑方法当成业务主流程。

---

## 1. 总规则

- 每个阶段顶层只保留少量业务主流程方法
- `main()` 只负责按顺序分发这些主流程方法
- 非业务方法统一降为 `xxx_tools_xx`
- 如果某个支撑方法不是该阶段独享，后面应该继续抽出去

---

## 2. `init`

### 业务目标

- 确认当前自动化面对的是哪个项目
- 确认项目、Codex、git 的前置条件是否满足
- 给出 `INIT_STATUS / INIT_REASON_CODES / INIT_NEXT`

### 主流程方法

| 编号 | 方法名 | 中文说明 |
| --- | --- | --- |
| `1001` | `init_step_01_load_context` | 读取固定项目配置和当前上下文。 |
| `1002` | `init_step_02_check_project_files` | 检查项目路径和关键 owner docs。 |
| `1003` | `init_step_03_check_codex_runtime` | 检查 Codex CLI、`app-server`、session 前提。 |
| `1004` | `init_step_04_check_git_runtime` | 检查 git 仓库、远端、认证和工作区状态。 |
| `1005` | `init_step_05_finalize` | 汇总结果并给出下一步。 |

### 支撑方法命名

- `init_tools_01` ~ `init_tools_10`

---

## 3. `learn`

### 业务目标

- 完成项目同频
- 生成基础 `learn` 产物
- 完成模型侧强同频
- 输出可进入 `ready` 的学习结果

### 主流程方法

| 编号 | 方法名 | 中文说明 |
| --- | --- | --- |
| `2001` | `learn_step_01_resolve_context` | 锁定 `learn` 运行配置、项目上下文和日志镜像模式。 |
| `2002` | `learn_step_02_prepare_artifacts` | 准备 `learn` 产物路径并清理旧的模型临时文件。 |
| `2003` | `learn_step_03_build_base_packet` | 生成基础 `learn` 报告和主线锚点。 |
| `2004` | `learn_step_04_run_model_sync` | 执行模型同频、解析结果、回写并校验 `learn` 产物。 |
| `2005` | `learn_step_05_finalize` | 打印 `learn` 产物位置并给出下一步。 |

### 支撑方法命名

- `learn_tools_01` ~ `learn_tools_24`

---

## 4. `ready`

### 业务目标

- 校验 `learn` / `sync` 门禁
- 解决未收口 run 的继续决策
- 生成最小 ready 合同
- 写出 `ready.json` 并进入 `orient`

### 主流程方法

| 编号 | 方法名 | 中文说明 |
| --- | --- | --- |
| `3001` | `ready_step_01_resolve_context` | 锁定 `ready` 运行上下文和各类门禁配置。 |
| `3002` | `ready_step_02_enforce_inputs` | 校验 `learn` / `sync` 输入门禁是否满足。 |
| `3003` | `ready_step_03_resolve_decision` | 处理未收口 run 的继续决策并生成默认合同草稿。 |
| `3004` | `ready_step_04_write_ready_contract` | 采集最小 ready 合同并写入 `ready.json`。 |
| `3005` | `ready_step_05_finalize` | 回写状态、记录证据并打印 ready 结果。 |

### 支撑方法命名

- `ready_tools_01` ~ `ready_tools_28`

---

## 5. `orient`

### 业务目标

- 基于当前 run 的 ready 合同和证据
- 生成候选方向
- 给出推荐方向和下一步 choose 命令

### 主流程方法

| 编号 | 方法名 | 中文说明 |
| --- | --- | --- |
| `4001` | `orient_step_01_resolve_context` | 锁定 `orient` 上下文并确定输出路径。 |
| `4002` | `orient_step_02_generate_draft` | 生成方向草案和 orient 产物。 |
| `4003` | `orient_step_03_finalize` | 记录 orient 证据并打印结果。 |

### 支撑方法命名

- `orient_tools_01` ~ `orient_tools_02`

---

## 6. `choose`

### 业务目标

- 从 `orient` 给出的候选方向中确认一个方向
- 生成 `orient_choice.json`
- 生成方向合同，交给 `council`

### 主流程方法

| 编号 | 方法名 | 中文说明 |
| --- | --- | --- |
| `5001` | `choose_step_01_resolve_context` | 锁定 `choose` 上下文并检查输入文件。 |
| `5002` | `choose_step_02_build_contract` | 确认方向并生成 choose/contract 产物。 |
| `5003` | `choose_step_03_finalize` | 记录 choose 证据并打印结果。 |

### 支撑方法命名

- `choose_tools_01` ~ `choose_tools_02`

---

## 7. `council`

### 业务目标

- 对当前方向做多角色独立评审
- 输出证据检查、角色意见和分歧
- 给 `arbiter` 提供收敛输入

### 主流程方法

| 编号 | 方法名 | 中文说明 |
| --- | --- | --- |
| `6001` | `council_step_01_resolve_context` | 锁定 `council` 上下文并检查前置产物。 |
| `6002` | `council_step_02_generate_reviews` | 生成多角色独立评审结果。 |
| `6003` | `council_step_03_finalize` | 记录 council 证据并打印结果。 |

### 支撑方法命名

- `council_tools_01` ~ `council_tools_03`

---

## 8. `arbiter`

### 业务目标

- 把 council 的独立评审收敛成执行合同
- 明确 blockers、warnings、role conditions
- 产出 `execution_contract`

### 主流程方法

| 编号 | 方法名 | 中文说明 |
| --- | --- | --- |
| `7001` | `arbiter_step_01_resolve_context` | 锁定 `arbiter` 上下文并检查前置产物。 |
| `7002` | `arbiter_step_02_build_contract` | 收敛 council 评审并生成 execution contract。 |
| `7003` | `arbiter_step_03_finalize` | 记录 arbiter 证据并打印结果。 |

### 支撑方法命名

- `arbiter_tools_01` ~ `arbiter_tools_02`

---

## 9. `slice_task`

### 业务目标

- 把 execution contract 切成最小任务
- 写入 `TASKS/QUEUE.md`
- 生成 `slice_state.json`

### 主流程方法

| 编号 | 方法名 | 中文说明 |
| --- | --- | --- |
| `8001` | `slice_step_01_resolve_context` | 锁定 `slice` 上下文并检查 execution contract。 |
| `8002` | `slice_step_02_build_queue` | 把 execution contract 切成 queue 任务并写入 `slice_state`。 |
| `8003` | `slice_step_03_finalize` | 记录 slice 证据并打印结果。 |

### 支撑方法命名

- `slice_tools_01` ~ `slice_tools_03`

---

## 10. 当前纠错方式

后面纠错时，顺序固定：

1. 先指出某个阶段的业务目标错没错
2. 再指出该阶段主流程步骤顺序错没错
3. 最后才指出该阶段的 `xxx_tools_xx` 是否还混进了不该留的职责

也就是说，优先纠错对象永远是：
- `1001-1005`
- `2001-2005`
- `3001-3005`
- `4001-4003`
- `5001-5003`
- `6001-6003`
- `7001-7003`
- `8001-8003`

不是先纠结底层工具方法。
