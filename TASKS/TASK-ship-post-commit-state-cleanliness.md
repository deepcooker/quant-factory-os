# TASK: ship post-commit state cleanliness

RUN_ID: run-2026-03-06-ship-post-commit-state-cleanliness
PROJECT_ID: project-0
STATUS: active

## Goal
修复 `tools/ship.sh` 在本地 commit 之后继续写成功态 `ship_state.json` 导致工作区重新变脏的问题，确保 `pr_created / merged / synced` 等成功路径不会破坏后续 PR merge 与 post-ship sync continuity。

## Scope
- `tools/ship.sh`
- `tests/`
- `TASKS/`
- `reports/`
- `docs/`

## Acceptance
- [ ] local commit 之后的成功路径不再重写 tracked `ship_state.json`
- [ ] PR create / merge / post-ship sync 不会再被当前 run 的 `ship_state.json` 未提交改动拦住
- [ ] 新增或刷新关键回归测试
- [ ] `make verify` 通过
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
