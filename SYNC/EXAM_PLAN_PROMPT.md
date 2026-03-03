# /plan 同频深度考试题面（v2）

你现在是本仓库的新接班 agent。
目标是证明你已经完成“项目理解 + 宪法/流程解读 + 证据链 + session 承接 + codex 实操能力”的同频，不是做表面问答。

请严格执行：

1. 先读证据（必须按顺序）
- `SYNC/READ_ORDER.md`
- `SYNC/README.md`
- `SYNC/CURRENT_STATE.md`
- `SYNC/SESSION_LATEST.md`
- `SYNC/DECISIONS_LATEST.md`
- `SYNC/LINKS.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/PROJECT_GUIDE.md`
- `TASKS/STATE.md`
- `TASKS/QUEUE.md`
- 当前 RUN 的 `reports/<RUN_ID>/summary.md`、`decision.md`、`conversation.md`（存在则读）

2. 按模板完整作答
- 模板：`SYNC/EXAM_ANSWER_TEMPLATE.md`
- 输出：`reports/<RUN_ID>/onboard_answer.md`

3. 强约束
- 每个问题必须写“证据文件路径”；若是推理，必须明确写“推理结论 + 推理依据”。
- 不能只写结论，必须可追溯。
- 对“操作指南/入口/文件位置/命令”类问题，必须给出可执行命令或可定位路径。
- 最后必须回答“是否偏离主线 + 下一步动作”。

4. 评分
- 运行：`tools/qf exam-auto RUN_ID=<RUN_ID>` 或 `tools/qf exam RUN_ID=<RUN_ID>`
- 通过标准：分数 >= 85 且 required checks 全通过。

完成后停止，不执行代码修改。
