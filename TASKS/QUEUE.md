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
