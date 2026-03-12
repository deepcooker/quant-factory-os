# TASK: appserverclient summarize refresh baseline loop

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-appserverclient-summarize-refresh-baseline-loop
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
补齐 appserverclient 的 summarize-current 和 refresh-baseline 最小闭环。

## Scope
- `tools/appserverclient.py`
- `tools/project_config.py`
- `tools/project_config.json`
- `tools/summarize_current_prompt.md`
- `tools/refresh_baseline_prompt.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`

## Non-goals

## Acceptance
- [x] appserverclient supports --summarize-current
- [x] appserverclient supports --refresh-baseline
- [x] project config writes current summary pointers
- [x] docs updated for mainline

## Inputs

## Risks / Rollback
- Risks: 
- Rollback plan:
