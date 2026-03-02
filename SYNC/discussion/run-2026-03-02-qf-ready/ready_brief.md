# Ready Brief (Discussion Draft)

RUN_ID: `run-2026-03-02-qf-ready`
Generated At (UTC): 2026-03-02T08:19:12.235085+00:00
Mode: discussion-only (pre-confirmation)

## 项目理解
- Summary: quant-factory-os is the governance/execution base for quant engineering.
- Goal: quant-factory-os 是一个“自举式智能工厂操作系统”：它能**自动执行任务**、能**从证据链与错题本学习变强**、能**训练/引导新的智能体加入并理解因果链**、能**自我迭代升级工具与流程**、最终能**多智能协作形成涌现智能**，并把这些能力用于任何项目（最初是量化策略工厂，最终是通用项目底座）。

## 宪法与工作流解读
- Constitution: 约束是任务驱动、证据优先、scope 严格、文档新鲜度硬门禁。
- Workflow: 流程以门禁推进：sync 同频 -> ready 上岗 -> orient/choose 定方向 -> council/arbiter 收敛 -> slice 拆解 -> do 执行 -> verify/review/ship 收尾。

## 证据链状态
- sync_report_file: reports/run-2026-03-02-qf-ready/sync_report.json
- ready_file: reports/run-2026-03-02-qf-ready/ready.json
- decision_exists: False
- summary_exists: False
- conversation_exists: True
- execution_exists: True
- ship_state_exists: False

## Session 承接
- continuity: partial_context
- current_run_id: run-2026-03-02-queue-state-closure
- current_task_file: TASKS/TASK-queue-state-closure-20260302.md
- current_status: done

## Restatement
- Goal: Close stale queue in-progress/unchecked leftovers and set session state to done.
- Scope: TASKS/QUEUE.md, TASKS/STATE.md, reports/{RUN_ID}/
- Acceptance: All stale slice-next: ... ready 先处理未收尾 run leftover items are no longer [ ]/[>].; TASKS/STATE.md status is done for the current run snapshot.; Command(s) pass: make verify; Evidence updated: reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md
- Steps: evidence -> implement -> verify -> reports -> ship
- Stop: finish and wait for next instruction; if blocked, record stop reason in decision.md

## Run 决策
- resolution_required: false
- decision: continue

