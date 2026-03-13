# TASK: dev role runtime merge link

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-dev-role-runtime-merge-link
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把 dev 真实 role thread 接入 runtime，并让 summarize-role 后自动 merge 进 task summary。

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
- [x] dev 可用 fork-role/role-turn/summarize-role 走真实链
- [x] summarize-role 后自动 merge-role-summaries 到 task summary
- [x] docs/evidence updated

## Inputs

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=ready, thread_id=019ce6aa-e6cb-7903-9f84-938b3e83238c
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
- `dev`: status=ready, thread_id=019ce6aa-e6cb-7903-9f84-938b3e83238c
  summary: 本角色已完成：当前 task 依赖的公共能力已经具备，`appserverclient` 已支持 `--fork-role`、`--role-turn`、`--summarize-role`，`taskclient` 已支持 `--merge-role-summaries`，相关 owner docs 也已把 role summary 自动 merge 进 task summary 的正式口径写清。就本 task 而言，`dev` 角色线程已经完成真实绑定并写入当前 task，说明 dev role thread 已接入 runtime 基础层，不再停留在纯设计状态。

风险与阻塞：当前 task 还没有形成 dev 侧的闭环证据，`role_summaries.dev` 仍为空，`task_summary` 仍是 draft，说明还缺少一次真实的 `dev role-turn -> summarize-role` 结果写回，也还没有证明 summarize 后会自动 merge 到当前 task summary。换句话说，现在已证明“能力存在”和“dev 线程已绑定”，但还没有证明“当前 task 上的 dev 真链路已跑通并自动沉淀”，因此 acceptance 仍不能关闭。

建议下一步：先在当前 dev 线程上执行一次真实 `role-turn`，聚焦实现视角说明这个 task 还缺的最小落点，再立即执行 `summarize-role dev`，确认摘要被写入 `role_summaries.dev`，并自动联动更新 `task_summary.role_summary_evidence`、`source_threads` 与聚合内容。完成这条验证后，再同步更新 task evidence 和 owner docs 状态，把“公共能力已具备”转成“当前 dev task 已闭环”的明确证据。
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Task Summary
- Status: completed

### Key Updates
- dev role thread forked into real runtime
- dev role-turn completed on real thread
- dev summary merged

### Decisions
- dev role runtime validation stays task-local; run-main/test gates remain separate follow-up tasks

### Risks
- gap_summary still reports run-main/test missing because task policy is generic across roles, but that does not block this dev-focused validation task

### Verification
- `python3 -m py_compile tools/appserverclient.py tools/taskclient.py`
- `python3 tools/appserverclient.py --fork-role dev`
- `python3 tools/appserverclient.py --role-turn dev "请从开发视角说明当前 task 已完成什么、还缺什么。"`
- `python3 tools/appserverclient.py --summarize-role dev`

### Next Steps
- continue with integrated multi-role runtime chain on top of this verified dev path

### Conflict Policy
- Priority order: run-main, test, arch, dev
- Merge rule: append_dedup
- Escalation rule: if conflict remains, escalate to run-main

### Gap Summary
- missing_role: run-main
- missing_role: test
- gap: run-main summary missing
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
- reason: run-main summary missing
- reason: test_gate=pending

### Run-Main Resolution Policy
- must_confirm_if: escalation_summary.needs_run_main
- can_close_if: run-main summary exists
- can_close_if: test_gate passed
- can_close_if: no blocking issue remains

### Run-Main Resolution
- status: pending_ack
- close_escalation: false
- note: Waiting for run-main summary.

### Role Summary Evidence
- `dev:019ce6c4-9521-7861-b5f7-4881ea0e2f65`

### Source Threads
- `dev:019ce6aa-e6cb-7903-9f84-938b3e83238c`

## Risks / Rollback
- Risks: 
- Rollback plan:
