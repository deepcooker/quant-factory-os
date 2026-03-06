# ENTITIES

对象模型先于流程模型。

本文件定义 `project_id / run_id / task_id / discussion artifacts / queue / evidence` 的边界、关系和生命周期。
`docs/WORKFLOW.md` 必须以这里的定义为基础，不得另起一套名词系统。

## 1. 设计原则

### 1.1 分层原则
- `project` 管长期上下文。
- `run` 管一轮方向到交付的周期。
- `task` 管 run 内最小可执行切片。
- `discussion artifacts` 管需求从模糊到收敛的中间产物。
- `queue` 只是执行入口池，不是顶层对象。

### 1.2 因果顺序
- 先有 `project`
- 再有 `run`
- run 内先讨论
- 讨论收敛后才切 `task`
- task 执行完成后更新 run evidence

禁止倒因果：
- 不允许先批量建 task 再反推需求。
- 不允许把 queue 当项目主线。
- 不允许把 session 等同于 run。

### 1.3 单一真相源
- 当前活动指针真相源：`TASKS/STATE.md`
- 当前 task 合同真相源：`TASKS/TASK-*.md`
- 当前 run 证据真相源：`reports/<RUN_ID>/`
- 项目长期认知真相源：`docs/PROJECT_GUIDE.md`
- 硬规则真相源：`AGENTS.md`
- 流程状态机真相源：`docs/WORKFLOW.md`

## 2. Project

### 2.1 定义
`project_id` 是项目长期命名空间，承载该项目的知识、规则、历史和默认同频作用域。

### 2.2 职责
- 标识这是哪个项目
- 承载长期 owner docs
- 作为 `learn` 的默认学习作用域
- 容纳多个 `run`

### 2.3 真相源
- `TASKS/STATE.md -> CURRENT_PROJECT_ID`
- 缺省值：`project-0`

### 2.4 生命周期
- 创建时机：项目建立时
- 关闭时机：通常不关闭，除非项目废弃

### 2.5 关系
- 一个 `project` 可以有多个 `run`
- 一个 `run` 只属于一个 `project`

## 3. Run

### 3.1 定义
`run_id` 是一轮方向讨论到交付的周期容器。

它不是：
- session
- 单个 task
- 单条命令
- 单个方向标题

它是：
- 当前这轮工作的证据命名空间
- 讨论、收敛、执行、复盘的聚合容器

### 3.2 职责
- 承载本轮讨论产物
- 承载本轮执行合同
- 承载本轮 task 的上下文
- 承载本轮 summary / decision / review / ship 证据

### 3.3 真相源
- `TASKS/STATE.md -> CURRENT_RUN_ID`
- run 证据目录：`reports/<RUN_ID>/`

### 3.4 生命周期
1. 新需求方向或新一轮迭代开始时创建
2. 在该 run 内完成 discussion -> contract -> slice -> task execution
3. 所有相关 task 完成，或明确终止时关闭

### 3.5 关系
- 一个 `run` 只属于一个 `project`
- 一个 `run` 可以包含多个 `task`
- 一个 `run` 可以包含多份 discussion artifacts

## 4. Task

### 4.1 定义
`task_id` 是 run 内最小可执行、可验证、可交付的切片。

### 4.2 职责
- 表达一次明确的小变更
- 固定 scope / acceptance / evidence
- 成为一次实现与 review 的最小单位

### 4.3 真相源
- `TASKS/TASK-*.md`

### 4.4 必要字段
- `RUN_ID`
- `Goal`
- `Scope`
- `Acceptance`

### 4.5 生命周期
1. discussion 收敛成 execution contract 后创建
2. 从 `slice_plan` 或 queue 中实体化
3. 执行、验证、review、ship
4. 完成后更新 run evidence 和 state

### 4.6 关系
- 一个 `task` 只属于一个 `run`
- 一个 `run` 可拆成多个 `task`
- 一个 task 对应一次最小交付

## 5. Discussion Artifacts

discussion artifacts 是 run 内从模糊需求到执行合同的中间对象，不是 task。

### 5.1 Direction
定义：候选方向集合。

职责：
- 给出多个可选方向
- 说明 each option 的 why / risk / priority / scope_hint

典型文件：
- `chatlogs/discussion/<RUN_ID>/orient.json`
- `chatlogs/discussion/<RUN_ID>/orient.md`

### 5.2 Selection
定义：用户确认后的方向选择结果。

职责：
- 记录选了哪个方向
- 说明选择理由
- 固定后续 discussion 的目标方向

典型文件：
- `reports/<RUN_ID>/orient_choice.json`

