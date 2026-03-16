# TASK: appserverclient taskstore integration

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-appserverclient-taskstore-integration
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
让 tools/appserverclient.py 显式读取 active task JSON，并把当前 task 上下文打印进运行时日志，确保 runtime/session 主线与 taskstore 对齐。

## Scope
- `tools/appserverclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `docs/FILE_INDEX.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不改 app-server 协议调用顺序。
- 不重写 learn/fork/current-turn 主流程。
- 不实现 queue 驱动的自动 task 切换。

## Acceptance
- [x] appserverclient 可读取 active task JSON
- [x] 运行时日志包含 active task JSON 的关键信息
- [x] python3 -m py_compile tools/appserverclient.py tools/taskstore.py tools/project_config.py
- [x] python3 tools/project_config.py
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `tools/appserverclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `TASKS/TASK-gitclient-taskstore-integration.json`

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
