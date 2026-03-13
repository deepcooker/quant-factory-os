# TOOLS_METHOD_FLOW_MAP

这份文档只描述当前正式主线的方法入口与调用关系。

阅读顺序固定为：
1. 先看主流程分层
2. 再看每个入口调用哪些底层方法
3. 最后再看历史兼容链路

不再把研发期过渡链路当成当前正式主流程。

---

## 1. 当前正式主线

当前正式主线固定为三层：

1. 准备层
   - `init`
2. 主流程层
   - `appserverclient`
   - `--learnbaseline`
   - `--fork-current`
   - `--fork-role`
   - `--role-turn`
   - `--summarize-role`
   - `--current-turn`
   - `--summarize-current`
   - `--refresh-baseline`
3. 收尾层
   - `gitclient`
   - `--commit`
   - `--rollback-last`
   - `--rollback-commit`

---

## 2. 准备层

### 2.1 `init`

业务目标：
- 读取统一配置
- 补齐项目基础骨架
- 检查 Codex / Git 前置条件
- 给出下一步动作建议

主流程方法：

| 编号 | 方法名 | 中文说明 |
| --- | --- | --- |
| `1001` | `init_step_01_load_context` | 调用 `project_config.py` 读取统一配置、校验必填项、打印统一配置 JSON。 |
| `1002` | `init_step_02_check_project_files` | 确保项目根目录下的标准骨架存在：`tools/`、`docs/`、`AGENTS.md`、`PROJECT_GUIDE.md`。 |
| `1003` | `init_step_03_check_codex_runtime` | 检查 `codex`、`app-server`、登录状态与 session 前提。 |
| `1004` | `init_step_04_check_git_runtime` | 检查 git 仓库、远端、认证、连通性与工作区状态。 |
| `1005` | `init_step_05_finalize` | 汇总检查结果并给出 `INIT_STATUS / INIT_REASON_CODES / INIT_NEXT`。 |

支撑方法命名：
- `init_tools_01` ~ `init_tools_xx`

---

## 3. 主流程层

### 3.1 `appserverclient --learnbaseline`

业务目标：
- 建立项目级 baseline 学习 session
- 用一次重型 `plan` 完成主线同频

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `A1` | `run_learnbaseline()` | baseline 学习流程总入口。 |
| `A2` | `connect()` | 初始化 `codex app-server` 连接，完成 `initialize / initialized`。 |
| `A3` | `list_collaboration_modes()` | 检查当前支持的协作模式。 |
| `A4` | `start_thread()` | 创建 baseline 学习 thread。 |
| `A5` | `start_turn()` | 以 `plan` 模式发送 baseline 学习提示词。 |
| `A6` | `wait_for_turn_completion()` | 等待 `task_complete / turn completed`。 |
| `A7` | `wait_for_rollout_ready()` | 等待 baseline rollout 文件可用。 |
| `A8` | `update_session_registry()` | 写回 `learn_session_baseline`。 |

输出：
- `session_registry.learn_session_baseline`

### 3.2 `appserverclient --fork-current`

业务目标：
- 从 baseline 派生当前工作 session

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `B1` | `run_fork_current()` | current session fork 总入口。 |
| `B2` | `connect()` | 初始化连接。 |
| `B3` | `resume_thread()` | 恢复 baseline session。 |
| `B4` | `fork_thread()` | 从 baseline fork 当前工作 session。 |
| `B5` | `wait_for_rollout_ready()` | 等待 current rollout 文件可用。 |
| `B6` | `update_session_registry()` | 写回 `fork_current_session`。 |

输出：
- `session_registry.fork_current_session`

### 3.2a `appserverclient --fork-role`

业务目标：
- 基于当前 `fork_current_session` 派生一个真实 role thread
- 把 role thread 绑定回当前 task 的 `role_threads`

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `B1a` | `run_fork_role()` | role thread fork 总入口。 |
| `B2a` | `connect()` | 初始化连接。 |
| `B3a` | `resume_thread()` | 恢复当前 run-main thread。 |
| `B4a` | `fork_thread()` | 从当前工作 thread 派生 role thread。 |
| `B5a` | `wait_for_rollout_ready()` | 等待 role rollout 文件可用。 |
| `B6a` | `set_thread_name()` | 给 role thread 写入角色名。 |
| `B7a` | `update_role_thread()` | 回写当前 task 的 `role_threads.<role>`。 |

输出：
- `TASKS/TASK-*.json -> role_threads.<role>`

说明：
- 这是最小 role thread binding 入口，不等于完整多 agent orchestration
- 当前优先服务 `dev/test`，`arch` 按需

### 3.2b `appserverclient --role-turn`

