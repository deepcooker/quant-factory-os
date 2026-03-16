# TASK: cleanup tool surface and prompt assets

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-cleanup-tool-surface-and-prompt-assets
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
move requirement guide to chatlogs, collect prompt files, archive obsolete shell entrypoints, and move TOOLS_METHOD_FLOW_MAP into docs.

## Scope
- `tools/`
- `docs/`
- `chatlogs/`

## Non-goals

## Acceptance
- [x] target files moved
- [x] docs and indexes updated
- [x] runtime pointers updated

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
- prompt templates now live under `tools/prompts`
- the requirement-analysis guide now lives under `chatlogs`
- `TOOLS_METHOD_FLOW_MAP` now lives under `docs` and obsolete top-level `start/onboard` shell entrypoints were archived

### Decisions
- formal tool references should follow the new `docs/tools/prompts/chatlogs` locations without rewriting historical evidence in bulk

### Risks
- historical task artifacts and logs still preserve old prompt and flow-map paths as audit residue

### Verification
- `python3 -m py_compile tools/project_config.py tools/appserverclient.py`
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline`

### Next Steps
- continue cleanup by reducing stale historical references only when they affect active automation or owner docs

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
