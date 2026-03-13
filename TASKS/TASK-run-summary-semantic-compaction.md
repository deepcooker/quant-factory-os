# TASK: run-summary-semantic-compaction

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-summary-semantic-compaction
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
收紧 run_summary 的语义压缩质量，减少 baseline refresh 直接消费时的宽表噪音，优先把 task/risk/next-step 聚合成更稳定的 run-level表达。

## Scope
- `tools/evidence.py`
- `reports/_SCHEMA.run_summary.json`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `reports/run-2026-03-11-vnext-release-baseline/run_summary.json`

## Non-goals
- 不改 baseline thread 存储
- 不做新的 run client

## Acceptance
- [x] run_summary semantic compaction available
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
- run_summary.json now carries `baseline_ready_summary` for shorter baseline refresh input

### Decisions
- baseline refresh should prefer the compact `baseline_ready_summary` block over expanding the full run_summary width

### Risks
- semantic compaction is still rule-based and capped by fixed list limits, not model-generated summarization inside `evidence.py`

### Verification
- `python3 -m py_compile tools/evidence.py tools/appserverclient.py`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --compact-run-summary`
- `python3 tools/appserverclient.py --refresh-baseline`

### Next Steps
- tighten compaction rules or promote selected task summaries into cleaner run-level wording before future baseline refreshes

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
