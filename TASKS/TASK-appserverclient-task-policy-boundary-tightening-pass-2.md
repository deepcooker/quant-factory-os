# TASK: appserverclient task-policy boundary tightening pass 2

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-appserverclient-task-policy-boundary-tightening-pass-2
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
继续把 appserverclient 中剩余偏 task policy 的写回做最小下沉，保持 formal mainline 行为不变。

## Scope
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`

## Non-goals
- 不改 role runtime 协议，不引入 agent 配置系统

## Acceptance
- [x] 再减少一处 appserverclient 对 task policy 细节的直接写回，docs/evidence 同步

## Inputs
- `tools/appserverclient.py`
- `tools/taskclient.py`

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
- role summary to task-summary evidence/source-thread linkage now lives in taskclient

### Decisions
- appserverclient no longer writes task_summary evidence/source_threads directly during summarize-role

### Risks
- further task policy additions should keep moving into taskclient to avoid runtime thickening

### Verification
- python3 -m py_compile tools/appserverclient.py tools/taskclient.py
- make evidence RUN_ID=run-2026-03-11-vnext-release-baseline

### Next Steps
- continue auditing appserverclient for remaining direct task aggregate writes

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
- note: boundary tightening pass 2 is internal call-path cleanup only

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
