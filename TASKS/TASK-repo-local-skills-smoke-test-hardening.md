# TASK: repo-local skills smoke test hardening

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-repo-local-skills-smoke-test-hardening
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
validate official repo-local skill layout and add a minimal smoke-test skill under .agents/skills

## Scope
- `.agents/skills/root-python-smoke/SKILL.md`
- `skill_test_one.py`
- `skill_test_two.py`
- `docs/FILE_INDEX.md`

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
- 已按官方 skill-creator 初始化脚本在 .agents/skills/root-python-smoke 下创建最小 repo-local skill。
- 已新增根目录 smoke 文件 skill_test_one.py 与 skill_test_two.py，并验证两者可直接运行输出 1/2。
- 已通过 codex exec 显式使用 $root-python-smoke，确认 repo-local skill 会被发现、读取并执行。

### Decisions
- repo-local skills 的正式落位应使用 .agents/skills，而不是普通 repo-root skills/ 目录。

### Risks

### Verification
- python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/root-python-smoke 通过。
- python3 skill_test_one.py && python3 skill_test_two.py 输出 1 和 2。
- codex exec -C /root/quant-factory-os "Use $root-python-smoke ..." 日志明确出现 Using root-python-smoke for this turn。

### Next Steps
- 后续如需把 session-coach 变成正式 repo-local skill，应迁到 .agents/skills/session-coach 并补齐 frontmatter。

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
