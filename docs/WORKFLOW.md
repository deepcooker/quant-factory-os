# WORKFLOW

Standard start

This document describes the expected workflow for changes in this repository.

## Document ownership
- Session entrypoint owner: `SYNC/READ_ORDER.md`
- Hard rules owner: `AGENTS.md`
- Execution details owner: `docs/WORKFLOW.md` (this file)
- Entity definitions owner: `docs/ENTITIES.md`
- Strategy/vision owner: `docs/PROJECT_GUIDE.md`
- Codex operation owner: `docs/CODEX_CLI_OPERATION.md`

## Session lifecycle state machine (single source)
- `S-1 Discussion-only` (optional)
  - Allowed only for read-only clarification/investigation.
  - Constraint: no repo mutation (no file edits, no generated artifacts, no ship).
  - Exit: before any mutation, bind to active `TASKS/TASK-*.md` + `RUN_ID`.
- `S0 Environment`: `tools/qf init`
  - Input: local repo checkout
  - Output: synced main + doctor checks + onboard summary
  - Note: this is environment preparation only, not readiness pass.
  - Output visibility: prints `INIT_STEP[<i>/<n>]` stage markers.
  - Safety: no implicit cleanup of `reports/run-*-pick-candidate` directories.
  - Boundary: init does not create a new business `RUN_ID`; it uses `CURRENT_RUN_ID` when present, otherwise session context only.
  - Project context: reads `CURRENT_PROJECT_ID` from `TASKS/STATE.md` (defaults to `project-0`).
  - Continuing runs: auto-handoff is executed by default (`QF_INIT_AUTO_HANDOFF=1`).
- `S1 Handoff`: `tools/qf handoff`
  - Input: `CURRENT_RUN_ID` (or explicit RUN_ID)
  - Output: `reports/{RUN_ID}/handoff.md`
  - Note: this is context reconstruction only, not readiness pass.
  - Format: concise session summary (main thread, key conclusions, small reflection, one next command).
- `S1.5 Sync Evidence`: `tools/qf sync`
  - Input: `SYNC/READ_ORDER.md` + required governance/startup files.
  - Output: `reports/{RUN_ID}/sync_report.json` + `reports/{RUN_ID}/sync_report.md`.
  - Gate: marks whether required sync files are all present/readable (`sync_passed`).
- `S1.6 Learn Gate`: `tools/qf learn`
  - Input: valid sync report; optional exam auto-flow (`tools/qf exam-auto`).
  - Output: `reports/projects/{project_id}/session/learn.json` + `reports/projects/{project_id}/session/learn.md`.
  - Output visibility: prints `LEARN_STEP[<i>/<n>]` stage markers.
  - Optional stdout mirror: `tools/qf learn -log` writes `reports/projects/{project_id}/session/learn.stdout.log` (or `LOG=<path>`).
  - Optional model sync (Codex real interaction):
    - `MODEL_SYNC=0|auto|1` (default `auto`)
    - strict mode: `MODEL_SYNC=1` (learn fails if model sync fails)
    - `PLAN_MODE=strong|basic` (default `strong`)
    - timeout/model override: `MODEL_TIMEOUT_SEC=<n>` (default 180), `MODEL=<slug>`
    - model artifacts:
      - `learn.model.prompt.txt`
      - `learn.model.raw.txt`
      - `learn.model.json`
      - `learn.model.events.jsonl`
      - `learn.model.stderr.log`
  - Required learn anchors:
    - `LEARN_MAINLINE`, `LEARN_CURRENT_STAGE`, `LEARN_NEXT_STEP`, `LEARN_REQUIRED_FILES_READ_LIST`
    - when model sync passes:
      - `LEARN_MODEL_MAINLINE`, `LEARN_MODEL_CURRENT_STAGE`, `LEARN_MODEL_NEXT_STEP`, `LEARN_MODEL_FILES_READ_LIST`
    - when `PLAN_MODE=strong` and model sync passes:
      - `LEARN_MODEL_PLAN_GOAL`, `LEARN_MODEL_PLAN_NON_GOAL`, `LEARN_MODEL_PLAN_REBUTTAL`, `LEARN_MODEL_PLAN_DECISION_STOP`
      - `LEARN_MODEL_ORAL_PROJECT`, `LEARN_MODEL_ORAL_CONSTITUTION`, `LEARN_MODEL_ORAL_EVIDENCE`, `LEARN_MODEL_ORAL_SESSION`
      - `LEARN_MODEL_ORAL_CURRENT_FOCUS`, `LEARN_MODEL_ORAL_NEXT_ACTION`, `LEARN_MODEL_ORAL_EXAM_QA_COUNT`
  - Purpose: materialize onboarding understanding (project/constitution/workflow/skills/session) with exam evidence.
