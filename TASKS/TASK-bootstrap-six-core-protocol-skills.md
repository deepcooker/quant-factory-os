# TASK: bootstrap six core protocol skills

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-bootstrap-six-core-protocol-skills
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
create six official repo-local skill skeletons for baseline/fork/run/role/task/refresh protocol layers under .agents/skills

## Scope
- `.agents/skills`
- `docs/FILE_INDEX.md`
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
- 已在 .agents/skills 下建立 baseline-learn、fork-identity、run-manager、role-worker、task-referee、baseline-refresh 六个正式 repo-local skill 骨架。
- 六个 skill 均已生成 SKILL.md 与 agents/openai.yaml。
- 六个 skill 已补齐最小合法 frontmatter，并全部通过官方 validator。

### Decisions
- 先建立六个协议层 skill 骨架供 owner 审阅，不在这一轮先写重逻辑。

### Risks

### Verification
- 六个目录均存在于 .agents/skills 下。
- 六个 skill 逐个执行 quick_validate.py 均返回 Skill is valid!。

### Next Steps
- 下一轮再逐个补具体方法论内容，而不是在这一轮把 6 个 skill 全部写重。

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
