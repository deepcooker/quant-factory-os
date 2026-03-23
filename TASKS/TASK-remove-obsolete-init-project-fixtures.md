# TASK: remove obsolete init-project fixtures

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-remove-obsolete-init-project-fixtures
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
delete legacy init-project fixture directories that are no longer part of the formal mainline

## Scope
- `fixtures`
- `reports/run-2026-03-11-vnext-release-baseline/summary.md`
- `reports/run-2026-03-11-vnext-release-baseline/decision.md`
- `tools/project_config.json`
- `TASKS/QUEUE.json`

## Non-goals

## Acceptance
- [ ] Command(s) pass: make verify
- [ ] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

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
- 已删除旧的 fixtures/ 目录，包括 init_project_fixture 与 init_project_real_material_fixture 两套遗留夹具。
- 已确认当前正式主线和活代码不再依赖 fixtures/；残留引用只出现在历史 evidence 和 project_all_files.txt 中。

### Decisions
- fixtures/ 属于旧的 init-project 测试资产，不再保留在当前主线仓库中。

### Risks

### Verification
- find . -maxdepth 2 -type d -name fixtures -o -path ./fixtures/* 无输出。
- git status 已显示 fixtures/* 为删除状态。

### Next Steps
- 后续如需保留夹具，应迁到独立测试仓或重新以正式测试策略引入，而不是长期留在主线仓。

### Conflict Policy
- Priority order: run-main, test, arch, dev
- Merge rule: append_dedup
- Escalation rule: if conflict remains, escalate to run-main

### Gap Summary

### Escalation Policy
- must_escalate_if: run-main summary missing
- must_escalate_if: test_gate not passed
- must_escalate_if: blocking issue remains
- can_resolve_in_task_if: only dev/arch detail alignment
- can_resolve_in_task_if: no blocking issue
- can_resolve_in_task_if: test gate already passed

### Escalation Summary
- needs_run_main: false

### Run-Main Resolution Policy
- must_confirm_if: escalation_summary.needs_run_main
- can_close_if: run-main summary exists
- can_close_if: test_gate passed
- can_close_if: no blocking issue remains

### Run-Main Resolution
- status: pending_ack
- close_escalation: false

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
