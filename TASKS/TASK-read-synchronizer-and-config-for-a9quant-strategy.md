# TASK: Read synchronizer and config for a9quant-strategy

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-read-synchronizer-and-config-for-a9quant-strategy
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
Read data_synchronizer.py and config.json in /root/a9quant-strategy to confirm the final dependency, reconciliation, and runtime configuration evidence before deciding whether phase-2 owner-doc writing is ready.

## Scope
- `Only inspect data_synchronizer.py and config.json`
- `Do not run phase-2 and do not write files in the target project`

## Non-goals

## Acceptance
- [x] Evidence summary captures synchronizer responsibilities and config-driven runtime assumptions for /root/a9quant-strategy

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
- `data_synchronizer.py` 已确认项目采用 `WS 主、REST 校准辅` 的 SoT 同步策略，而不是让策略或 OMS 直接篡改持仓与账户真相。
- 同步层已经实现 `position_uncertain`、`consistency_score`、private channel health、REST 强制对账和 execution-event evidence hooks。
- `config.json` 已确认当前运行假设：Bitget、sandbox=true、代理开启、swap、`BTC/USDT:USDT`、`initial_capital=200`。

### Decisions
- 现在证据已经足够支撑 owner-doc 级描述：运行时、同步层、状态账本、契约层、风控、执行、ws 桥接和测试面都已读到。
- 下一步可以讨论是否进入 `--init-project` Phase 2，但如果进入，必须把 sample config 仍带 sandbox 凭据和环境耦合默认值这件事写进风险项。

### Risks
- `config.json` 里仍有硬编码 Bitget sandbox 凭据和代理配置，这是明显的卫生与可移植性风险。
- `data_synchronizer.py` 仍依赖特定交易所的 `fetch_balance/fetch_positions` 行为，并且 `margin_ratio` 处理较简化，owner docs 不应把交易所抽象描述得过满。

### Verification
- Read `data_synchronizer.py` and confirmed WS-first updates, force_rest_sync calibration, SoT snapshot export, consistency scoring, private-channel health checks, and execution-event evidence hooks.
- Read `config.json` and confirmed exchange, symbol, sandbox, proxy, dry-run/live-trading, and risk bootstrap assumptions.
- Combined with prior reads, the target project now has evidence for controller, data sync, state ledger, contracts, risk, engines, ws bridge, oms, and tests.

### Next Steps
- Decide whether to run `--init-project` Phase 2 owner-doc reverse-writing for `/root/a9quant-strategy`.
- If Phase 2 proceeds, explicitly preserve the sandbox-credential hygiene risk and environment-coupled defaults in the generated owner docs.

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
