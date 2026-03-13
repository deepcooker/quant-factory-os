# TASK: run-summary-aggregation-reconciliation

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-summary-aggregation-reconciliation
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
收紧 run_summary 的任务聚合语义，优先基于 task JSON 的真实状态维护 active/completed/source task 列表，减少陈旧条目和手工漂移。

## Scope
- `tools/evidence.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `AGENTS.md`
- `reports/_SCHEMA.run_summary.json`

## Non-goals
- 不改 baseline refresh 入口
- 不做通用 orchestrator

## Acceptance
- [x] run_summary active/completed/source task reconciliation available
- [x] docs and evidence updated

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
- tools/evidence.py now supports run-summary reconciliation from task JSON truth

### Decisions
- run summary active/completed/source task lists should be reconciled from same-run task JSON payloads instead of hand-maintained leftovers

### Risks
- reconciliation now exposes historical active task truth; stale task cleanup still requires separate task-level cleanup

### Verification
- python3 -m py_compile tools/evidence.py
- python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --reconcile-run-summary
- python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary

### Next Steps
- clean stale active task truth so run_summary reconciliation can converge with less historical noise

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
