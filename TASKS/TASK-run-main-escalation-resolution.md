# TASK: run-main escalation resolution

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-main-escalation-resolution
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
补 run-main 收到 task 升级后的确认、回写和关闭链。

## Scope
- `tools/taskclient.py`
- `TASKS/_SCHEMA.task.json`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `AGENTS.md`

## Non-goals
- 不扩 run summary
- 不做多角色调度器

## Acceptance
- [ ] task 机器层有 run-main resolution 字段或约定
- [ ] taskclient 有最小 run-main resolution 刷新/写回入口
- [ ] docs/evidence updated

## Inputs

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Test Gate
- Status: passed
- Owner role: test

### Required Axes
- functional
- flow
- data
- non_functional

### Evidence
- manual verification demo

### Blocking Issues

## Role Summaries
- `run-main`: status=ready, thread_id=run-main-demo-thread
  summary: run-main confirmed current escalation and requests final test clearance.
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Task Summary
- Status: completed

### Key Updates
- task 机器层新增 run_main_resolution_policy 和 run_main_resolution。
- taskclient 新增 --run-main-resolution / --set-run-main-resolution / --refresh-run-main-resolution。
- 已验证 pending_ack 和手动 close_escalation 写回。

### Decisions
- run-main resolution 只处理升级后的确认与关闭，不替代 escalation 判断。

### Risks

### Verification
- python3 -m py_compile tools/taskclient.py
- python3 tools/taskclient.py --refresh-task-gaps --task-json-file TASKS/TASK-run-main-escalation-resolution.json
- python3 tools/taskclient.py --refresh-task-escalation --task-json-file TASKS/TASK-run-main-escalation-resolution.json
- python3 tools/taskclient.py --refresh-run-main-resolution --task-json-file TASKS/TASK-run-main-escalation-resolution.json
- python3 tools/taskclient.py --set-run-main-resolution --task-json-file TASKS/TASK-run-main-escalation-resolution.json --resolution-status closed --resolution-note 'run-main manually closed resolved escalation.' --close-escalation
- python3 tools/taskclient.py --run-main-resolution --task-json-file TASKS/TASK-run-main-escalation-resolution.json
- make evidence RUN_ID=run-2026-03-11-vnext-release-baseline

### Next Steps
- 继续定义 run-main 收到升级后的真实 role thread turn 与 resolution 的联动。

### Conflict Policy
- Priority order: run-main, test, arch, dev
- Merge rule: append_dedup
- Escalation rule: if conflict remains, escalate to run-main

### Gap Summary
- missing_role: dev
- missing_role: test
- gap: dev summary missing
- gap: test summary missing

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
- status: closed
- close_escalation: true
- note: run-main manually closed resolved escalation.

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
