# TASK: run-summary-merge-quality

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-summary-merge-quality
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Improve run-level semantic merge quality so merge_rewrite fields produce more stable run-level expressions instead of lightly humanized task fragments.

## Scope
- `tools/evidence.py`
- `reports/_SCHEMA.run_summary.json`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `reports/run-2026-03-11-vnext-release-baseline/run_summary.json`

## Non-goals
- Do not introduce model-based rewriting or change baseline refresh boundaries.

## Acceptance
- [x] merge_rewrite produces more stable run-level phrasing for common task summary patterns and the rule is documented.

## Inputs
- `tools/evidence.py`
- `reports/run-2026-03-11-vnext-release-baseline/run_summary.json`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`

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
- merge_rewrite now canonicalizes common multi-role and test-gate patterns into steadier run-level phrasing

### Decisions
- high-frequency semantic cleanup should happen in the merge_rewrite path before baseline compaction, not only in the final display layer

### Risks
- canonicalization is intentionally narrow and still leaves uncommon task-local phrasings untouched

### Verification
- python3 -m py_compile tools/evidence.py
- python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary

### Next Steps
- expand canonical merge rules only when a repeated run-level pattern appears often enough to justify a stable rule

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
