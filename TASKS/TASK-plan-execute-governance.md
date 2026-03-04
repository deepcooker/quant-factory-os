# TASK: plan-execute governance: /plan 与 qf plan 去歧义 + /compact 策略落地

RUN_ID: run-2026-03-04-plan-execute-governance
OWNER: <you>
PRIORITY: P1

## Goal
把 Codex `/plan`、`tools/qf plan`、`tools/qf discuss/execute` 的职责边界写清楚，
并把 `/compact` 的使用时机落地到 owner 文档，消除流程语义混乱。

## Scope (Required)
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/CODEX_CLI_OPERATION.md`
- `docs/PROJECT_GUIDE.md`
- `tools/evidence.py`
- `TASKS/QUEUE.md`
- `TASKS/STATE.md`
- `reports/{RUN_ID}/`

## Non-goals
- 不修改 `tools/qf` 脚本行为（仅文档治理层修正）。
- 不重构现有 queue/slice 执行逻辑。

## Acceptance
- [ ] 文档明确区分：Codex `/plan`（讨论协议）与 `tools/qf plan`（队列提案工具）
- [ ] 文档明确 `Plan -> Confirm -> Execute` 的触发点与执行边界
- [ ] 文档明确 `/compact` 不是每 task 强制，而是按上下文体量与里程碑触发
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `docs/PROJECT_GUIDE.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/CODEX_CLI_OPERATION.md`
- OpenAI Codex official docs (CLI reference, slash commands, noninteractive, agents-md, rules)

## Steps (Optional)
1) 对齐官方语义与本地实现差异。
2) 更新 owner 文档边界与操作指引。
3) 记录证据并完成验证。

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: 文档改动影响现有习惯，短期内需要适配。
- Rollback plan: 回滚本任务改动，恢复上一版 owner 文档与状态指针。