业务目标：
- 在已绑定的 role thread 上继续推进真实 turn

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `B1b` | `run_role_turn()` | role thread turn 总入口。 |
| `B2b` | `get_role_threads()` | 从当前 task 读取 role thread 绑定。 |
| `B3b` | `connect()` | 初始化连接。 |
| `B4b` | `resume_thread()` | 恢复对应 role thread。 |
| `B5b` | `start_turn()` | 在 role thread 上发送输入。 |
| `B6b` | `wait_for_turn_completion()` | 等待当前 turn 收口。 |
| `B7b` | `wait_for_rollout_ready()` | 等待 role rollout 文件可用。 |
| `B8b` | `update_role_thread()` | 维持当前 task 的 role 绑定状态。 |

### 3.2c `appserverclient --summarize-role`

业务目标：
- 在已绑定的 role thread 上生成一个 role-level 去噪总结
- 把结果写回当前 task 的 `role_summaries`
- 同时把引用证据追加到 `task_summary.role_summary_evidence`

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `B1c` | `run_summarize_role()` | role summary 总入口。 |
| `B2c` | `get_role_threads()` | 从当前 task 读取 role thread 绑定。 |
| `B3c` | `resume_thread()` | 恢复对应 role thread。 |
| `B4c` | `start_turn()` | 在 role thread 上发送 role summary prompt。 |
| `B5c` | `wait_for_turn_completion()` | 等待 role summary turn 收口。 |
| `B6c` | `read_thread()` | 读取对应 thread 最新内容。 |
| `B7c` | `extract_last_agent_message()` | 抽取 role summary 正文。 |
| `B8c` | `update_role_summary()` | 把 role summary 写回 task JSON。 |
| `B9c` | `update_task_summary()` | 给 task summary 追加 source/evidence。 |

### 4.3 `taskclient --merge-role-summaries`

业务目标：
- 当一个 task 下已有多个 role summaries 时，把它们按最小去重规则汇入 `task_summary`

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `T1` | `merge_role_summaries_into_task_summary()` | task-level 聚合总入口。 |
| `T2` | `default_role_summaries()` | 提供标准角色位。 |
| `T3` | `normalize_list()` | 对 `source_threads` 和 `role_summary_evidence` 做去重。 |
| `T4` | `save_task()` | 把更新后的 task summary 写回 task JSON。 |

说明：
- 当前只做最小聚合，不做复杂语义 merge
- 当前会去重追加：
  - `task_summary.source_threads`
  - `task_summary.role_summary_evidence`
  - `task_summary.key_updates` 中的 `<role> summary merged`

### 4.3b `evidence.py --merge-task-summary`

业务目标：
- 把稳定的 task summary 提升到 run summary，同时按字段类别执行不同聚合规则

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `R1` | `_merge_task_summary()` | run-level 聚合总入口。 |
| `R2` | `_field_merge_mode()` | 读取 `run_summary.merge_policy` 中该字段的归并类别。 |
| `R3` | `_merge_append_dedup_field()` | 对 `append_dedup` 字段保留 task 证据前缀并去重。 |
| `R4` | `_merge_rewrite_field()` | 对 `merge_rewrite` 字段做最小 run-level 轻改写再去重。 |
| `R5` | `_reconcile_run_summary()` | 对 `reconcile_only` 字段交由 task 真相源重算。 |

说明：
- 当前规则表是：
  - `active_tasks` / `completed_tasks`: `reconcile_only`
  - `source_tasks` / `verification_overview`: `append_dedup`
  - `key_updates` / `cross_task_decisions` / `cross_task_risks` / `next_run_or_next_tasks`: `merge_rewrite`
- 当前 `merge_rewrite` 仍是规则化轻归并，不做模型推理
- 当前已内置的高频规则包括：
  - 多个 `<role> summary merged` -> 一条 multi-role run-level 结论
  - `test gate=blocked/passed` -> 更稳定的 gate 状态表达
  - `cross_task_risks` 中通用 blocked-gate 句与更具体 blocked-gate 解释句并存时，保留更具体那条

### 4.3c `evidence.py --normalize-run-summary`

业务目标：
- 对历史已经落进 run-level 语义字段的旧 task 前缀条目做显式维护式清理

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `R6` | `_normalize_run_summary()` | 历史语义清理总入口。 |
| `R7` | `_normalize_legacy_run_summary_fields()` | 只处理 `legacy_cleanup_policy.target_fields` 中声明的字段。 |
| `R8` | `_humanize_summary_item()` | 去掉旧 task 前缀并做最小规范化。 |
| `R9` | `_build_baseline_ready_summary()` | 用清理后的 run-level 表达重建 baseline 压缩视图。 |

