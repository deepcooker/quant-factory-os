# TASK: ship post-sync cleanliness

RUN_ID: run-2026-03-06-ship-post-sync-cleanliness
PROJECT_ID: project-0
STATUS: active

## Goal
修复 `tools/ship.sh` 在 PR 合并后因自身写入 `ship_state.json` 导致 post-ship sync 被脏工作区拦住的问题。

## Scope
- `tools/ship.sh`
- `tests/`
- `TASKS/`
- `reports/`
- `docs/`

## Acceptance
- [ ] merged PR 路径下不会被 `ship_state.json` 自身阻塞 post-ship sync
- [ ] 新增或刷新关键回归测试
- [ ] `make verify` 通过
- [ ] 更新 `reports/run-2026-03-06-ship-post-sync-cleanliness/summary.md`
- [ ] 更新 `reports/run-2026-03-06-ship-post-sync-cleanliness/decision.md`

## Notes
- 这个任务直接来源于真实 smoke：PR #166 已合并，但 post-ship sync 被 `reports/run-2026-03-06-task-ship-smoke/ship_state.json` 的本地改动阻塞。
