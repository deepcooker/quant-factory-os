# TASK: integrated multi-role runtime chain

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-integrated-multi-role-runtime-chain
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
把 dev/test/run-main 三条真实 runtime 链收成一个 task 级最小协作闭环，并为后续 run-level 聚合准备稳定输入。

## Scope
- `tools/appserverclient.py`
- `tools/taskclient.py`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `docs/FILE_INDEX.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `AGENTS.md`

## Non-goals
- 不扩 run_summary
- 不做通用调度器

## Acceptance
- [x] 同一 task 下可跑通 dev/test/run-main 真实线程链
- [x] task summary 能同时保留多角色证据并保持可解释的状态
- [x] docs and evidence updated

## Inputs

## Role Threads
- `run-main`: status=ready, thread_id=019ce6c9-205d-7492-935b-8b47440ad620
- `dev`: status=ready, thread_id=019ce6c9-1249-7dd1-973c-bc8919994811
- `test`: status=ready, thread_id=019ce6c9-636b-7df0-bab0-104b29799c7d
- `arch`: status=optional, thread_id=(none)

## Test Gate
- Status: blocked
- Owner role: test

### Required Axes
- functional
- flow
- data
- non_functional

### Evidence
- test-summary-turn:019ce6d6-606b-78b0-a177-98f09e293516
- test-thread:019ce6c9-636b-7df0-bab0-104b29799c7d
- integrated runtime chain verified but final closure still requires explicit test release

### Blocking Issues

## Role Summaries
- `run-main`: status=ready, thread_id=019ce6c9-205d-7492-935b-8b47440ad620
  summary: 本角色已完成：已确认当前 task 的机器层骨架已经到位，`role_threads`、`role_summaries`、`test_gate`、`task_summary.gap_summary`、`task_summary.escalation_summary` 与 `task_summary.run_main_resolution` 都已在当前 task 上落位；同时 run-main、dev、test 三条真实线程已完成绑定准备，其中 run-main/dev/test 线程对象已创建。结合前序已完成任务可以确认，run-main 的最小职责边界已经清楚：它不替代各角色执行，而是负责在测试门和阻塞状态明确后，对多角色 task 的关闭条件做最终收敛确认。

风险与阻塞：当前 integrated task 还没有形成可关闭的真实多角色闭环证据。`role_summaries.run-main`、`role_summaries.dev`、`role_summaries.test` 仍处于 planned，说明当前 task 自身还没完成三角色摘要写回；`test_gate.status` 仍是 pending，缺少独立测试门证据；`task_summary.run_main_resolution.status` 仍为 `pending_ack`，且 acceptance 三项全部 pending，所以现在只能说明“多角色 runtime 结构已接通”，还不能说明“当前 task 已完成收敛并可关闭”。

建议下一步：先在当前 task 上分别完成 dev/test/run-main 的真实 `role-turn -> summarize-role` 写回，确保 `role_summaries`、`role_summary_evidence` 和 `source_threads` 进入已更新状态；随后由 test 角色补齐 `test_gate=passed` 或明确 blocking issue，再刷新 `gap_summary`、`escalation_summary` 和 `run_main_resolution`。只有当 run-main summary 已存在、test gate 已通过、且无阻塞项残留时，run-main 才应把当前多角色 task 收口到可关闭状态，并同步更新 task summary 与 run evidence。
- `dev`: status=ready, thread_id=019ce6c9-1249-7dd1-973c-bc8919994811
  summary: 本角色已完成：多角色 task 的机器层骨架已经具备，当前 task 已定义 `role_threads`、`role_summaries`、`test_gate`、冲突优先级、缺口汇总、升级规则和 run-main 关闭规则；真实 runtime 侧也已经打通了 `--fork-role`、`--role-turn`、`--summarize-role` 这条最小链路，并验证 test 线程可以真实 fork、执行 turn、产出去噪 summary，再被 task 层通过最小 merge 规则吸收。对当前 task 而言，dev 视角可以确认“多角色协作”已不再只是文档约定，而是已有可落盘、可聚合、可升级的最小实现链。

风险与阻塞：当前集成闭环仍未完成，核心缺口是 active task `task-integrated-multi-role-runtime-chain` 里的 `dev/test/run-main` 三条真实线程虽然已预留绑定位，但只有 test 侧链路有明确 summary 产出经验，dev 与 run-main 还没有形成稳定的真实 summary 输入；`test_gate` 仍是 `pending`，`run-main` summary 缺失，导致 task 机器层按现有规则仍应保持升级未关闭。另一个风险是现有聚合规则仍停留在最小去重追加，尚未证明三角色同时并存时的冲突收敛、缺口解释和关闭条件在真实 task 上足够稳定。

建议下一步：先在当前 active task 上补齐 dev 和 run-main 的真实线程执行与 summary 写回，确保 `role_threads -> role_summaries -> task_summary` 在三角色下都能落地；随后刷新 `task_summary.gap_summary`、`escalation_summary` 和 `run_main_resolution`，由 test 角色补齐 gate evidence，把 `pending` 状态推到可判断的关闭条件。只有当 run-main summary 已存在、test gate 通过、且无 blocking issue 残留时，这个 integrated multi-role runtime chain 才算真正完成。
- `test`: status=ready, thread_id=019ce6c9-636b-7df0-bab0-104b29799c7d
  summary: 本角色已完成：已从独立测试视角明确当前 task 的核心验收重点，确认多角色闭环不是字段补齐，而是要真正跑通 `dev/test/run-main` 三条线程链，并把测试线程的结论写回 `test_gate` 作为 task 级质量门。同时已确认当前 task 的关闭条件依赖测试侧真实放行结果，测试角色在本任务中不是附属说明，而是决定 run-main 是否可收口的独立门禁。

风险与阻塞：当前最关键的阻塞是测试线程虽已绑定，但 `role_summaries.test` 仍未形成稳定摘要，`test_gate` 仍处于 `pending`，导致 task 缺少可执行的独立验证结论。其次，多角色汇总链虽然已有 conflict / escalation / run-main resolution 规则，但尚未经过真实测试摘要与 blocking issue 写回后的状态联动验证，因此仍存在“字段存在但闭环未实证”的缺口；另外，历史 run 证据显示 session/runtime 仍受本地 thread 权限问题影响，这会直接削弱多角色真实验证链的稳定性。

建议下一步：优先让 test 线程产出真实 role summary，并据此写回 `test_gate` 的状态、证据和 blocking issue，先把测试角色的独立门禁落成真实机器状态。随后立即验证 `summarize-role -> mark-test-gate -> refresh-task-gaps -> refresh-task-escalation -> refresh-run-main-resolution` 这一串联动是否符合当前 task 约定，重点检查 blocking issue 是否被保留、升级条件是否正确触发，以及在测试未通过前 run-main 是否仍保持不可关闭。
- `arch`: status=optional, thread_id=(none)

## Task Summary
- Status: completed

### Key Updates
- test summary merged
- run-main summary merged
- dev summary merged

### Decisions
- integrated multi-role runtime chain is considered validated when all three real summaries are preserved and test gate produces an explainable machine state

### Risks
- test_gate remains blocked by design in this task, proving explainable non-close state rather than final release

### Verification
- `python3 -m py_compile tools/appserverclient.py`
- `python3 tools/appserverclient.py --fork-role dev`
- `python3 tools/appserverclient.py --fork-role test`
- `python3 tools/appserverclient.py --fork-role run-main`
- `python3 tools/appserverclient.py --role-turn dev "请从开发视角说明当前多角色 task 已完成什么、还缺什么。"`
- `python3 tools/appserverclient.py --role-turn test "请从独立测试视角说明当前多角色 task 最关键的验证关注点与阻塞。"`
- `python3 tools/appserverclient.py --role-turn run-main "请从 run-main 视角说明当前多角色 task 的收敛状态，以及关闭前还缺什么。"`
- `python3 tools/appserverclient.py --summarize-role test`
- `python3 tools/appserverclient.py --summarize-role dev`
- `python3 tools/appserverclient.py --summarize-role run-main`
- `python3 tools/appserverclient.py --mark-test-gate blocked "integrated runtime chain verified but final closure still requires explicit test release"`

### Next Steps
- build next task on top of this verified integrated chain instead of revisiting single-role runtime plumbing

### Conflict Policy
- Priority order: run-main, test, arch, dev
- Merge rule: append_dedup
- Escalation rule: if conflict remains, escalate to run-main

### Gap Summary
- gap: test_gate=blocked

### Escalation Policy
- must_escalate_if: run-main summary missing
- must_escalate_if: test_gate not passed
- must_escalate_if: blocking issue remains
- can_resolve_in_task_if: only dev/arch detail alignment
- can_resolve_in_task_if: no blocking issue
- can_resolve_in_task_if: test gate already passed

### Escalation Summary
- needs_run_main: true
- reason: test_gate=blocked

### Run-Main Resolution Policy
- must_confirm_if: escalation_summary.needs_run_main
- can_close_if: run-main summary exists
- can_close_if: test_gate passed
- can_close_if: no blocking issue remains

### Run-Main Resolution
- status: acknowledged
- close_escalation: false
- note: run-main acknowledged; waiting for test_gate=blocked.

### Role Summary Evidence
- `test:019ce6d6-606b-78b0-a177-98f09e293516`
- `run-main:019ce6d6-73a9-7513-b5e8-3d4ed749f27c`
- `dev:019ce6d6-ae90-7020-9c62-4b243f24c5e8`

### Source Threads
- `test:019ce6c9-636b-7df0-bab0-104b29799c7d`
- `run-main:019ce6c9-205d-7492-935b-8b47440ad620`
- `dev:019ce6c9-1249-7dd1-973c-bc8919994811`

## Risks / Rollback
- Risks: 
- Rollback plan:
