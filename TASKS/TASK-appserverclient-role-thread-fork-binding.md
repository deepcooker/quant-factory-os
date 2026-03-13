# TASK: appserverclient role thread fork binding

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-appserverclient-role-thread-fork-binding
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
让 run-main 基于当前 fork session 派生 dev/test role thread，并回写 task role_threads。

## Scope
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`

## Non-goals
- 不做完整多agent orchestration
- 不自动聚合 thread summary

## Acceptance
- [ ] appserverclient 支持最小 role fork; task role_threads 回写生效; docs/evidence updated

## Inputs
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `tools/project_config.json`
- `docs/WORKFLOW.md`

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
