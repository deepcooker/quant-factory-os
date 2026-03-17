# TASK: validate init-project instruction flow on uninitialized fixture

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-validate-init-project-instruction-flow-on-uninitialized-fixture
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Run init and init-project with --instruction-text against an uninitialized fixture project, verify session_execution_instruction and manual continuation state are persisted correctly.

## Scope
- `fixtures/init_project_fixture`
- `tools/appserverclient.py`
- `tools/project_config.json`
- `reports/run-2026-03-11-vnext-release-baseline/summary.md`
- `reports/run-2026-03-11-vnext-release-baseline/decision.md`

## Non-goals

## Acceptance
- [x] python3 tools/init.py and python3 tools/appserverclient.py --init-project --instruction-text ... run against the fixture project
- [x] session_execution_instruction and continuation payload are visible in init_project_session

## Inputs

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

## Role Summaries
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Task Summary
- Status: completed

### Key Updates
- 已真实跑通 `init -> --init-project --instruction-text` 到未初始化 fixture
- 已确认 `session_execution_instruction` 和 continuation payload 写回的是目标项目自己的 `tools/project_config.json`

### Decisions
- init-project session 状态必须定向写回目标项目，而不是 foundation 仓
- 一句话补充执行指令应作为同一 init session 的正式约束继续保留

### Risks
- 当前仍是本地 session/state runtime，而非真实 app-server init thread

### Verification
- `python3 tools/init.py`
- `python3 tools/appserverclient.py --init-project -new --instruction-text "总纲优先，README 次之，中央银行设计是风控与现金流核心"`
- `python3 tools/view.sh fixtures/init_project_fixture/tools/project_config.json --from 1 --to 160`
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py tools/init.py`

### Next Steps
- 把同一套手工续跑方式迁移到真实未初始化项目

### Conflict Policy
- Priority order: run-main, test, arch, dev
- Merge rule: append_dedup
- Escalation rule: if conflict remains, escalate to run-main

### Gap Summary

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
- status: pending_ack
- close_escalation: false

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
