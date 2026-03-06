# QUEUE

## Queue

- [x] TODO Title: slice-next: P0: 收敛 learn 的日常同频体验 - core delivery  Picked: run-2026-03-06-slice-next-p0-learn-core-delivery 2026-03-06T19:40:11+0800
  Goal: 当前合同直接把 learn 和 PROJECT_GUIDE 同频列为增量重点；结合最新 learn focus，下一步最合理的是继续收敛强同频输出和主线回拉体验：继续围绕当前 active run 收敛 learn 主线、流程边界和日常使用体验。
  Scope: `tools/learn.py`, `docs/PROJECT_GUIDE.md`, `docs/WORKFLOW.md`, `AGENTS.md`
  Acceptance:
  - [ ] deliver selected direction option `learn-daily-ergonomics` with bounded scope
  - [ ] command(s) pass: make verify
  - [ ] reports summary/decision updated for this run
  - [ ] owner docs updated in same run when behavior/rules changed
  - [ ] critical path regression tests added or refreshed
  - [ ] failure-path assertions are explicit and actionable
  - [ ] bash tools/legacy.sh review STRICT=1 AUTO_FIX=1 passes
  - [ ] decision records accepted tradeoffs and residual risks
  - [ ] Command(s) pass: `make verify`
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
  Slice: run_id=run-2026-03-05-ops-vnext-release task_id=slice-1
  Done: commit `8c0342c`

- [x] TODO Title: task ship safety: keep active run branch on task/ship handoff  Picked: run-2026-03-06-task-ship-branch-safety 2026-03-06T20:05:00+0800
  Goal: 修复 `tools/task.sh` / `tools/ship.sh` 在收尾时强制切到 `main` 导致活跃 run 分支和 Python-first 基线错位的问题。
  Scope: `tools/task.sh`, `tools/ship.sh`, `tests/`, `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] `tools/task.sh` 在活跃 run 分支上不会把收尾流程带到错误基线
  - [ ] `tools/ship.sh` 的分支切换策略与当前 run / branch continuity 一致
  - [ ] 新增或刷新关键回归测试
  - [ ] Command(s) pass: `make verify`
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
  Done: branch continuity defaulted to active base branch; review pass recorded in run-2026-03-06-task-ship-branch-safety

- [ ] TODO Title: vnext release baseline
  
- [x] TODO Title: task ship smoke: real task-to-ship continuity check  Picked: run-2026-03-06-task-ship-smoke 2026-03-06T20:18:00+0800
  Done: PR #166, RUN_ID=run-2026-03-06-task-ship-smoke
  Goal: 用一个最小无害改动真实演练 `tools/task.sh -> tools/ship.sh`，验证新的 branch continuity 策略不会把会话带到错误基线。
  Scope: `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] 真实执行 `tools/task.sh -> tools/ship.sh`
  - [ ] 发货前后 active branch continuity 符合预期
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

- [>] TODO Title: ship post-sync cleanliness: avoid self-dirty ship_state on merged PR flow  Picked: run-2026-03-06-ship-post-sync-cleanliness 2026-03-06T20:25:00+0800
  Goal: 修复 `tools/ship.sh` 在 PR 合并后因自身写入 `ship_state.json` 导致 post-ship sync 被脏工作区拦住的问题。
  Scope: `tools/ship.sh`, `tests/`, `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] merged PR 路径下不会被 `ship_state.json` 自身阻塞 post-ship sync
  - [ ] 新增或刷新关键回归测试
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
  Done: commit `4e5aed6`

- [x] TODO Title: ship post-sync smoke: real merged-PR sync continuity check  Picked: run-2026-03-06-ship-post-sync-smoke 2026-03-06T20:40:00+0800
  Done: PR #167, RUN_ID=run-2026-03-06-ship-post-sync-smoke
  Goal: 用一个最小无害改动真实演练 `tools/task.sh -> tools/ship.sh`，确认 merged PR 后 post-ship sync 不再被当前 run 的 `ship_state.json` 自身阻塞。
  Scope: `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] 真实执行 `tools/task.sh -> tools/ship.sh`
  - [ ] merged PR 后 post-ship sync 成功越过 `ship_state.json` 自脏点
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
  Goal: 进入开发设计阶段的新版本基线，保持流程最小可用并可继续迭代。
  Scope: `TASKS/`, `reports/`, `tools/`, `docs/`, `tests/`
  Acceptance:
  - [ ] `tools/*.py` 命令链可用
  - [ ] task/report 历史噪音已清理
  - [ ] 提交 PR
