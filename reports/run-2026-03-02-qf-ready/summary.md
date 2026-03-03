# Summary

RUN_ID: `run-2026-03-02-qf-ready`

## What changed
- Re-entered the `qf-ready` run via `tools/qf ready` and regenerated readiness/orientation artifacts.
- Confirmed direction `ready-exit-resolution`, then executed the full discussion workflow:
  - `choose -> council -> arbiter -> slice`
  - produced direction contract, multi-role review, execution contract, and slice state.
- Ran strict drift review and fixed run state pointer mismatch:
  - `TASKS/STATE.md` now points to `TASKS/TASK-qf-ready.md` for this run.
- Verified execution queue status:
  - `tools/qf do queue-next` reports no pending `- [ ]` tasks.
- Refreshed orientation output for next direction selection and stored session snapshots.

## Commands / Outputs
- `QF_ALLOW_RUN_ID_MISMATCH=1 tools/qf ready RUN_ID=run-2026-03-02-qf-ready`
  - sync pass, ready pass, 5 orient options generated
- `tools/qf choose RUN_ID=run-2026-03-02-qf-ready OPTION=ready-exit-resolution`
- `tools/qf council RUN_ID=run-2026-03-02-qf-ready`
- `tools/qf arbiter RUN_ID=run-2026-03-02-qf-ready`
- `tools/qf slice RUN_ID=run-2026-03-02-qf-ready`
  - tasks_total=3, queue_existing=3, queue_inserted=0
- `tools/qf review RUN_ID=run-2026-03-02-qf-ready STRICT=1 AUTO_FIX=1`
  - status=pass, blockers=0, warnings=0
- `tools/qf do queue-next`
  - no unfinished queue items (`- [ ]`)
- `tools/qf orient RUN_ID=run-2026-03-02-qf-ready`
  - regenerated 5 options, recommended `ready-exit-resolution`
- `make verify`
  - `109 passed in 30.22s`
- `tools/qf snapshot RUN_ID=run-2026-03-02-qf-ready NOTE=...` (twice)
- `make verify`
  - `109 passed in 30.29s`
- `tools/ship.sh "run-2026-03-02-qf-ready: close ready-exit-resolution direction cycle"`
  - failed at scope gate: missing task file (requires `SHIP_TASK_FILE`)
- `SHIP_TASK_FILE=TASKS/TASK-qf-ready.md tools/ship.sh "run-2026-03-02-qf-ready: close ready-exit-resolution direction cycle"`
  - failed at auth gate: `gh auth status` reports invalid token for `github.com`

## Notes
- Discussion and execution evidence separation is functioning: discussion outputs are under `SYNC/discussion/...`, execution artifacts are under `reports/run-2026-03-02-qf-ready/`.
- Current blocker is external auth (`gh` token invalid); ship cannot continue until re-authenticated.

## Iteration: ready/init output-mode hardening
- Added unified stage output primitives in `tools/qf`:
  - human-readable markers: `INIT_STEP[<i>/<n>]`, `READY_STEP[<i>/<n>]`
  - optional machine stream: `QF_EVENT_STREAM=1` emits JSONL `qf_event` lines to stdout.
- Updated `cmd_init`:
  - now prints 8 deterministic stage markers.
  - removed implicit `cleanup_pick_candidate_dirs` side effect from init path.
- Updated `cmd_ready`:
  - now prints 11 deterministic stage markers from run-context resolution to artifact output.
- Added regression tests:
  - `tests/test_qf_ready_gate.py::test_qf_ready_prints_step_markers_and_supports_json_stream`
  - `tests/test_qf_handoff.py::test_qf_init_keeps_pick_candidate_dirs_and_prints_steps`
- Updated owner docs:
  - `AGENTS.md` (stage marker + JSONL stream + init no hidden cleanup)
  - `docs/WORKFLOW.md` (S0/S2 visibility + stream flag)

## Verify (this iteration)
- `make verify`
  - `111 passed in 30.35s`

## Iteration: discuss shortcut + execute visibility
- Added `tools/qf discuss` as discussion-first shortcut:
  - default behavior runs `execute` pipeline with `TARGET=prepare`
  - chain: `orient -> choose -> council -> arbiter -> slice`
  - output stops before `do`, with explicit next command `tools/qf do queue-next`
- Enhanced `tools/qf execute` runtime visibility:
  - emits deterministic markers `EXECUTE_STEP[1/7] ... EXECUTE_STEP[7/7]`
  - reuses existing optional JSONL stream via `QF_EVENT_STREAM=1`
