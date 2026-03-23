# ENTITIES

对象模型先于流程模型。

本文件定义当前**实验线**的核心对象、边界、真相源与生命周期。
`WORKFLOW.md` 必须以这里的对象系统为基础，不再回到旧 `tools/` 对象系统解释当前主线。

## 1. 对象总原则

### 1.1 分层
- `project`：长期命名空间
- `baseline_snapshot`：长期学习真相
- `job`：一次进入系统的工作单
- `claim`：待验证判断
- `evidence_pack`：围绕 claim 的证据包
- `corrected_job`：经校正后可进入规划的工作单
- `task_plan`：从 corrected_job 拆出的执行计划
- `thread`：角色执行单元
- `defect_triage`：质量分流决策
- `merge_result`：项目级收敛结果
- `state/events/checkpoints`：运行保障层

### 1.2 当前真相源
- 配置真相源：
  - `tools/project_config.json`
- 运行真相源：
  - `state/registry.json`
- 审计真相源：
  - `state/events.jsonl`
- 阶段恢复真相源：
  - `state/checkpoints/`
- 学习锚点：
  - `docs/PROJECT_GUIDE.md`
- 宪法：
  - `AGENTS.md`
- 状态机：
  - `docs/WORKFLOW.md`

### 1.3 历史兼容对象
以下对象仍可保留作对照，但不再是当前主线的解释中心：
- `tools/project_config.json -> runtime_state`
- `bootstrap_state`
- `init_project_session`
- 旧 `session_registry.*`

## 2. Project

### 2.1 定义
`project` 是长期项目命名空间。

### 2.2 职责
- 标识这是哪个项目
- 承载长期 owner docs
- 承载默认 skills / policy / gate 配置
- 容纳多个 jobs 和长期 baseline

### 2.3 真相源
- `tools/project_config.json`

### 2.4 生命周期
- 创建于项目建立时
- 一般不关闭

## 3. Baseline Snapshot

### 3.1 定义
`baseline_snapshot` 是项目长期真相快照。

### 3.2 职责
- 记录稳定 truth
- 为新 job 提供长期认知背景
- 吸收 merge 后的稳定结论

### 3.3 真相源
- `state/registry.json -> baseline_snapshot`

### 3.4 生命周期
- 初始化时创建
- merge 后刷新
- 中断恢复时继续复用

## 4. Job

### 4.1 定义
`job` 是一次进入系统的工作单。

### 4.2 职责
- 承载 `raw_request`
- 串联 coach、verification、correction、planning、execution、merge、refresh
- 形成整轮执行状态

### 4.3 当前关键字段
- `job_id`
- `raw_request`
- `clarified_job_v1`
- `evidence_packs`
- `clarified_job_v2`
- `corrected_job`
- `task_plan`
- `defect_triage`
- `final_summary`
- `status`
- `defect_status`
- `repair_cycle_count`
- `replan_cycle_count`
- `discussion_cycle_count`

### 4.4 真相源
- `state/registry.json -> jobs`

### 4.5 生命周期
- `NEW`
- `COACHED`
- `VERIFIED`
- `CORRECTED`
- `PLANNED`
- `EXECUTING`
- `MERGED`
- `DONE`
- 各类 blocked / defect 状态

## 5. Claim

### 5.1 定义
`claim` 是待验证判断，不是最终结论。

### 5.2 职责
- 把“猜测”拆成可核证对象
- 为 evidence workers 提供检索目标
- 支撑 correction 和 contradiction 检查

### 5.3 当前关键字段
- `claim_id`
- `claim`
- `type`
- `confidence`
- `evidence_level`
- `verification_required`
- `status`
- `doc_support`
- `code_support`
- `runtime_support`
- `contradictions`

### 5.4 真相源
- `state/registry.json -> claims`

## 6. Evidence Pack

### 6.1 定义
`evidence_pack` 是围绕单个或一组 claims 的证据集合。

### 6.2 职责
- 汇总 doc / code / runtime / contradiction 结果
- 为 coach v2 和 correction 提供基础

### 6.3 主要来源
- `doc-evidence-worker`
- `code-evidence-worker`
- `runtime-evidence-worker`
- `contradiction-checker`

