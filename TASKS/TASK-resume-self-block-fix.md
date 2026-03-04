# TASK: qf resume reliability: avoid self-block on checkout main

RUN_ID: run-2026-03-04-resume-self-block-fix
OWNER: <you>
PRIORITY: P0

## Goal
修复 `tools/qf resume` 在 merged PR 收尾时可能被自身产生的工作区改动卡住（`git checkout main` 失败），确保可稳定完成收尾同步。

## Scope (Required)
- `tools/qf`
- `tests/`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `TASKS/STATE.md`
- `reports/{RUN_ID}/`

## Non-goals
- 不改动 `tools/ship.sh` 主流程。
- 不重构 `resume` 的 PR 创建/合并策略。

## Acceptance
- [ ] 修复后 `tools/qf resume` 在 merged PR 场景不因自身日志写入而阻塞 `checkout main`
- [ ] 增加回归测试，覆盖“resume 前工作区因执行日志变脏”的场景
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `tools/qf`
- `tests/test_qf_current_run.py`
- `reports/run-2026-03-04-plan-execute-governance/ship_state.json`

## Steps (Optional)
1) 在 `cmd_resume` 的 `checkout main` 前增加防自阻塞保护。
2) 增加回归测试并跑 `make verify`。
3) 更新报告与文档并 ship。

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: 自动 stash 可能增加临时 stash 噪音。
- Rollback plan: 回滚本任务改动并恢复 `tools/qf` 到上一版行为。
