# TASK: run-main role runtime resolution link

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-run-main-role-runtime-resolution-link
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
把 run-main 真实 role thread turn、summarize-role 与 task resolution 刷新串起来。

## Scope
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `AGENTS.md`

## Non-goals
- 不扩 run summary
- 不做多角色调度器

## Acceptance
- [ ] run-main 可用 fork-role/role-turn/summarize-role 走真实链
- [ ] run-main summarize 后自动刷新 task escalation/resolution
- [ ] docs/evidence updated

## Inputs

## Role Threads
- `run-main`: status=ready, thread_id=019ce69a-7e4f-7aa3-b1f2-9e9299c70d61
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
- `run-main`: status=ready, thread_id=019ce69a-7e4f-7aa3-b1f2-9e9299c70d61
  summary: 本角色已完成：已确认当前 task 的升级项定义和关闭条件已经在 task 机器层落位，`task_summary.run_main_resolution_policy`、`task_summary.run_main_resolution`、`role_threads`、`role_summaries`、`test_gate` 这些字段与最小刷新入口都已存在。当前 task 也已经明确把目标收敛为“把真实 `fork-role / role-turn / summarize-role` 链路与 task escalation / run-main resolution 自动刷新串起来”，不再停留在纯规则设计阶段。

风险与阻塞：真实 runtime 链路还没有完成闭环，当前 `run_main_resolution` 仍是 `pending_ack`，`role_summaries.run-main/dev/test` 还没有真实摘要写回，`dev/test` 角色线程仍未进入已执行状态，`test_gate` 也还是 `pending`。在这些条件未满足前，升级项不能关闭；当前主要缺口不是规则不清，而是真实 role thread 执行证据、自动刷新结果和独立测试门证据还未补齐。

建议下一步：先跑通真实 `fork-role -> role-turn -> summarize-role`，至少补齐 `run-main` 和 `test` 两条关键角色线程的有效摘要写回，并验证写回后会自动刷新 task 的 `gap_summary / escalation_summary / run_main_resolution`。随后由 `test` 侧补齐 `test_gate=passed` 或明确 blocking issue，再更新 docs/evidence，使 task 具备关闭升级项的最小条件。
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Task Summary
- Status: draft

### Key Updates

### Decisions

### Risks

### Verification

### Next Steps

### Conflict Policy
- Priority order: run-main, test, arch, dev
- Merge rule: append_dedup
- Escalation rule: if conflict remains, escalate to run-main

### Gap Summary
- missing_role: dev
- missing_role: test
- gap: dev summary missing
- gap: test summary missing
- gap: test_gate=pending

### Escalation Policy
- must_escalate_if: run-main summary missing
- must_escalate_if: test_gate not passed
- must_escalate_if: blocking issue remains
- can_resolve_in_task_if: only dev/arch detail alignment
- can_resolve_in_task_if: no blocking issue
- can_resolve_in_task_if: test gate already passed

### Escalation Summary
- needs_run_main: true
- reason: test_gate=pending

### Run-Main Resolution Policy
- must_confirm_if: escalation_summary.needs_run_main
- can_close_if: run-main summary exists
- can_close_if: test_gate passed
- can_close_if: no blocking issue remains

### Run-Main Resolution
- status: acknowledged
- close_escalation: false
- note: run-main acknowledged; waiting for test_gate=pending.

### Role Summary Evidence
- `run-main:019ce69c-2cfa-73a1-a821-25634ddbdc43`

### Source Threads
- `run-main:019ce69a-7e4f-7aa3-b1f2-9e9299c70d61`

## Risks / Rollback
- Risks: 
- Rollback plan:
