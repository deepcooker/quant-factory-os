# TASK: shortest stable mainline documentation

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-shortest-stable-mainline-documentation
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把当前最短稳定主线、四个主工具边界和不应再继续拆的原则写成非常清晰的操作面。

## Scope
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `AGENTS.md`

## Non-goals
- 不改任何 runtime 行为，不新增命令

## Acceptance
- [x] owner docs 明确最短稳定主线和当前冻结边界

## Inputs
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`

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
- shortest stable mainline is now written explicitly in WORKFLOW and FILE_INDEX

### Decisions
- pause further splitting and keep the current operator path as the recommended stable path

### Risks
- adding more optional middle steps would increase flow length and reduce debug clarity

### Verification
- python3 -m py_compile tools/appserverclient.py tools/taskclient.py tools/evidence.py tools/gitclient.py
- make evidence RUN_ID=run-2026-03-11-vnext-release-baseline

### Next Steps
- treat this shortest path as the default until a new capability proves it needs another formal step

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
- close_escalation: true
- note: documentation-only shortest-path clarification

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
