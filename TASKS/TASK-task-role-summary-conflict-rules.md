# TASK: task role summary conflict rules

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-task-role-summary-conflict-rules
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
定义 task 层多角色 role summaries 冲突时的优先级和缺口汇总规则，并补最小机器层落点。

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
- [x] task 机器层有多角色 summary 冲突规则字段或约定
- [x] taskclient 有最小缺口汇总入口或写回规则
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
- task 机器层新增 `conflict_policy` 和 `gap_summary` 字段约定。
- `taskclient` 新增 `--refresh-task-gaps`，用于基于 `role_summaries` 和 `test_gate` 刷新 task-level 缺口。
- 已用现有 `test` role summary task 做真实 gap refresh 验证。

### Decisions
- 当前 task 层默认优先级顺序为 `run-main -> test -> arch -> dev`。

### Risks

### Verification
- `python3 -m py_compile tools/taskclient.py`
- `python3 tools/taskclient.py --refresh-task-gaps --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
- `python3 tools/taskclient.py --task-summary --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`

### Next Steps
- 继续定义多角色 summary 冲突时哪些内容必须升级给 `run-main` 决策。

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