- `S2 Ready gate`: `tools/qf ready`
  - Input: restatement fields (goal/scope/acceptance/steps/stop)
  - Output: `reports/{RUN_ID}/ready.json`
  - Output visibility: prints `READY_STEP[<i>/<n>]` stage markers.
  - Machine-readable stream (optional): `QF_EVENT_STREAM=1` emits JSONL step events to stdout.
  - Learn dependency: `QF_READY_REQUIRE_LEARN=auto` (default) enforces learn gate when sync gate is enabled.
    - auto recovery: `QF_READY_AUTO_LEARN=1` auto-runs `tools/qf learn` when learn evidence is missing/expired.
  - Sync dependency: requires valid `sync_report.json`; default auto-runs `tools/qf sync` if missing (`QF_READY_AUTO_SYNC=1`).
  - Low-friction mode: fields auto-fill from active task contract by default (`QF_READY_AUTO=1`).
  - Exit resolution gate: if unresolved run context is detected, must choose:
    - `DECISION=resume-close` (run `tools/qf resume`)
    - `DECISION=abandon-new` (continue new direction cycle)
  - Resolution persistence: `abandon-new` is stored in `ready.json` for the same RUN to avoid repeated prompts on subsequent `ready`.
  - Ready also writes discussion brief to `SYNC/discussion/{RUN_ID}/ready_brief.json|md`.
  - Gate: `tools/qf do` must fail without valid `ready.json`.
- `S2.4 Plan protocol gate` (discussion-first, required for complex changes)
  - Interactive planning command: Codex `/plan` (not `tools/qf plan`).
  - Required output packet (strong): goal/non-goal/evidence/alternatives/rebuttal/decision+stop-condition.
  - Confirmation: plan must be explicitly accepted before entering execution target.
  - Evidence sink: record final accepted plan into run evidence (`direction_contract` / `execution_contract` / `decision.md`).
- `S2.5 Direction gate`: `tools/qf orient` + `tools/qf choose`
  - Input: `docs/PROJECT_GUIDE.md` + governance docs + state/evidence.
  - Output:
    - discussion draft: `SYNC/discussion/{RUN_ID}/orient.json|md`
    - confirmed decision: `reports/{RUN_ID}/orient_choice.json`
    - direction contract: `reports/{RUN_ID}/direction_contract.json|md`
  - Purpose: confirm direction/priority before execution queue pick.
- `S2.6 Council gate`: `tools/qf council`
  - Input: `orient_choice.json` + `direction_contract.json`
  - Output: `SYNC/discussion/{RUN_ID}/council.json|md`
  - Purpose: product/architect/dev/qa independent review before convergence.
  - Rule: council output must be evidence-based (sync/ready/scope/verify/docs/queue pressure checks), not static templates.
- `S2.7 Arbiter gate`: `tools/qf arbiter`
  - Input: `council.json` + `direction_contract.json`
  - Output: `reports/{RUN_ID}/execution_contract.json|md`
  - Purpose: converge independent views into one executable contract.
  - Rule: execution slices must reflect council blockers/warnings/role conditions.
