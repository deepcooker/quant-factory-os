# PROJECT_GUIDE.md

## 问答

### 1. 整个项目是做什么的，背景，目标是什么，我最终要什么，我是用什么开发方式来完成这个项目的？
- 回答：
  - 项目定位：`quant-factory-os` 是一个“基建型执行与治理系统”，核心是把 AI 工作流做成可审计、可交接、可迭代的工程系统。
  - 背景：多窗口/多会话/多 Agent 协作会丢上下文，必须把“会话记忆”转成仓库内证据（`TASKS/` + `reports/` + 文档）。
  - 目标：形成“同频学习 -> 方向讨论 -> 合同收敛 -> 切片执行 -> 复盘修正”的闭环自动化流程。
  - 你最终要的结果：新 AI 上岗后可以自我理解项目、对齐主线、按门禁执行，并持续更新文档与证据。
  - 开发方式：Task 驱动 + Gate 驱动 + Evidence 驱动（先定义任务与边界，再执行最小改动，再用验证和报告闭环）。
- 证据文件：
  - `README.md`
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `docs/ENTITIES.md`

### 2. 项目有几个阶段性目标，现在完成到哪个阶段，每个阶段都完成了什么？
- 回答：
  - 阶段划分（当前文档定义）：
    - Stage 0：基座硬化（门禁、流程、证据链）
    - Stage 1：学习系统（同频、考试、复盘沉淀）
    - Stage 2：训练系统（新 Agent 上岗标准化）
    - Stage 3：自我升级（通过证据驱动工具改进）
    - Stage 4：多智能协作收敛
    - Stage 5：接入具体业务项目（如财富系统）
  - 当前阶段：Stage 0/1 交界，重点在“learn 同频可信度”和“流程自动化体验”。
  - 已完成主成果：`qf` 流程链路、learn 模型同频锚点、ready 门禁、discuss/execute/review 基本闭环。
- 证据文件：
  - `docs/WORKFLOW.md`
  - `TASKS/STATE.md`
  - `TASKS/QUEUE.md`
  - `reports/run-2026-03-02-qf-ready/summary.md`

### 3. 这个基建项目做完之后，它会作为基座的项目，我们接下来第一个项目将完成什么，你会怎么去落地，我们现在设计的结构是把这个变成一个插件好呢还是独立项目好，项目最难的是读懂和同频我的意图，你读了项目后，你准备用什么样的方式来接？
- 回答：
  - 第一优先业务落地：财富系统新建项目引导与集成合同（先 dry-run、后实执行）。
  - 落地方式：先独立项目（推荐），基座仓负责流程治理，业务仓负责业务代码；通过“集成合同”连接。
  - 插件化建议：放到后期（基座稳定后再做分发），当前过早插件化会放大耦合和变更风险。
  - 最难点：不是写代码，是“意图同频 + 主线不跑偏 + 证据可追踪”。
  - 我的承接方式：每次先跑同频链路并输出主线锚点，再进入讨论与执行，执行后强制写入报告。
- 证据文件：
  - `docs/WORKFLOW.md`
  - `docs/ENTITIES.md`
  - `AGENTS.md`
  - `reports/run-2026-03-02-qf-ready/decision.md`
- 说明：
  - “独立项目优先、插件后置”属于基于当前流程成熟度的工程推理，依据是现有门禁与证据机制的稳定性要求。

### 4. 如果完成这个项目，我把gpt网页端当做大脑，codex cli当做手脚，你是怎么让codex cli 和 gpt保持同频的，一样吗，如果不一样，都需要怎么做？
- 回答：
  - 不一样：
    - GPT 网页端：负责策略、评审、反驳、方向选择（大脑层）。
    - Codex CLI：负责本地执行、改动、验证、证据落盘（执行层）。
  - 同频操作顺序：
    - `tools/qf init`
    - `tools/qf learn MODEL_SYNC=1 PLAN_MODE=strong -log`
    - `tools/qf ready`
  - 必读文件清单：
    - `SYNC/READ_ORDER.md`
    - `AGENTS.md`
    - `docs/WORKFLOW.md`
    - `docs/ENTITIES.md`
    - `TASKS/STATE.md`
    - `TASKS/QUEUE.md`
  - 优化点：继续降低命令摩擦，把“组件命令”与“组合编排”分层，保证体验简单但审计不丢失。
- 证据文件：
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `docs/CODEX_CLI_OPERATION.md`

