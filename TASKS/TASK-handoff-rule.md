# TASK: solidify handoff hard rules (uncommitted changes do not exist; handoff via PR/commit + reports)

RUN_ID: run-2026-02-11-handoff-rule
OWNER: codex
PRIORITY: P1

## Goal
固化 handoff 硬规则，明确“未提交=不存在”以及“handoff 只能通过 PR/commit + reports/<RUN_ID>”。
确保规则入口在 `docs/WORKFLOW.md` 与 `TASKS/STATE.md` 中可直接定位。

## Non-goals
- 不修改任何代码、脚本、测试。
- 不触碰除 `docs/WORKFLOW.md`、`TASKS/STATE.md`、任务文件、`reports/<RUN_ID>/` 之外的文件。

## Acceptance
- [ ] `docs/WORKFLOW.md` 的 Memory & Context 明确包含三条 hard rule：
  - 未提交改动对其他 agent/cloud runs 不存在
  - handoff 仅通过 PR 或 commit hash，且证据在 `reports/<RUN_ID>/`
  - 本地上下文写入结构化证据或 `TASKS/STATE.md`，不写 chat
- [ ] `TASKS/STATE.md` 增加入口引用：Handoff hard rules -> `docs/WORKFLOW.md` Memory & Context
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-handoff-rule/summary.md` and `reports/run-2026-02-11-handoff-rule/decision.md`

## Inputs
- `TASKS/_TEMPLATE.md`
- `docs/WORKFLOW.md`
- `TASKS/STATE.md`

## Steps (Optional)
1. 创建任务文件并确认验收标准。
2. 运行 `make evidence RUN_ID=run-2026-02-11-handoff-rule`。
3. 最小改动更新 `docs/WORKFLOW.md` 与 `TASKS/STATE.md`。
4. 运行 `make verify` 并记录结果。
5. 更新 `reports/run-2026-02-11-handoff-rule/summary.md` 与 `decision.md`。
6. 运行 `RUN_ID=run-2026-02-11-handoff-rule tools/task.sh TASKS/TASK-handoff-rule.md` ship。

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
  - 改动超出限定文件范围，导致 ship 时被 `git add -u` 误带入。
  - 文案歧义导致 hard rule 可执行性不足。
- Rollback plan:
  - 仅回滚本任务涉及文件并重做最小改动。
