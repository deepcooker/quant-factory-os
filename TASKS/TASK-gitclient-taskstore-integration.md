# TASK: gitclient taskstore integration

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-gitclient-taskstore-integration
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
让 tools/gitclient.py 通过 taskstore 读取当前 active task，提交说明优先使用 task JSON 的结构化上下文，而不是继续依赖 TASKS/*.md 文件名。

## Scope
- `tools/gitclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `docs/FILE_INDEX.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写 commit / PR / merge 主流程。
- 不改更多 shell 兼容层。
- 不做完整 task title 规范化。

## Acceptance
- [x] gitclient 可通过 taskstore 读取 active task
- [x] resolve_commit_message() 优先使用 task JSON 的 title/task_id
- [x] python3 -m py_compile tools/gitclient.py tools/taskstore.py tools/project_config.py
- [x] python3 tools/taskstore.py --active-task
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `tools/gitclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `TASKS/TASK-taskstore-bootstrap.json`

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
