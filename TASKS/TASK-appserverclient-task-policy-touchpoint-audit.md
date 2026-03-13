# TASK: appserverclient task-policy touchpoint audit

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-appserverclient-task-policy-touchpoint-audit
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
审计 appserverclient 中剩余直接触碰 task policy 的点，并判断是否还有必要继续做第四刀最小解耦。

## Scope
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`

## Non-goals
- 不直接扩实现，除非发现非常明显的一刀式解耦点

## Acceptance
- [x] 列出剩余 touchpoints，并给出是否继续第四刀的结论；若只需文档收尾则同步 evidence

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
- remaining appserverclient touchpoints are now mostly runtime-necessary rather than task-policy-heavy

### Decisions
- no fourth decoupling pass is justified right now; further cuts would likely reduce clarity more than they reduce coupling

### Risks
- over-decoupling the remaining runtime-required touchpoints would make the flow longer and harder to debug

### Verification
- grep -nE "load_active_task|get_role_threads|update_role_thread|update_role_summary_with_task_links|update_test_gate_from_test_summary|refresh_task_coordination" tools/appserverclient.py
- tools/view.sh tools/appserverclient.py --from 836 --to 1001

### Next Steps
- pause decoupling here and keep future cuts limited to obvious task-policy leakage

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
- note: touchpoint audit only; no run-main escalation needed

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
