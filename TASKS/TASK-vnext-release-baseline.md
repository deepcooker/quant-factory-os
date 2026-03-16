# TASK: vnext release baseline

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-vnext-release-baseline
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
扶正 run 为当前正式对象，移除 TASKS/STATE.md 这类过渡镜像，并让 tools/project_config.json -> runtime_state 成为唯一运行时真相源。

## Scope
- `tools/project_config.py`
- `tools/project_config.json`
- `tools/project_config.template.json`
- `tools/gitclient.py`
- `tools/evidence.py`
- `docs/`
- `AGENTS.md`
- `TASKS/`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写 legacy.sh 全链路。
- 不在本任务里完整重做新的 task 体系。
- 不扩 appserverclient 新命令。

## Acceptance
- [x] runtime_state 成为唯一运行时真相源，不再镜像到 TASKS/STATE.md
- [x] runtime_state 支持 current_task_id，并允许“有 run、无 task”状态
- [x] formal mainline 文档口径与新真相源一致
- [x] python3 -m py_compile tools/project_config.py tools/gitclient.py tools/evidence.py tools/appserverclient.py
- [x] make verify
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `docs/PROJECT_GUIDE.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `tools/project_config.json`
- `TASKS/QUEUE.md`

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
