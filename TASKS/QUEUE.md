# QUEUE

## Queue

- [x] TODO Title: tools orchestrator entry  Picked: run-2026-03-08-tools-orchestrator-entry 2026-03-08T12:10:00+0000
  Goal: 新增一个 Python 总入口，顺序编排 `tools` 研发流程调用，并提供统一 logging，让普通窗口可以通过单入口执行流程、输出逐行日志，便于 Codex 后续根据日志定位和修复问题。
  Scope: `tools/`, `Makefile`, `docs/WORKFLOW.md`, `TASKS/`, `reports/`
  Acceptance:
  - [x] 新增 Python 总入口脚本
  - [x] 总入口能顺序调用现有 `tools` 流程
  - [x] 总入口对每个流程有开始/结束/失败日志
  - [x] 子流程 stdout/stderr 每一行都被统一日志记录
  - [x] 关键方法带简洁注释
  - [x] `TASKS/STATE.md` 已绑定本次 task/run
  - [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
  - [x] 至少完成一次可执行验证

- [x] TODO Title: remove templates pivot  Picked: run-2026-03-08-remove-templates-pivot 2026-03-08T11:13:21+0000
  Goal: 删除 `templates/` 路线、`imports/` 内容、相关 project-repo / adoption 文档，以及当前仓库下全部测试文件，明确这条基建方向不再作为当前自动化 1.0 的继续路径。
  Scope: `templates/`, `imports/`, `docs/`, `TASKS/`, `reports/`, `tests/`
  Acceptance:
  - [x] 仓库内全部 `templates/` 文件已删除
  - [x] `imports/` 相关内容已删除
  - [x] `project repo / adoption` 相关文档已删除
  - [x] 仓库内全部测试文件已删除
  - [x] owner docs 不再把 `templates/` 或这组 project-repo 文档作为当前路线输出
  - [x] `TASKS/STATE.md` 已绑定本次 task/run
  - [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
  - [x] `make verify` 已执行并记录结果

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

- [x] TODO Title: vnext release baseline  Picked: run-2026-03-06-vnext-release-baseline 2026-03-06T21:20:00+0800
  
- [x] TODO Title: task ship smoke: real task-to-ship continuity check  Picked: run-2026-03-06-task-ship-smoke 2026-03-06T20:18:00+0800
  Done: PR #166, RUN_ID=run-2026-03-06-task-ship-smoke
  Goal: 用一个最小无害改动真实演练 `tools/task.sh -> tools/ship.sh`，验证新的 branch continuity 策略不会把会话带到错误基线。
  Scope: `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] 真实执行 `tools/task.sh -> tools/ship.sh`
  - [ ] 发货前后 active branch continuity 符合预期
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

- [x] TODO Title: ship post-sync cleanliness: avoid self-dirty ship_state on merged PR flow  Picked: run-2026-03-06-ship-post-sync-cleanliness 2026-03-06T20:25:00+0800
  Goal: 修复 `tools/ship.sh` 在 PR 合并后因自身写入 `ship_state.json` 导致 post-ship sync 被脏工作区拦住的问题。
  Scope: `tools/ship.sh`, `tests/`, `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] merged PR 路径下不会被 `ship_state.json` 自身阻塞 post-ship sync
  - [ ] 新增或刷新关键回归测试
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
  Done: commit `4e5aed6`

- [x] TODO Title: ship post-sync smoke: real merged-PR sync continuity check  Picked: run-2026-03-06-ship-post-sync-smoke 2026-03-06T20:40:00+0800
  Done: self-dirty `ship_state.json` no longer blocked post-ship sync; PR #167 exposed next gap at `pr_merge`
  Goal: 用一个最小无害改动真实演练 `tools/task.sh -> tools/ship.sh`，确认 merged PR 后 post-ship sync 不再被当前 run 的 `ship_state.json` 自身阻塞。
  Scope: `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] 真实执行 `tools/task.sh -> tools/ship.sh`
  - [ ] merged PR 后 post-ship sync 成功越过 `ship_state.json` 自脏点
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

- [x] TODO Title: ship pr-merge resilience: handle non-clean merge path without losing continuity  Picked: run-2026-03-06-ship-pr-merge-resilience 2026-03-06T20:55:00+0800
  Goal: 修复 `tools/ship.sh` 在 PR 已创建但 `gh pr merge` 遇到 non-clean merge 时的处理策略，确保错误可恢复且不污染本地 continuity。
  Scope: `tools/ship.sh`, `tests/`, `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] `pr_merge` 冲突路径有明确、可恢复、低副作用的处理策略
  - [ ] 新增或刷新关键回归测试
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
  Done: clear `pr_merge_blocked` guard added; review pass recorded in run-2026-03-06-ship-pr-merge-resilience

