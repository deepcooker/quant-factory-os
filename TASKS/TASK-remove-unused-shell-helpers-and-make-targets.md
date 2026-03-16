# TASK: remove unused shell helpers and make targets

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-remove-unused-shell-helpers-and-make-targets
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
delete Makefile, smoke.sh, enter.sh, and doctor.sh if they are no longer part of the formal mainline.

## Scope
- `Makefile`
- `tools/`
- `docs/`
- `AGENTS.md`

## Non-goals

## Acceptance
- [x] unused shell helpers removed
- [x] formal docs updated
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
- archived top-level `doctor.sh`, `enter.sh`, and `smoke.sh`
- removed broken legacy targets from `Makefile` while keeping `make evidence`, `make verify`, and `make slice`

### Decisions
- `Makefile` stays because `make evidence`, `make verify`, and `make slice` are still formal entrypoints

### Risks
- historical docs and task artifacts still preserve old shell helper references as audit residue

### Verification
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py`
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline`
- `make verify`

### Next Steps
- continue code-level减负 instead of deleting more files that still support formal targets

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
