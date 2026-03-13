# TASK: task role summary merge rules

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-task-role-summary-merge-rules
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
为多角色 role summaries 并存时的 task-level 去重与聚合补最小规则和写回入口。

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
- [x] task 机器层有 role summary merge 字段或约定
- [x] taskclient 有最小 merge 入口
- [x] 已有 role_summaries 可聚合进 task_summary
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
- `taskclient` 新增 `--merge-role-summaries`，用于按最小规则把 role summaries 汇入 task summary。
- 当前聚合规则会去重追加 `source_threads`、`role_summary_evidence` 和 `<role> summary merged` 标记。
- 已用现有 `test` role summary 做真实聚合验证。

### Decisions
- 当前只做最小去重聚合，不做复杂语义 merge 或 run-level 自动汇总。

### Risks

### Verification
- `python3 -m py_compile tools/taskclient.py`
- `python3 tools/taskclient.py --merge-role-summaries --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`
- `python3 tools/taskclient.py --task-summary --task-json-file TASKS/TASK-role-thread-summary-to-task-summary.json`

### Next Steps
- 继续定义多角色 summary 冲突时的优先级与缺口汇总规则。

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
