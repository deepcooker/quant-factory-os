# TASK: multi-thread collaboration minimum chain

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-multi-thread-collaboration-minimum-chain
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
定义并最小落地 run-main 到 dev/test 的多线程协作链，明确 task 绑定、summary 回收和 test gate。

## Scope
- `docs/ENTITIES.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `tools/appserverclient.py`
- `tools/taskclient.py`

## Non-goals
- 不一次性实现完整多agent orchestration
- 不引入 swarm

## Acceptance
- [x] 明确 run-main/dev/test 最小协作链; 文档与必要最小实现同步; evidence updated

## Inputs
- `docs/ENTITIES.md`
- `docs/WORKFLOW.md`
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `tools/project_config.json`

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=active, thread_id=thread-dev-sample
- `test`: status=planned, thread_id=(none)
- `arch`: status=planned, thread_id=(none)

## Test Gate
- Status: blocked
- Owner role: test

### Required Axes

### Evidence
- test plan drafted

### Blocking Issues
- functional regression coverage pending

## Task Summary
- Status: completed

### Key Updates
- task JSON now supports role_threads and test_gate for the minimum run-main/dev/test chain

### Decisions
- minimum multi-thread collaboration persists in taskclient and TASKS/TASK-*.json before app-server orchestration

### Risks
- full role-thread lifecycle and automatic summary aggregation are still not implemented

### Verification
- python3 -m py_compile tools/taskclient.py
- python3 tools/taskclient.py --role-threads
- python3 tools/taskclient.py --test-gate

### Next Steps
- wire run-main/dev/test thread creation to real appserver sessions later

### Source Threads
- `dev`
- `test`

## Risks / Rollback
- Risks: 
- Rollback plan:
