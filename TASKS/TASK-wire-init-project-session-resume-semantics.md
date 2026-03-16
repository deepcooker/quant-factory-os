# TASK: Wire init-project session resume semantics

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-wire-init-project-session-resume-semantics
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Connect init-project phase-1 intake to session_registry.init_project_session so --init-project resumes by default and --init-project -new resets the slot explicitly.

## Scope
- `Implement minimal session-slot lifecycle and writeback for init-project without attempting full owner-doc reverse-writing or full app-server init-thread execution.`

## Non-goals

## Acceptance
- [x] Command(s) pass: `python3 -m py_compile tools/project_config.py tools/appserverclient.py`
- [x] `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md` updated

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
- `init_project_session` now gets written back during phase-1 intake.
- Default `--init-project` resumes the same local phase-1 session; `--init-project -new` creates a new session id.

### Decisions
- Keep session semantics local for now instead of pretending phase-1 already owns a real app-server thread.
- Make init-project owner-doc checks and intake scanning depend on the current `project_root`.

### Risks
- `init_project_session` is still local phase-1 state, not a real app-server thread.
- Phase-2 reverse-writing and real app-server continuation remain pending.

### Verification
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py`
- Local resume/new smoke test on a temporary demo project root

### Next Steps
- Decide whether `init_project_session` should become a real app-server thread before phase-2 owner-doc writing.

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
