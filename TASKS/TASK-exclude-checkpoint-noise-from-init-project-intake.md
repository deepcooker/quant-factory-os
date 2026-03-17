# TASK: Exclude checkpoint noise from init-project intake

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-exclude-checkpoint-noise-from-init-project-intake
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Exclude docs/.ipynb_checkpoints and similar checkpoint artifacts from init-project raw docs discovery so phase-1 intake stays aligned with real source materials.

## Scope
- `Touch only init-project intake discovery and the corresponding docs/evidence wording; do not change phase-2 or app-server thread behavior.`

## Non-goals

## Acceptance
- [x] init-project phase-1 no longer includes docs/.ipynb_checkpoints files in raw_docs_read or docs_files

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
- init-project docs discovery now excludes `.ipynb_checkpoints` and similar checkpoint directories
- rerunning Phase 1 on `/root/a9quant-strategy` now returns only the five real source docs under `docs/`

### Decisions
- Phase-1 intake should scan only real source materials under `docs/`, not notebook checkpoint artifacts

### Risks

### Verification
- `python3 tools/appserverclient.py --init-project` against `/root/a9quant-strategy` no longer includes checkpoint files in `raw_docs_read` or `docs_files`

### Next Steps
- Review the cleaned `must_read_next` set and decide whether to begin second-round code reads for the target project

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
