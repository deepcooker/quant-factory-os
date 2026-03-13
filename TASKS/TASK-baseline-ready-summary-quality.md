# TASK: baseline-ready-summary-quality

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-baseline-ready-summary-quality
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
提升 baseline_ready_summary 的表达质量，减少 task 前缀和机械列表感，让 baseline refresh 吃到更像真正 run-level summary 的压缩表述。

## Scope
- `tools/evidence.py`
- `tools/appserverclient.py`
- `reports/_SCHEMA.run_summary.json`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `reports/run-2026-03-11-vnext-release-baseline/run_summary.json`

## Non-goals
- 不改 baseline thread storage
- 不引入新的 summarizer client

## Acceptance
- [x] baseline_ready_summary expression improved
- [x] run_summary updated
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
- baseline_ready_summary now reads more like run-level prose instead of task-prefixed mechanical lists

### Decisions
- baseline-ready summary quality should be improved inside `evidence.py` by normalizing common task-prefixed phrases before baseline refresh consumes them

### Risks
- quality is still based on deterministic rewrite rules, so wording remains bounded by existing `run_summary` inputs

### Verification
- `python3 -m py_compile tools/evidence.py`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --compact-run-summary`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary`

### Next Steps
- if needed later, add a stricter normalization table for common run-level phrases before baseline refresh

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
