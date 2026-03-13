# ENTITIES

对象模型先于流程模型。

本文件定义 `project_id / run_id / task_id / thread summary / discussion artifacts / queue / evidence` 的边界、关系和生命周期。
`docs/WORKFLOW.md` 必须以这里的定义为基础，不得另起一套名词系统。

## 1. 设计原则

### 1.1 分层原则
- `project` 管长期上下文。
- `baseline` 管项目长期学习基线。
- `run` 管一轮方向到交付的周期。
- `task` 管 run 内最小可执行切片。
- `thread` 管 task 内单个角色或单次连续会话的局部结论。
- `discussion artifacts` 管需求从模糊到收敛的中间产物。
- `queue` 只是执行入口池，不是顶层对象。

### 1.2 因果顺序
- 先有 `project`
- 再有 `baseline`
- 再有 `run`
- run 内先讨论
- 讨论收敛后才切 `task`
- task 内再产生一个或多个 `thread`
- thread 先总结，task 再聚合
- task 执行完成后更新 run evidence

禁止倒因果：
- 不允许先批量建 task 再反推需求。
- 不允许把 queue 当项目主线。
- 不允许把 session 等同于 run。
- 不允许把单个 thread summary 直接当成最终 run summary。

### 1.3 单一真相源
- 当前活动指针真相源：`tools/project_config.json -> runtime_state`
- 当前 task 合同真相源：`TASKS/TASK-*.json`
- 当前 run 证据真相源：`reports/<RUN_ID>/`
- 项目长期认知真相源：`docs/PROJECT_GUIDE.md`
- 硬规则真相源：`AGENTS.md`
- 流程状态机真相源：`docs/WORKFLOW.md`

### 1.4 运行时边界
- `tools` 是本仓自动化研发体系的执行层。
- Codex CLI 是研发期的人机调试/接管界面，不是长期产品入口。
- Codex app-server 是程序化运行时接口；长期应由 Python orchestrator 通过它驱动智能交互。

## 2. Project

### 2.1 定义
`project_id` 是项目长期命名空间，承载该项目的知识、规则、历史和默认同频作用域。

### 2.2 职责
- 标识这是哪个项目
- 承载长期 owner docs
- 作为 `learn` 的默认学习作用域
- 容纳多个 `run`

### 2.3 真相源
- `tools/project_config.json -> project_id`
- 当前状态指针：`tools/project_config.json -> runtime_state.current_project_id`
- 缺省值：`quant-factory-os`

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
- 承载本轮 task 的上下文与聚合结果
- 承载本轮 summary / decision / review / ship 证据
- 在多 task 场景下，成为 task summaries 的聚合层

### 3.3 真相源
- `tools/project_config.json -> runtime_state.current_run_id`
- run 证据目录：`reports/<RUN_ID>/`

当前最小实现：
- 机器真相源：`reports/<RUN_ID>/run_summary.json`
- 人类视图：`reports/<RUN_ID>/summary.md` 和 `reports/<RUN_ID>/decision.md`
- 当前最小写回入口：`python3 tools/evidence.py --set-run-summary --run-id <RUN_ID> ...`

当前最小字段建议：
- `status`
- `run_goal`
- `scope`
- `non_goals`
- `impacted_modules`
- `non_functional_constraints`
- `acceptance`
- `active_tasks`
- `completed_tasks`
- `source_tasks`
- `key_updates`
- `cross_task_decisions`
- `cross_task_risks`
- `verification_overview`
- `next_run_or_next_tasks`

当前 machine merge 规则：
- `active_tasks` / `completed_tasks`: `reconcile_only`
- `source_tasks` / `verification_overview`: `append_dedup`
- `key_updates` / `cross_task_decisions` / `cross_task_risks` / `next_run_or_next_tasks`: `merge_rewrite`

说明：
- `reconcile_only` 表示该字段应由 task 真相源重算，不从单个 task summary 直接追加
- `append_dedup` 表示保留 task 级证据粒度，允许带 task 前缀追加后去重
- `merge_rewrite` 表示 task-level 文本在进入 run summary 前应先做最小 run-level 归并；当前实现只做规则化轻改写，不做模型推理
- 当前 `merge_rewrite` 允许少量明确的高频模式归并，例如：
  - 多个角色的 `summary merged` 合并成一条 multi-role run-level 结论
  - `test gate=blocked/passed` 归并成更稳定的 gate 状态表达
- 对 `cross_task_risks`，若同时存在通用 blocked-gate 句与更具体的 blocked-gate 解释句，则优先保留更具体的 run-level 风险表达；证据粒度仍保留在 `verification_overview`

### 3.4 生命周期
1. 新需求方向或新一轮迭代开始时创建
2. 在该 run 内完成 discussion -> contract -> slice -> task execution
3. 所有相关 task 完成，或明确终止时关闭

