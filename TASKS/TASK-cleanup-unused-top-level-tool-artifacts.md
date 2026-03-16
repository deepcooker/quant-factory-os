# TASK: cleanup unused top-level tool artifacts

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-cleanup-unused-top-level-tool-artifacts
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
remove clearly unused top-level tool artifacts and identify remaining non-mainline files in tools/.

## Scope
- `tools/`
- `docs/`

## Non-goals

## Acceptance
- [x] unused files removed or archived
- [x] owner docs updated if formal surface changed
- [x] verification passed

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
- removed unused `tools/console.txt` from the top-level tool surface
- archived top-level `taskstore.py` and `sync_exam.py` into `tools/backup`

### Decisions
- `slice.py` stays because it is still the implementation behind `make slice`

### Risks
- historical tasks and backup scripts still preserve references to old `taskstore` and `sync_exam` paths

### Verification
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py`
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline`

### Next Steps
- continue reducing top-level tool noise without touching files still used by Makefile or formal mainline

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
