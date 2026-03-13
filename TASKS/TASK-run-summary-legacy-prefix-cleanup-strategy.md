# TASK: run-summary-legacy-prefix-cleanup-strategy

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-summary-legacy-prefix-cleanup-strategy
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Define and implement a minimal gradual cleanup strategy for historical task-prefixed items already stored in run_summary semantic fields.

## Scope
- `tools/evidence.py`
- `reports/_SCHEMA.run_summary.json`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `AGENTS.md`

## Non-goals
- Do not introduce model-based rewriting or destructive bulk history rewrites.

## Acceptance
- [x] A documented gradual cleanup policy exists and evidence.py can normalize legacy task-prefixed semantic items during an explicit maintenance action.

## Inputs
- `tools/evidence.py`
- `reports/_SCHEMA.run_summary.json`
- `reports/run-2026-03-11-vnext-release-baseline/run_summary.json`

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
- run_summary now supports explicit maintenance-only cleanup for legacy task-prefixed semantic items

### Decisions
- historical semantic cleanup should only run through an explicit evidence command, not during normal merge or reconcile

### Risks
- existing verification_overview entries intentionally keep task-prefixed evidence granularity

### Verification
- python3 -m py_compile tools/evidence.py
- python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary

### Next Steps
- apply normalize-run-summary selectively when a run summary still carries legacy semantic prefixes

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