- `S2.8 Slice gate`: `tools/qf slice`
  - Input: `execution_contract.json`
  - Output:
    - `reports/{RUN_ID}/slice_state.json`
    - queue insertion into `TASKS/QUEUE.md` (idempotent by slice marker)
  - Purpose: turn contract into smallest executable queue tasks.
- `S2.9 Discuss shortcut`: `tools/qf discuss`
  - Purpose: one command to run discussion chain (`orient/choose/council/arbiter/slice`) and stop before execution.
  - Default target: `prepare` (prints `EXECUTE_STATUS: prepared` + next do command).
- `tools/qf plan [N]` (legacy helper)
  - Purpose: generate `TASKS/TODO_PROPOSAL.md` queue suggestions only.
  - Non-goal: this command is not the planning gate and does not authorize execution.
- `S3 Execute`: `tools/qf do queue-next`
  - Input: valid gates (`ready.json` + `orient_choice.json` + `council.json` + `execution_contract.json` + `slice_state.json`)
  - Output: task pick + evidence skeleton + execution trace updates
  - Task pick command: `tools/task.sh --next` (no `plan 20` dependency in critical path)
  - Queue pick policy: prefer unchecked item whose `Slice: run_id=<CURRENT_RUN_ID>` matches `TASKS/STATE.md`; fallback to first unchecked item.
  - Auto checkpoint: runs `tools/qf review RUN_ID=<picked-run> AUTO_FIX=1 NON_BLOCKING=1` to emit drift report early.
- `S2.5~S3 Orchestrator (optional)`: `tools/qf execute`
  - Purpose: low-friction single command to advance gate chain and execute.
  - Output visibility: prints `EXECUTE_STEP[<i>/<n>]` stage markers.
  - Default behavior: if no confirmed option, stop with actionable choose command.
  - Contract confirm gate for execution:
    - `TARGET=do` requires `reports/{RUN_ID}/execution_contract_confirm.json`.
    - quick confirm command: `tools/qf execute RUN_ID=<run-id> PROJECT_ID=<project-id> CONFIRM_CONTRACT=1 TARGET=do`.
    - automation mode: `QF_EXECUTE_AUTO_CONFIRM_CONTRACT=1 tools/qf execute`.
  - Auto mode: `QF_EXECUTE_AUTO_CHOOSE=1 tools/qf execute` uses orient recommended option and continues through `council->arbiter->slice->do`.
- `S3.5 Review`: `tools/qf review`
  - Input: run evidence (`summary/decision/ready/choice/contract`) and optional flags (`AUTO_FIX`, `STRICT`).
  - Output: `reports/{RUN_ID}/drift_review.json|md`; blockers additionally write `SYNC/discussion/{RUN_ID}/drift_todo.md`.
  - Gate: strict mode blockers must be resolved before ship.
- `S4 Ship`: `tools/ship.sh` (or `make ship`)
  - Input: verified diff + in-scope task contract
  - Output: PR + merge + main sync
- `S5 Learn`: reports/mistakes updates
  - Input: execution and verification outcomes
  - Output: durable memory for next session handoff.

## Evidence minimum fields
- Required run evidence files: `reports/{RUN_ID}/meta.json`, `summary.md`, `decision.md`.
- `meta.json` minimum gate fields:
  - `run_id`
  - `task_id`
  - `stop_reason`
  - `commands_run`
  - `artifacts`
- Full schema ownership: `docs/ENTITIES.md`.

## Status snapshot rule
Before each ship, record `/status` output in the evidence for the active RUN_ID.

## File list rule
`project_all_files.txt` is a local generated artifact and is excluded from PRs by
default. Update it only with a dedicated task, and call out the change in the PR
body.

## Scope gate rule
Task files must declare a `## Scope` section with allowed change paths. `tools/ship.sh`
validates staged files against this declared scope by default.

## Context snapshot (for ChatGPT)
`project_all_files.txt` is a context index snapshot for external models. It is
not evidence and does not belong in PRs by default. If it must be updated,
create a dedicated task, set `SHIP_ALLOW_FILELIST=1`, and use
`git add -f project_all_files.txt`.

## Memory & Context (handoff rules)
- The following hard rules are handoff gates and apply to every delivery.
- Do not store full chat transcripts or raw logs in the repo. Keep them local
  under `chatlogs/` and ensure it is listed in `.gitignore`.
- Preferred startup for full local transcript fallback:
  - `./tools/start.sh` (default `START_SESSION_LOG=1`)
  - optional controls:
    - `START_SESSION_LOG=0` disable transcript logging
    - `START_SESSION_LOG_FILE=/abs/path/session.log` set explicit log file path
- For anti-loss fallback, store concise session checkpoints in
  `reports/{RUN_ID}/conversation.md` via:
  - `tools/qf snapshot RUN_ID=<run-id> NOTE="decision/next-step summary"`
- `/compact` policy:
  - Use when conversation/context becomes large or when moving to a new milestone.
  - Not a mandatory "every task" gate.
  - Always snapshot first, then compact.
- `tools/qf do` / `tools/qf resume` 自动记录执行轨迹到
  `reports/{RUN_ID}/execution.jsonl`（默认脱敏，可审计）。
- `tools/qf sync` / `tools/qf ready` / `tools/qf orient` / `tools/qf choose` /
  `tools/qf council` / `tools/qf arbiter` / `tools/qf slice` 默认写入
  `reports/{RUN_ID}/conversation.md` checkpoint（可用 `QF_AUTO_CONVERSATION=0` 关闭）。
- Discussion drafts are intentionally separated from execution evidence:
  - pre-confirmation drafts in `SYNC/discussion/{RUN_ID}/`
  - post-confirmation execution evidence in `reports/{RUN_ID}/`
- 断线恢复建议先生成接班摘要：
  - `tools/qf handoff RUN_ID=<run-id>` -> `reports/{RUN_ID}/handoff.md`
- Repo memory is limited to: `docs/` (rules), `TASKS/STATE.md` (current state),
  `reports/{RUN_ID}/decision.md` (key decisions), and `MISTAKES/` (postmortems
  when enabled).
- When sharing code with an external model, use `project_all_files.txt` as the
  context snapshot. It is ignored by default and must only be updated via a
  dedicated task with explicit approval to commit.
- Hard rule (gate): Uncommitted changes do not exist for other agents or cloud runs.
- Hard rule (gate): Handoff must be via PR or commit hash, with evidence under
  `reports/{RUN_ID}/`.
- Hard rule (gate): If local-only context is needed, record it as structured evidence
  (`summary.md`, `decision.md`, `MISTAKES/`) or in `TASKS/STATE.md`, not in chat.
- `TASKS/STATE.md` is the source-of-truth for `CURRENT_PROJECT_ID` and `CURRENT_RUN_ID`.

## Sync completion criteria (must be true before execution)
- `tools/qf init` completed successfully.
- `tools/qf handoff` completed for continuing runs (auto by init unless explicitly disabled).
- `tools/qf sync` produced valid `reports/{RUN_ID}/sync_report.json`.
- `tools/qf learn` produced valid `reports/projects/{project_id}/session/learn.json` (`RUN_ID` optional).
- `tools/qf ready` produced `reports/{RUN_ID}/ready.json`.
- `tools/qf orient` produced `SYNC/discussion/{RUN_ID}/orient.json`.
- `tools/qf choose` produced `reports/{RUN_ID}/orient_choice.json`.
- `tools/qf council` produced `SYNC/discussion/{RUN_ID}/council.json`.
- `tools/qf arbiter` produced `reports/{RUN_ID}/execution_contract.json`.
- `tools/qf slice` produced `reports/{RUN_ID}/slice_state.json`.
- `tools/qf do queue-next` requires all gates above and then picks via `tools/task.sh --next`.
- `tools/task.sh --next` prioritizes queue blocks that match `CURRENT_RUN_ID` slice marker before generic first-unchecked fallback.
- Optional shortcut: `tools/qf execute` can run the same chain with explicit/auto option strategy.