- Fixed readiness gate determinism:
  - `ready_file_is_valid` now prefers `ready.json.sync_gate.required` when present (fallback to env only if missing)
  - avoids env-drift false negatives when validating existing ready markers.
- Added regression tests:
  - `tests/test_qf_execute.py::test_qf_discuss_runs_to_prepare_and_generates_contract_chain`
  - `tests/test_qf_execute.py::test_qf_execute_prints_step_markers_and_json_stream`

## Verify (this iteration)
- `make verify`
  - `113 passed in 36.80s`

## Iteration: learn gate + ready aggregation cleanup
- Added `tools/qf learn` as onboarding/learning gate command (replacing planned `qualify` naming):
  - visible runtime markers: `LEARN_STEP[1/8] ... LEARN_STEP[8/8]`
  - aggregates sync + optional exam evidence and writes:
    - `reports/{RUN_ID}/learn.json`
    - `reports/{RUN_ID}/learn.md`
  - includes context digest + TTL to detect stale learning state.
- Updated `tools/qf ready` to enforce learn gate before execution readiness:
  - step flow is now `READY_STEP[1/12] ... READY_STEP[12/12]`
  - new behavior:
    - `QF_READY_REQUIRE_LEARN=auto` (default; enabled when sync gate enabled)
    - `QF_READY_AUTO_LEARN=1` auto-runs `tools/qf learn` if missing/expired
  - ready artifact now includes `learn_gate` status and prints `READY_LEARN_REPORT`.
- Updated `tools/qf sync` next-command hints:
  - if learn missing -> recommends `tools/qf learn`
  - low-friction suggestion now respects `learn -> ready -> execute` progression.
- Fixed learn digest stability bug:
  - removed `TASKS/STATE.md` from context digest inputs (it changes on state updates and caused false invalidation).
- Added/updated regression tests:
  - `tests/test_qf_sync_gate.py::test_qf_learn_generates_report_and_step_markers`
  - `tests/test_qf_sync_gate.py::test_qf_ready_requires_learn_when_enabled_and_auto_disabled`
  - `tests/test_qf_sync_gate.py::test_qf_ready_auto_runs_learn_when_missing`
  - updated existing sync/ready tests for new learn-first hints and ready step counts.
- Updated owner docs:
  - `AGENTS.md`: added learn gate rule and ready learn dependency.
  - `docs/WORKFLOW.md`: added `S1.6 Learn Gate`, sync-completion criterion, startup checklist order.

## Verify (this iteration)
- `make verify`
  - `116 passed in 39.97s`

## Iteration: init/run boundary cleanup
- Refined `init` run boundary to remove business `RUN_ID` creation:
  - when `CURRENT_RUN_ID` exists: init reuses it as context.
  - when missing: init uses session context only and prints:
    - `INIT_RUN_ID_SOURCE: session-context-only (init does not create business RUN_ID)`
    - `INIT_RUN_ID: (none)`
- `cmd_init` no longer emits execution event into a synthetic `run-*-qf-init` namespace when no active run exists.
- Added guardrail regression in `tests/test_qf_handoff.py`:
  - verifies init prints boundary markers
  - verifies no `reports/run-*-qf-init` directory is created.
- Updated owner docs to lock boundary rule:
  - `AGENTS.md`: init must not create business RUN_ID.
  - `docs/WORKFLOW.md`: S0 boundary clarification.

## Verify (this iteration)
- `make verify`
  - `116 passed in 39.92s`

## Iteration: learn `-log` output mirror
- Added `tools/qf learn -log` support:
  - command still prints live steps to terminal
  - same stdout is mirrored into `reports/{RUN_ID}/learn.stdout.log` by default
  - custom path supported: `LOG=<path>`
- Updated usage/help and learn argument parser accordingly.
- Added regression test:
  - `tests/test_qf_sync_gate.py::test_qf_learn_log_flag_writes_stdout_log`
- Updated owner docs:
  - `AGENTS.md` and `docs/WORKFLOW.md` now document `learn -log` behavior.

## Verify (this iteration)
- `make verify`
  - `117 passed in 40.97s`

## Iteration: decouple learn gate from RUN_ID
- Refactored `learn` gate to session scope:
  - learn artifacts moved from run namespace to session namespace:
    - `reports/session/learn.json`
    - `reports/session/learn.md`
    - `reports/session/learn.stdout.log` (for `-log`)
- `ready` now validates session learn gate (not `reports/<RUN_ID>/learn.json`).
- `sync` next-command hints now check session learn marker.
- `tools/qf learn` still accepts optional `RUN_ID=<context-run-id>` only as context source for sync/exam inputs; learn gate ownership is session-level.
- Updated docs:
  - `AGENTS.md`: learn output/log paths now session-scoped.
  - `docs/WORKFLOW.md`: S1.6 learn output/log and sync completion criteria updated.
