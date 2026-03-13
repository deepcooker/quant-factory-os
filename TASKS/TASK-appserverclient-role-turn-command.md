# TASK: appserverclient role turn command

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-appserverclient-role-turn-command
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
新增 appserverclient --role-turn，让已绑定的 dev/test role thread 能执行真实 current-turn。

## Scope
- `tools/appserverclient.py`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`

## Non-goals
- 不做 thread summary 自动汇总
- 不做多角色调度器

## Acceptance
- [ ] 新增 --role-turn 命令; 已绑定 role thread 可执行真实 turn; docs/evidence updated

## Inputs
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `TASKS/TASK-appserverclient-fork-role-command.json`

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Test Gate
- Status: pending
- Owner role: test

### Required Axes
- functional
- flow
- data
- non_functional

### Evidence

### Blocking Issues

## Task Summary
- Status: draft

### Key Updates

### Decisions

### Risks

### Verification

### Next Steps

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