### 3.5 关系
- 一个 `run` 只属于一个 `project`
- 一个 `run` 可以包含多个 `task`
- 一个 `run` 可以包含多份 discussion artifacts
- 一个 `run` 的最终稳定结论应来自 task summaries 的聚合，而不是单个 thread
- 一个 `run` 在 task 创建前，允许先存在一版 `Markdown intake draft`

补充说明：
- `Markdown intake draft` 用于把客户杂乱材料先整理成 run 级讨论输入
- 它属于协议层草稿，不等于 `run summary`
- 它不是机器真相源，不直接替代 `tools/project_config.json`、`TASKS/*.json` 或 `reports/<RUN_ID>/run_summary.json`

## 4. Task

### 4.1 定义
`task_id` 是 run 内最小可执行、可验证、可交付的切片。

### 4.2 职责
- 表达一次明确的小变更
- 固定 scope / acceptance / evidence
- 成为一次实现与 review 的最小单位
- 聚合该 task 下多个角色 thread 的有效结论

### 4.3 Task Summary
`task summary` 是 task 层的稳定聚合结果，位于多个 thread summaries 之上、run summary 之下。

当前最小字段建议：
- `status`
- `key_updates`
- `decisions`
- `risks`
- `verification`
- `next_steps`
- `source_threads`

### 4.4 真相源
- `TASKS/TASK-*.json`
- 当前绑定指针（可为空）：`tools/project_config.json -> runtime_state.current_task_id/current_task_json_file/current_task_file`

说明：
- 当前最小实现把 `task_summary` 直接放在 `TASKS/TASK-*.json` 内，不额外拆独立文件

### 4.5 必要字段
- `RUN_ID`
- `Goal`
- `Scope`
- `Acceptance`

建议补充的需求边界字段：
- `NonGoal`
- `ImpactedModules`
- `Dependencies`
- `Risks`
- `AbnormalFlows`
- `NonFunctionalConstraints`
- `role_threads`
- `test_gate`

### 4.6 生命周期
1. discussion 收敛成 execution contract 后创建
2. 从 `slice_plan` 或 queue 中实体化
3. 执行、验证、review、ship
4. 完成后更新 run evidence 和 state

### 4.7 关系
- 一个 `task` 只属于一个 `run`
- 一个 `run` 可拆成多个 `task`
- 一个 task 对应一次最小交付
- 一个 `task` 可以包含多个 `thread`
- 一个 `task summary` 聚合该 task 下多个 `thread summaries`

### 4.8 Role Threads
`role_threads` 是 task 内最小角色协作真相源，当前最小建议固定为：
- `run-main`
- `dev`
- `test`
- `arch`（按需）

最小字段建议：
- `thread_id`
- `thread_path`
- `status`

说明：
- `run-main` 负责收敛与确认
- `dev` 负责实现与自证
- `test` 负责独立验证
- `arch` 仅在复杂任务时启用
- 当前 runtime 最小入口是 `appserverclient --fork-role <role>`，它负责把真实 role thread 绑定回当前 task
- 已绑定 role thread 的执行入口是 `appserverclient --role-turn <role> [text...]`
- 已绑定 role thread 的去噪入口是 `appserverclient --summarize-role <role>`
- 当前 `run-main` 也属于正式 role，可通过真实 role thread 路径参与 task 升级处理
- task 机器层现在同时承载 `role_threads`、`role_summaries` 和 `task_summary.role_summary_evidence`
- `taskclient --merge-role-summaries` 是当前 task-level 最小聚合入口：它不做复杂推理，只按去重规则把已有 role summaries 的来源和引用证据并入 `task_summary`
- `taskclient.refresh_task_coordination()` 是当前 task-level 的统一刷新入口：它负责按需 merge role summaries，并继续刷新 `gap_summary / escalation_summary / run_main_resolution`
- `appserverclient --summarize-role <role>` 现在会在写回单个 `role_summaries.<role>` 后调用该统一刷新入口
- `taskclient.update_role_summary_with_task_links()` 现在统一承接 `role_summaries.<role>` 与 `task_summary.role_summary_evidence/source_threads` 的联动写回，避免 runtime 直接改 task aggregate 字段
- `task_summary.conflict_policy` 是当前 task 层的最小优先级约定，当前默认顺序是：`run-main -> test -> arch -> dev`
- `task_summary.gap_summary` 是当前 task 层的最小缺口汇总，当前至少记录：
  - `missing_roles`
  - `open_gaps`
- `taskclient --refresh-task-gaps` 会基于现有 `role_summaries` 和 `test_gate` 刷新这两块
- `task_summary.escalation_policy` 是当前 task 层“哪些情况必须升级给 run-main”的最小规则
- `task_summary.escalation_summary` 是当前 task 层“这次是否需要升级”的最小结果
- `taskclient --refresh-task-escalation` 会基于现有 `gap_summary` 与 `test_gate` 刷新这两块
- `task_summary.run_main_resolution_policy` 是当前 task 层“升级给 run-main 后，什么条件下必须确认、什么条件下可以关闭升级项”的最小规则
- `task_summary.run_main_resolution` 是当前 task 层“run-main 已否确认、是否可以关闭升级项”的最小结果
- `taskclient --refresh-run-main-resolution` 会基于现有 `escalation_summary`、`role_summaries.run-main` 与 `test_gate` 刷新这两块
- `appserverclient --mark-test-gate <status>` 是当前最小 test runtime 写回入口：其 test thread/turn 证据拼接现由 `taskclient.update_test_gate_from_test_summary()` 统一承接，并继续调用统一刷新入口

### 4.9 Test Gate
`test_gate` 是 task 内独立验证门，不等于开发自测结果。

当前最小字段建议：
- `status`
- `owner_role`
- `required_axes`
- `evidence`
- `blocking_issues`
- `updated_at`

说明：
- task 不应只因 `dev` 完成实现就直接视为完成
- `test_gate` 应作为 task summary 与 run summary 之间的重要质量门

### 4.10 Tool Boundaries
当前正式主工具边界固定为：
- `appserverclient`: runtime / session / role thread
- `taskclient`: task machine truth / task gates / task escalation
- `evidence.py`: run evidence / run summary / run-level normalization
- `gitclient`: git delivery / rollback / commit message fallback

当前推荐边界：
- `appserverclient` 只负责真实 thread 生命周期与必要写回，不继续承载更多 task/run 聚合规则
- `taskclient` 只负责 `TASKS/TASK-*.json` 的结构化真相源，不接管 runtime transport
- `evidence.py` 只负责 `reports/<RUN_ID>/` 下的 run-level truth 与压缩视图，不接管 task 机器层
- `gitclient` 保持独立，不回灌 runtime / task / run 规则

当前已观察到的变厚点：
- `appserverclient` 已开始了解 `test_gate / gap_summary / escalation_summary / run_main_resolution`
- `evidence.py` 已同时承担 run summary 写回、聚合、压缩和历史清理

下一轮解耦方向：
- 把更多 task 规则继续留在 `taskclient`
- 让 `appserverclient` 只调用 task/run 层的显式入口，而不是继续内嵌规则
- 保持 `gitclient` 不被重新耦合回 runtime 主线

## 5. Thread Summary

### 5.1 定义
`thread summary` 是 task 内单个角色或一次连续工作会话的最小总结单元，通常对应某个 fork session 的局部结论。

### 5.2 职责
- 承接某个角色 thread 的局部进展、风险和下一步
- 作为 task summary 的输入，而不是直接替代 task 或 run summary

推荐角色：
- `run-main`: run 主线程，负责需求收敛、task 拆分和最终确认
- `dev`: 实现、debug、单元/最小集成自证
- `test`: 独立验证、功能/流程/数据/非功能检查
- `arch`: 复杂任务下的结构边界与约束评估

### 5.3 真相源
- 当前过渡实现：`tools/project_config.json -> session_registry.current_summary`
- 长期应扩展到 task 内多个 role/session summaries

### 5.4 关系
- 一个 `thread summary` 只属于一个 `task`
- 一个 `task` 可以聚合多个 `thread summaries`
- `baseline` 不应长期直接消费原始 thread summary

## 6. Discussion Artifacts

discussion artifacts 是 run 内从模糊需求到执行合同的中间对象，不是 task。

### 5.1 Direction
定义：候选方向集合。

职责：
- 给出多个可选方向
- 说明 each option 的 why / risk / priority / scope_hint

典型文件：
- `reports/<RUN_ID>/orient_choice.json`

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
- `reports/<RUN_ID>/execution_contract.json`

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
- `TASKS/QUEUE.json` 中的 queue items

## 7. Queue

### 6.1 定义
`queue` 是待执行 task 的入口池，不是项目主线，也不是讨论真相源。

### 6.2 职责
- 承接 slice 后产生的待办切片
- 作为后续 Python-first task picker 的选择入口

### 6.3 真相源
- `TASKS/QUEUE.json`

### 6.4 关系
- queue item 来自某个 `run` 的 `slice_plan`
- queue item 最终会实体化为 `TASKS/TASK-*.json`

### 6.5 设计原则
- queue 在 discussion 之后
- queue 不定义需求，只承接已收敛合同
- queue 不是 project/run 的替代物

## 8. Evidence

### 7.1 定义
evidence 是仓库内记忆，不依赖聊天上下文。

### 8.2 Run 级 evidence
位置：
- `reports/<RUN_ID>/`

最低要求：
- `meta.json`
- `summary.md`
- `decision.md`

说明：
- 当前阶段 `summary.md` 和 `decision.md` 仍以 active task evidence 为主，路径属于 run 容器，但内容粒度通常更接近 task-focused run evidence
- `run_summary.json` 是当前新增的 run-level machine truth，后续应逐步承接 task summaries 的聚合结果
- 多 task 成熟后，run evidence 应进一步承担 task summaries 的聚合表达

### 8.3 Learn 级 evidence
位置：
- `learn/<project_id>.json`
- `learn/<project_id>.md`
- `learn/<project_id>.stdout.log`
- `learn/<project_id>.model.*`

### 8.4 职责
- 记录本轮做了什么
- 记录为什么这么做
- 记录验证和风险
- 记录模型同频结果

## 9. Session

### 8.1 定义
session 是一次聊天/终端交互会话。

### 8.2 原则
- session 不是 run
- session 可以服务 run
- run 不能依赖 session 记忆存在

### 8.3 正确关系
- session 通过 `learn` 和 run evidence 对齐到当前 `project/run/task`
- session 结束后，真相仍应留在仓库文件里

## 10. Ready Contract

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

## 11. PR

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

## 12. 对象关系总图

```text
project
  -> baseline
  -> run
    -> direction
    -> selection
    -> council review
    -> execution contract
    -> slice plan
    -> queue items
    -> task-1
      -> thread-summary-a
      -> thread-summary-b
    -> task-2
    -> task-3
    -> run evidence
  -> baseline refresh input
```

## 13. 生命周期顺序

```text
project
  -> init
  -> baseline learn
  -> run
  -> discussion
  -> task
  -> thread summary
  -> task summary
  -> run evidence
  -> baseline refresh
  -> run close
```

## 14. 反模式

以下都是错误设计：

- 把 `run_id` 当成 `task_id`
- 把 `session` 当成 `run`
- 把单个 `thread summary` 直接当成 `run summary`
- 先批量建 task 再讨论需求
- 把 queue 当顶层对象
- 让 `ready` 负责学习
- 让 `learn` 负责执行许可
- 让 discussion artifacts 直接替代 task contract

## 15. 本仓当前推荐结论

- `project_id`：长期上下文
- `baseline`：项目长期学习基线
- `run_id`：一轮工作周期容器
- `task_id`：run 内最小执行切片
- `thread summary`：task 内角色/会话级局部结论，当前过渡实现为 `session_registry.current_summary`
- `direction/selection/council/execution_contract/slice_plan`：讨论层对象
- `queue`：slice 后的待执行入口池
- `evidence`：仓库内长期记忆

当前实现说明：
- `reports/<RUN_ID>/summary.md` 和 `decision.md` 目前仍以 active task evidence 为主，属于 run 容器下的过渡态表达
- `session_registry.current_summary` 当前是 thread-level transitional summary，不应长期等同于最终 run summary
- `reports/<RUN_ID>/run_summary.json` 当前是最小 machine truth 落点；`summary.md/decision.md` 继续承担 run 级 md 视图
- `run_summary.json.baseline_ready_summary` 是给 baseline refresh 使用的压缩视图，不是新的独立对象；它只是 run-level machine truth 的一段更短表达
- `run_summary.json.merge_policy` 是 task -> run 聚合规则的机器层声明；长期可以演进，但当前必须显式保留字段类别，不允许把所有 summary 字段继续当成统一 append 列表
- `run_summary.json.legacy_cleanup_policy` 是 run-level 历史语义项的渐进清理声明；当前策略必须是 `explicit_maintenance_only`，不允许在普通 merge/reconcile 时静默重写全部旧条目
- `run_summary.json.legacy_cleanup_last_applied_at` 只记录最近一次显式清理动作；它不是 run-level 业务状态
- `run_summary.json.active_tasks/completed_tasks/source_tasks` 当前应优先通过 task JSON 真相源重算；如果 task 真相源本身保留历史 `active` 项，run summary 也应如实暴露，而不是在 run 层静默抹平
- baseline 当前已优先消费 `run_summary`，仅在缺失时回退 `current_summary`；长期仍应以 run summary 为主，必要时再吸收经过筛选的 task summary
- `session_registry.current_summary` 当前还承担 baseline refresh 的回写槽位，并记录 `baseline_refresh_input_type / baseline_refresh_input_ref`，用于说明本次 baseline refresh 的真实输入源

后续如果 `docs/WORKFLOW.md` 与这里冲突，以本文件为准，并同步修正 workflow。