### 5. 这个项目当前的宪法是什么样的？
- 回答：
  - 当前宪法是 `AGENTS.md`：定义了任务入口、证据义务、允许命令、门禁链路、失败协议、文档更新硬规则。
  - 是否合理：总体合理，能防止“无任务改代码、无证据交付、跨范围漂移”。
  - 优化建议：保持规则不降级，只优化可用性（更清晰的输出、更少重复命令、更强自动补齐）。
- 证据文件：
  - `AGENTS.md`

### 6. 这个项目当前工作流是什么样的？
- 回答：
  - 工作流说明位置：`docs/WORKFLOW.md`。
  - 主流程：`init -> sync -> learn -> ready -> orient -> choose -> council -> arbiter -> slice -> do -> review -> ship`。
  - 子流程：
    - 同频子流程：`init/sync/learn/ready`
    - 讨论子流程：`orient/choose/council/arbiter/slice`
    - 执行子流程：`do/review/ship`
  - 操作指南位置：`AGENTS.md`（硬规则）+ `docs/WORKFLOW.md`（状态机）+ `docs/CODEX_CLI_OPERATION.md`（CLI实践）。
- 证据文件：
  - `docs/WORKFLOW.md`
  - `AGENTS.md`
  - `docs/CODEX_CLI_OPERATION.md`

### 7. 我们现在的项目有没有未完成的任务呢，最新的批次在讨论什么问题，你是怎么查的？
- 回答：
  - 查法：
    - 当前指针看 `TASKS/STATE.md`
    - 队列状态看 `TASKS/QUEUE.md`
    - 当前 run 的细节看 `reports/<RUN_ID>/summary.md` 与 `decision.md`
  - 当前状态（本次会话前）：历史队列大多已完成，核心讨论集中在“learn 同频质量、考试机制、流程自动化和文档一致性”。
- 证据文件：
  - `TASKS/STATE.md`
  - `TASKS/QUEUE.md`
  - `reports/run-2026-03-02-qf-ready/summary.md`
  - `reports/run-2026-03-02-qf-ready/decision.md`

### 8. 你查了最近的session说了什么，你是从哪里查的？
- 回答：
  - 查阅路径：`SYNC/SESSION_LATEST.md`、`SYNC/CURRENT_STATE.md`、`reports/<RUN_ID>/conversation.md`、`summary.md`、`decision.md`。
  - 最近 session 摘要：主线是“强化 learn 同频、明确 codex 与模型交互证据、压缩流程摩擦并保持文档实时更新”。
  - 如果你认为不对：回到源证据文件逐条核对，以 `conversation.md + decision.md + 已合并PR` 为准。
  - 是否偏离主线判断：凡是不能提升“同频可信度/执行闭环/证据可审计”的动作都算偏离。
- 证据文件：
  - `SYNC/SESSION_LATEST.md`
  - `SYNC/CURRENT_STATE.md`
  - `reports/run-2026-03-02-qf-ready/conversation.md`
  - `reports/run-2026-03-02-qf-ready/decision.md`

### 9. 基建项目讨论项目应该用哪个流程？
- 回答：
  - 使用“讨论优先”流程：`orient -> choose -> council -> arbiter -> slice`，收敛后才允许 `do`。
  - 目的：保证多角色独立分析，再统一裁决，避免先写代码后补理由。
- 证据文件：
  - `docs/WORKFLOW.md`
  - `AGENTS.md`

### 10. 基建项目的代码实施流程是什么样的，它需要哪些agent进行协作呢，怎么保证这些角色都是独立思考的，他们每一个角色的定义是什么样子的，怎么保证其独立思考的，我们现在都实现了吗，怎么实现的？
- 回答：
  - 实施流程：`do -> verify -> review -> ship`。
  - 角色协作：
    - 产品：目标与边界
    - 架构：技术方案与影响面
    - 研发：改动实现与回归
    - 测试：用例与失败路径
  - 独立思考机制：`council` 先产出多角色独立意见，`arbiter` 再统一合同。
  - 实现现状：已实现基础版（流程与产物齐备），并行执行能力仍可继续增强。
- 证据文件：
  - `docs/WORKFLOW.md`
  - `tools/qf`
  - `SYNC/discussion/<RUN_ID>/council.json`
  - `reports/<RUN_ID>/execution_contract.json`

