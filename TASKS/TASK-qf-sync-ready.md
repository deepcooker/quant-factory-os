# TASK: qf sync 自动同频 + ready 硬门禁 + 对话证据自动更新

RUN_ID: run-2026-03-01-qf-sync-ready
OWNER: <you>
PRIORITY: P1

## Goal
把同频阶段做成高自动化闭环：自动读取必读链路、自动生成同频报告、ready 强制校验同频完成，并在关键命令自动更新会话证据。

## Scope (Required)
- `tools/qf`
- `tests/`
- `docs/WORKFLOW.md`
- `AGENTS.md`
- `SYNC/`
- `TASKS/`
- `reports/{RUN_ID}/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [ ] 新增 `tools/qf sync`：自动读取必读文件并落盘 `reports/{RUN_ID}/sync_report.json` 与 `sync_report.md`，包含“已读文件清单、项目总况、宪法、工作流、技能查找入口、当前任务阶段、会话承接状态、下一条命令”。
- [ ] `tools/qf ready` 在缺失有效同频报告时不得通过；默认自动补跑同频后再写 `ready.json`（可通过开关关闭自动补跑）。
- [ ] `tools/qf plan` 在常见脏工作区（STATE/execution/report 变更）下不再反复卡住，保持低摩擦可用。
- [ ] `make verify` 通过；本 RUN 的 `reports/{RUN_ID}/summary.md` 与 `decision.md` 记录变更、验证和风险。

## Inputs
- Links / files / references
- If data is needed, specify allowed sample constraints (max rows, time window)

## Steps (Optional)
Suggested approach, if you have one.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
- Rollback plan:
