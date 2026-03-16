# TASK: stabilize view tool and tests

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-stabilize-view-tool-and-tests
PROJECT_ID: quant-factory-os
STATUS: completed
PRIORITY: P1

## Goal
将 tools/view.sh 收成稳定高效的分段读取工具，并补最小自动化测试覆盖。

## Scope
- `tools/view.sh`
- `docs/`
- `tests/`

## Non-goals

## Acceptance
- [x] view.sh 同时支持直接执行与 python3 调用
- [x] 范围读取、查找、denylist 和 repo 边界有自动化测试
- [x] 正式文档与 evidence 更新

## Inputs

## Role Threads
- `run-main`: status=planned, thread_id=(none)
- `dev`: status=planned, thread_id=(none)
- `test`: status=planned, thread_id=(none)
- `arch`: status=optional, thread_id=(none)

## Test Gate
- Status: not_needed
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
- `tools/view.sh` 已改成稳定的 Python 实现，同时保留原工具路径。
- 现在同时支持直接执行和 `python3 tools/view.sh ...`，并兼容历史 `--lines START:END`。

### Decisions
- 继续保留 `tools/view.sh` 作为正式文件读取入口，不再新开第二个 `view.py`。
- 使用标准库 `unittest` 做回归，不让验证依赖外部 `pytest` 安装。

### Risks
- `tools/view.sh` 仍是正式阅读规则的一部分，后续更改必须保持窄范围并继续回归验证。

### Verification
- `python3 -m py_compile tools/view.sh`
- `tools/view.sh AGENTS.md --from 1 --to 3`
- `python3 tools/view.sh AGENTS.md --from 1 --to 3`
- `python3 tools/view.sh AGENTS.md --lines 1:3`
- `tools/view.sh AGENTS.md --find '^## 0' --context 1`
- `python3 -m unittest -q tests.test_view_tool`

### Next Steps
- 后续如果再动文件读取策略，先跑这组 unittest，再改阅读协议。

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
- status: not_needed
- close_escalation: true

### Role Summary Evidence

### Source Threads

## Risks / Rollback
- Risks: 
- Rollback plan:
