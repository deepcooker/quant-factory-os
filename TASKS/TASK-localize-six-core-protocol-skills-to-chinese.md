# TASK: localize six core protocol skills to Chinese

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-localize-six-core-protocol-skills-to-chinese
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
translate the six protocol skill display metadata and SKILL.md bodies into Chinese while keeping the internal skill names stable

## Scope
- `.agents/skills/baseline-learn`
- `.agents/skills/fork-identity`
- `.agents/skills/run-manager`
- `.agents/skills/role-worker`
- `.agents/skills/task-referee`
- `.agents/skills/baseline-refresh`
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
- 已把六个协议层 skill 的 agents/openai.yaml 展示名、短描述和默认提示改成中文。
- 已把六个 skill 的 SKILL.md 正文最小中文化，内部触发名 name 保持英文稳定。
- 六个中文化 skill 继续全部通过官方 validator。

### Decisions
- 对 owner 友好的做法是：内部 skill 名保持英文稳定，展示层和正文中文化。

### Risks

### Verification
- 六个 skill 逐个执行 quick_validate.py 均返回 Skill is valid!。

### Next Steps
- 下一轮可开始逐个往六个 skill 里补更具体的方法论，而不是继续停留在 skeleton。

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
