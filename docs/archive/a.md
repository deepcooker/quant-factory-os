我按你贴的这版内容做了一个**更适合放进文档/README 的收口版**，核心不改，只把表达收得更清楚、更像正式说明。原始内容参考你贴的这版总表。

---

# AI 研发基座样机：总流程完成度总表

## 一、主流程完成度

| 序号 | 流程步骤                                      | 是否走 skill                                             | 当前状态         | 当前实现情况                                                                                                       | 需要优化 / 未完成点                                                |
| -- | ----------------------------------------- | ----------------------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| 0  | 启动 orchestrator，加载配置、状态、skill 注册表         | 否                                                     | 已完成          | `Orchestrator` 已能加载 config/state、初始化 client、加载 skill registry                                                | 无                                                          |
| 1  | 读取 `project_config.json`                  | 否                                                     | 已完成          | 已读取 docs、skills、thread policy、verification policy、human gates 等配置                                            | 无                                                          |
| 2  | 校验技能、文档、schemas、仓库、state 环境               | 否                                                     | 已完成          | `validate_environment()` 已检查 docs、skills、schemas、state 可写                                                    | 可继续增强细粒度错误提示，但不影响主流程成立                                     |
| 3  | 恢复或创建 learning baseline thread            | 否                                                     | 已完成          | `ensure_learning_thread()` 已接通                                                                               | 无                                                          |
| 4  | 用 `$learn-baseline` 初始化或刷新项目知识            | 是：`learn_baseline`                                    | 已完成          | baseline init / refresh 已走 skill，并在校验后写回 baseline snapshot                                                   | 真实 app-server 下完整长期主链尚未全链路证明                               |
| 5  | 恢复或创建 run baseline thread                 | 否                                                     | 已完成          | `ensure_run_thread()` 已接通                                                                                    | 无                                                          |
| 6  | 接收原始需求 `raw_request`                      | 否                                                     | 已完成          | 当前主线支持 manual raw_request                                                                                    | `queue_file` / `event_jobs` 尚未接入主线                         |
| 7  | 进入 coach 澄清回合                             | 是：`project_coach`                                     | 已完成          | `coach_round_v1()` 已走 helper + schema                                                                        | 无                                                          |
| 8  | 输出 `clarified_job_v1 + claims`            | 是：`project_coach`                                     | 已完成          | `clarified_job` 和 `claims` 引用结构已接通                                                                           | 无                                                          |
| 9  | 进入 verification coordinator               | 否（协调层）                                                | 已完成          | orchestrator 已能编排 verification                                                                               | 无                                                          |
| 10 | 收集 `evidence_pack`                        | 是：`doc/code/runtime/contradiction`                    | 已完成          | 四类 evidence skills 已接通，能生成 `evidence_pack`                                                                   | `enable_runtime_verification` 的配置与执行层尚未完全严格对齐              |
| 11 | project-coach 二次修正，输出 `clarified_job_v2`  | 是：`project_coach`                                     | 已完成          | `coach_round_v2()` 已接通 helper + schema                                                                       | 无                                                          |
| 12 | 进入需求博弈 / 校正环节                             | 是：`demand_critic / solution_designer / risk_reviewer` | 已完成          | 三个 correction skills 已接通                                                                                     | 无                                                          |
| 13 | 输出 `corrected_job`                        | 部分                                                    | 已完成          | correction skills 输出 + helper 合成 `corrected_job` 并校验                                                         | 无                                                          |
| 14 | run baseline 拆 `task_plan`                | 是：`run_manager`                                       | 已完成          | `planning_round()` → `run_task_planning()` 已接通                                                               | 无                                                          |
| 15 | orchestrator fork dev / test / arch 等角色线程 | 否                                                     | 已完成          | `spawn_role_threads()` / `spawn_selected_tasks()` 已接通                                                        | 无                                                          |
| 16 | 子线程执行                                     | 是：`dev_worker / test_worker / arch_reviewer`          | 已完成          | 角色线程执行已走通                                                                                                    | `subagents` 真执行仍未完成                                        |
| 17 | 回收当前有效结果集（active results）                 | 否                                                     | 已完成          | 已按 `task_id + role` 聚合当前有效结果，不再混旧结果                                                                          | 无                                                          |
| 18 | 进入 defect triage                          | 是：`defect_triage`                                     | 已完成          | triage gate 已正式插入主流程                                                                                         | 无                                                          |
| 19 | 根据 triage 分流                              | 部分                                                    | 已完成          | 已支持 `send_back_to_dev / send_to_run_manager / start_discussion_round / proceed_merge`                        | 无                                                          |
| 20 | repair loop（返工回路）                         | 部分                                                    | 已完成          | `dev repair + test recheck + triage again` 已接通，且为 task 级返工                                                   | 无                                                          |
| 21 | replan loop（重规划回路）                        | 部分                                                    | 已完成          | `run_replan_round()` + `_consume_replan_decision()` 已接通，且为 task 级精准重跑                                        | 无                                                          |
| 22 | discussion round（讨论/仲裁回路）                 | 目前主要由 `run_manager` 兼任                                | 已完成          | `discussion_resolution.next_route` 已能驱动继续流转                                                                  | 独立 `review-mediator / implementation-critic` 未落地，但不影响主流程成立 |
| 23 | cycle limits（循环上限保护）                      | 否                                                     | 已完成          | 已有 repair / replan / discussion cycle 上限，超限可阻断                                                               | 无                                                          |
| 24 | defect flow status（缺陷状态流）                 | 否                                                     | 已完成          | 已有 `DEFECT_REPAIRING / DEFECT_REPLANNING / DEFECT_DISCUSSING / DEFECT_BLOCKED / READY_TO_MERGE`              | 可继续精简命名，但不影响主流程                                            |
| 25 | run baseline 去噪汇总                         | 是：`run_manager`                                       | 已完成          | `merge_in_run_baseline()` → `run_merge()` 已接通                                                                | 无                                                          |
| 26 | 汇总结果回流 learning baseline                  | 是：`learn_baseline`                                    | 已完成          | `refresh_learning_baseline()` 已写回 baseline snapshot                                                          | 无                                                          |
| 27 | 更新 registry / state / evidence / claim 状态 | 否                                                     | 已完成          | `_save_state()`、state 更新、claim / evidence 挂接已接通                                                              | `human_gates` 尚未实际执行                                       |
| 28 | 事件审计日志（events）                            | 否                                                     | 已完成          | `events.jsonl` 已接通，记录关键决策与状态变化                                                                               | 无                                                          |
| 29 | 阶段 checkpoint                             | 否                                                     | 已完成          | 关键阶段 checkpoint 已接通                                                                                          | 无                                                          |
| 30 | resume / recover 从中间继续                    | 否                                                     | 已完成          | `resume_job()` / `resume_latest_incomplete_job()` 已接通                                                        | 无                                                          |
| 31 | smoke suite（开发级回归）                        | 否                                                     | 已完成          | `run_smoke_suite.py` 已覆盖 happy path、replan、resume、repair、discussion block、cycle limit、contract test          | 无                                                          |
| 32 | gate（发布级统一验证门）                            | 否                                                     | 已完成          | `run_gate.py` 已统一跑 `py_compile + smoke_suite + optional integration_real_app`                                | 无                                                          |
| 33 | gate 可读性（`summary_text / md 报告 / 失败摘要`）   | 否                                                     | 已完成          | gate 已能输出更人类可读的结果和报告                                                                                         | 按本地最新状态视为已完成                                               |
| 34 | 最小真实 app-server integration smoke         | 否                                                     | 部分完成         | 已有 `integration_real_app_smoke.py`，默认 `SKIPPED`，显式开启可跑                                                       | 只证明最小集成，不等于完整真实主链长期稳定实跑                                    |
| 35 | bootstrap：结构级接入骨架                         | 否                                                     | 已完成          | 可生成 `AGENTS.md / project_config.json / docs / .agents/skills / schemas / state / reports / artifacts / logs` | 无                                                          |
| 36 | bootstrap：runnable mode（最小可运行接入骨架）        | 否                                                     | 已完成          | `--with-core-skills` 已可写入最小 skills registry，并复制 core skills                                                  | 无                                                          |
| 37 | bootstrap：runtime-bundle mode（自带运行包）      | 否                                                     | 已完成（按最新执行结果） | `--with-runtime-bundle` 已可复制最小 runtime 文件、最小 schema 集，并生成 `bootstrap_manifest.json`                          | 当前聊天里对 step28 的直接文件证据不如本地执行结果强，但按最新回报视为完成                  |
| 38 | bootstrap smoke（接入骨架 / 运行包验证）             | 否                                                     | 已完成          | `smoke_bootstrap_project.py` 已通过；`smoke_bootstrap_runtime_bundle.py` 也已通过                                    | 同上，runtime-bundle smoke 按最新执行结果视为完成                        |
| 39 | 文档：实验线 gate 说明                            | 否                                                     | 已完成          | `EXPERIMENT_LINE_GATE.md` 已说明 fake smoke / gate / real app smoke 的使用方式                                       | 无                                                          |
| 40 | 文档：bootstrap 说明                           | 否                                                     | 已完成          | `PROJECT_BOOTSTRAP.md` 已说明 skeleton / runnable / runtime-bundle 模式                                           | 无                                                          |
| 41 | 文档：`NEXT_STEPS` 生成                        | 否                                                     | 已完成          | bootstrap 后可给目标项目生成 `docs/NEXT_STEPS.md`                                                                     | 无                                                          |

