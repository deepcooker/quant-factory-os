# TASK: task-to-run-summary-merge-rules

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-task-to-run-summary-merge-rules
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Define and document explicit task-summary to run-summary merge rules for key_updates, cross_task_decisions, cross_task_risks, and next_run_or_next_tasks.

## Scope
- `tools/evidence.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `AGENTS.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `reports/_SCHEMA.run_summary.json`

## Non-goals
- Do not implement model-based rewriting or change baseline refresh behavior.

## Acceptance
- [x] Explicit merge rule table exists in docs and machine-layer hooks reflect the rule categories.

## Inputs
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `reports/_SCHEMA.run_summary.json`
- `tools/evidence.py`

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
- merge rule table now distinguishes append_dedup and merge_rewrite paths

### Decisions
- run-level semantic fields should not keep task prefixes by default

### Risks
- legacy run summaries still contain historical task-prefixed items until re-merged

### Verification
- python3 -m py_compile tools/evidence.py

### Next Steps
- re-run task-to-run aggregation on future tasks with merge_policy enabled

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
