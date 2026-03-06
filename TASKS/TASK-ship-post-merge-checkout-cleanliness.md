# TASK: ship post-merge checkout cleanliness

RUN_ID: run-2026-03-06-ship-post-merge-checkout-cleanliness
PROJECT_ID: project-0
STATUS: active

## Goal
修复 `tools/ship.sh` 在 PR 已 merge 后写入当前 run 的 `ship_state.json`，导致切回 base branch 做 post-ship sync 时被本地未提交改动拦住的问题。

## Scope
- `tools/ship.sh`
- `tests/`
- `TASKS/`
- `reports/`
- `docs/`

## Acceptance
- [ ] merged PR 后切回 base branch 的 sync 路径不会再被当前 run 的 `ship_state.json` 拦住
- [ ] 新增或刷新关键回归测试
- [ ] `make verify` 通过
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
