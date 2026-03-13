# TASK: appserverclient task-policy boundary tightening pass 3

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-appserverclient-task-policy-boundary-tightening-pass-3
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
继续把 appserverclient 中 mark-test-gate 仍在自己拼 test 证据的逻辑下沉到 taskclient，保持 formal mainline 更短更清晰。

## Scope
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`

## Non-goals
- 不改 test gate 语义，不引入新配置层

## Acceptance
- [x] mark-test-gate 的 test 证据拼接下沉到 taskclient，docs/evidence 同步

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
- test gate evidence assembly now lives in taskclient

### Decisions
- appserverclient mark-test-gate no longer reads role_summaries.test directly

### Risks
- remaining runtime-side task policy should keep shrinking toward taskclient helpers

### Verification
- python3 -m py_compile tools/appserverclient.py tools/taskclient.py
- make evidence RUN_ID=run-2026-03-11-vnext-release-baseline

### Next Steps
- continue auditing appserverclient for any remaining direct task policy reads

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
- note: boundary tightening pass 3 is internal call-path cleanup only

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
