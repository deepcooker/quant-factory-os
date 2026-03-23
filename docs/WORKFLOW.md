# WORKFLOW

本文件定义本仓**当前正式实验线**的主流程状态机。

它回答的是：
- 当前主线从哪里开始
- 每个阶段做什么
- 哪些阶段走 skill，哪些阶段由 orchestrator / state 层负责
- 哪些属于配套验证与项目接入，不属于单次 job 主运行

当前解释中心是：
- [AGENTS.md](/root/quant-factory-os/AGENTS.md)
- [PROJECT_GUIDE.md](/root/quant-factory-os/docs/PROJECT_GUIDE.md)
- [ENTITIES.md](/root/quant-factory-os/docs/ENTITIES.md)
- 根目录实验线代码与状态文件

历史 `tools/` 主线保留为兼容与迁移对照资产，不再作为本文件的正文主位。

## 1. 总体定位

### 1.1 当前主线是什么
当前主线不是旧的 `tools/appserverclient -> fork-current -> summarize -> refresh` 叙事。

当前主线是根目录实验线：
- `tools/main.py`
- `tools/app.py`
- `tools/project_config.json`
- `schemas/`
- `.agents/skills/`
- `state/`
- `tests/`
- `scripts/bootstrap_experiment_project.py`

### 1.2 当前目标是什么
当前目标不是“堆更多命令”，而是把这条实验线做成：
- 可学习
- 可澄清
- 可核证
- 可规划
- 可执行
- 可分流
- 可恢复
- 可验证
- 可接入第二个项目

### 1.3 三层结构
当前固定分三层：

1. 准备层
- owner docs
- runtime truth
- init
- bootstrap
- sync

2. 主运行层
- baseline
- coach
- verification
- correction
- planning
- role execution
- defect triage
- repair / replan / discussion
- merge
- baseline refresh

3. 配套层
- events
- checkpoints
- resume / recover
- smoke
- gate
- init
- sync
- bootstrap / runtime-bundle

### 1.4 Runtime Client 现状
当前 `app-server` 运行时已收敛到：
- `tools/app.py`

它负责：
- thread lifecycle：`new / resume / fork / rename`
- turn execution：`default / plan`
- optional skill attachment
- `run_business_turn(...)` 统一业务入口

`tools/main.py` 当前默认通过 `tools/app.py` 推进 baseline、run、role、triage、merge、refresh 相关线程动作与 turn 调用。

历史调试文件：
- `tools/backup/runtime_demo_archive/appserver_demo.py`

它只保留为已归档的协议验证稿，不再属于当前主线入口。

## 2. 主流程总览

当前正式主运行流程：

```text
project
  -> initialize / refresh learning baseline
  -> receive raw_request
  -> coach_round_v1
  -> verification_round
  -> coach_round_v2
  -> correction_round
  -> planning_round
  -> role execution
  -> collect active results
  -> defect triage
  -> repair / replan / discussion if needed
  -> merge
  -> baseline refresh
  -> state update
  -> events / checkpoints
  -> resume / recover when interrupted
```

注意：
- `smoke / gate / bootstrap` 是正式配套能力，但不是每个 job 都必经的主运行阶段
- 新项目接入先走 bootstrap，再进入主运行流程

## 3. 各阶段说明

### 3.1 准备层

准备层输入：
- `AGENTS.md`
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `tools/project_config.json`
- `state/registry.json`
- `TASKS/QUEUE.json`
- `reports/<RUN_ID>/`
- `tools/init.py`
- `tools/project_config.template.json`
- `tools/sync_tools.py`
- `scripts/bootstrap_experiment_project.py`
- `templates/experiment_project/`

准备层目标：
- 确认当前主线和阶段
- 确认运行真相源
- 确认当前最小 runtime 骨架是否完整
- 确认是否是当前仓执行，还是新项目接入

当前准备层工具：
- `python3 tools/init.py`
  - 补齐并校验 `tools/project_config.template.json` 与 `tools/project_config.json`
  - 输出 `INIT_STEP[...]`
  - 输出 `APP_RUNTIME_STATE_START/END`
  - 检查 `codex` / `app-server` / skills / schemas / git 工作区
- `python3 tools/sync_tools.py`
  - 向目标项目同步当前实验线 runtime bundle
  - 同步 docs、schemas、skills、`tools/app.py`、`tools/main.py`、tests 和模板工具
  - 默认不覆盖目标项目自己的 `tools/project_config.json`

准备层不做：
- 不直接实现需求
- 不替代主运行
- 不把 bootstrap 当成单次 job 的执行步骤

### 3.2 Learning Baseline

作用：
- 建立或刷新长期项目真相
- 吸收稳定结论
- 不吸收日常执行噪音

当前入口：
- `initialize_or_refresh_learning_baseline()`
- `refresh_learning_baseline()`

当前主要使用的 skill：
- `learn-baseline`

输出：
- `state.baseline_snapshot`

### 3.3 Coach / Clarification

