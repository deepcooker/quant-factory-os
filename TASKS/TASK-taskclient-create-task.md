# TASK: taskclient create task

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskclient-create-task
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
给 tools/taskclient.py 增加一个最小 JSON-first task bootstrap 入口，用来创建新的 TASKS/TASK-*.json 和兼容 md 视图，并可选追加到 TASKS/QUEUE.json。

## Scope
- `tools/taskclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `AGENTS.md`
- `docs/FILE_INDEX.md`
- `docs/WORKFLOW.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不复刻旧 task.sh 的交互式模板流程。
- 不实现复杂的 queue 规划或批量切片。
- 不改 ship / PR 链。

## Acceptance
- [x] tools/taskclient.py 支持创建新的 task JSON/MD
- [x] 创建入口支持可选写入 TASKS/QUEUE.json
- [x] python3 tools/taskclient.py --create-task --title "..." --goal "..." --scope tools/
- [x] python3 -m py_compile tools/taskclient.py tools/taskstore.py tools/project_config.py
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `tools/taskclient.py`
- `tools/taskstore.py`
- `TASKS/QUEUE.json`
- `TASKS/_SCHEMA.task.json`
- `TASKS/_SCHEMA.queue.json`

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
