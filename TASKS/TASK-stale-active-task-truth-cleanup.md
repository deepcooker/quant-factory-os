# TASK: stale-active-task-truth-cleanup

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-stale-active-task-truth-cleanup
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
清理 run-2026-03-11-vnext-release-baseline 下历史遗留的 active task 真相源，使 task JSON 状态与当前主线完成态一致，减少 run_summary reconciliation 噪音。

## Scope
- `TASKS/`
- `tools/project_config.json`
- `reports/run-2026-03-11-vnext-release-baseline/run_summary.json`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`

## Non-goals
- 不改 appserver runtime
- 不改 baseline refresh

## Acceptance
- [x] stale active task truth cleaned
- [x] run_summary reconciled
- [x] evidence updated

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
- cleaned six stale active task records that were either superseded placeholders or sample verification tasks

### Decisions
- run summary reconciliation should expose stale active truth first, then cleanup should happen at task JSON source rather than being hidden in `run_summary`

### Risks
- other historical tasks may still need deeper semantic cleanup beyond simple status correction

### Verification
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --reconcile-run-summary`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary`

### Next Steps
- use reconciled run summary to identify any remaining historical task cleanup work

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
