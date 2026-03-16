# TASK: compatibility shell archive

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-compat-shell-archive
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把已被正式主线淘汰的 shell 兼容脚本归档到 tools/backup/，并在原路径保留最小兼容壳层，避免当前仓库引用立即断裂。

## Scope
- `tools/backup/`
- `tools/legacy.sh`
- `tools/task.sh`
- `tools/observe.sh`
- `tools/ship.sh`
- `tools/project_config.json`
- `docs/`
- `AGENTS.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写这些兼容脚本的内部逻辑。
- 不在本任务里删除所有历史引用。
- 不扩 appserverclient 或 gitclient 新能力。

## Acceptance
- [x] tools/backup/ 收纳 legacy.sh / task.sh / observe.sh / ship.sh
- [x] 原路径只保留兼容壳层并可转发到 tools/backup/
- [x] formal mainline 文档说明这些 shell 脚本已降级为归档兼容资产
- [x] bash tools/legacy.sh --help || true
- [x] python3 tools/project_config.py
- [x] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

## Inputs
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `docs/PROJECT_GUIDE.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `tools/project_config.json`
- `reports/run-2026-03-11-vnext-release-baseline/summary.md`
- `reports/run-2026-03-11-vnext-release-baseline/decision.md`

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=planned, thread_id=(none)

## Test Gate
- Status: pending
- Owner role: test

### Required Axes

### Evidence

### Blocking Issues

## Role Summaries
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=planned, thread_id=(none)

## Task Summary
- Status: draft

### Key Updates

### Decisions

### Risks

### Verification

### Next Steps

### Conflict Policy
- Priority order: 
- Merge rule: 
- Escalation rule: 

### Gap Summary

### Escalation Policy

### Escalation Summary
- needs_run_main: false

### Run-Main Resolution Policy

### Run-Main Resolution
- status: pending_ack
- close_escalation: false

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
