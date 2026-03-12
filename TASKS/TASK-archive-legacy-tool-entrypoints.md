# TASK: archive legacy tool entrypoints

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-archive-legacy-tool-entrypoints
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把已经退出主流程的旧 Python 和 shell 入口归档到 tools/backup，只保留当前正式主流程入口。

## Scope
- `tools/`
- `docs/`

## Non-goals

## Acceptance
- [x] listed legacy entrypoints moved to tools/backup
- [x] owner docs reflect Python mainline whitelist

## Inputs

## Risks / Rollback
- Risks: 
- Rollback plan:
