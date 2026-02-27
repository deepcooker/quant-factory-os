# 同频入口

用途：这是给任何模型/会话（Codex CLI 或网页端 GPT）使用的**唯一同频入口层**。  
目标是在不依赖聊天历史的情况下，几分钟完成接班。

如果只读一个目录，就先读 `SYNC/`。

## 建议阅读顺序
1. `SYNC/READ_ORDER.md`
2. `SYNC/CURRENT_STATE.md`
3. `SYNC/SESSION_LATEST.md`
4. `SYNC/DECISIONS_LATEST.md`
5. `SYNC/LINKS.md`

## 规则
- 先同频，后执行。
- `TASKS/STATE.md` 是 `CURRENT_RUN_ID` 的权威来源。
- `tools/qf init` 只负责环境准备，不等于同频完成。
- 接力会话下，`tools/qf init` 默认自动执行 `tools/qf handoff`（可用 `QF_INIT_AUTO_HANDOFF=0` 关闭）。
- `tools/qf handoff` 只负责接班摘要，不等于门禁通过。
- `tools/qf ready` 是唯一上岗门禁；没有 `ready.json` 不得执行 `tools/qf do`.
- `tools/qf ready` 默认可从当前任务合同自动填充复述字段（可用 `QF_READY_AUTO=0` 强制手填）。
- 如果 `SYNC/*` 与深层证据冲突，以最新证据为准：
  - `reports/<RUN_ID>/decision.md`
  - `main` 上已合并 PR 状态
- 流程/规则有变更时，必须同步更新 owner 文档（AGENTS/WORKFLOW/SYNC），否则不允许 ship。
- 退出前必须更新 `SYNC/SESSION_LATEST.md`。
