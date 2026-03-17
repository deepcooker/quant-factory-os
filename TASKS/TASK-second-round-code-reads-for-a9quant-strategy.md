# TASK: Second-round code reads for a9quant-strategy

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-second-round-code-reads-for-a9quant-strategy
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Read the current must_read_next code files for /root/a9quant-strategy and extract implementation evidence before any owner-doc reverse-writing.

## Scope
- `Only inspect the eight phase-1 must_read_next files and summarize what is already implemented`
- `what is missing`
- `and what this implies for owner-doc writing; do not run phase-2 and do not write files in the target project.`

## Non-goals

## Acceptance
- [x] Evidence summary captures the current implementation status across the eight must_read_next files for /root/a9quant-strategy

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
- `advanced_risk.py` 已确认实现 `RiskManager`、持久化锚定本金、水位线重置、系统模式状态机和 `approve_action` 风控闸门。
- `ccxt_utils.py` 已确认实现 `ExchangeTrader` 的 CCXT/Bitget 交易适配层，包括市场细节提取、保证金/杠杆设置、持仓查询、平仓逻辑和合约余额查询。
- 结合前一轮已读文件，`trend_engine/shark_engine/base_bitget_ws/bitget_ws_bridge/market_data_hub/tiny_oms` 已经证明目标项目不是概念草图，而是存在真实实现的交易系统骨架。

### Decisions
- `a9quant-strategy` 的 owner docs 反写必须按“已有实现”来写，不能按纯愿景型项目来写。
- 在读取 `main_controller.py / account_state.py / contracts.py / tests` 之前，不进入 Phase 2 owner-doc 写入。

### Risks
- 仍未读取 `main_controller.py / account_state.py / contracts.py / tests`，当前证据不足以准确描述真实主线和测试完成度。
- `ccxt_utils.py` 的 `__main__` 测试块内仍有硬编码 Bitget sandbox 凭据，属于明显的卫生与安全风险。

### Verification
- Read `advanced_risk.py` in three chunks and confirmed risk policy/state-machine implementation.
- Read `ccxt_utils.py` in multiple chunks and confirmed exchange adapter, margin/leverage, positions, close-position, and balance helpers.
- Combined with prior reads of `trend_engine.py`, `shark_engine.py`, `base_bitget_ws.py`, `bitget_ws_bridge.py`, `market_data_hub.py`, and `tiny_oms.py`, the current architecture already has engine/ws/data/oms layers implemented.

### Next Steps
- Read `main_controller.py`, `account_state.py`, `contracts.py`, and selected tests before any Phase 2 owner-doc write.
- Keep `/root/a9quant-strategy` in Phase 1 plan mode; do not write owner docs yet.

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
