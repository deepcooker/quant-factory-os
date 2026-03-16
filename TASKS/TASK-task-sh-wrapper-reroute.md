# TASK: task sh wrapper reroute

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-task-sh-wrapper-reroute
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把原 tools/task.sh wrapper 的最常用主线路径直接改为转到 Python-first 的 taskclient，进一步减少旧 shell task 入口继续充当正式主线。

## Scope
- `tools/task.sh`
- `tools/project_config.json`
- `AGENTS.md`
- `docs/FILE_INDEX.md`
- `docs/WORKFLOW.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写 tools/backup/task.sh。
- 不动旧 ship 链。
- 不删除所有历史对 tools/task.sh 的引用。

## Acceptance
- [x] tools/task.sh --next 直接转到 python3 tools/taskclient.py --pick-next
- [x] tools/task.sh --pick queue-next 直接转到 python3 tools/taskclient.py --pick-next
- [x] 其他旧参数仍回退到 tools/backup/task.sh
- [x] tools/project_config.json 的 active task 指针与当前 runtime task 一致
- [x] bash tools/task.sh --next
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `tools/task.sh`
- `tools/taskclient.py`
- `tools/backup/task.sh`

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