---

## 二、当前不影响主流程成立、但仍值得继续优化的点

| 项目                                           | 当前状态  | 是否影响主流程成立 | 说明                                                               |
| -------------------------------------------- | ----- | --------- | ---------------------------------------------------------------- |
| 真实 app-server 下整条主线长期实跑                      | 未完全完成 | 否         | 现在 fake smoke / gate / 最小 real integration 已有，但完整真实主链长期稳定性仍未完全证明 |
| `subagents` 真执行                              | 未完成   | 否         | 当前只是配置层支持，代码里还没有真实 spawn subagents                               |
| `queue / event job source`                   | 未完成   | 否         | 当前 manual raw_request 已足够支撑主流程成立                                 |
| `human gates / approval`                     | 未完成   | 否         | 配置位已在，但不影响实验线主流程跑通                                               |
| 独立 `review-mediator / implementation-critic` | 未完成   | 否         | discussion 目前由 `run_manager` 兼任，主流程仍能成立                          |
| verification policy 对 runtime worker 的严格执行对齐 | 未完全完成 | 否         | 配置和执行层还有细化空间，但不影响主线成立                                            |
| gate 可读性在聊天上传快照与本地代码的一致性                     | 部分    | 否         | 本地已确认完成，说明实验线本体没问题，只是聊天中文件快照有时滞后                                 |

---

## 三、当前已经真正成立的正式主流程

```text
启动/配置/环境校验
→ baseline init
→ coach v1
→ verification
→ coach v2
→ correction
→ planning
→ role execution
→ active results
→ defect triage
→ repair / replan / discussion / or proceed_merge
→ merge
→ baseline refresh
→ state update
→ events / checkpoints / resume
→ smoke / gate
→ bootstrap
```

---

## 四、一句话总评

**从头到尾看，这条实验线已经把“核心主流程 + 质量治理 + 恢复审计 + 回归验证 + 新项目接入”全部串起来了。**

它现在最准确的定位是：

**一个可恢复、可分流、可重跑、可回归、可 bootstrap，并且已经具备发布级验证门的 AI 研发基座样机。**

---

如果你要，我可以继续把这版再压成一个更短的：
**《README / WORKFLOW 可直接贴入版》**。
