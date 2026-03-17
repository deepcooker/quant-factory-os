# TASK: validate init-project phase1 on fixture

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-validate-init-project-phase1-on-fixture
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
Run the new init-project phase1 against an uninitialized in-repo fixture and verify answered_questions unclear_questions customer_followups quality.

## Scope
- `tools/appserverclient.py`
- `tools/project_config.py`
- `tools/prompts/init_project_prompt.md`
- `docs/WORKFLOW.md`

## Non-goals

## Acceptance
- [ ] Phase1 runs on an uninitialized in-repo fixture and returns the new schema fields
- [ ] Evidence updated for the validation run

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
- Status: draft

### Key Updates

### Decisions

### Risks

### Verification

### Next Steps

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
