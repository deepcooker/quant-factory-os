# TASK: qf ready 讨论执行分离 + 强认知输出 + 多角色评审闭环

RUN_ID: run-2026-03-02-qf-ready
OWNER: <you>
PRIORITY: P1

## Goal
把 `ready` 升级为“先判定会话状态、再给方向、确认后执行”的决策中枢，并将讨论态与执行态证据彻底分层。

## Scope (Required)
- `tools/qf`
- `tests/`
- `docs/WORKFLOW.md`
- `docs/PROJECT_GUIDE.md`
- `docs/CODEX_CLI_OPERATION.md`
- `README.md`
- `AGENTS.md`
- `chatlogs/sync/`
- `TASKS/`
- `reports/{RUN_ID}/`
- `reports/projects/`

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [ ] `tools/qf ready` 在检测到上次 run 非完成态时，必须先给出“收尾（resume-close）/抛弃并新开（abandon-new）”决策，不得直接进入新方向。
- [ ] `ready` 输出固定包含：项目目标解读、宪法/工作流解读、证据链状态、session 承接状态、风险/阻塞、建议下一步。
- [ ] `ready` 通过后自动产出 3-5 个方向候选（含优先级/收益/风险/成本/依赖）并支持用户确认；用户确认前不写入 `reports/{RUN_ID}/` 执行证据。
- [ ] 确认方向后进入多角色评审（产品/架构/研发/测试）并产出统一执行契约；执行结束后自动做偏差审计（需求/实现/测试/文档）与必要修复。
- [ ] 文档更新为硬门禁：流程或规则变更若未同步 owner docs 和 run evidence，不能通过收尾。
- [ ] `make verify` 通过；新增回归测试覆盖“讨论态不入 report、确认后入 report、旧 run 决策分流”。

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
