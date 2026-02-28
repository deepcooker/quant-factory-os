# QUEUE

Purpose: this is the "next-shot" queue for new Codex sessions. On startup, only
`TASKS/STATE.md` + `TASKS/QUEUE.md` are used to decide what to do next.

## Item format (minimum)
- Title
- Goal (one sentence)
- Scope (allowed files/directories)
- Acceptance (3 checks: verify, evidence, scope)
- Optional: RUN_ID (if omitted, generate at execution time)

## Queue

- [x] TODO Title: qf sync 自动同频 + ready 硬门禁 + 对话证据自动更新  Picked: run-2026-03-01-qf-sync-ready 2026-03-01T01:30:01+0800
  Done: local verify passed, RUN_ID=run-2026-03-01-qf-sync-ready
  Goal: 把同频阶段做成高自动化闭环：自动读取必读链路、自动生成同频报告、ready 强制校验同频完成，并在关键命令自动更新会话证据。
  Scope: `tools/qf`, `tests/`, `docs/WORKFLOW.md`, `AGENTS.md`, `SYNC/`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - [x] 新增 `tools/qf sync`：自动读取必读文件并落盘 `reports/{RUN_ID}/sync_report.json` 与 `sync_report.md`，包含“已读文件清单、项目总况、宪法、工作流、技能查找入口、当前任务阶段、会话承接状态、下一条命令”。
  - [x] `tools/qf ready` 在缺失有效同频报告时不得通过；默认自动补跑同频后再写 `ready.json`（可通过开关关闭自动补跑）。
  - [x] `tools/qf plan` 在常见脏工作区（STATE/execution/report 变更）下不再反复卡住，保持低摩擦可用。
  - [x] `make verify` 通过；本 RUN 的 `reports/{RUN_ID}/summary.md` 与 `decision.md` 记录变更、验证和风险。

- [x] TODO Title: qf exam-auto 默认自动填答并自动评分  Picked: run-2026-02-28-qf-exam-auto 2026-02-28T15:02:01+0800
  Done: PR #142, RUN_ID=run-2026-02-28-qf-exam-auto
  Goal: 让 `tools/qf exam-auto` 在答卷缺失时默认自动生成可评分答案并立刻评分，避免人工先填模板再重跑。
  Scope: `tools/qf`, `tests/`, `docs/WORKFLOW.md`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - [ ] `tools/qf exam-auto` 在缺答卷时默认不再返回 3，而是自动填答并产出 `sync_exam_result.json`。
  - [ ] 保留手动模式开关（可显式只生成模板不自动填答）。
  - [ ] 新增/更新回归测试覆盖“默认自动化”和“手动模式”两条路径。
  - [ ] `make verify` 通过，证据写入 `reports/{RUN_ID}/`。

- [x] TODO Title: qf resume 已合并场景避免重复创建 PR  Picked: run-2026-02-28-qf-resume-pr 2026-02-28T12:01:19+0800
  Done: PR #141, RUN_ID=run-2026-02-28-qf-resume-pr
  Goal: 当 `tools/qf resume` 读取到的 `ship_state` 对应 PR 已经 `MERGED` 时，直接走本地同步收尾，不再重复创建新 PR。
  Scope: `tools/qf`, `tests/`, `docs/WORKFLOW.md`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - [ ] 复现路径下（`ship_state` 已有 `pr_url` 且 PR 已合并），`tools/qf resume` 不再调用 `gh pr create`。
  - [ ] 仍完成 `checkout main + pull --rebase origin main`，并输出 `resume done`。
  - [ ] 新增/更新回归测试覆盖该分支逻辑。
  - [ ] `make verify` 通过，证据写入 `reports/{RUN_ID}/`。

- [x] TODO Title: tools/qf 三命令收敛：init/plan/do + git 自愈（sync/retry/resume）+ 临时产物隔离  Picked: run-2026-02-26-tools-qf-init-plan-do-git-sync-retry-resume 2026-02-26T16:28:23+0800
  Done: PR #109, RUN_ID=run-2026-02-26-tools-qf-init-plan-do-git-sync-retry-resume
  Goal: 将 enter/onboard/task/ship 收敛到一个产品级入口 `tools/qf`，固定为三命令 `init/plan/do`，并补齐 git 自愈与临时产物隔离。
  Scope: `tools/`, `tests/`, `docs/WORKFLOW.md`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - `tools/qf init` 处理 dirty（可恢复 stash）、强制 sync main、执行 doctor/onboard 并输出下一步提示。
  - `tools/qf plan [N]` 生成候选且不污染工作区；proposal 落在 `/tmp` 或 `reports/{RUN_ID}/` 并打印路径。
  - `tools/qf do queue-next` 在 plan 前置下自动领取任务并输出 `TASK_FILE`/`RUN_ID`/`EVIDENCE_PATH`。
  - 关键 git 步骤支持 retry/resume，失败记录写入 `reports/{RUN_ID}/ship_state.json`。
  - 临时产物隔离后不再污染工作区，`make verify` 全绿。




- [x] TODO Title: risk guardrail: recurring risk/rollback from decisions  Picked: run-2026-02-25-risk-guardrail-recurring-risk-rollback-from-decisions 2026-02-25T19:21:51+0800
  Done: PR #107, RUN_ID=run-2026-02-25-risk-guardrail-recurring-risk-rollback-from-decisions
  Goal: Aggregate recurring risk/rollback signals in recent decisions and add one preventive guardrail task.
  Scope: `TASKS/STATE.md`, `tests/`, `reports/{RUN_ID}/`
  Acceptance:
  - Guardrail task is queue-ready
  - make verify


- [x] TODO Title: 强化 tools/task.sh --plan：Queue 为空时生成 Suggested tasks（可复制入队）  Picked: run-2026-02-25-tools-task-sh-plan-queue-suggested-tasks 2026-02-25T13:15:27+0800
  Done: PR #105, RUN_ID=run-2026-02-25-tools-task-sh-plan-queue-suggested-tasks
  Goal: 当 Queue candidates 为 none 时，--plan 仍应基于 repo 证据（reports/*/decision.md、TASKS/STATE.md、可选 MISTAKES/）生成 10~20 条 Suggested tasks，并输出可直接粘贴的 QUEUE item 片段（含 Title/Goal/Scope/Acceptance 骨架），把“自动拿任务”真正做成单行可用。
  Scope: `tools/task.sh`, `tests/`, `docs/WORKFLOW.md`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - `tools/task.sh --plan 20` 生成的 `TASKS/TODO_PROPOSAL.md` 新增 `## Suggested tasks`：
    - Queue 为空时也至少产出 5 条建议
    - 每条包含可复制的 QUEUE item 片段（TODO Title/Goal/Scope/Acceptance）
  - Suggested tasks 的来源至少覆盖：
    - 最近 N 个 reports/run-*/decision.md（抓取 next/todo/suggest/风险/rollback 等信号）
    - TASKS/STATE.md（风险/未完成信号）
    - 若存在 MISTAKES/ 则读取其中 *.md（抓取 recurring issue/action）
  - docs/WORKFLOW.md 补充：Queue 为空时，用 Suggested tasks 选一条入队→再 --next/--pick
  - `make verify` 全绿


- [x] TODO Title: enter.sh 支持显式自动 stash（ENTER_AUTOSTASH=1）并打印 stash 名  Picked: run-2026-02-25-enter-sh-stash-enter-autostash-1-stash 2026-02-25T01:55:06+0800
  Done: PR #103, RUN_ID=run-2026-02-25-enter-sh-stash-enter-autostash-1-stash
  Goal: 解决单人开发常见摩擦：工作区不干净时 enter.sh 直接失败。新增显式开关 ENTER_AUTOSTASH=1，使 enter.sh 在同步前自动 git stash push -u，并打印 stash 名与恢复指令；默认行为保持严格失败。
  Scope: `tools/enter.sh`, `tests/`, `docs/WORKFLOW.md`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - 默认 enter.sh：工作区不干净仍失败（不改变安全默认）。
  - 设置 ENTER_AUTOSTASH=1 时：
    - 自动 stash（含 untracked），并打印：stash 名 + 如何恢复（git stash list / pop）
    - enter 正常继续 pull/doctor
  - make verify 全绿
  - docs/WORKFLOW.md 补充这一用法


