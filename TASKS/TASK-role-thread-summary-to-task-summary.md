# TASK: role thread summary to task summary

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-role-thread-summary-to-task-summary
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
补 role thread 的最小 thread summary 落点，并让 task summary 能引用这些结果。

## Scope
- `tools/appserverclient.py`
- `TASKS/_SCHEMA.task.json`
- `tools/taskclient.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `AGENTS.md`

## Non-goals
- 不做 run summary 自动聚合
- 不做多角色调度器

## Acceptance
- [ ] 新增 role thread summary 机器层字段并可写回
- [ ] 新增最小 runtime 入口生成 role summary
- [ ] task summary 可记录 source_threads 和 role summary evidence
- [ ] docs/evidence updated

## Inputs

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=ready, thread_id=019ce651-9a94-7da0-b919-76a9339ec173
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
- `test`: status=ready, thread_id=019ce651-9a94-7da0-b919-76a9339ec173
  summary: 本角色已完成：已从独立测试视角把当前 task 的验证目标收敛为“role thread summary 是否形成稳定落点，以及 task summary 是否能直接引用这些结果”。已明确这不是聊天摘要问题，而是证据结构与聚合链路问题，测试关注点应放在 role-level 结论是否足够去噪、是否可被 task 层稳定消费、以及输出是否保持固定结构与可重复性。

风险与阻塞：当前主要风险是 role summary 仍可能混入过程性聊天噪音，导致 task summary 无法稳定抽取有效结论；另一处缺口是 task summary 对 role summary 的引用关系是否已经真正打通，如果只是生成文本但没有形成可消费的机器层落点，链路仍然是不完整的。当前阻塞不在业务逻辑，而在摘要写回格式、字段边界和聚合消费之间是否已经闭环验证。

建议下一步：优先验证 role summary 的最小写回结果是否稳定、可重复、可被 task summary 直接引用，并补一条面向聚合链路的回归检查，确认 test 角色输出进入 task summary 后不会带入噪音或丢失风险项。若链路已通，再进一步检查多角色 summary 并存时 task summary 的去重、优先级和缺口汇总是否符合 task 层使用预期。
- `arch`: status=optional, thread_id=(none)

## Task Summary
- Status: completed

### Key Updates
- task 机器层新增 role_summaries，用于保存 role-level 去噪摘要。
- appserverclient 新增 --summarize-role，可在已绑定 role thread 上生成真实 role summary。
- task_summary 已能回写 source_threads 和 role_summary_evidence。
- test summary merged

### Decisions
- 当前先把 role summary 作为 task JSON 内机器层对象落地，不单独新建 role client。

### Risks

### Verification
- python3 -m py_compile tools/taskclient.py tools/appserverclient.py
- python3 tools/appserverclient.py --fork-role test
- python3 tools/taskclient.py --role-threads
- python3 tools/appserverclient.py --role-turn test "请从独立测试视角给出这个 task 当前最关键的验证关注点。"
- python3 tools/appserverclient.py --summarize-role test
- python3 tools/taskclient.py --role-summaries
- python3 tools/taskclient.py --active-task

### Next Steps
- 继续补多角色 role summary 并存时的 task-level 聚合与去重策略。

### Conflict Policy
- Priority order: run-main, test, arch, dev
- Merge rule: append_dedup
- Escalation rule: if conflict remains, escalate to run-main

### Gap Summary
- missing_role: run-main
- missing_role: dev
- gap: run-main summary missing
- gap: dev summary missing
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

### Role Summary Evidence
- `test:019ce651-f5e6-77d1-a7c2-17385201902e`

### Source Threads
- `test:019ce651-9a94-7da0-b919-76a9339ec173`

## Risks / Rollback
- Risks: 
- Rollback plan:
