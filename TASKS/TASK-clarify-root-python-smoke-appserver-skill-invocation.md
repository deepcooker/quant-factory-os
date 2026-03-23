# TASK: clarify root-python-smoke appserver skill invocation

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-clarify-root-python-smoke-appserver-skill-invocation
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
adjust the root-python-smoke skill wording so it clearly presents appserver/Codex skill invocation rather than looking like a standalone shell workflow

## Scope
- `.agents/skills/root-python-smoke/SKILL.md`
- `reports/run-2026-03-11-vnext-release-baseline/summary.md`
- `reports/run-2026-03-11-vnext-release-baseline/decision.md`
- `tools/project_config.json`
- `TASKS/QUEUE.json`

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
- 已把 root-python-smoke 的说明改成明确的 Codex/appserver skill invocation 模式，不再像独立 shell 流程。
- 已新增 Invocation Model 段，明确通过 `Use $root-python-smoke ...` 触发。

### Decisions
- skill 文案应明确区分：skill 本身是被 Codex/appserver 调起的能力包，shell 命令只是 skill 触发后的执行动作。

### Risks

### Verification
- python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/root-python-smoke 通过。

### Next Steps
- 如需，后续可用同样口径继续收紧 session-coach 的说明层。

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
