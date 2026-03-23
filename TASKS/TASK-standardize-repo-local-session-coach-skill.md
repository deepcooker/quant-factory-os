# TASK: standardize repo-local session-coach skill

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-standardize-repo-local-session-coach-skill
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
align session-coach with official Codex repo-local skill layout and metadata after comparing against official docs and system skills

## Scope
- `.agents/skills/session-coach`
- `skills/session-coach/SKILL.md`
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
- 已对比系统 skills：openai-docs、skill-creator、skill-installer 的 SKILL.md frontmatter 与 agents/openai.yaml。
- 已把 session-coach 迁到官方 repo-local 位置 .agents/skills/session-coach，并补齐 name/description frontmatter。
- 已通过 codex exec 显式使用 $session-coach，确认 repo-local session-coach skill 会被发现并执行。

### Decisions
- repo-local skill 的正式落位统一使用 .agents/skills/<skill-name>/，并保留 agents/openai.yaml 作为 UI 元数据。

### Risks

### Verification
- python3 /root/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/session-coach 通过。
- codex exec -C /root/quant-factory-os "Use $session-coach ..." 日志明确出现 Using session-coach for a baseline identity confirmation step。

### Next Steps
- 后续可删除或归档旧的 skills/session-coach/SKILL.md 草稿，避免和正式 repo-local skill 双轨并存。

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
