# TASK: task queue json bootstrap

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-task-queue-json-bootstrap
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
为当前 run 建立最小可执行的 task.json / queue.json 机器真相源，并把运行时指针切到 JSON；同时只归档一个明确无人引用的旧 Python 入口。

## Scope
- `TASKS/QUEUE.json`
- `TASKS/TASK-*.json`
- `tools/project_config.json`
- `tools/project_config.py`
- `tools/project_config.template.json`
- `tools/init.py`
- `docs/`
- `tools/backup/`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不全量回填历史 task/queue 到 JSON。
- 不重写 task picker 或 queue writer。
- 不删除所有遗留 TASKS/*.md。

## Acceptance
- [x] 当前 run 下存在可用的 TASKS/QUEUE.json 和 TASKS/TASK-*.json
- [x] runtime_state 支持 current_task_json_file
- [x] owner docs 明确 json 是 task/queue 机器真相源，md 只是迁移期可读视图
- [x] tools/run_a9.py 已归档到 tools/backup/
- [x] python3 tools/project_config.py
- [x] python3 -m py_compile tools/project_config.py tools/init.py tools/appserverclient.py tools/gitclient.py tools/evidence.py
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `AGENTS.md`
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `tools/project_config.json`
- `TASKS/TASK-compat-shell-archive.md`
- `TASKS/TASK-vnext-release-baseline.md`

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