- Updated regression tests:
  - `tests/test_qf_sync_gate.py` adjusted for session learn paths and ready learn-gate messaging.

## Verify (this iteration)
- `make verify`
  - `117 passed in 41.05s`

## Iteration: learn/run_id boundary (session-first)
- Refined `tools/qf learn` run binding semantics:
  - `RUN_ID` is now optional for learn.
  - learn no longer implicitly falls back to "latest report run" when run context is absent.
  - when run context exists: learn keeps using run evidence (`sync_report` + optional `exam-auto`).
  - when run context is absent: learn enters `session-direct-read` mode, reads required docs directly, and produces session learn evidence without run ownership.
- Added explicit runtime output for the new boundary:
  - `LEARN_SYNC_MODE: run-evidence | session-direct-read`
  - `LEARN_EXAM_BYPASS_NO_RUN_CONTEXT: true` (only when exam required but no run-context exam evidence is available)
- Kept artifacts session-scoped:
  - `reports/session/learn.json`
  - `reports/session/learn.md`
- Added regression tests for the new behavior:
  - `tests/test_qf_sync_gate.py::test_qf_learn_session_mode_without_run_context`
  - `tests/test_qf_sync_gate.py::test_qf_learn_session_mode_bypasses_exam_without_run_context`
- Updated owner docs for startup semantics:
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `SYNC/README.md`
  - `SYNC/READ_ORDER.md`

## Verify (this iteration)
- `make verify`
  - `119 passed in 42.02s`

## Final verify (post-doc alignment)
- `make verify`
  - `119 passed in 41.58s`

## Iteration: Slice A (`project_id` + learn path migration)
- Added `project_id` base model in runtime:
  - new resolver in `tools/qf`: `CURRENT_PROJECT_ID` from `TASKS/STATE.md` (default `project-0`).
  - mismatch guard added for explicit project overrides (`QF_ALLOW_PROJECT_ID_MISMATCH=1` escape hatch).
  - `update_state_current` now persists `CURRENT_PROJECT_ID`.
- Migrated learn artifacts to project/session namespace:
  - new primary path: `reports/projects/<project_id>/session/learn.json|learn.md|learn.stdout.log`.
  - backward-compatible read kept: legacy `reports/session/learn.json` still accepted for `project-0`.
  - ready gate now resolves learn by project (`resolve_learn_file_for_project`).
- Added `project_id` into key JSON artifacts:
  - `reports/<RUN_ID>/sync_report.json`
  - `reports/<RUN_ID>/ready.json`
  - `reports/<RUN_ID>/orient_choice.json`
  - `reports/<RUN_ID>/direction_contract.json`
  - `SYNC/discussion/<RUN_ID>/orient.json`
  - `SYNC/discussion/<RUN_ID>/council.json`
  - `reports/<RUN_ID>/execution_contract.json`
  - `reports/<RUN_ID>/slice_state.json`
- Updated docs for the new hierarchy and learn path:
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `docs/ENTITIES.md`
  - `SYNC/README.md`
  - `SYNC/READ_ORDER.md`
  - `TASKS/STATE.md` now includes `CURRENT_PROJECT_ID: project-0`.
- Updated tests:
  - `tests/test_qf_sync_gate.py` switched to new learn path, added legacy compatibility case.
  - `tests/test_qf_execute.py` seed state now includes `CURRENT_PROJECT_ID`.

## Verify (this iteration)
- `make verify`
  - `120 passed in 47.32s`

## Iteration: Slice B (`execute` contract-confirm orchestration gate)
- Upgraded `tools/qf execute` with execution contract confirmation before `TARGET=do`:
  - new flags:
    - `CONFIRM_CONTRACT=1` (one-shot manual confirm)
    - `AUTO_CONFIRM_CONTRACT=1` / `QF_EXECUTE_AUTO_CONFIRM_CONTRACT=1` (auto mode)
  - confirmation artifact:
    - `reports/<RUN_ID>/execution_contract_confirm.json` (includes `project_id`, `run_id`, `source`, timestamp)
  - behavior:
    - `TARGET=do` + no confirmation -> stop with:
      - `EXECUTE_NEEDS_CONTRACT_CONFIRM: true`
      - actionable next command with `CONFIRM_CONTRACT=1`
    - `TARGET=prepare` remains discussion-first and does not require confirmation to prepare.
- Propagated `PROJECT_ID` support through orchestrated commands:
  - `execute -> orient/choose/council/arbiter/slice` now forwards `PROJECT_ID`.
- Updated docs for new gate:
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `SYNC/README.md`
- Added regression coverage:
  - `tests/test_qf_execute.py`
    - `test_qf_execute_do_requires_contract_confirmation`
    - `test_qf_execute_prepare_writes_contract_confirmation_when_requested`
  - `tests/test_qf_orient_and_do.py`
    - updated auto-execute path to use `QF_EXECUTE_AUTO_CONFIRM_CONTRACT=1`.

## Verify (this iteration)
- `make verify`
  - `122 passed in 53.10s`

## Iteration: repository noise cleanup (reports/tasks/tests)
- Scope: remove non-current historical artifacts to reduce operational noise in baseline repo.
- Kept:
  - current run evidence: `reports/run-2026-03-02-qf-ready/`
  - current task contract: `TASKS/TASK-qf-ready.md`
  - active tests source files under `tests/*.py`
- Removed:
  - historical run reports: all `reports/run-*` except current run
  - legacy report dirs: `reports/archive`, `reports/session`
  - historical task contracts: all `TASKS/TASK-*.md` except current task
  - transient noise dirs: `.ipynb_checkpoints`, `tests/__pycache__`

## Verify (post-cleanup)
- `make verify`
  - `122 passed in 53.24s`

## Cleanup snapshot
- `reports` top-level dirs after cleanup: `reports/projects`, `reports/run-2026-03-02-qf-ready`
- `TASKS` key files after cleanup:
  - `TASKS/STATE.md`
  - `TASKS/QUEUE.md`
  - `TASKS/TASK-qf-ready.md`
  - templates (`_TEMPLATE.md`, `KNOWLEDGE_SYNC_TEMPLATE.md`, `TODO_PROPOSAL.md`)

## Iteration: learn 强同频 + 考试 v2 + Codex 操作手册
- 重构 `tools/qf learn`：
  - 支持 `MODEL_SYNC=auto|0|1`、`PLAN_MODE=strong|basic`、`MODEL_TIMEOUT_SEC`、`MODEL`。
  - 增加真实 Codex 模型同频链路（read-only + JSONL 事件流 + output-last-message）。
  - 增加主线锚点输出：`LEARN_MAINLINE` / `LEARN_CURRENT_STAGE` / `LEARN_NEXT_STEP` / `LEARN_REQUIRED_FILES_READ_LIST`。
  - 强模式增加口述与问答锚点：`LEARN_MODEL_PLAN_*`、`LEARN_MODEL_ORAL_*`。
  - 模型证据落盘：`learn.model.prompt/raw/json/events/stderr`。
  - 严格模式 `MODEL_SYNC=1` 下，模型同频失败会阻断 learn。
- 修复 `tools/qf learn MODEL_SYNC=1 ...` 被误判为 run_id 的参数解析问题。
- 重构同频考试体系（`SYNC/EXAM_*`）为 15+2 深度问卷：
  - 新题面：`SYNC/EXAM_PLAN_PROMPT.md`
  - 新模板：`SYNC/EXAM_ANSWER_TEMPLATE.md`
  - 新流程：`SYNC/EXAM_WORKFLOW.md`
  - 新评分：`SYNC/EXAM_RUBRIC.json`（pass_score=85）
- 升级 `tools/qf exam-auto`：当发现旧答卷格式时，自动迁移填充为新模板，避免 learn 自动链路被旧答卷阻塞。
- 新增 Codex 操作手册：`docs/CODEX_CLI_OPERATION.md`。
- 更新 owner docs 与同步层：
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `docs/PROJECT_GUIDE.md`
  - `README.md`
  - `SYNC/README.md`
  - `SYNC/READ_ORDER.md`
  - `SYNC/LINKS.md`
  - `SYNC/CURRENT_STATE.md`
  - `SYNC/SESSION_LATEST.md`
  - `SYNC/DECISIONS_LATEST.md`

## Runtime evidence
- `tools/qf learn -log`
  - 产出 `LEARN_MODEL_ORAL_*` 与 `LEARN_MODEL_PLAN_*` 锚点。
  - 产出模型证据文件 `reports/projects/project-0/session/learn.model.*`。
- `tools/qf ready`
  - 通过 learn/sync gate 并输出 `READY_STEP[1/12..12/12]`。
- `tools/qf sync`
  - 刷新 sync_report 并纳入 `docs/CODEX_CLI_OPERATION.md` 到必读链路。
- `tools/qf learn MODEL_SYNC=1 PLAN_MODE=strong -log`
  - 严格模型同频通过；`LEARN_SYNC_REQUIRED_READ: 18/18`。
- `make verify`
  - `123 passed in 55.36s`。
