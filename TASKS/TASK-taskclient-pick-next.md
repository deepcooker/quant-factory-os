# TASK: taskclient pick next

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskclient-pick-next
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
新增一个 Python-first 的 task picker，先替代旧 task.sh 中“从 queue 选择下一个 task 并绑定 runtime_state”的核心职责。

## Scope
- `tools/taskclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `AGENTS.md`
- `docs/FILE_INDEX.md`
- `docs/WORKFLOW.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写旧 task.sh 的 task 模板生成逻辑。
- 不接 ship / PR / merge 流程。
- 不全量迁移历史 QUEUE.md 内容。

## Acceptance
- [x] 新增 python3 tools/taskclient.py --pick-next
- [x] picker 读取 TASKS/QUEUE.json 并绑定 active task 到 runtime_state
- [x] picker 会把 queue item 状态写回 JSON
- [x] python3 tools/taskclient.py --pick-next
- [x] python3 -m py_compile tools/taskclient.py tools/taskstore.py tools/project_config.py
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `tools/taskstore.py`
- `tools/project_config.py`
- `TASKS/QUEUE.json`
- `TASKS/TASK-appserverclient-taskstore-integration.json`

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
