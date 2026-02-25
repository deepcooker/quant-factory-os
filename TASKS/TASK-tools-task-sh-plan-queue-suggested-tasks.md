# TASK: 强化 tools/task.sh --plan：Queue 为空时生成 Suggested tasks（可复制入队）

RUN_ID: run-2026-02-25-tools-task-sh-plan-queue-suggested-tasks
OWNER: <you>
PRIORITY: P1

## Goal
当 Queue candidates 为 none 时，--plan 仍应基于 repo 证据（reports/*/decision.md、TASKS/STATE.md、可选 MISTAKES/）生成 10~20 条 Suggested tasks，并输出可直接粘贴的 QUEUE item 片段（含 Title/Goal/Scope/Acceptance 骨架），把“自动拿任务”真正做成单行可用。

## Scope (Required)
- `tools/task.sh`
- `tests/`
- `docs/WORKFLOW.md`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- `tools/task.sh --plan 20` 生成的 `TASKS/TODO_PROPOSAL.md` 新增 `## Suggested tasks`：
- Queue 为空时也至少产出 5 条建议
- 每条包含可复制的 QUEUE item 片段（TODO Title/Goal/Scope/Acceptance）
- Suggested tasks 的来源至少覆盖：
- 最近 N 个 reports/run-*/decision.md（抓取 next/todo/suggest/风险/rollback 等信号）
- TASKS/STATE.md（风险/未完成信号）
- 若存在 MISTAKES/ 则读取其中 *.md（抓取 recurring issue/action）
- docs/WORKFLOW.md 补充：Queue 为空时，用 Suggested tasks 选一条入队→再 --next/--pick
- `make verify` 全绿

## Inputs
- Links / files / references
- If data is needed, specify allowed sample constraints (max rows, time window)

## Steps (Optional)
Suggested approach, if you have one.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
- Rollback plan:
