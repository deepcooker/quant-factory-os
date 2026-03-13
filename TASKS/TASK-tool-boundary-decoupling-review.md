# TASK: tool boundary decoupling review

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-tool-boundary-decoupling-review
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
梳理四个主工具的职责边界、当前变厚点和下一轮解耦方向，并把 agent 配置化后置到 todo。

## Scope
- `tools/`
- `docs/`
- `todo.md`

## Non-goals
- 不扩新 runtime 能力

## Acceptance
- [ ] owner docs 明确四工具边界和解耦方向；todo.md 记录 agent 配置化后置

## Inputs
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `tools/evidence.py`
- `tools/gitclient.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `todo.md`

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
- formal tool boundaries and current thick spots are now documented

### Decisions
- agent role configuration is deferred until tool boundaries stabilize

### Risks
- appserverclient and evidence.py remain the current thick spots if new logic keeps accumulating there

### Verification
- python3 -m py_compile tools/appserverclient.py tools/taskclient.py tools/evidence.py tools/gitclient.py
- make evidence RUN_ID=run-2026-03-11-vnext-release-baseline

### Next Steps
- keep new runtime logic out of gitclient and prefer taskclient/evidence boundary-first growth

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
- note: documentation-only boundary review; no run-main escalation needed

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
