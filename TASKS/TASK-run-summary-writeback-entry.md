# TASK: run summary writeback entry

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-summary-writeback-entry
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
为 run_summary.json 增加最小读写入口，不改 baseline 消费链。

## Scope
- `tools/evidence.py`
- `reports/_SCHEMA.run_summary.json`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `docs/ENTITIES.md`

## Non-goals

## Acceptance
- [x] evidence.py can print run summary
- [x] evidence.py can update run summary fields
- [x] docs describe evidence.py as run summary writeback entry

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