### 6.4 真相落点
- 当前以 `job.evidence_packs` 为主
- 运行时审计可回看 `state/events.jsonl`

## 7. Corrected Job

### 7.1 定义
`corrected_job` 是经 coach + verification + correction 之后，可进入 planning 的工作单。

### 7.2 职责
- 收敛需求边界
- 清理伪需求、错目标、错路径
- 形成后续 task planning 的正式输入

### 7.3 真相落点
- `state/registry.json -> jobs[*].corrected_job`

## 8. Task Plan

### 8.1 定义
`task_plan` 是从 corrected_job 拆出的执行计划。

### 8.2 职责
- 定义最小执行切片
- 决定 role 分工
- 决定是否需要 repair / replan / discussion 的后续处理

### 8.3 真相落点
- `state/registry.json -> jobs[*].task_plan`

说明：
- 当前实验线主真相在 `state/registry.json`
- `TASKS/QUEUE.json` 仍可作为更高层任务池存在，但不是当前 job 状态机的唯一真相源

## 9. Thread

### 9.1 定义
`thread` 是角色执行单元。

### 9.2 当前角色
- `run_manager`
- `project_coach`
- `dev_worker`
- `test_worker`
- `arch_reviewer`
- `defect_triage`
- 各 evidence workers

### 9.3 当前关键字段
- `thread_id`
- `role`
- `status`
- `parent_thread_id`
- `job_id`
- `task_id`
- `result`

### 9.4 真相落点
- `state/registry.json -> threads`

## 10. Active Results

### 10.1 定义
`active results` 是当前有效结果集，不是历史全集。

### 10.2 职责
- 避免旧结果污染当前 triage / merge / replan
- 让 repair / re-check 只消费最新结果

### 10.3 当前实现锚点
- `collect_active_child_results()`

## 11. Defect Triage

### 11.1 定义
`defect_triage` 是测试后的质量分流决策。

### 11.2 职责
- 判断：
  - `send_back_to_dev`
  - `send_to_run_manager`
  - `start_discussion_round`
  - `proceed_merge`
- 记录目标 task 和缺陷级别

### 11.3 真相落点
- `state/registry.json -> jobs[*].defect_triage`

### 11.4 缺陷状态
当前统一使用：
- `DEFECT_REPAIRING`
- `DEFECT_REPLANNING`
- `DEFECT_DISCUSSING`
- `DEFECT_BLOCKED`
- `READY_TO_MERGE`

## 12. Merge Result

### 12.1 定义
`merge_result` 是 run / job 级收敛结果。

### 12.2 职责
- 汇总有效角色结果
- 形成最终项目级结论
- 为 baseline refresh 提供输入

### 12.3 真相落点
- `state/registry.json -> jobs[*].final_summary`

## 13. Events

### 13.1 定义
`events` 是运行过程的审计流，不是业务结果本身。

### 13.2 职责
- 记录阶段推进
- 记录决策和状态变化
- 支持复盘与恢复

### 13.3 真相源
- `state/events.jsonl`

## 14. Checkpoints

### 14.1 定义
`checkpoints` 是阶段快照。

### 14.2 职责
- 支持 resume / recover
- 支持回看关键阶段产物

### 14.3 真相源
- `state/checkpoints/job_<id>/`

## 15. Smoke / Gate

### 15.1 定义
这不是单次 job 对象，而是实验线质量保障对象。

### 15.2 关键入口
- `tests/run_smoke_suite.py`
- `tests/run_gate.py`

### 15.3 关键产物
- `state/test_reports/smoke_summary.json`
- `state/test_reports/gate_summary.json`
- `state/test_reports/gate_summary.md`

## 16. Bootstrap Manifest

### 16.1 定义
`bootstrap_manifest.json` 是新项目接入时的产物，不属于单次 job 主流程对象。

### 16.2 职责
- 记录来源仓库
- 记录 bootstrap mode
- 记录复制的 skills / runtime / schemas
- 支持后续升级与迁移

## 17. Supplementary Overviews

以下文档是补充总览，不是正式入口：
- `docs/archive/总纲.md`
  - 流程总纲摘要
- `docs/archive/a.md`
  - 完成度矩阵 / 汇报稿

它们可用于总览和复盘，但不替代：
- `AGENTS.md`
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
