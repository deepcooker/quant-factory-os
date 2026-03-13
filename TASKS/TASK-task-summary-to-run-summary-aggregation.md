# TASK: task-summary-to-run-summary-aggregation

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-task-summary-to-run-summary-aggregation
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把当前已验证的 integrated multi-role task summary 提升为 run-level 可复用的最小聚合输入，并建立稳定的 run summary 写回路径。

## Scope
- `tools/evidence.py`
- `tools/taskclient.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `AGENTS.md`
- `reports/_SCHEMA.run_summary.json`

## Non-goals
- 不改 baseline refresh 消费优先级
- 不做通用 orchestrator

## Acceptance
- [x] 可从 task summary 提取最小 run-level aggregation
- [x] run_summary 保留 source_tasks 和关键更新
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
- task summary can now be promoted into run summary through tools/evidence.py

### Decisions
- run summary aggregation stays inside tools/evidence.py instead of adding a separate run client

### Risks
- run-level aggregation is still minimal append-only promotion, not semantic dedupe across many tasks

### Verification
- `python3 -m py_compile tools/evidence.py`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --merge-task-summary --task-json-file TASKS/TASK-integrated-multi-role-runtime-chain.json`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary`

### Next Steps
- use this run-level aggregation path as the input for later baseline and higher-level coordination improvements

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
