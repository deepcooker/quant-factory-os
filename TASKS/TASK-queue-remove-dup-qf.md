# TASK: queue remove duplicate qf item

RUN_ID: run-2026-02-26-queue-remove-dup-qf
OWNER: <you>
PRIORITY: P1

## Goal
删除 TASKS/QUEUE.md 中重复的 tools/qf 队列条目（残留的未完成 [ ]），避免再次被 pick。

## Scope (Required)
- `TASKS/QUEUE.md`

## Acceptance
- make verify 通过
- 本次提交只变更 TASKS/QUEUE.md（其余由 ship 自动附带 task+reports）