### 11. 项目基建里的task，pr，run，product 的都是什么意思，还有其他的概念吗，他们的生命周期管理是怎么样的？
- 回答：
  - `task`：需求合同（范围与验收）
  - `pr`：交付与审阅单元
  - `run`：一次执行证据命名空间（`reports/<RUN_ID>/`）
  - `project`：上层项目维度（`project-0` 为当前基座）
  - 其他关键概念：`queue`（待办入口）、`gate`（流程门禁）、`evidence`（审计记忆）。
  - 生命周期：`QUEUE -> TASK -> RUN evidence -> verify -> PR -> merge -> 状态更新`。
- 证据文件：
  - `docs/ENTITIES.md`
  - `docs/WORKFLOW.md`
  - `AGENTS.md`

### 12. 我们在项目的准备工作做好后，我们一个需求讨论方向，从流程的哪一步开始？
- 回答：
  - 从 `orient` 开始；随后 `choose -> council -> arbiter -> slice`。
  - 最新方向存储：
    - 草案：`SYNC/discussion/<RUN_ID>/orient.md|json`
    - 选择结果：`reports/<RUN_ID>/orient_choice.json`
    - 收敛合同：`reports/<RUN_ID>/execution_contract.json|md`
  - 需求讨论需要多角色；与代码实施角色相关但职责不同（讨论是决策层，实施是执行层）。
- 证据文件：
  - `docs/WORKFLOW.md`
  - `AGENTS.md`
  - `SYNC/discussion/`
  - `reports/<RUN_ID>/`

### 13. 我们分支代码的管理是怎么样的，现在满足需求吗？
- 回答：
  - 当前规则：`一任务一分支一PR`，PR 标题要含 RUN_ID，正文要含 Why/What/Verify/Evidence。
  - 结论：规则满足当前基建阶段需求；后续若并行度大幅增加，再补充分支命名与合并策略细则。
- 证据文件：
  - `AGENTS.md`
  - `tools/ship.sh`

### 14. 每次做完任务，你必须要做什么事情？
- 回答：
  - 必做：
    - 运行验证（通常 `make verify`）
    - 更新 `reports/<RUN_ID>/summary.md` 和 `decision.md`
    - 变更流程/规则时同步更新 owner docs
    - 再执行 ship
- 证据文件：
  - `AGENTS.md`
  - `docs/WORKFLOW.md`

### 15. 这个项目是基建项目吗，如果我要的体验是为了用起来很爽，完全自动化，有哪些必要的需要优化的？
- 回答：
  - 是基建项目。
  - 必要优化优先级：
    - P0：同频质量（learn 真实模型交互 + 口述 + 考试 + 锚点可见）
    - P1：流程爽感（组合编排入口，减少手动多命令）
    - P2：文档自动更新（改动后自动提示/自动门禁）
    - P3：失败恢复（中断后一键恢复主线）
- 证据文件：
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `tools/qf`

## 实操技能

### 16. 这个项目codex 的正确打开方式你会吗，所有的codex 正确的方法你会使用，我们项目中用到了哪些，你能列出来吗？
- 回答：
  - 会。
  - 本项目使用方式：
    - 讨论模式：`codex --sandbox read-only --ask-for-approval never --search`
    - 执行模式：`codex --sandbox workspace-write --ask-for-approval on-request --search`
    - 非交互审计：`codex exec --json ...`
  - 当前已确认版本：`codex-cli 0.106.0`
  - 操作手册：`docs/CODEX_CLI_OPERATION.md`
  - 相关文件：`AGENTS.md`、`docs/WORKFLOW.md`、`tools/qf`
  - 样例证据：`reports/run-2026-03-02-qf-ready/codex_exec.check.events.jsonl`
- 证据文件：
  - `docs/CODEX_CLI_OPERATION.md`
  - `reports/run-2026-03-02-qf-ready/codex_exec.check.events.jsonl`
  - `reports/run-2026-03-02-qf-ready/codex_exec.check.last.txt`

## 拉回主线

### 17. 根据最新的session，你现在做的东西是否偏离了我们现在最重要的任务，你是否认为我们偏离了主线，为什么，接下来我们应该怎么做？
- 回答：
  - 主线：提高“同频可信度 + 自动化执行体验 + 文档证据一致性”。
  - 偏离判定：任何不能增强这三项的动作都是偏离。
  - 接下来动作：先保证 `PROJECT_GUIDE` 成为高质量问答真相源，再用该真相源驱动 learn 与考试，最后继续收敛流程自动化。
- 证据文件：
  - `SYNC/SESSION_LATEST.md`
  - `TASKS/STATE.md`
  - `reports/run-2026-03-02-qf-ready/decision.md`
