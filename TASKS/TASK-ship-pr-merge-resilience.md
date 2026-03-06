# TASK: ship pr-merge resilience

RUN_ID: run-2026-03-06-ship-pr-merge-resilience
PROJECT_ID: project-0
STATUS: active

## Goal
修复 `tools/ship.sh` 在 PR 已创建但 `gh pr merge` 遇到 non-clean merge 时的处理策略，确保错误可恢复且不污染本地 continuity。

## Scope
- `tools/ship.sh`
- `tests/`
- `TASKS/`
- `reports/`
- `docs/`

## Acceptance
- [ ] `pr_merge` 冲突路径有明确、可恢复、低副作用的处理策略
- [ ] 新增或刷新关键回归测试
- [ ] `make verify` 通过
- [ ] 更新 `reports/run-2026-03-06-ship-pr-merge-resilience/summary.md`
- [ ] 更新 `reports/run-2026-03-06-ship-pr-merge-resilience/decision.md`

## Notes
- 这个任务直接来源于第二次真实 smoke：`ship_state.json` 自脏问题已不再复现，但 PR #167 在 `pr_merge` 阶段因 merge commit 无法 clean 创建而失败。
