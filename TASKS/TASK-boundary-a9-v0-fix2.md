# TASK: add docs/BOUNDARY_A9.md (fix2)

RUN_ID: run-2026-02-11-boundary-a9-v0-fix2
OWNER: codex
PRIORITY: P1

## Goal
补齐 `docs/BOUNDARY_A9.md`，修复 `TASKS/STATE.md` 中 Boundary v0 入口悬空问题。
确保本次 PR 的变更范围明确包含该文件，避免再次出现“已合并但文件未进入提交”。

## Non-goals
- 不修改 `TASKS/STATE.md`。
- 不扩大改动到与本任务无关的代码、测试或文档。

## Acceptance
- [ ] `docs/BOUNDARY_A9.md` 必须出现在 PR 的“变更范围/涉及文件”里（否则禁止 ship）。
- [ ] `docs/BOUNDARY_A9.md` 仅包含 A/B/C/D 四章。
- [ ] A/B/C 每条规则末尾必须标注 `【出处：文件名】`；无证据内容只能进入 D。
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-boundary-a9-v0-fix2/summary.md` and `reports/run-2026-02-11-boundary-a9-v0-fix2/decision.md`（记录 why/what/verify）

## Inputs
- `TASKS/_TEMPLATE.md`
- `TASKS/STATE.md`
- `docs/WORKFLOW.md`
- `AGENTS.md`
- `Makefile`
- `tools/*.sh`
- `tests/*`

## Steps (Optional)
1. 创建任务与证据骨架：`make evidence RUN_ID=run-2026-02-11-boundary-a9-v0-fix2`
2. 新增 `docs/BOUNDARY_A9.md`（仅 A/B/C/D；A/B/C 每条附出处）
3. 用 `tools/view.sh` 回读 `docs/BOUNDARY_A9.md` 确认文件真实存在且内容完整
4. 运行 `make verify`
5. 更新 `reports/run-2026-02-11-boundary-a9-v0-fix2/summary.md` 与 `decision.md`
6. 通过 `RUN_ID=run-2026-02-11-boundary-a9-v0-fix2 tools/task.sh` ship

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
  - PR 提交阶段漏选 `docs/BOUNDARY_A9.md`，导致入口仍悬空。
  - 边界条目出处不充分，导致规则不可追溯。
- Rollback plan:
  - 若验证失败或内容不符合约束，回滚本次新增文档与任务文件后重做最小改动。
