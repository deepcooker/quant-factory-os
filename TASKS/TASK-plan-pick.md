# TASK: 自动生成任务候选清单（plan）并支持确认后领取（pick）

RUN_ID: run-2026-02-25-plan-pick
OWNER: <you>
PRIORITY: P1

## Goal
新增非交互式“计划/确认”机制：Codex 根据 repo 证据与当前 QUEUE/STATE 生成 10~20 条候选任务清单供人确认；确认后可一键领取当前队列任务（串行接力），减少人肉写 queue/拼命令。

## Scope (Required)
- `tools/`
- `docs/`
- `tests/`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- 新增命令：`tools/task.sh --plan N=20`（或默认 N=20）生成 `TASKS/TODO_PROPOSAL.md`，并在 stdout 打印摘要（top N + 如何 pick）。
- 清单至少包含两块信息：
- 新增命令：`tools/task.sh --pick queue-next`：在已生成 proposal 的前提下，执行领取（等价于 `tools/task.sh --next`）并打印 TASK_FILE/RUN_ID；默认不自动写代码、不自动 ship。
- 更新 docs/WORKFLOW.md：补充 plan/pick 的使用方式（用于 session 内串行接力）。
- `make verify` 全绿，并为该 RUN_ID 写齐 evidence 三件套。

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
