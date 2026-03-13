# TASK: run-summary-baseline-refresh-automation-boundary

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-summary-baseline-refresh-automation-boundary
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
明确并最小实现 run_summary 到 baseline refresh 的自动化边界，优先让 refresh-baseline 稳定消费 run-level machine truth，并减少 thread-level fallback 的隐性漂移。

## Scope
- `tools/appserverclient.py`
- `tools/refresh_baseline_prompt.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `reports/run-2026-03-11-vnext-release-baseline/run_summary.json`

## Non-goals
- 不改 baseline thread 存储介质
- 不做通用 orchestrator

## Acceptance
- [x] refresh-baseline automation boundary clarified and minimally implemented
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
- refresh-baseline now records whether baseline refresh consumed `run_summary` or `current_summary`

### Decisions
- baseline refresh input selection should be explicit and traceable instead of remaining an implicit prompt-level fallback

### Risks
- run_summary semantics are still append-oriented, so baseline may absorb noisy run-level breadth until later summary compaction improves

### Verification
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py`
- `python3 tools/appserverclient.py --refresh-baseline`

### Next Steps
- tighten `run_summary` semantic compaction before further increasing baseline automation depth

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
