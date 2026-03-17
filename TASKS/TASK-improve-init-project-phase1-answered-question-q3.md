# TASK: improve init-project phase1 answered question q3

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-improve-init-project-phase1-answered-question-q3
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Use stable README and raw-doc evidence from the richer real-material fixture to answer Q3 without broadening phase1 heuristics.

## Scope
- `tools/appserverclient.py`
- `fixtures/init_project_real_material_fixture`
- `reports/run-2026-03-11-vnext-release-baseline`
- `TASKS`

## Non-goals

## Acceptance
- [x] Command(s) pass: `python3 -m py_compile tools/appserverclient.py tools/project_config.py`
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

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
- Added a stable Q3 heuristic using only explicit total-goal and first-phase strategy evidence from the richer real-material fixture.
- Verified that Q3 now appears in first-round `answered_questions` together with Q1/Q2/Q5/Q6/Q11.

### Decisions
- Answer Q3 only when raw docs explicitly cover both long-term system capability and first landing target.

### Risks
- Q3 should remain unclear on projects that only describe vision or only describe first implementation details.

### Verification
- `python3 tools/appserverclient.py --init-project -new` on `fixtures/init_project_real_material_fixture`
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py`
- `python3 tools/project_config.py` after restoring `project_root` to `/root/quant-factory-os`

### Next Steps
- Continue expanding `answered_questions` only where README and raw docs provide equally explicit evidence.

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