作用：
- 把原始需求压成可执行问题
- 先做澄清，不直接做实现
- 产出 `clarified_job_v1`、claims、缺失证据项

当前入口：
- `coach_round_v1()`
- `coach_round_v2()`

当前主要使用的 skill：
- `project-coach`

### 3.4 Verification

作用：
- 围绕 claims 收集证据
- 让需求判断建立在证据上

当前入口：
- `verification_round()`

当前主要使用的 skills：
- `doc-evidence-worker`
- `code-evidence-worker`
- `runtime-evidence-worker`
- `contradiction-checker`

输出：
- `evidence_pack`

### 3.5 Correction

作用：
- 对需求本身进行质疑、方案比较和风险审查
- 形成 `corrected_job`

当前入口：
- `correction_round()`

当前主要使用的 skills：
- `demand-critic`
- `solution-designer`
- `risk-reviewer`

### 3.6 Planning

作用：
- 从 `corrected_job` 生成 `task_plan`
- 决定是否需要角色线程和最小切片

当前入口：
- `planning_round()`

当前主要使用的 skill：
- `run-manager`

### 3.7 Role Execution

作用：
- 执行最小任务切片
- 生成角色侧结果

当前入口：
- `spawn_role_threads()`
- `spawn_selected_tasks()`

当前主要使用的 skills：
- `dev-worker`
- `test-worker`
- `arch-reviewer`

说明：
- 当前角色执行已成立
- `subagents` 真实执行仍未闭合

### 3.8 Active Results

作用：
- 只消费当前有效结果
- 不把旧 test fail 和新 re-check 结果混在一起

当前关键方法：
- `collect_active_child_results()`

### 3.9 Defect Triage

作用：
- 在测试完成后做质量分流
- 决定进入：
  - repair
  - replan
  - discussion
  - proceed_merge

当前入口：
- `defect_triage_round()`

当前主要使用的 skill：
- `defect-triage`

### 3.10 Repair / Replan / Discussion

这是 triage 之后的质量治理层。

repair：
- 回开发修复
- 再测试 re-check

replan：
- 重新调整 task 方案
- 支持 task 级精准重跑

discussion：
- 处理重大缺陷、冲突或无法直接拍板的问题

当前说明：
- 这三条已经进入主流程
- 不再是外围附属逻辑

### 3.11 Merge

作用：
- 汇总当前有效结果
- 生成 run 级收敛结果

当前入口：
- `merge_in_run_baseline()`

当前主要使用的 skill：
- `run-manager`

输出：
- `merge_result`

### 3.12 Baseline Refresh

作用：
- 把本轮稳定结论回流到长期 baseline

当前入口：
- `refresh_learning_baseline()`

当前主要使用的 skill：
- `learn-baseline`

### 3.13 State / Events / Checkpoints / Resume

这些属于正式运行保障层，不是附属功能。

当前包含：
- `state/registry.json`
- `state/events.jsonl`
- `state/checkpoints/`
- `resume_job(job_id)`
- `resume_latest_incomplete_job()`

它们负责：
- 状态持久化
- 审计
- checkpoint
- 中断后恢复

## 4. 配套验证与发布

### 4.1 Smoke

开发级一键回归：

```bash
python3 tests/run_smoke_suite.py
```

作用：
- 跑实验线的核心 smoke 覆盖
- 确认主流程关键分支没有被改坏

### 4.2 Gate

发布级统一验证门：

```bash
python3 tests/run_gate.py
```

默认会执行：
- `py_compile`
- `smoke_suite`
- `integration_real_app`（默认 `SKIPPED`）

作用：
- 给实验线提供统一发布门
- 输出 gate 汇总结果
- 作为“这轮是否达到可继续推进/可交付”的最小机器化判断入口

当前 gate 产物：
- `state/test_reports/gate_summary.json`
- `state/test_reports/gate_summary.md`

### 4.3 Integration Real App

作用：
- 最小真实 app-server 集成烟测

当前状态：
- 已有最小入口
- 还不代表整条真实长链长期稳定闭合

## 5. 新项目接入

统一入口：

```bash
python3 scripts/bootstrap_experiment_project.py <target_path>
```

当前模式：
- `skeleton`
- `runnable`
- `runtime-bundle`

说明：
- `skeleton` 只生成最小骨架
- `runnable` 补 core skills registry 和最小接入能力
- `runtime-bundle` 再补最小 runtime、自验证 gate、最小 schema 和 manifest

## 6. 当前未完全闭合的边界

这些不影响实验线成立，但仍然是下一阶段边界：
- 真实 app-server 下整条主链长期稳定实跑
- `subagents` 真执行
- `queue / event job source`
- `human gates / approval`
- 更独立的 discussion / mediator 角色

## 7. 历史兼容线

旧 `tools/` 主线当前只保留为：
- 历史对照
- 兼容资产
- 迁移参考

它不再是本文件的正式解释中心。真正需要回看时，再单独去看：
- `tools/appserverclient.py`
- `tools/project_config.json`
- `tools/gitclient.py`
