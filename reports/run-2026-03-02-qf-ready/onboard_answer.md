## 问答 1：项目使命、背景、目标、最终结果、开发方式
- 回答：项目是 quant-factory-os 基建系统，目标是自动化执行 + 证据驱动学习 + 多角色协作收敛，最终形成可复用的项目操作系统；开发方式是 task 驱动、门禁驱动、PR 驱动。
- 证据文件路径：`README.md`、`docs/PROJECT_GUIDE.md`、`docs/WORKFLOW.md`、`AGENTS.md`

## 问答 2：阶段性目标、当前阶段、各阶段已完成事项
- 回答：阶段目标按基建硬化 -> 同频/考试 -> 讨论收敛 -> 执行闭环推进；当前在同频与自动化增强阶段，已完成 ready/discuss/execute/review 等主链路建设。
- 证据文件路径：`docs/PROJECT_GUIDE.md`、`TASKS/QUEUE.md`、`reports/run-2026-03-02-qf-ready/summary.md`

## 问答 3：基建完成后第一个项目如何落地（插件 vs 独立项目）与同频承接方法
- 回答：优先独立项目落地，通过 integration contract 与基座解耦；插件化作为后续分发形态。承接方式是先读 STATE/QUEUE/REPORTS 再进实施。
- 证据文件路径：`docs/PROJECT_GUIDE.md`、`docs/WORKFLOW.md`
- 推理结论与依据（若有）：推理结论=先独立后插件；依据=基建期需要降低耦合和升级风险。

## 问答 4：GPT 网页端（大脑）与 Codex CLI（手脚）如何同频，是否一致，操作顺序与优化
- 回答：原则一致但职责不同：GPT做策略/评审，Codex做执行/验证。顺序是 init -> learn -> ready -> discuss/execute -> review/ship。建议优化 learn 的模型同频证据和失败语义。
- 同频操作指南路径：`docs/WORKFLOW.md`、`SYNC/EXAM_WORKFLOW.md`
- 证据文件路径：`AGENTS.md`、`tools/qf`、`reports/run-2026-03-02-qf-ready/conversation.md`

## 问答 5：当前项目“宪法”是什么、是否合理、可优化点
- 回答：宪法是 AGENTS.md 的硬规则，核心是 task syscall、evidence memory、gate first、doc freshness。总体合理，需持续优化同频可见性和自动化体验。
- 证据文件路径：`AGENTS.md`

## 问答 6：当前工作流是什么（总流程/子流程/操作指南/涉及文件）
- 回答：总流程是 init -> sync -> learn -> ready -> orient/choose -> council/arbiter -> slice -> do -> review -> ship；子流程包含讨论态与执行态分层。
- 操作指南路径：`docs/WORKFLOW.md`
- 证据文件路径：`docs/WORKFLOW.md`、`SYNC/READ_ORDER.md`、`tools/qf`

## 问答 7：未完成任务与最新讨论批次是什么，如何查询
- 回答：通过 `TASKS/STATE.md` 看当前 run/task，通过 `TASKS/QUEUE.md` 看未完成项，通过 `reports/<RUN_ID>/` 与 `SYNC/discussion/<RUN_ID>/` 看最新批次讨论。
- 操作指南路径：`docs/WORKFLOW.md#Codex-session-startup-checklist`
- 证据文件路径：`TASKS/STATE.md`、`TASKS/QUEUE.md`、`reports/run-2026-03-02-qf-ready/conversation.md`

## 问答 8：最近 session 说了什么，从哪里查，如何追溯源文件，是否偏离主线
- 回答：先看 summary/decision/conversation，再回看具体产物文件与脚本。当前主线是强化 learn 同频和自动化编排，不应偏离到无关细节。
- 操作指南路径：`SYNC/READ_ORDER.md`
- 最近 session 总结路径：`reports/run-2026-03-02-qf-ready/summary.md`
- 源文件路径：`reports/run-2026-03-02-qf-ready/conversation.md`、`reports/run-2026-03-02-qf-ready/decision.md`
- 偏离判断：若改动不能提升同频、门禁或执行闭环，即判定偏离。

## 问答 9：基建项目“讨论”应使用的流程
- 回答：采用 orient -> choose -> council -> arbiter -> slice 的讨论收敛流，再进入 do。
- 操作指南路径：`docs/WORKFLOW.md`
- 证据文件路径：`tools/qf`、`SYNC/discussion/run-2026-03-02-qf-ready/`