- [x] TODO Title: 领取任务时自动 make evidence + 打印下一步清单（避免人肉步骤）  Picked: run-2026-02-25-make-evidence 2026-02-25T01:00:03+0800
  Done: PR #101, RUN_ID=run-2026-02-25-make-evidence
  Goal: 在 tools/task.sh --next 与 --pick queue-next 领取任务时自动生成 reports/{RUN_ID}/ 证据三件套，并打印标准下一步清单；若 evidence 失败则回滚 QUEUE 变更，避免出现 [>] 锁死需要手动修复。
  Scope: `tools/task.sh`, `tests/`, `docs/WORKFLOW.md`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - `tools/task.sh --next` 领取后默认自动执行 make evidence，并输出：TASK_FILE/RUN_ID/EVIDENCE_PATH + “下一步清单”。
  - `tools/task.sh --pick queue-next` 同样默认自动 evidence + 下一步清单。
  - 若 evidence 失败：QUEUE 不应从 `[ ]` 变为 `[>]`（自动回滚），并给出明确错误提示。
  - docs/WORKFLOW.md 补充：领取任务已自动生成 evidence，无需再手动 make evidence。
  - `make verify` 全绿。


- [x] TODO Title: ship 成功后自动同步本地 main 到最新（无需手动 enter）  Picked: run-2026-02-25-ship-main-enter 2026-02-25T00:46:47+0800
  Done: PR #99, RUN_ID=run-2026-02-25-ship-main-enter
  Goal: 解决单人开发“PR 合并后本地 main 不更新”的摩擦：在 tools/ship.sh 成功结束时强制执行 git 同步，把本地 main fast-forward/rebase 到 origin/main 最新，避免每次手动 ./tools/enter.sh 才看到最新队列与代码。
  Scope: `tools/`, `tests/`, `docs/`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - ship 成功后（PR 创建/合并流程结束），脚本会自动执行 sync：`git fetch` + `git checkout main` + `git pull --rebase origin main`，并打印同步后的 main HEAD。
  - 同步前若工作区不干净，明确报错并退出（不做隐式覆盖）。
  - 不引入额外慢检查：不调用 doctor/pytest（只做 git 同步）。
  - 更新 docs/WORKFLOW.md：说明“ship 后 main 已自动同步，本地无需再手动 enter 才能看到最新”。
  - `make verify` 全绿，并为该 RUN_ID 写齐 evidence 三件套。


- [x] TODO Title: 自动生成任务候选清单（plan）并支持确认后领取（pick）  Picked: run-2026-02-25-plan-pick 2026-02-25T00:19:46+0800
  Done: PR #97, RUN_ID=run-2026-02-25-plan-pick
  Goal: 新增非交互式“计划/确认”机制：Codex 根据 repo 证据与当前 QUEUE/STATE 生成 10~20 条候选任务清单供人确认；确认后可一键领取当前队列任务（串行接力），减少人肉写 queue/拼命令。
  Scope: `tools/`, `docs/`, `tests/`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - 新增命令：`tools/task.sh --plan N=20`（或默认 N=20）生成 `TASKS/TODO_PROPOSAL.md`，并在 stdout 打印摘要（top N + 如何 pick）。
  - 清单至少包含两块信息：
    1) 当前可执行的 QUEUE 候选（未完成项），标注“推荐下一枪”（queue-next）
    2) 从最近 reports/*/decision.md（可选含 MISTAKES/、STATE）提取的“建议新任务”（只做建议，不直接改 QUEUE）
  - 新增命令：`tools/task.sh --pick queue-next`：在已生成 proposal 的前提下，执行领取（等价于 `tools/task.sh --next`）并打印 TASK_FILE/RUN_ID；默认不自动写代码、不自动 ship。
  - 更新 docs/WORKFLOW.md：补充 plan/pick 的使用方式（用于 session 内串行接力）。
  - `make verify` 全绿，并为该 RUN_ID 写齐 evidence 三件套。


- [x] TODO Title: Session 一键初始化（onboard）+ 串行接下一枪（after-ship next）  Picked: run-2026-02-24-session-onboard-after-ship-next 2026-02-24T23:36:31+0800
  Done: PR #95, RUN_ID=run-2026-02-24-session-onboard-after-ship-next
  Goal: 新增一次-session 的自动入职/对齐脚本（同步+环境确认+必读清单+强制复述模板+最近 decision/PR 摘要），并在 ship 成功后自动提示下一枪命令（可选自动生成下一 TASK_FILE+RUN_ID，但不自动改代码）。
  Scope: `tools/`, `tests/`, `docs/`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - 新增入口：`tools/onboard.sh`（或 `make onboard`）可运行；输出包含：宪法/背景/阶段/工作流/复述模板/最近 decision 入口。
  - ship 成功后输出 “下一枪建议”：若 QUEUE 还有 `[ ]`，提示 `tools/task.sh --next`；可选：在开关启用时自动执行 `--next` 并打印 TASK_FILE/RUN_ID。
  - `make verify` 全绿，并为该 RUN_ID 写齐 evidence 三件套。


- [x] TODO Title: 修复 {RUN_ID} 占位符渲染 + 忽略 pytest 缓存确保工作区干净  Picked: run-2026-02-24-run-id-pytest 2026-02-24T22:27:17+0800
  Done: PR #93, RUN_ID=run-2026-02-24-run-id-pytest
  Goal: 将 repo 中用于文档/队列/模板的 `{RUN_ID}` 占位符替换为 `{RUN_ID}`（或转义为 `&lt;RUN_ID&gt;`），避免 Markdown 渲染吞字符；同时把 `.pytest_cache/` 加入 `.gitignore`，避免 doctor/pytest 造成工作区“脏”。
  Scope: `.gitignore`, `TASKS/QUEUE.md`, `TASKS/_TEMPLATE.md`, `docs/WORKFLOW.md`, `tests/`（如需补回归）
  Acceptance:
  - GitHub 渲染下不再出现 `reports//`、`RUN_ID=` 这种空洞显示（示例：QUEUE 与模板中的占位符可读）。
  - `tools/doctor.sh`（含 pytest）运行后，工作区保持干净（无未忽略的新增缓存文件）。
  - `make verify` 全绿。


- [x] TODO Title: 增加只读 Observer 周报（awareness digest）  Picked: run-2026-02-24-observer-awareness-digest 2026-02-24T21:21:37+0800
  Done: PR #91, RUN_ID=run-2026-02-24-observer-awareness-digest
  Goal: 新增只读观察器，从 repo 证据链（reports/*、TASKS/STATE.md、可选 MISTAKES/）生成周报报告，落到 reports/{RUN_ID}/awareness.md，形成可审计“学习产物”。
  Scope: `tools/`, `tests/`, `docs/`, `TASKS/`, `reports/{RUN_ID}/`
  Acceptance:
  - 新增入口：`make awareness RUN_ID={RUN_ID}`（或等价 tools/observe.sh）可运行。
  - 输出：`reports/{RUN_ID}/awareness.md`，并在 summary/decision 里引用。
  - 周报至少包含：本周 shipped runs（扫描 reports/run-*/decision.md）、重复失败模式（可选扫描 MISTAKES/）、当前风险（读 STATE）、下一枪建议（<=5 条、task-shaped）。
  - `make verify` 全绿。


