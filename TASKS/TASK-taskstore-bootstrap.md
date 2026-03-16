# TASK: taskstore bootstrap

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskstore-bootstrap
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
新增一个最小 tools/taskstore.py，统一读写 TASKS/QUEUE.json 与 TASKS/TASK-*.json，并先让 evidence.py 依赖这层读取运行态 task。

## Scope
- `tools/taskstore.py`
- `tools/evidence.py`
- `tools/project_config.json`
- `docs/FILE_INDEX.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写全部 task/queue 调用方。
- 不实现完整 task picker。
- 不删除现有 md 兼容视图。

## Acceptance
- [x] 新增 tools/taskstore.py
- [x] taskstore 可读取 active task、指定 task 和 queue
- [x] tools/evidence.py 通过 taskstore 解析当前 run 的 task_id
- [x] python3 tools/taskstore.py --active-task
- [x] python3 -m py_compile tools/taskstore.py tools/evidence.py tools/project_config.py
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `tools/project_config.json`
- `TASKS/QUEUE.json`
- `TASKS/TASK-task-queue-json-bootstrap.json`
- `TASKS/TASK-compat-shell-archive.json`

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=planned, thread_id=(none)

## Test Gate
- Status: pending
- Owner role: test

### Required Axes

### Evidence

### Blocking Issues

## Role Summaries
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=planned, thread_id=(none)

## Task Summary
- Status: draft

### Key Updates

### Decisions

### Risks

### Verification

### Next Steps

### Conflict Policy
- Priority order: 
- Merge rule: 
- Escalation rule: 

### Gap Summary

### Escalation Policy

### Escalation Summary
- needs_run_main: false

### Run-Main Resolution Policy

### Run-Main Resolution
- status: pending_ack
- close_escalation: false

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
