# TASK: short stable mainline regression

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-short-stable-mainline-regression
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
围绕当前最短稳定主线做一轮回归验证，确认默认路径在不扩结构的前提下可持续稳定运行。

## Scope
- `tools/init.py`
- `tools/appserverclient.py`
- `tools/gitclient.py`
- `tools/taskclient.py`
- `tools/evidence.py`
- `docs/WORKFLOW.md`

## Non-goals
- 不新增功能，不改对象模型，不引入新角色配置系统

## Acceptance
- [x] 完成一轮短主线回归并记录结论与阻塞

## Inputs
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `tools/project_config.json`

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
- short stable mainline regression completed for init, learnbaseline, and fork-current

### Decisions
- treat sandbox access to `/root/.codex/sessions` as environment-specific, not a mainline logic failure

### Risks
- fork-current still needs escalated access to /root/.codex/sessions in the current sandboxed environment

### Verification
- `python3 tools/init.py` started normally with visible `INIT_STEP` output
- `python3 tools/appserverclient.py --learnbaseline` passed in sandbox
- `python3 tools/appserverclient.py --fork-current` passed after escalated rerun and wrote a new `fork_current_session`

### Next Steps
- keep shortest stable mainline as the default path and treat role-thread steps as opt-in

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
- status: not_needed
- close_escalation: false
- note: This regression task only validates the shortest stable mainline and does not require run-main escalation.

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