说明：
- 当前 `legacy_cleanup_policy.mode=explicit_maintenance_only`
- 它不会在普通 `merge-task-summary` 或 `reconcile-run-summary` 中自动执行
- 当前只清理：
  - `key_updates`
  - `cross_task_decisions`
  - `cross_task_risks`
  - `next_run_or_next_tasks`
- `verification_overview` 和 `source_tasks` 继续保留证据粒度，不在这一步被重写

### 4.4 `taskclient --refresh-task-gaps`

业务目标：
- 根据现有 `role_summaries` 和 `test_gate` 刷新 task 层的缺口汇总与冲突优先级

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `T5` | `refresh_task_gap_summary()` | task-level 缺口刷新总入口。 |
| `T6` | `default_role_summaries()` | 提供标准角色位。 |
| `T7` | `default_test_gate()` | 提供 test gate 默认结构。 |
| `T8` | `normalize_list()` | 对 `missing_roles` 与 `open_gaps` 做去重。 |
| `T9` | `save_task()` | 把冲突规则和缺口汇总写回 task JSON。 |

说明：
- 当前默认优先级顺序是 `run-main -> test -> arch -> dev`
- 当前最小缺口来源是：
  - 缺失的 `role_summaries`
  - 未完成的 `test_gate`
  - `test_gate.blocking_issues`

### 4.5 `taskclient --refresh-task-escalation`

业务目标：
- 判断当前 task 是否必须升级给 `run-main`

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `T10` | `refresh_task_escalation()` | task-level 升级判断总入口。 |
| `T11` | `gap_summary` | 读取当前缺口汇总。 |
| `T12` | `test_gate` | 读取当前 test gate 状态与阻塞项。 |
| `T13` | `normalize_list()` | 对升级原因做去重。 |
| `T14` | `save_task()` | 把升级规则和当前升级结果写回 task JSON。 |

说明：
- 当前最小必须升级条件是：
  - `run-main summary missing`
  - `test_gate` 未通过
  - 仍有 blocking issue
- 当前输出落点是：
  - `task_summary.escalation_policy`
  - `task_summary.escalation_summary`

### 4.6 `taskclient --refresh-run-main-resolution`

业务目标：
- 当 task 已升级给 `run-main` 后，判断 run-main 是否已确认、以及升级项是否可关闭

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `T15` | `refresh_run_main_resolution()` | run-main resolution 刷新总入口。 |
| `T16` | `escalation_summary` | 读取当前 task 是否仍需升级。 |
| `T17` | `role_summaries.run-main` | 判断 run-main 是否已给出 summary。 |
| `T18` | `test_gate` | 判断测试门是否已通过、是否仍有 blocking issue。 |
| `T19` | `save_task()` | 把 resolution policy 和 resolution result 写回 task JSON。 |

说明：
- 当前最小状态约定是：
  - `not_needed`
  - `pending_ack`
  - `acknowledged`
  - `closed`
- 当前最小关闭条件是：
  - 已存在 `run-main` summary
  - `test_gate` 已通过
  - 没有 blocking issue
- 当前输出落点是：
  - `task_summary.run_main_resolution_policy`
  - `task_summary.run_main_resolution`

### 3.2b `appserverclient --fork-role <run-main|dev|test|arch>`

业务目标：
- 从当前 `run-main` 工作副本再派生真实 role thread，并绑定回当前 task

说明：
- 当前 `run-main` 也可以通过该入口建立真实 role thread
- 当前 role thread 的真实写回落点是：
  - `role_threads.<role>`

### 3.2c `appserverclient --summarize-role <role>`

业务目标：
- 对单个 role thread 做去噪总结，并把结果回写 task 机器层

说明：
- 当前输出落点是：
  - `role_summaries.<role>`
  - `task_summary.role_summary_evidence`
- 当前单个 role summary 与 `task_summary.role_summary_evidence/source_threads` 的联动写回由：
  - `taskclient.update_role_summary_with_task_links()`
  统一承接
- 当前会统一调用：
  - `taskclient.refresh_task_coordination(include_role_merge=True)`
- 由 task 层统一完成：
  - `merge_role_summaries_into_task_summary()`
  - `task_summary.gap_summary`
  - `task_summary.escalation_summary`
  - `task_summary.run_main_resolution`

### 3.2d `appserverclient --mark-test-gate <status>`

业务目标：
- 把真实 `test` 角色线程的阶段性结论写回 `test_gate`，并刷新 task 层升级状态

说明：
- 当前会先写回：
  - `test_gate`
- 当前 test summary 对应的 thread/turn 证据拼接由：
  - `taskclient.update_test_gate_from_test_summary()`
  统一承接
- 然后统一调用：
  - `taskclient.refresh_task_coordination(include_role_merge=False)`

说明：
- 当前会自动复用：
  - `role_summaries.test.summary_turn_id`
  - `role_summaries.test.thread_id`
