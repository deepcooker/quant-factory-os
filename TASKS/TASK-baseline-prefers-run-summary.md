# TASK: baseline prefers run summary

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-baseline-prefers-run-summary
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
让 refresh-baseline 优先消费 run_summary.json，并仅在缺失时回退 current_summary。

## Scope
- `tools/appserverclient.py`
- `tools/evidence.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`

## Non-goals

## Acceptance
- [x] refresh-baseline loads run summary when available
- [x] refresh-baseline falls back to current_summary only when run summary is unavailable
- [x] docs describe baseline input priority clearly

## Inputs

## Task Summary
- Status: draft

### Key Updates

### Decisions

### Risks

### Verification

### Next Steps

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
