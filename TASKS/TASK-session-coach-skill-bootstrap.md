# TASK: session coach skill bootstrap

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-session-coach-skill-bootstrap
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
create a minimal reusable session-coach skill/protocol for baseline and fork-run multi-window guidance

## Scope
- `docs/PROJECT_GUIDE.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `docs/SESSION_COACH_PROTOCOL.md`
- `skills/session-coach/SKILL.md`

## Non-goals

## Acceptance
- [ ] Command(s) pass: make verify
- [ ] reports/{RUN_ID}/summary.md and reports/{RUN_ID}/decision.md updated

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
- 已新增 docs/SESSION_COACH_PROTOCOL.md，固化 baseline 与 fork-run 多窗口协作的最小教练协议。
- 已新增 skills/session-coach/SKILL.md，提供可复用的轻量 session coach skill 模板。
- 已把 runtime_state 与 QUEUE.json 当前 active task 指针切到 session-coach skill bootstrap，避免文档变更挂在旧 cleanup task 上。

### Decisions
- 当前不做自动多窗口控制器；先把个人多窗口的提问/验收/下一跳协议固定下来。

### Risks

### Verification
- docs/SESSION_COACH_PROTOCOL.md 已落库。
- skills/session-coach/SKILL.md 已落库。
- docs/WORKFLOW.md 与 docs/FILE_INDEX.md 已补最小入口说明。

### Next Steps
- 下一轮如需真正安装 skill 到 ~/.codex/skills，可直接复用仓库内 skills/session-coach/SKILL.md 作为源模板。

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
