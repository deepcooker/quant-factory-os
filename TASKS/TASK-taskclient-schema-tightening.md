# TASK: taskclient schema tightening

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskclient-schema-tightening
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把 taskclient --create-task 和 TASKS/_SCHEMA.task.json 收到一版更稳定的字段口径，补齐必要字段、默认值和最小校验。

## Scope
- `tools/taskclient.py`
- `tools/taskstore.py`
- `TASKS/_SCHEMA.task.json`
- `docs/FILE_INDEX.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不做复杂交互式 wizard。
- 不做完整 JSON schema 校验器。
- 不清理本轮之前生成的样例 task。

## Acceptance
- [x] TASKS/_SCHEMA.task.json 与当前 task payload 字段对齐
- [x] taskclient --create-task 支持 priority/non-goal/input/acceptance/risks/rollback-plan
- [x] create-task 有最小字段校验与重复文件保护
- [x] save_queue() 会刷新 updated_at
- [x] python3 tools/taskclient.py --create-task --title "schema sample task" --goal "验证 schema 收紧。" --scope docs/ --run-id run-2026-03-11-vnext-release-baseline --priority P2 --non-goal "不改运行时" --input AGENTS.md --acceptance "owner docs updated" --queue
- [x] python3 -m py_compile tools/taskclient.py tools/taskstore.py
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `TASKS/_SCHEMA.task.json`
- `tools/taskclient.py`
- `tools/taskstore.py`

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
