# TASK: task escalation to run-main rules

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-task-escalation-to-run-main-rules
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
定义 task 层哪些冲突必须升级给 run-main、哪些可在 task 内自行收敛，并补最小机器层落点。

## Scope
- `tools/taskclient.py`
- `TASKS/_SCHEMA.task.json`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `AGENTS.md`

## Non-goals
- 不做 run summary 自动聚合
- 不做多角色调度器

## Acceptance
- [x] task 机器层有 escalation 规则字段或约定
- [x] taskclient 有最小 escalation 刷新入口或写回规则
- [x] docs/evidence updated

## Inputs

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

## Role Summaries
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Task Summary
- Status: completed

### Key Updates
- task 机器层新增 `escalation_policy` 和 `escalation_summary` 字段约定。
- `taskclient` 新增 `--refresh-task-escalation`，用于判断当前 task 是否必须升级给 `run-main`。
- 已用现有真实 task 做 escalation refresh 验证。

### Decisions
- 当前最小必须升级条件是 `run-main summary missing`、`test_gate` 未通过或 `blocking issue` 仍存在。

### Risks

### Verification
- `python3 -m py_compile tools/taskclient.py`
- `python3 tools/taskclient.py --refresh-task-gaps --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
- `python3 tools/taskclient.py --refresh-task-escalation --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
- `python3 tools/taskclient.py --task-summary --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`

### Next Steps
- 继续定义升级给 `run-main` 后，`run-main` 应如何确认、回写和关闭升级项。

### Conflict Policy
- Priority order: run-main, test, arch, dev
- Merge rule: append_dedup
- Escalation rule: if conflict remains, escalate to run-main

### Gap Summary

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
