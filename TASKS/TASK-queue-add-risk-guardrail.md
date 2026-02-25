# TASK: queue-add risk guardrail

RUN_ID: run-2026-02-25-queue-add-risk-guardrail
OWNER: <you>
PRIORITY: P1

## Goal
将 risk guardrail 队列项写入 TASKS/QUEUE.md，使其成为可领取的下一枪任务。

## Scope (Required)
- `TASKS/QUEUE.md`

## Acceptance
- `make verify` 通过
- 本次提交仅变更：TASKS/QUEUE.md（其余由 ship 自动附带 task+reports）

## Non-goals
- 不实现 guardrail 逻辑（只入队）
