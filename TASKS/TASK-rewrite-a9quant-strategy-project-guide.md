# TASK: Rewrite a9quant strategy project guide

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-rewrite-a9quant-strategy-project-guide
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
Regenerate /root/a9quant-strategy/docs/PROJECT_GUIDE.md from the foundation PROJECT_GUIDE curriculum structure instead of summary prose

## Scope
- `learn/a9quant-strategy_phase2_draft.json and /root/a9quant-strategy/docs/PROJECT_GUIDE.md`

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
- Rewrote /root/a9quant-strategy/docs/PROJECT_GUIDE.md as a curriculum-style guide instead of a summary page.

### Decisions
- For project guides
- inherit the foundation curriculum structure and projectize the answers; do not summarize the repository into a short overview.

### Risks
- The rewritten guide still needs your qualitative review
- but it now follows the intended course structure.

### Verification

### Next Steps
- Review the corrected PROJECT_GUIDE.md in /root/a9quant-strategy and decide whether the same standard should tighten other generated docs.

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
