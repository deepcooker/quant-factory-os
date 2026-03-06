# TASK: ship post-sync smoke

RUN_ID: run-2026-03-06-ship-post-sync-smoke
PROJECT_ID: project-0
STATUS: active

## Goal
用一个最小无害改动真实演练 `tools/task.sh -> tools/ship.sh`，确认 merged PR 后 post-ship sync 不再被当前 run 的 `ship_state.json` 自身阻塞。

## Scope
- `TASKS/`
- `reports/`
- `docs/`

## Acceptance
- [ ] 真实执行 `tools/task.sh -> tools/ship.sh`
- [ ] merged PR 后 post-ship sync 成功越过 `ship_state.json` 自脏点
- [ ] `make verify` 通过
- [ ] 更新 `reports/run-2026-03-06-ship-post-sync-smoke/summary.md`
- [ ] 更新 `reports/run-2026-03-06-ship-post-sync-smoke/decision.md`

## Notes
- 这是第二次真实 smoke，不引入新的工具行为变更。
