# Ready Brief (Discussion Draft)

PROJECT_ID: `project-0`
RUN_ID: `run-2026-03-02-qf-ready`
Generated At (UTC): 2026-03-03T04:31:33.919118+00:00
Mode: discussion-only (pre-confirmation)

## 项目理解
- Summary: quant-factory-os is the governance/execution base for quant engineering.
- Goal: quant-factory-os 是一个“自举式智能工厂操作系统”：它能**自动执行任务**、能**从证据链与错题本学习变强**、能**训练/引导新的智能体加入并理解因果链**、能**自我迭代升级工具与流程**、最终能**多智能协作形成涌现智能**，并把这些能力用于任何项目（最初是量化策略工厂，最终是通用项目底座）。

## 宪法与工作流解读
- Constitution: 约束是任务驱动、证据优先、scope 严格、文档新鲜度硬门禁。
- Workflow: 流程以门禁推进：sync 同频 -> ready 上岗 -> orient/choose 定方向 -> council/arbiter 收敛 -> slice 拆解 -> do 执行 -> verify/review/ship 收尾。

## 证据链状态
- learn_report_file: reports/projects/project-0/session/learn.json
- sync_report_file: reports/run-2026-03-02-qf-ready/sync_report.json
- ready_file: reports/run-2026-03-02-qf-ready/ready.json
- decision_exists: True
- summary_exists: True
- conversation_exists: True
- execution_exists: True
- ship_state_exists: True

## Session 承接
- continuity: partial_context
- current_run_id: run-2026-03-02-queue-state-closure
- current_task_file: TASKS/TASK-queue-state-closure-20260302.md
- current_status: done

## Restatement
- Goal: 把 `ready` 升级为“先判定会话状态、再给方向、确认后执行”的决策中枢，并将讨论态与执行态证据彻底分层。
- Scope: tools/qf, tests/, docs/WORKFLOW.md, AGENTS.md, SYNC/, TASKS/, reports/{RUN_ID}/
- Acceptance: tools/qf ready 在检测到上次 run 非完成态时，必须先给出“收尾（resume-close）/抛弃并新开（abandon-new）”决策，不得直接进入新方向。; ready 输出固定包含：项目目标解读、宪法/工作流解读、证据链状态、session 承接状态、风险/阻塞、建议下一步。; ready 通过后自动产出 3-5 个方向候选（含优先级/收益/风险/成本/依赖）并支持用户确认；用户确认前不写入 reports/{RUN_ID}/ 执行证据。; 确认方向后进入多角色评审（产品/架构/研发/测试）并产出统一执行契约；执行结束后自动做偏差审计（需求/实现/测试/文档）与必要修复。; 文档更新为硬门禁：流程或规则变更若未同步 owner docs 和 run evidence，不能通过收尾。; make verify 通过；新增回归测试覆盖“讨论态不入 report、确认后入 report、旧 run 决策分流”。
- Steps: evidence -> implement -> verify -> reports -> ship
- Stop: finish and wait for next instruction; if blocked, record stop reason in decision.md

## Run 决策
- resolution_required: false
- decision: abandon-new

