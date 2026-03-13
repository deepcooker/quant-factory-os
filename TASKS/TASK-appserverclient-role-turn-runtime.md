# TASK: appserverclient role turn runtime

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-appserverclient-role-turn-runtime
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
新增 appserverclient --role-turn，让已绑定的 role thread 执行真实 turn。

## Scope
- `tools/appserverclient.py`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `AGENTS.md`

## Non-goals
- 不做 thread summary 自动回收
- 不做多角色调度器

## Acceptance
- [x] 新增 --role-turn 命令; 已绑定 role thread 可执行真实 turn; docs/evidence updated

## Inputs
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `TASKS/TASK-appserverclient-fork-role-command.json`

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=ready, thread_id=019ce64a-8ad1-7733-a6e0-f8b0c15d22f2
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
- `tools/appserverclient.py` 新增 `--role-turn`，可在已绑定 role thread 上执行真实 turn。
- 当前 task 已成功 fork 并绑定 `test` role thread `019ce64a-8ad1-7733-a6e0-f8b0c15d22f2`。
- 真实 role-turn 已执行成功，并返回 test 线程职责说明。

### Decisions
- role thread 执行面先通过 `appserverclient --role-turn` 打通，不在本轮引入 thread summary 自动回收。

### Risks

### Verification
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py`
- `python3 tools/appserverclient.py --fork-role test`
- `python3 tools/taskclient.py --role-threads`
- `python3 tools/appserverclient.py --role-turn test "请用一句话说明你当前作为 test 线程的职责。"`

### Next Steps
- 继续补 role thread 的 thread summary 产出与回收到 task summary。

### Source Threads
- `test:019ce64a-8ad1-7733-a6e0-f8b0c15d22f2`

## Risks / Rollback
- Risks: 
- Rollback plan:
