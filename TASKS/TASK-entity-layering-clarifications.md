# TASK: entity layering clarifications

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-entity-layering-clarifications
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把 thread/task/run/baseline 四层职责与数据流以最小方式写入 owner docs。

## Scope
- `docs/ENTITIES.md`
- `docs/WORKFLOW.md`

## Non-goals

## Acceptance
- [x] entities defines thread-task-run-baseline layering
- [x] workflow describes current_summary as thread-level transitional summary
- [x] workflow states baseline should eventually prefer run-level summaries

## Inputs

## Risks / Rollback
- Risks: 
- Rollback plan:
