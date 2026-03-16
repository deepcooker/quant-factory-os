# TASK: run summary stale prose cleanup

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-summary-stale-prose-cleanup
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
clean outdated run_summary risk and next-step prose so run evidence matches current code and runtime truth

## Scope
- `reports/`
- `tools/`
- `docs/`

## Non-goals

## Acceptance
- [x] outdated run_summary prose removed
- [x] baseline_ready_summary updated
- [x] docs or evidence updated if wording contract changed

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
- normalize-run-summary now rewrites stale baseline-consumption prose to match the current run-summary-driven refresh path
- baseline_ready_summary now describes run-level prose alignment as the remaining work instead of reconnecting baseline to run summary

### Decisions
- stale run-summary prose cleanup stays in evidence.py normalization rules instead of ad hoc manual report edits

### Risks
- other historical run-local phrases may still remain until they are explicitly covered by narrow normalization rules

### Verification
- python3 -m py_compile tools/evidence.py
- python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary
- python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --compact-run-summary
- python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary

### Next Steps
- continue tightening run-level prose with narrow deterministic rewrite rules only when stale wording is proven

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
- note: run-summary stale prose cleanup is evidence-only maintenance and did not require run-main escalation

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
