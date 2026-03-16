# TASK: Formalize init-project phase protocol

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-formalize-init-project-phase-protocol
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Define the formal two-phase init-project protocol: phase 1 JSON planning/gating and phase 2 markdown owner-doc writing.

## Scope
- `Update prompt and owner docs to define init-project input rules`
- `phase outputs`
- `and session/state behavior without implementing reverse-writing yet.`

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
- `--init-project` phase protocol is now formalized across prompt and owner docs.
- Phase 1 is fixed as JSON-first gating; phase 2 is fixed as Markdown-first owner-doc writing.

### Decisions
- Default `--init-project` must resume `session_registry.init_project_session`; only `--init-project -new` may recreate it.
- Default intake now starts from `README.md` and raw `docs/**/*.md|txt|doc|docx`, excluding owner docs target files.

### Risks
- Reverse-writing runtime is still not implemented; only gate/session/prompt/doc protocol is defined.
- Phase outputs are documented but not yet enforced by execution code.

### Verification
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py`

### Next Steps
- Implement the runtime flow that executes phase 1 against `init_project_session` before any owner-doc writing.

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
