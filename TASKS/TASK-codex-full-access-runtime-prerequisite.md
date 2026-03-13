# TASK: codex full access runtime prerequisite

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-codex-full-access-runtime-prerequisite
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
补充 Codex TUI 下做真实 baseline/fork/session runtime 调试时需要 Full Access 的最小运行前提说明。

## Scope
- `docs/`
- `tools/`

## Non-goals

## Acceptance
- [x] workflow and file index mention the prerequisite

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
- documented Codex TUI Full Access as the runtime prerequisite for real session debugging

### Decisions
- treat `/root/.codex/sessions` access failures under Default permissions as outer-session permission issues, not mainline logic failures

### Risks

### Verification
- `python3 tools/appserverclient.py --fork-current` passed after switching Codex TUI permissions to Full Access
- `python3 tools/appserverclient.py --summarize-current` passed under Full Access
- `python3 tools/appserverclient.py --refresh-baseline` passed under Full Access

### Next Steps
- keep this prerequisite as an operational note only and do not change the formal mainline structure

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
- status: not_needed
- close_escalation: false
- note: This is an operational documentation clarification and does not require run-main escalation.

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
