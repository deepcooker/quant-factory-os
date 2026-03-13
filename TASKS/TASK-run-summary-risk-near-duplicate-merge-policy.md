# TASK: run summary risk near-duplicate merge policy

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-summary-risk-near-duplicate-merge-policy
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
收紧 run_summary.cross_task_risks 的近义风险句合并规则，区分应保留的并列证据和应归并的 run-level 风险表达。

## Scope
- `tools/evidence.py`
- `reports/_SCHEMA.run_summary.json`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `AGENTS.md`

## Non-goals
- 不扩 run 层以外的对象，不引入模型改写，不修改 verification_overview 证据粒度

## Acceptance
- [x] cross_task_risks 近义 blocked-gate 风险不再重复堆叠；保留证据粒度字段不变；文档与 evidence 同步

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
- cross_task_risks now keeps the more specific blocked-gate risk line instead of stacking a generic duplicate

### Decisions
- near-duplicate blocked-gate risk lines should merge at run level while evidence remains in `verification_overview`

### Risks
- the current rule only handles blocked-gate near-duplicates and does not yet normalize broader risk synonym families

### Verification
- `python3 -m py_compile tools/evidence.py`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --normalize-run-summary`
- `python3 tools/evidence.py --run-id run-2026-03-11-vnext-release-baseline --run-summary`
- `make evidence RUN_ID=run-2026-03-11-vnext-release-baseline`

### Next Steps
- define which other risk synonym families deserve run-level merge rules beyond blocked-gate cases

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

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