- [x] TODO Title: ship pr-merge recovery guidance  Picked: run-2026-03-06-ship-pr-merge-recovery-guidance 2026-03-06T21:55:00+0800
  Goal: 收紧 `tools/ship.sh` 在 `pr_merge_blocked` 之后的恢复指引，让 base-into-head 的冲突恢复路径更明确、低风险、可复制。
  Scope: `tools/ship.sh`, `tests/`, `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] `pr_merge_blocked` 输出包含明确的 base-into-head 恢复命令
  - [ ] `ship_state.json` 保留足够恢复上下文
  - [ ] 新增或刷新关键回归测试
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

- [x] TODO Title: automation 1.0 definition  Picked: run-2026-03-06-automation-1-0-definition 2026-03-06T22:05:00+0800
  Goal: 把“自动化 1.0”的成功定义正式落到 foundation repo 文档：明确它是面向业务项目交付的单入口目标、基座退后台、1.0 验收到交付为止，以及 foundation repo / business project repo 的分层关系。
  Scope: `docs/`, `AGENTS.md`, `TASKS/`, `reports/`
  Acceptance:
  - [ ] `Automation 1.0` 的成功定义形成正式文档
  - [ ] 文档与 `ENTITIES / WORKFLOW / PROJECT_GUIDE` 现有术语保持一致
  - [ ] 明确 1.0 到交付为止，不把运行迭代闭环算入当前验收
  - [ ] 明确 foundation repo 与 business project repo 的分层关系
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

- [ ] TODO Title: vnext release baseline  Picked: run-2026-03-11-vnext-release-baseline 2026-03-11T16:40:00+0000
  Goal: 进入开发设计阶段的新版本基线，保持流程最小可用并可继续迭代。
  Scope: `TASKS/`, `reports/`, `tools/`, `docs/`, `tests/`
  Acceptance:
  - [ ] `tools/*.py` 命令链可用
  - [ ] task/report 历史噪音已清理
  - [ ] 提交 PR

- [x] TODO Title: ship post-merge checkout cleanliness  Picked: run-2026-03-06-ship-post-merge-checkout-cleanliness 2026-03-06T16:00:00+0000
  Goal: 修复 `tools/ship.sh` 在 PR merged 后因当前 run 的 `ship_state.json` 未提交改动阻塞切回 base branch / post-ship sync 的问题。
  Scope: `tools/ship.sh`, `tests/`, `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] merged PR 后切回 base branch 的 sync 路径不会再被当前 run 的 `ship_state.json` 拦住

- [x] TODO Title: ship post-commit state cleanliness  Picked: run-2026-03-06-ship-post-commit-state-cleanliness 2026-03-06T16:05:00+0000
  Goal: 修复 `tools/ship.sh` 在 local commit 之后继续写成功态 `ship_state.json` 导致工作区重新变脏、阻塞 PR merge 与 post-ship sync continuity 的问题。
  Scope: `tools/ship.sh`, `tests/`, `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] local commit 之后的成功路径不再重写 tracked `ship_state.json`
  - [ ] PR create / merge / post-ship sync 不会再被当前 run 的 `ship_state.json` 未提交改动拦住
  - [ ] 新增或刷新关键回归测试
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

- [x] TODO Title: ship retry success-state cleanliness  Picked: run-2026-03-07-ship-retry-success-state-cleanliness 2026-03-07T00:06:00+0000
  Goal: 修复 `tools/ship.sh` 的 `run_with_retry_capture()` 在成功步骤统一重写 `ship_state.json` 的行为，确保 local commit 之后的成功路径不再通过 helper 隐式弄脏工作区。
  Scope: `tools/ship.sh`, `tests/`, `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] `run_with_retry_capture()` 的成功态 `ship_state` 写入可按阶段关闭
  - [ ] local commit 之后，helper 不再为 `push / pr_create / pr_state / sync_checkout_base` 等成功步骤重写 tracked `ship_state.json`
  - [ ] 新增或刷新关键回归测试
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

- [x] TODO Title: learn model packet finalization  Picked: run-2026-03-07-learn-model-packet-finalization 2026-03-07T00:40:00+0000
  Goal: 修复 `tools/learn.py` / `tools/codex_transport.py` 在 app-server 真实 plan 同频后未稳定落出 `learn/<project_id>.model.json` 的问题，确保 `ready` 能基于有效 model packet 继续通过。
  Scope: `tools/learn.py`, `tools/codex_transport.py`, `tests/`, `TASKS/`, `reports/`, `docs/`
  Acceptance:
  - [ ] app-server final-answer 事件可稳定产出可解析的 learn model packet
  - [ ] `learn/<project_id>.model.json` 在真实 `learn` 运行后稳定落盘
  - [ ] `python3 tools/ready.py` 在完成 `learn` 后恢复通过
  - [ ] 新增或刷新关键回归测试
  - [ ] `make verify` 通过
  - [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

- [x] TODO Title: learn final artifact persistence  Picked: run-2026-03-07-learn-final-artifact-persistence 2026-03-07T01:50:00+0000
  Goal: 修复真实 `learn -low/-daily` 完整输出后 `model.json` / `model.raw.txt` 仍未稳定落盘、导致 `ready` 不认账的问题。
  Scope: `tools/learn.py`, `tools/codex_transport.py`, `tests/`, `learn/`, `TASKS/`, `reports/`, `docs/`
  Note: Deferred by owner decision; keep as post-Automation-1.0 optimization.

- [x] TODO Title: business project repo skeleton  Picked: run-2026-03-07-business-project-repo-skeleton 2026-03-07T03:05:00+0000
  Goal: 定义 business project repo 最小骨架与单入口 `factory.py run` 的 v0 形态，作为自动化 1.0 接项目的下一步。
  Scope: `docs/AUTOMATION_1_0.md`, `docs/BUSINESS_PROJECT_REPO_V0.md`, `templates/business_project_repo_v0/`, `TASKS/`, `reports/`

- [x] TODO Title: project guide mainline reinforcement  Picked: run-2026-03-07-project-guide-mainline-reinforcement 2026-03-07T01:35:00+0000
  Goal: 在不改变题库骨架的前提下，把 `PROJECT_GUIDE.md` 进一步收紧成 `learn` 的高质量提问主课程，并先生成 `PROJECT_GUIDE_1.0_backup.md`。
  Scope: `docs/PROJECT_GUIDE.md`, `docs/PROJECT_GUIDE_1.0_backup.md`, `docs/WORKFLOW.md`, `AGENTS.md`, `TASKS/`, `reports/`