### 5.3 Council Review
定义：多角色独立评审结果。

职责：
- 从产品 / 架构 / 研发 / 测试等视角独立产出意见
- 暴露 blocker / warn / disagreement

典型文件：
- `chatlogs/discussion/<RUN_ID>/council.json`
- `chatlogs/discussion/<RUN_ID>/council.md`

### 5.4 Execution Contract
定义：讨论收敛后的可执行合同。

职责：
- 固定目标
- 固定非目标
- 固定 scope
- 固定 acceptance
- 固定约束和风险

典型文件：
- `reports/<RUN_ID>/execution_contract.json`
- `reports/<RUN_ID>/execution_contract.md`

### 5.5 Slice Plan
定义：把 execution contract 拆成最小执行切片的结果。

职责：
- 给出 task 拆分
- 给出先后顺序
- 给出每个 task 的 acceptance

典型文件：
- `reports/<RUN_ID>/slice_state.json`
- `TASKS/QUEUE.md` 中由 slice 写入的 block

## 6. Queue

### 6.1 定义
`queue` 是待执行 task 的入口池，不是项目主线，也不是讨论真相源。

### 6.2 职责
- 承接 slice 后产生的待办切片
- 作为 `tools/task.sh --next` 的选择入口

### 6.3 真相源
- `TASKS/QUEUE.md`

### 6.4 关系
- queue item 来自某个 `run` 的 `slice_plan`
- queue item 最终会实体化为 `TASKS/TASK-*.md`

### 6.5 设计原则
- queue 在 discussion 之后
- queue 不定义需求，只承接已收敛合同
- queue 不是 project/run 的替代物

## 7. Evidence

### 7.1 定义
evidence 是仓库内记忆，不依赖聊天上下文。

### 7.2 Run 级 evidence
位置：
- `reports/<RUN_ID>/`

最低要求：
- `meta.json`
- `summary.md`
- `decision.md`

### 7.3 Learn 级 evidence
位置：
- `learn/<project_id>.json`
- `learn/<project_id>.md`
- `learn/<project_id>.stdout.log`
- `learn/<project_id>.model.*`

### 7.4 职责
- 记录本轮做了什么
- 记录为什么这么做
- 记录验证和风险
- 记录模型同频结果

## 8. Session

### 8.1 定义
session 是一次聊天/终端交互会话。

### 8.2 原则
- session 不是 run
- session 可以服务 run
- run 不能依赖 session 记忆存在

### 8.3 正确关系
- session 通过 `learn` 和 run evidence 对齐到当前 `project/run/task`
- session 结束后，真相仍应留在仓库文件里

## 9. Ready Contract

### 9.1 定义
`ready.json` 是当前 run/task 的开工许可，不是项目学习产物，也不是方向合同。

### 9.2 职责
- 检查 `learn` 是否通过
- 确认当前 `project/run/task` 指针
- 固定当前工作最小合同：
  - `goal`
  - `scope`
  - `acceptance`
  - `stop_condition`

### 9.3 典型文件
- `reports/<RUN_ID>/ready.json`

## 10. PR

### 10.1 定义
PR 是 task 的交付与审查单元。

### 10.2 原则
- one task -> one branch -> one PR

### 10.3 必备内容
- Why
- What
- Verify
- Evidence paths
- RUN_ID

## 11. 对象关系总图

```text
project
  -> run
    -> direction
    -> selection
    -> council review
    -> execution contract
    -> slice plan
    -> queue items
    -> task-1
    -> task-2
    -> task-3
    -> run evidence
```

## 12. 生命周期顺序

```text
project
  -> init
  -> learn
  -> ready
  -> orient
  -> choose
  -> council
  -> arbiter
  -> slice
  -> queue/task
  -> do
  -> review
  -> ship
  -> run close
```

## 13. 反模式

以下都是错误设计：

- 把 `run_id` 当成 `task_id`
- 把 `session` 当成 `run`
- 先批量建 task 再讨论需求
- 把 queue 当顶层对象
- 让 `ready` 负责学习
- 让 `learn` 负责执行许可
- 让 discussion artifacts 直接替代 task contract

## 14. 本仓当前推荐结论

- `project_id`：长期上下文
- `run_id`：一轮工作周期容器
- `task_id`：run 内最小执行切片
- `direction/selection/council/execution_contract/slice_plan`：讨论层对象
- `queue`：slice 后的待执行入口池
- `evidence`：仓库内长期记忆

后续如果 `docs/WORKFLOW.md` 与这里冲突，以本文件为准，并同步修正 workflow。
