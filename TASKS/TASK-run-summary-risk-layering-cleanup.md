# TASK: run summary risk layering cleanup

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-summary-risk-layering-cleanup
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
separate operational/mainline risks from audit-history risks in run summary so baseline-facing summaries stay cleaner

## Scope
- `reports/`
- `tools/`
- `docs/`

## Non-goals

## Acceptance
- [x] run summary risk fields are layered or filtered
- [x] baseline_ready_summary excludes audit-only noise
- [x] docs and evidence updated

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
- run summary now separates operational risks from audit-history risks

### Decisions
- baseline-facing compaction should consume `cross_task_risks` only and leave audit-only cleanup risk in `audit_risks`

### Risks
- future normalize rules must keep audit classification narrow so real runtime risk does not get hidden

### Verification
- `python3 -m py_compile tools/evidence.py`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --compact-run-summary`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary`

### Next Steps
- continue tightening run-level prose without mixing audit residue back into baseline-facing summaries

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
