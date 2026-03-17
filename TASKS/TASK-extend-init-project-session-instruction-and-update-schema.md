# TASK: extend init-project session instruction and update schema

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-extend-init-project-session-instruction-and-update-schema
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Add generic session-level execution instruction support to init-project, persist it in init_project_session, and document the xhigh plan/session update protocol.

## Scope
- `tools/appserverclient.py`
- `tools/project_config.py`
- `tools/project_config.template.json`
- `tools/prompts/init_project_prompt.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `AGENTS.md`
- `reports/run-2026-03-11-vnext-release-baseline/summary.md`
- `reports/run-2026-03-11-vnext-release-baseline/decision.md`

## Non-goals

## Acceptance
- [x] python3 -m py_compile tools/appserverclient.py tools/project_config.py
- [x] docs and evidence updated

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
- `--init-project` 现在支持 `--instruction-text` 和 `--instruction-file`
- `init_project_session` 现在持久化 `session_execution_instruction` 与 `operator_notes`

### Decisions
- 一句话 owner 指令应进入 init-project session，而不是继续写成代码里的特殊化规则
- 手工续跑需要把补充执行指令和人工备注稳定写回 `project_config.json`

### Risks
- 目前仍是本地 session/state runtime，而不是真实 app-server init thread

### Verification
- `python3 -m py_compile tools/appserverclient.py tools/project_config.py tools/init.py`
- `python3 tools/appserverclient.py --init-project --instruction-text "总纲优先，README 次之，中央银行设计是风控与现金流核心"`
- `python3 tools/project_config.py`

### Next Steps
- 继续只提升 prompt/session 质量，不再引入项目化代码规则

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
