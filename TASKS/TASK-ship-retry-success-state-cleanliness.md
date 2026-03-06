# TASK: ship retry success-state cleanliness

RUN_ID: run-2026-03-07-ship-retry-success-state-cleanliness
PROJECT_ID: project-0
STATUS: active

## Goal
修复 `tools/ship.sh` 的 `run_with_retry_capture()` 在成功步骤统一重写 `ship_state.json` 的行为，确保 local commit 之后的成功路径不再通过 helper 隐式弄脏工作区。

## Scope
- `tools/ship.sh`
- `tests/`
- `TASKS/`
- `reports/`
- `docs/`

## Acceptance
- [ ] `run_with_retry_capture()` 的成功态 `ship_state` 写入可按阶段关闭
- [ ] local commit 之后，helper 不再为 `push / pr_create / pr_state / sync_checkout_base` 等成功步骤重写 tracked `ship_state.json`
- [ ] 新增或刷新关键回归测试
- [ ] `make verify` 通过
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