## Codex session startup checklist
- Do not rely on chat/session memory; rely only on repo memory:
  `TASKS/STATE.md`, `TASKS/QUEUE.md`, `reports/{RUN_ID}/`.
- First read owner entrypoint: `SYNC/READ_ORDER.md`.
- Codex 参数/模式参考：`docs/CODEX_CLI_OPERATION.md`。
- Preferred entrypoint: `tools/qf` (`init/sync/learn/ready/orient/choose/council/arbiter/slice/execute/do/review/resume`).
- Compatibility wrappers: `tools/enter.sh` and `tools/onboard.sh` forward to `tools/qf`.
- 1) 运行 `tools/qf init`（自动 stash 可恢复 + sync main + doctor + onboard）。
- 1.0) 若希望在终端消费结构化日志，可设置 `QF_EVENT_STREAM=1`（stdout 会追加 JSONL 事件）。
- 1.1) 可选清理历史临时 stash：先预览 `tools/qf stash-clean`，确认后执行 `tools/qf stash-clean apply KEEP=0`。
- 2) 若为接力会话（`CURRENT_RUN_ID` 已存在），`tools/qf init` 默认自动执行 `handoff`。
- 2.1) 如需手动控制，可用：`QF_INIT_AUTO_HANDOFF=0 tools/qf init` 后再手动 `tools/qf handoff`。
- 3) 按 `SYNC/READ_ORDER.md` 顺序完成阅读与复述。
- 3.1) 运行 `tools/qf sync` 固化同频证据（读文件清单/项目总况/治理入口/当前阶段/下一步）。
- 3.2) 新/陌生 agent 建议先完成同频考试：
  - v2 深度题面：`SYNC/EXAM_PLAN_PROMPT.md`（15+2 问卷）
  - 按 `SYNC/EXAM_ANSWER_TEMPLATE.md` 输出到 `reports/{RUN_ID}/onboard_answer.md`
  - 用 `tools/sync_exam.py` 评分，结果写入 `reports/{RUN_ID}/sync_exam_result.json`
  - 低摩擦首选：`tools/qf exam-auto`（默认缺答卷会自动填答并直接评分）
  - 手动模式：`tools/qf exam-auto AUTO_FILL=0`（只落模板，不自动填答）
  - 兼容命令：`tools/qf exam`（只做评分，不自动生成答卷）
- 3.3) 运行 `tools/qf learn` 固化“上岗学习”证据（项目+宪法+工作流+技能+session+考试），默认打印分步日志。
  - `RUN_ID` 可选：
    - 有 `RUN_ID`/`CURRENT_RUN_ID`：复用该 run 的 `sync/exam` 证据。
    - 无 run 上下文：进入 `session-direct-read`，直接读取必读文档并生成 learn 证据（不隐式绑定历史 run）。
  - `project_id` 默认来自 `TASKS/STATE.md: CURRENT_PROJECT_ID`（缺省 `project-0`），也可通过环境变量覆盖：`PROJECT_ID` / `QF_PROJECT_ID`。
    - 无 run 上下文且不存在 session exam 结果时，会打印 `LEARN_EXAM_BYPASS_NO_RUN_CONTEXT: true` 并降级为“仅文档同频门禁”。
- 4) 运行 `tools/qf ready` 完成复述上岗门禁（默认绑定 `CURRENT_RUN_ID`，默认可自动填充；默认缺失 learn/sync 时可自动补跑）。
- 4.0) 若 `ready` 提示 unresolved run context，先二选一：
  - `tools/qf resume RUN_ID=<run-id>`（收尾）
  - `tools/qf ready RUN_ID=<run-id> DECISION=abandon-new`（明确抛弃旧上下文后继续）
