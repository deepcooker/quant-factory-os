# TASK: fix placeholder RUN_ID introduced by PR #67

RUN_ID: run-2026-02-11-handoff-rule-fix-placeholder
OWNER: codex
PRIORITY: P1

## Goal
修复 PR #67 引入的占位符 RUN_ID（legacy placeholder token），恢复为真实 RUN_ID
`run-2026-02-11-handoff-rule`，避免污染后续接力与审计链路。

## Non-goals
- 不修改业务代码、脚本、测试。
- 不改 `docs/WORKFLOW.md` / `TASKS/STATE.md`，除非发现它们包含占位符路径引用。

## Acceptance
- [ ] repo 内不再存在该 legacy placeholder RUN_ID 字符串
- [ ] legacy placeholder reports 目录（已删除）不再存在
- [ ] 新目录 `reports/run-2026-02-11-handoff-rule/` 下 `meta.json`、`summary.md`、`decision.md` 三件套存在
- [ ] `TASKS/TASK-handoff-rule.md` 的 `RUN_ID` 与 Acceptance 中 reports 路径已同步修正为 `run-2026-02-11-handoff-rule`
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-handoff-rule-fix-placeholder/summary.md` and `reports/run-2026-02-11-handoff-rule-fix-placeholder/decision.md`

## Inputs
- `TASKS/TASK-handoff-rule.md`
- `reports/run-2026-02-11-handoff-rule/meta.json`
- `reports/run-2026-02-11-handoff-rule/summary.md`
- `reports/run-2026-02-11-handoff-rule/decision.md`

## Steps (Optional)
1. 创建本任务文件并运行 `make evidence RUN_ID=run-2026-02-11-handoff-rule-fix-placeholder`。
2. 修正 `TASKS/TASK-handoff-rule.md` 的 RUN_ID 与 reports 路径引用。
3. 复制旧 reports 内容到 `reports/run-2026-02-11-handoff-rule/` 三件套，再删除旧目录下三文件。
4. 用 `tools/view.sh` 对新旧路径做存在性门禁检查。
5. 运行 `make verify`，更新本 RUN_ID evidence 并 ship。

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
  - 旧路径删除不完整，导致占位符残留。
  - ship 时遗漏新目录文件，导致证据迁移不完整。
- Rollback plan:
  - 回滚本任务提交并按同一 RUN_ID 重新执行占位符修复。
