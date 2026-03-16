# TASK: sync view tool usage docs

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-sync-view-tool-usage-docs
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P2

## Goal
将 view.sh 的正式使用说明最小同步到主线文档，反映当前支持的调用方式和阅读协议。

## Scope
- `docs/WORKFLOW.md`
- `docs/PROJECT_GUIDE.md`
- `README.md`

## Non-goals

## Acceptance
- [x] WORKFLOW/PROJECT_GUIDE/README 同步 view.sh 当前用法
- [x] 不改题库结构
- [x] evidence 更新

## Inputs

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Test Gate
- Status: not_needed
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
- `docs/WORKFLOW.md` 和 `docs/PROJECT_GUIDE.md` 已明确写入 `tools/view.sh` 的正式调用方式。
- `README.md` 已补上最小的 `tools/view.sh` 使用示例。

### Decisions
- 保持最小同步，不改 `PROJECT_GUIDE` 题库结构。
- 同时写清直接执行与 `python3` 调用，避免历史调用方式继续模糊。

### Risks

### Verification
- `python3 tools/view.sh docs/PROJECT_GUIDE.md --from 1 --to 12`
- `python3 tools/view.sh docs/WORKFLOW.md --from 1 --to 18`
- `python3 tools/view.sh README.md --from 1 --to 20`

### Next Steps

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
- status: not_needed
- close_escalation: true

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
