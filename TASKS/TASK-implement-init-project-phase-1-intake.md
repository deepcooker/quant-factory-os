# TASK: Implement init-project phase-1 intake

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-implement-init-project-phase-1-intake
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Implement minimal runtime support for init-project phase 1: collect README/raw docs inputs, generate light_repo_findings, and expose must-read planning inputs without owner-doc writing.

## Scope
- `Extend appserverclient init-project flow with lightweight repo scanning and raw material discovery while preserving current gates and session model.`

## Non-goals

## Acceptance
- [x] Command(s) pass: `python3 -m py_compile tools/appserverclient.py tools/project_config.py`
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
- `appserverclient --init-project` now produces a real phase-1 intake payload.
- Phase-1 intake now includes `light_repo_findings`, explicit file matching, and `must_read_next`.

### Decisions
- Keep this implementation at phase-1 gating only; do not fake an app-server init thread or owner-doc reverse-writing yet.
- Use hard file-system matching instead of NLP guessing for first-pass file discovery.

### Risks
- `init_project_session` still has no live app-server thread behind it.
- Multi-round continuation and phase-2 reverse-writing remain unimplemented.

### Verification
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py`
- Phase-1 payload smoke test on a temporary demo project root under the repository

### Next Steps
- Resume the design from `init_project_session` continuation before phase-2 owner-doc writing.

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
