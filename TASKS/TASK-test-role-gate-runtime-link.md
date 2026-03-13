# TASK: test role gate runtime link

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-test-role-gate-runtime-link
PROJECT_ID: quant-factory-os
STATUS: active
PRIORITY: P1

## Goal
把 test 真实 role thread、summarize-role 与 test_gate / escalation close 条件串起来。

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
- [ ] test 可用 fork-role/role-turn/summarize-role 走真实链
- [ ] 可通过 appserverclient 真实写回 test_gate 并自动刷新 task escalation/resolution
- [ ] docs/evidence updated

## Inputs

## Role Threads
- `run-main`: status=ready, thread_id=019ce6a3-60c3-7860-a79d-4a204ad15508
- `dev`: status=planned, thread_id=(none)
- `test`: status=ready, thread_id=019ce6a1-61dd-7003-a3ef-ebcc3dcfcfd1
- `arch`: status=optional, thread_id=(none)

## Test Gate
- Status: passed
- Owner role: test

### Required Axes
- functional
- flow
- data
- non_functional

### Evidence
- test-summary-turn:019ce6a2-b02d-7ab2-85d1-1a174f7964e2
- test-thread:019ce6a1-61dd-7003-a3ef-ebcc3dcfcfd1
- real test gate passed from runtime

### Blocking Issues

## Role Summaries
- `run-main`: status=ready, thread_id=019ce6a3-60c3-7860-a79d-4a204ad15508
  summary: 本角色已完成：已从 run-main 视角把当前 task 的关闭判定收口到机器层规则，确认升级项关闭不再只看 test 线程是否存在，而是要同时满足 `run-main summary exists`、`test_gate passed`、`no blocking issue remains`。当前 task 已具备 `run_main_resolution_policy`、`run_main_resolution`、`role_threads`、`role_summaries` 与 `test_gate` 这些正式字段，且 test 侧真实线程与测试摘要证据已经进入 task 机器层，`test_gate` 当前状态已为 passed。

风险与阻塞：当前最大的阻塞不是 test gate，而是 run-main 自身的关闭确认还未完成。机器层仍显示 `role_summaries.run-main` 为 planned、`task_summary.gap_summary` 里存在 `run-main summary missing`、`task_summary.escalation_summary.needs_run_main=true`，且 `run_main_resolution.status=pending_ack`、`close_escalation=false`，这意味着升级项还不能正式关闭；同时三个 acceptance 仍是 pending，说明 task 级完成态尚未被显式收口。

建议下一步：先把本次 run-main 去噪总结正式写入 `role_summaries.run-main`，随后刷新 task gaps / escalation / run-main resolution，让机器层重新计算关闭条件。若刷新后仍保持 `test_gate=passed`、无 blocking issue，且 run-main summary 已存在，再推进 `run_main_resolution` 进入可关闭状态，并同步更新 task summary 与 run evidence，把“test gate 已过、升级项可否关闭”的最终结论沉淀到 task 层。
- `dev`: status=planned, thread_id=(none)
- `test`: status=ready, thread_id=019ce6a1-61dd-7003-a3ef-ebcc3dcfcfd1
  summary: 本角色已完成：已从独立测试视角确认当前 task 的关键关闭条件不是“角色线程存在”本身，而是 test 真实线程产出的验证结论必须进入 task 机器层并驱动 `test_gate` 与升级关闭判断。当前已能确认正式主线要求 test 作为独立质量门参与关闭决策，且关闭升级项至少需要满足 `test_gate passed`、无 blocking issue，并与 run-main resolution 状态联动。

风险与阻塞：当前 task 机器层仍未形成可关闭的测试证据链，`test_gate` 还是待通过状态，`role_summaries.test` 还没有稳定摘要，说明 `fork-role -> role-turn -> summarize-role -> test_gate` 的正式闭环在本 task 上还未完成。若此时提前关闭升级项，会把“测试角色已接入 runtime”和“测试验证已完成并写回机器层”混为一谈，导致 task summary 与 escalation close 缺少独立测试证据支撑。

建议下一步：先在当前 test 角色线程上完成一次真实 `role-turn` 与 `summarize-role`，沉淀只保留稳定验证结论的 role summary，再把结果写入 `test_gate`，明确各验证维度是否通过以及是否存在 blocking issue。只有当 test 侧机器层状态明确为通过，且不再存在阻塞项时，再推动 run-main resolution 进入关闭升级项。
- `arch`: status=optional, thread_id=(none)

## Task Summary
- Status: draft

### Key Updates
- run-main summary merged
- test summary merged

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
- gap: dev summary missing

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
- note: No active escalation requires run-main handling.

### Role Summary Evidence
- `run-main:019ce6a4-a8c4-7b20-989a-8bf082ce019f`
- `test:019ce6a2-b02d-7ab2-85d1-1a174f7964e2`

### Source Threads
- `run-main:019ce6a3-60c3-7860-a79d-4a204ad15508`
- `test:019ce6a1-61dd-7003-a3ef-ebcc3dcfcfd1`

## Risks / Rollback
- Risks: 
- Rollback plan:
