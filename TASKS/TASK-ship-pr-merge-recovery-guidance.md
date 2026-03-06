# TASK: ship pr-merge recovery guidance

RUN_ID: run-2026-03-06-ship-pr-merge-recovery-guidance
PROJECT_ID: project-0
STATUS: active

## Goal
收紧 `tools/ship.sh` 在 `pr_merge_blocked` 之后的恢复指引，让 base-into-head 的冲突恢复路径更明确、低风险、可复制。

## Scope
- `tools/ship.sh`
- `tests/`
- `TASKS/`
- `reports/`
- `docs/`

## Acceptance
- [ ] `pr_merge_blocked` 输出包含明确的 base-into-head 恢复命令
- [ ] `ship_state.json` 保留足够恢复上下文
- [ ] 新增或刷新关键回归测试
- [ ] `make verify` 通过
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
