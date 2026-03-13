# TASK: appserverclient fork role command

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-appserverclient-fork-role-command
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
新增 appserverclient --fork-role，让当前 run-main fork 出 dev/test role thread 并回写 task role_threads。

## Scope
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `docs/ENTITIES.md`

## Non-goals
- 不做 thread summary 自动聚合
- 不做完整多agent orchestration

## Acceptance
- [x] 新增 --fork-role 命令; dev/test role thread 可真实 fork 并回写当前 task; docs/evidence updated

## Inputs
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `tools/project_config.json`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=ready, thread_id=019ce643-7e04-7d61-a980-bec20518d20b
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
- Status: completed

### Key Updates
- `appserverclient` 新增 `--fork-role`，可基于当前 run-main thread 派生真实 role thread 并回写 task `role_threads`。
- 已真实 fork 出 `test` role thread 并写回当前 task。

### Decisions
- 当前先把真实 role thread binding 收在 `appserverclient + taskclient`，不在这一刀里引入 thread summary 自动聚合。

### Risks
- run-main/dev/test 的完整生命周期、thread summary 产出和自动聚合仍未打通。

### Verification
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py`
- `python3 tools/appserverclient.py --fork-role test`
- `python3 tools/taskclient.py --role-threads`

### Next Steps
- 继续让 role thread 支持真实 `current-turn` 和后续 thread summary 回收。

### Source Threads
- `test`

## Risks / Rollback
- Risks: 
- Rollback plan:
