# TASK: task summary bootstrap

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-task-summary-bootstrap
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
为 task summary 设计并落最小真相源与入口，不扩 run summary。

## Scope
- `tools/taskclient.py`
- `TASKS/_SCHEMA.task.json`
- `docs/ENTITIES.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`

## Non-goals

## Acceptance
- [x] task json supports summary payload
- [x] taskclient can show or update task summary
- [x] docs describe task summary as task-level aggregate

## Inputs

## Task Summary
- Status: completed

### Key Updates
- task summary stored inside TASKS/TASK-*.json

### Decisions
- task summary stays inside task json instead of a separate file

### Risks
- run summary still not implemented

### Verification
- python3 -m py_compile tools/taskclient.py

### Next Steps
- design run summary after task summary stabilizes

### Source Threads
- `fork_current_session:019ce213-6d27-70c3-bb87-b53ba904f28c`

## Risks / Rollback
- Risks: 
- Rollback plan:
