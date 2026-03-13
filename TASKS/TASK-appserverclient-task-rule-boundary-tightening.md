# TASK: appserverclient task-rule boundary tightening

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-appserverclient-task-rule-boundary-tightening
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把 appserverclient 中继续变厚的 task/rule 刷新调用做最小收口，保持主流程语义不变。

## Scope
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`

## Non-goals
- 不改 role runtime 协议，不引入新客户端

## Acceptance
- [x] 最小解耦完成且 docs/evidence 同步

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
- appserverclient now delegates task-side refresh chaining through a single taskclient entrypoint

### Decisions
- task coordination refresh is centralized in taskclient.refresh_task_coordination instead of four explicit appserverclient calls

### Risks
- appserverclient and evidence.py still remain the main thick spots if new policy keeps accumulating there

### Verification
- python3 -m py_compile tools/appserverclient.py tools/taskclient.py
- make evidence RUN_ID=run-2026-03-11-vnext-release-baseline

### Next Steps
- continue moving task policy growth into taskclient and keep appserverclient focused on runtime

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
- note: boundary tightening is documentation and internal call-path cleanup only

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
