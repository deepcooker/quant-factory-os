# TASK: Read mainline, state, contracts, and tests for a9quant-strategy

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-read-mainline-state-contracts-and-tests-for-a9quant-strategy
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Read main_controller.py, account_state.py, contracts.py, and selected tests in /root/a9quant-strategy to confirm the real mainline, state ledger, contract layer, and verification surface before any phase-2 owner-doc writing.

## Scope
- `Only inspect main_controller.py`
- `account_state.py`
- `contracts.py`
- `test_integration.py`
- `and test_regression.py`
- `Do not run phase-2 and do not write files in the target project`

## Non-goals

## Acceptance
- [x] Evidence summary captures the actual entrypoint
- [x] state model
- [x] contracts
- [x] and test surface of /root/a9quant-strategy

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
- `main_controller.py` 已确认真实主入口：交易适配、DataSynchronizer、AccountState、RiskManager、MarketDataHub、TinyOMS、BitgetWSBridge、TrendEngine、SharkEngine 都在同一异步主控制器下编排。
- `account_state.py` 和 `contracts.py` 已确认项目已有 typed state ledger / contract boundary，而不是松散 dict 拼接。
- `test_integration.py` 与 `test_regression.py` 已确认存在真实验证面，覆盖 live gate、trace 传播、同步器唯一状态更新、OMS 幂等、重连校准、replay 驱动链路和 risk gate 约束。

### Decisions
- Phase 2 owner-doc reverse-writing 现在可以按“controller-centered implemented system”来写，不必再把项目当成只有模块草图。
- 但在进入 Phase 2 前，仍应再补一轮 `data_synchronizer.py` 和 `config.json` 证据，避免对环境依赖和同步层说错。

### Risks
- `data_synchronizer.py` 和 `config.json` 还未在这一轮读透，因此运行依赖和配置面仍有残缺。
- 当前验证结论来自静态代码/测试阅读，不是实际跑通目标项目测试。

### Verification
- Read `main_controller.py` and confirmed async main loop, policy evaluation, signal processing, OMS submission, reconciliation, and shutdown flow.
- Read `account_state.py` and confirmed state updates come from `DataSynchronizer` snapshots and split into `RiskSnapshot` and `StrategySnapshot`.
- Read `contracts.py` and confirmed typed dataclass contracts for risk, intent, market, snapshot, position, and account objects.
- Read `test_integration.py` and `test_regression.py` and confirmed coverage for live gate, trace propagation, synchronizer-only state updates, OMS idempotency, reconnect calibration, replay-driven execution, and risk-gate enforcement.

### Next Steps
- Read `data_synchronizer.py` and `config.json` before any Phase 2 owner-doc write.
- Keep `/root/a9quant-strategy` in `--init-project` Phase 1 mode until that final dependency/config evidence is added.

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
