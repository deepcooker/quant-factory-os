# TASK: taskclient create-task ux

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-taskclient-create-task-ux
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
优化 taskclient --create-task 的使用体验，在不破坏当前 JSON schema 的前提下，让它更适合日常直接使用。

## Scope
- `tools/taskclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`
- `docs/FILE_INDEX.md`
- `docs/WORKFLOW.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不改 task JSON schema。
- 不做交互式 wizard。
- 不重写 pick-next 行为。

## Acceptance
- [x] --run-id 可省略，默认使用当前 runtime run
- [x] --scope/--input/--non-goal/--acceptance 支持重复传参和逗号分隔
- [x] 支持创建后立即绑定 active task
- [x] python3 tools/taskclient.py --create-task --title "ux sample task" --goal "验证 create-task 体验优化。" --scope "tools/,docs/" --non-goal "不改 schema,不改 ship" --input "AGENTS.md,docs/WORKFLOW.md" --acceptance "docs updated,task json created" --activate
- [x] python3 -m py_compile tools/taskclient.py tools/taskstore.py
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `tools/taskclient.py`
- `tools/taskstore.py`
- `tools/project_config.json`

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
