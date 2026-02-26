# TASK: queue-add-qf-3cmd

RUN_ID: run-2026-02-26-queue-add-qf-3cmd
OWNER: codex
PRIORITY: P1

## Goal
在 `TASKS/QUEUE.md` 顶部新增一条关于 tools/qf 三命令收敛的待办条目，供后续会话领取。

## Scope (Required)
- `TASKS/QUEUE.md`

## Non-goals
- 不改动 `tools/`、`tests/`、`docs/`。
- 不实现 qf 功能本身，仅入队任务。

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/QUEUE.md`

## Steps (Optional)
1) 按 Queue 既有格式在 `## Queue` 顶部新增条目。
2) 运行 evidence 与 verify。
3) 更新本 RUN 的 evidence 文档并 ship。

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: 队列格式错误导致领取脚本解析异常。
- Rollback plan: 回滚 `TASKS/QUEUE.md` 本次新增条目。
