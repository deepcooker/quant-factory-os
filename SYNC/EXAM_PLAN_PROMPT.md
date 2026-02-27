# /plan 同频考试题面（CLI + 网页 GPT 通用）

你现在是本仓库的新接班 agent。  
目标不是答题，而是通过结构化输出证明你已经完成“思想层 + 执行层”同频学习。

请严格按以下步骤完成：

1. 只基于仓库证据阅读：  
`SYNC/READ_ORDER.md` -> `SYNC/CURRENT_STATE.md` -> `SYNC/SESSION_LATEST.md` -> `SYNC/DECISIONS_LATEST.md` -> `SYNC/LINKS.md` -> `docs/WORKFLOW.md` -> `docs/PROJECT_GUIDE.md` -> `TASKS/STATE.md` -> `TASKS/QUEUE.md`

2. 按模板文件输出答案：  
`SYNC/EXAM_ANSWER_TEMPLATE.md`

3. 输出约束：
- 不得空话；每段要有证据路径或明确因果说明。
- “下一步命令”只能写一条。
- “失败回退命令”必须可执行。
- 必须解释“这一步如何服务终点：自动化 -> 自我迭代 -> 涌现智能”。

4. 输出文件：
- 写入 `reports/<RUN_ID>/onboard_answer.md`
- `<RUN_ID>` 使用 `TASKS/STATE.md` 的 `CURRENT_RUN_ID`

完成后停止，不执行代码修改。