- [x] TODO Title: auto-mark queue done on successful ship  Picked: run-2026-02-22-auto-mark-queue-done-on-successful-ship 2026-02-22T03:15:24+0800
  Done: PR #89, RUN_ID=run-2026-02-22-auto-mark-queue-done-on-successful-ship
  Goal: after a successful ship/PR open (and/or merge), automatically mark the picked `[>]` queue item as `[x]` and append `Done: PR #<n>, RUN_ID=<id>`.
  Scope: `tools/task.sh`, `tools/ship.sh` (if needed), `TASKS/QUEUE.md`, `tests/`
  Acceptance:
  - When shipping a task created by `--next`, the corresponding queue item is updated from `[>]` to `[x]` with Done metadata.
  - No effect if ship fails or no matching picked item exists.
  - `make verify` passes and evidence recorded under `reports/{RUN_ID}/`.
  RUN_ID: (optional)


- [x] TODO Title: bootstrap next: normalize Scope + validate scope bullets  Picked: run-2026-02-22-bootstrap-next-normalize-scope-validate-scope-bullets 2026-02-22T02:17:45+0800
  Goal: `tools/task.sh --next` must render Scope as one-path-per-bullet and fail fast if Scope cannot be parsed into valid bullets.
  Scope: `tools/task.sh`
  Acceptance:
  - Generated task Scope is multi-line bullets (each bullet is a single backticked path).
  - No non-path explanatory bullet is appended to Scope.
  - If Scope has no valid bullet paths, `--next` exits non-zero with a clear error.
  - `make verify` passes and evidence recorded under `reports/{RUN_ID}/`.
  RUN_ID: (optional)
  Done: PR #86, RUN_ID=run-2026-02-22-bootstrap-next-normalize-scope-validate-scope-bullets

- [x] TODO Title: add minimal regression tests for workflow gates (P1)
  Goal: cover scope gate / expected-files gate / single-run guard with small
  regression tests to prevent workflow regressions.
  Scope: ship/task tooling tests and minimal test fixtures.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)
  Done: PR #81, RUN_ID=run-2026-02-21-add-minimal-regression-tests-for-workflow-gates-p1

- [x] TODO Title: startup prints session entrypoints + active RUN_ID (P0)
  Goal: make `tools/start.sh` or `tools/enter.sh` print startup entrypoints
  (`TASKS/STATE.md`, `TASKS/QUEUE.md`, `docs/WORKFLOW.md`) and current `RUN_ID`.
  Scope: `tools/start.sh`, `tools/enter.sh`, startup docs/tests only as needed.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)
  Done: PR #78, RUN_ID=run-2026-02-21-startup-entrypoints-runid

- [x] TODO Title: ENTITIES.md minimal dictionary sync (P1)
  Goal: ensure `docs/ENTITIES.md` has minimal definitions for existing entities:
  Task, PR, RUN_ID, Evidence, STATE, MISTAKES, Gate, Tool.
  Scope: `docs/ENTITIES.md` and narrowly related docs references if required.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)
  Done: PR #77, RUN_ID=run-2026-02-12-entities-min-dict

- [x] TODO Title: ship allowlist includes docs
  Goal: update `tools/ship.sh` so untracked allowlist includes `docs/*`.
  Scope: `tools/ship.sh`, tests/docs directly related to this rule.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)

- [x] TODO Title: ship expected-files gate
  Goal: add expected-files guard so ship validates task-declared allowed files.
  Scope: ship/task tooling and related workflow docs/tests.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)

- [x] TODO Title: add `.codex_read_denylist` baseline
  Goal: add default read denylist to reduce noisy context snapshots.
  Scope: `.codex_read_denylist` and minimal workflow docs references only.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)
  
- [x] TODO Title: queue pick lock (in-progress marker)
  Goal: when `tools/task.sh --next` picks the top item, mark it as in-progress (`[>]`) and record RUN_ID+timestamp to avoid duplicate picks across sessions.
  Scope: `tools/task.sh`, `TASKS/QUEUE.md`, minimal tests for queue parsing/locking.
  Acceptance:
  - Picking changes `[ ]` -> `[>]` and appends `Picked: {RUN_ID} <timestamp>`.
  - Re-running `--next` does not pick the same `[>]` item again.
  - `make verify` passes and evidence recorded under `reports/{RUN_ID}/`.
  RUN_ID: (optional)