- 4.1) 运行 `tools/qf orient` 生成方向候选与优先级（L1 方向层）。
- 4.2) 运行 `tools/qf choose OPTION=<id>` 确认方向后再进入执行层（L2）。
- 4.2.1) 运行 `tools/qf council` 生成产品/架构/研发/测试独立评审结果（讨论态）。
- 4.2.2) 运行 `tools/qf arbiter` 收敛为统一执行契约（执行态）。
- 4.2.3) 运行 `tools/qf slice` 把执行契约拆成最小 queue tasks（幂等入队）。
- 4.2.4) 低摩擦讨论收敛可用：`tools/qf discuss`（默认停在 prepare，不直接 do）。
- 4.3) 在关键决策点执行 `tools/qf snapshot NOTE="..."`，把“本轮结论/下一步”写入仓库证据，避免会话丢失。
- 5) 运行 `tools/qf do queue-next` 领取下一枪（内部强制 ready + choose + council + arbiter + slice 前置；并自动产出一次 non-blocking drift review）。
- 5.0) 低摩擦可选：`tools/qf execute`
  - 默认在缺少方向确认时停在 choose（保留人工确认）
  - 自动推进模式：`QF_EXECUTE_AUTO_CHOOSE=1 tools/qf execute`
- 5.1) 需求执行完成后，显式运行 `tools/qf review RUN_ID=<run-id> STRICT=1 AUTO_FIX=1`，清空 blocker 后再 ship。
- 6) Expand that item into `TASKS/TASK-*.md` (from template), then run:
  implement minimal diff -> `make verify` -> update reports -> `tools/task.sh` ship.
- Ship failure recovery: `tools/ship.sh` writes `reports/{RUN_ID}/ship_state.json`
  at key steps. On push/PR/merge/sync failure, run `tools/qf resume RUN_ID=...`.
- `tools/qf resume` 会先检查是否已存在同分支的已合并 PR；若已合并则跳过重复 `pr create/merge`，直接执行本地 `main` 同步收尾。
- Ship success behavior: after merge, ship auto-syncs local `main` to `origin/main`.
- 7) On failure, write failure reason, repro, and next step in
  `reports/{RUN_ID}/summary.md` + `reports/{RUN_ID}/decision.md` (and `MISTAKES/`
  or `TASKS/STATE.md` when needed).

## Pause/stop reason taxonomy (required in decision.md)
- Use one canonical stop reason when pausing/stopping a run:
  - `task_done`
  - `needs_human_decision`
  - `infra_network`
  - `infra_quota_or_auth`
  - `tool_or_script_error`
  - `verify_failed`
  - `external_blocked`

## Documentation freshness gate (hard rule)
- Process/rule/tooling behavior changed in this RUN => update owner docs in this RUN.
- Minimum documentation set for process changes:
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `SYNC/*` startup docs if order/semantics changed
  - `TASKS/STATE.md` pointers if run/task context changed
  - `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- If documentation is stale, do not ship.

## Codex governance and automation
- Session constitution and operation standard: `AGENTS.md` + `docs/CODEX_CLI_OPERATION.md`
- Default policy: PR-driven flow with local `make verify`; do not depend on GitHub Actions queues.
- If automation is ever re-enabled, it must be explicitly requested and documented in task acceptance.
- `tools/ship.sh` hard gate blocks `.github/workflows/*.yml|*.yaml` by default; explicit override required:
  - `SHIP_ALLOW_WORKFLOWS=1 tools/ship.sh "<msg>"`
- `tools/ship.sh` appends process mistakes to `reports/{RUN_ID}/mistake_log.jsonl` on retries/failures.
- `tools/observe.sh` summarizes these logs under `过程错题（执行/思考）`.
- Process mistake template reference: `docs/MISTAKES_TEMPLATE.md`.
