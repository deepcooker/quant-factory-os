# TASK: bootstrap and sync hardening

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-bootstrap-and-sync-hardening
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
harden external-project bootstrap order, sync tooling, and plan timeout defaults

## Scope
- `tools/project_config.py`
- `tools/init.py`
- `tools/sync_tools.py`
- `docs/PROJECT_BOOTSTRAP_PROTOCOL.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`

## Non-goals

## Acceptance
- [ ] Command(s) pass: make verify
- [ ] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

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
- raised plan timeout to 1 hour
- added sync_tools.py as fixed-list sync entry
- added FOUNDATION_BRIDGE.md to init skeleton and sync list

### Decisions
- target-project bootstrap order is now sync_tools first
- then target-project init
- docs/FOUNDATION_BRIDGE.md is treated as a fixed reusable template

### Risks

### Verification
- python3 -m py_compile tools/appserverclient.py tools/project_config.py tools/init.py tools/sync_tools.py
- python3 tools/sync_tools.py -p /root/a9quant-strategy
- python3 -m py_compile /root/a9quant-strategy/tools/appserverclient.py /root/a9quant-strategy/tools/project_config.py /root/a9quant-strategy/tools/init.py /root/a9quant-strategy/tools/sync_tools.py

### Next Steps
- next session can focus on larger automation work with clean bootstrap/sync baseline

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