- 当前输出落点是：
  - `test_gate`
- 当前还会自动联动刷新：
  - `task_summary.gap_summary`
  - `task_summary.escalation_summary`
  - `task_summary.run_main_resolution`

### 3.3 `appserverclient --current-turn`

业务目标：
- 在当前工作 session 上继续推进需求、讨论、验证

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `C1` | `run_current_turn()` | current turn 总入口。 |
| `C2` | `connect()` | 初始化连接。 |
| `C3` | `resume_thread()` | 恢复 current session。 |
| `C4` | `start_turn()` | 以 `default` 模式发送当前输入。 |
| `C5` | `wait_for_turn_completion()` | 等待当前 turn 收口。 |
| `C6` | `wait_for_rollout_ready()` | 等待 rollout 文件可用。 |
| `C7` | `update_session_registry()` | 维持 `fork_current_session` 为当前工作副本。 |

说明：
- `mode` 是 `turn` 级别，不是 `thread` 级别。
- baseline 学习使用 `plan`。
- 日常 current turn 使用 `default`。

### 3.4 `appserverclient --summarize-current`

业务目标：
- 对当前工作 session 做去噪总结，并写回 `session_registry.current_summary`

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `D1` | `run_summarize_current()` | current summary 总入口。 |
| `D2` | `connect()` | 初始化连接。 |
| `D3` | `resume_thread()` | 恢复 current session。 |
| `D4` | `start_turn()` | 发送 summarize prompt。 |
| `D5` | `wait_for_turn_completion()` | 等待总结 turn 收口。 |
| `D6` | `read_thread()` | 读取当前 thread 详情。 |
| `D7` | `extract_last_agent_message()` | 抽取最后一条 agent 摘要正文。 |
| `D8` | `update_current_summary()` | 写回 `session_registry.current_summary`。 |

### 3.5 `appserverclient --refresh-baseline`

业务目标：
- 只用 current summary 的去噪结论增量刷新 baseline

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `E1` | `run_refresh_baseline()` | baseline refresh 总入口。 |
| `E2` | `connect()` | 初始化连接。 |
| `E3` | `resume_thread()` | 恢复 baseline session。 |
| `E4` | `start_turn()` | 发送 refresh prompt。 |
| `E5` | `wait_for_turn_completion()` | 等待 refresh turn 收口。 |
| `E6` | `read_thread()` | 读取 baseline thread 详情。 |
| `E7` | `extract_last_agent_message()` | 抽取最新 baseline 增量更新。 |
| `E8` | `update_session_registry()` | 维持 `learn_session_baseline` 最新状态。 |
| `E9` | `update_current_summary()` | 在 `current_summary` 中记录本次 baseline refresh 结果。 |

---

## 4. 收尾层

### 4.1 `gitclient --commit`

业务目标：
- 将当前工作区改动提交、创建 PR、合并并同步本地 `main`

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `G1` | `run_commit()` | 提交入口。 |
| `G2` | `git checkout -b <work_branch>` | 从当前工作面建立提交分支。 |
| `G3` | `git add -A` | 收集改动。 |
| `G4` | `git commit` | 生成提交。 |
| `G5` | `git push` | 推远端分支。 |
| `G6` | `gh pr create` | 创建 PR。 |
| `G7` | `gh pr merge` / `gh pr merge --auto` | 合并或挂 auto merge。 |
| `G8` | `gh pr view` 轮询 | 等待真正 `MERGED`。 |
| `G9` | `git fetch / checkout main / pull --rebase` | 同步本地 `main`。 |

### 4.2 `gitclient --rollback-last`

业务目标：
- 回滚主线最近一次提交

主流程调用关系：
- 从最新 `main` 建回滚分支
- `git revert`
- push
- 创建回滚 PR
- 合并并同步本地 `main`

### 4.3 `gitclient --rollback-commit`

业务目标：
- 回滚指定提交

主流程调用关系：
- 与 `--rollback-last` 相同，只是回滚目标为指定 commit

---

## 5. 实验性流程扩展

当前正式主线之后的发展方向是：
- baseline fork 多角色 session
- 按角色拆最小 task
- 各角色 session 去噪总结
- 将有效结论回灌 baseline

这部分未来会继续沉到 `appserverclient` 附近，而不是再回到旧的长链路中。

---

## 6. 历史兼容链路

以下链路保留为研发期过渡材料或兼容实现，不再作为当前正式主线：
- `learn`
- `ready`
- `orient`
- `choose`
- `council`
- `arbiter`
- `slice_task`
- `run_main`

这些文件仍可作为历史实现参考，但不再代表当前正式业务主流程。
对应 shell 兼容入口已归档到 `tools/backup/`，原 `tools/*.sh` 只保留过渡转发层。