## 问答 10：基建项目“代码实施”流程、角色定义、独立思考保障、当前实现状态
- 回答：实施流程是 do + verify + review + ship；角色为产品/架构/研发/测试，独立思考通过 council 分角色输出与 arbiter 统一裁决保障。
- 操作手册路径：`docs/WORKFLOW.md`
- 证据文件路径：`tools/qf`、`SYNC/discussion/run-2026-03-02-qf-ready/council.json`

## 问答 11：task / pr / run / project 等概念与生命周期管理
- 回答：task 是合同，run 是证据命名空间，pr 是交付单元，project 是上层项目命名空间；生命周期由 STATE/QUEUE 与 reports 协同推进。
- 流程入口与操作指南：`docs/ENTITIES.md`、`docs/WORKFLOW.md`
- 证据文件路径：`docs/ENTITIES.md`、`TASKS/STATE.md`

## 问答 12：准备工作完成后，需求方向讨论从哪一步开始，如何保存与多角色协作
- 回答：从 orient 开始；方向保存于 `SYNC/discussion/<RUN_ID>/orient.*` 与 `reports/<RUN_ID>/orient_choice.json`；多角色通过 council/arbiter 收敛。
- 方向保存位置：`SYNC/discussion/run-2026-03-02-qf-ready/orient.json`、`reports/run-2026-03-02-qf-ready/orient_choice.json`
- 讨论流程与入口：`tools/qf discuss` 或分步命令
- 证据文件路径：`docs/WORKFLOW.md`、`tools/qf`

## 问答 13：分支与代码管理策略，当前是否满足需求
- 回答：策略是一 task 一分支一 PR，title 含 RUN_ID，body 包含 Why/What/Verify/Evidence。当前满足基础需求，但仍需继续降低 ship 摩擦。
- 操作手册路径：`AGENTS.md`、`tools/ship.sh`
- 证据文件路径：`AGENTS.md`、`TASKS/QUEUE.md`

## 问答 14：每次任务完成后必须做什么
- 回答：必须 verify、更新 summary/decision、通过 review 校验偏差，再 ship；流程/规则变化还必须同步 owner docs。
- 操作指南路径：`docs/WORKFLOW.md`、`AGENTS.md`
- 证据文件路径：`reports/run-2026-03-02-qf-ready/summary.md`、`reports/run-2026-03-02-qf-ready/decision.md`

## 问答 15：如果目标是“简单、爽用、自动化高”，当前必须优化的点
- 回答：优先优化 learn 的模型同频可见锚点、run 级事件流审计稳定性、讨论与执行组合入口体验，以及文档自动更新门禁。
- 优先级与理由：P0=learn同频可信度；P1=单入口编排体验；P2=细节脚本重构。
- 证据文件路径：`tools/qf`、`docs/WORKFLOW.md`、`AGENTS.md`

## 实操技能 1：Codex 正确打开方式、版本、项目内用法、样例与实操结果
- Codex CLI 版本：`codex-cli 0.106.0`
- 操作手册路径：`docs/CODEX_CLI_OPERATION.md`
- 实操涉及文件：`reports/run-2026-03-02-qf-ready/codex_exec.events.jsonl`、`reports/run-2026-03-02-qf-ready/codex_exec.last.txt`、`reports/run-2026-03-02-qf-ready/codex_exec.stderr.log`
- 我实际执行的命令与结果：`codex --search --ask-for-approval never exec --sandbox read-only --json --output-last-message ...` 已执行并落盘事件流。
- 证据文件路径：`reports/run-2026-03-02-qf-ready/codex_exec.events.jsonl`

## 拉回主线 2：是否偏离当前最重要任务，原因，下一步动作
- 判断：不偏离，当前最重要任务就是强化 learn 同频与考试标准化。
- 原因：这是所有后续自动化与多角色博弈质量的前置条件。
- 下一步唯一命令：`tools/qf learn RUN_ID=run-2026-03-02-qf-ready MODEL_SYNC=1 PLAN_MODE=strong -log`
- 证据文件路径：`TASKS/STATE.md`、`reports/run-2026-03-02-qf-ready/conversation.md`
