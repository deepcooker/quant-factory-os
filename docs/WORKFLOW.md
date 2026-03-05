# WORKFLOW

Standard start

This document describes the expected workflow for changes in this repository.

## Document ownership
- Session entrypoint owner: `AGENTS.md` + `docs/PROJECT_GUIDE.md`
- Hard rules owner: `AGENTS.md`
- Execution details owner: `docs/WORKFLOW.md` (this file)
- Entity definitions owner: `docs/ENTITIES.md`
- Strategy/vision owner: `docs/PROJECT_GUIDE.md`
- Codex operation owner: `CODEX_CLI_PLAYBOOK.md`
- Codex operation audit owner: `CODEX_CLI_SOURCE_AUDIT.md`

## Session lifecycle state machine (single source)
- Runtime dispatcher note:
  - No single main entrypoint is required.
  - Python-first commands: `init/learn/ready/orient/choose/council/arbiter/slice_task`.
  - Non-migrated commands run via `bash tools/legacy.sh <subcommand>`.
- `S-1 Discussion-only` (optional)
  - Allowed only for read-only clarification/investigation.
  - Constraint: no repo mutation (no file edits, no generated artifacts, no ship).
  - Exit: before any mutation, bind to active `TASKS/TASK-*.md` + `RUN_ID`.
- `S0 Environment`: `python3 tools/init.py`
  - Input: local repo checkout
  - Output: environment/readiness diagnosis only (account/version/branch/diff/run-context/last-change evidence)
  - Implementation: Python-first (`tools/init.py`).
  - Note: this is environment preparation only, not readiness pass.
  - Output visibility: prints `INIT_STEP[<i>/<n>]` stage markers.
  - Safety: no automatic stash/sync/handoff side effects.
  - Boundary: init does not create a new business `RUN_ID`; it uses `CURRENT_RUN_ID` when present, otherwise session context only.
  - Project context: reads `CURRENT_PROJECT_ID` from `TASKS/STATE.md` (defaults to `project-0`).
  - Modes:
    - default (`python3 tools/init.py`): check + recommendation output (`INIT_STATUS` + `INIT_NEXT`)
    - `-status`: status-only query, suppress resume reminder text
    - `-main`: strict mode, requires main-oriented clean state; otherwise non-zero exit
- `S1 Handoff`: `bash tools/legacy.sh handoff`
  - Input: `CURRENT_RUN_ID` (or explicit RUN_ID)
  - Output: `reports/{RUN_ID}/handoff.md`
  - Note: this is context reconstruction only, not readiness pass.
  - Format: concise session summary (main thread, key conclusions, small reflection, one next command).
- `S1.6 Learn Gate`: `python3 tools/learn.py`
  - Input: required owner docs (`AGENTS.md` + `docs/PROJECT_GUIDE.md` + workflow + codex playbook + state).
  - Output: `learn/{project_id}.json` + `learn/{project_id}.md`.
  - Implementation: Python-first (`tools/learn.py`).
  - Output visibility: prints `LEARN_STEP[<i>/<n>]` stage markers.
  - Stdout mirror is enabled by default: `python3 tools/learn.py` writes `learn/{project_id}.stdout.log`.
  - Model sync is mandatory (Codex real interaction):
    - enforced mode (fixed): `MODEL_SYNC=1`
    - enforced plan protocol (fixed): `PLAN_MODE=strong`
    - transport is fixed internally: `auto(app-server->exec)` (no external override)
      - primary: `app-server` (plan-mode style read-only model sync)
      - fallback: `exec` (same prompt contract, strict parse gate unchanged)
    - default model is `gpt-5.4`
    - one-shot override is allowed: `model=<slug>` or `-model <slug>`
    - reasoning profile input: `-minimal|-low|-medium|-high|-xhigh` (default `-xhigh`)
      - runtime compatibility: `-minimal` auto-upgrades to `low` with explicit stdout reason anchor
    - model artifacts:
      - `learn/{project_id}.model.prompt.txt`
      - `learn/{project_id}.model.raw.txt`
      - `learn/{project_id}.model.json`
      - `learn/{project_id}.model.events.jsonl`
      - `learn/{project_id}.model.stderr.log`
  - Required learn anchors:
    - `LEARN_MAINLINE`, `LEARN_CURRENT_STAGE`, `LEARN_NEXT_STEP`, `LEARN_REQUIRED_FILES_READ_LIST`
    - when model sync passes (mandatory gate):
      - `LEARN_MODEL_MAINLINE`, `LEARN_MODEL_CURRENT_STAGE`, `LEARN_MODEL_NEXT_STEP`, `LEARN_MODEL_FILES_READ_LIST`
    - plan/oral packet anchors (strong mode, mandatory):
      - `LEARN_MODEL_PLAN_GOAL`, `LEARN_MODEL_PLAN_NON_GOAL`, `LEARN_MODEL_PLAN_REBUTTAL`, `LEARN_MODEL_PLAN_DECISION_STOP`
      - `LEARN_MODEL_ORAL_PROJECT`, `LEARN_MODEL_ORAL_CONSTITUTION`, `LEARN_MODEL_ORAL_EVIDENCE`, `LEARN_MODEL_ORAL_SESSION`
      - `LEARN_MODEL_ORAL_CURRENT_FOCUS`, `LEARN_MODEL_ORAL_NEXT_ACTION`, `LEARN_MODEL_ORAL_EXAM_QA_COUNT`
      - `LEARN_MODEL_ORAL_EXAM_QID1..N` (must map to `Q1..Q17` in `docs/PROJECT_GUIDE.md`)
      - `LEARN_MODEL_ANCHOR_QUESTION_ID`, `LEARN_MODEL_ANCHOR_STATUS`, `LEARN_MODEL_ANCHOR_DRIFT_DETAIL`, `LEARN_MODEL_ANCHOR_RETURN_ACTION`
      - `LEARN_MODEL_PRACTICE_COMMAND_COUNT`, `LEARN_MODEL_PRACTICE_SAMPLE_1` (and optional more samples)
    - hard validation gates:
      - practice evidence must include `tools/view.sh` reads that cover each required file at least once
      - `plan_protocol.evidence` must mention each required file at least once
      - `oral_exam` must have at least 2 `pass` items
    - optional human-readable console block:
      - `LEARN_READOUT_BEGIN` ... `LEARN_READOUT_END`
  - Purpose: materialize onboarding understanding (project/constitution/workflow/skills/session) with mandatory model-sync evidence.
- `S2 Ready gate`: `python3 tools/ready.py`
  - Input: restatement fields (goal/scope/acceptance/steps/stop)
  - Output: `reports/{RUN_ID}/ready.json`
  - Implementation: Python-first (`tools/ready.py`).
  - Output visibility: prints `READY_STEP[<i>/<n>]` stage markers.
  - Machine-readable stream (optional): `QF_EVENT_STREAM=1` emits JSONL step events to stdout.
  - Learn dependency: `QF_READY_REQUIRE_LEARN=auto` (default) enforces learn gate by default.
    - auto recovery: `QF_READY_AUTO_LEARN=1` auto-runs `python3 tools/learn.py` when learn evidence is missing/invalid.
  - Low-friction mode: fields auto-fill from active task contract by default (`QF_READY_AUTO=1`).
  - Exit resolution gate: if unresolved run context is detected, must choose:
    - `DECISION=resume-close` (run `bash tools/legacy.sh resume`)
    - `DECISION=abandon-new` (continue new direction cycle)
  - Resolution persistence: `abandon-new` is stored in `ready.json` for the same RUN to avoid repeated prompts on subsequent `ready`.
  - Ready also writes discussion brief to `chatlogs/discussion/{RUN_ID}/ready_brief.json|md`.
  - Gate: `bash tools/legacy.sh do` must fail without valid `ready.json`.
- `S2.4 Plan protocol gate` (discussion-first, required for complex changes)
  - Interactive planning command: Codex `/plan` (not `bash tools/legacy.sh plan`).
  - Required output packet (strong): goal/non-goal/evidence/alternatives/rebuttal/decision+stop-condition.
  - Confirmation: plan must be explicitly accepted before entering execution target.
  - Evidence sink: record final accepted plan into run evidence (`direction_contract` / `execution_contract` / `decision.md`).
- `S2.5 Direction gate`: `python3 tools/orient.py` + `python3 tools/choose.py`
  - Input: `docs/PROJECT_GUIDE.md` + governance docs + state/evidence.
  - Output:
    - discussion draft: `chatlogs/discussion/{RUN_ID}/orient.json|md`
    - confirmed decision: `reports/{RUN_ID}/orient_choice.json`
    - direction contract: `reports/{RUN_ID}/direction_contract.json|md`
  - Purpose: confirm direction/priority before execution queue pick.
- `S2.6 Council gate`: `python3 tools/council.py`
  - Input: `orient_choice.json` + `direction_contract.json`
  - Output: `chatlogs/discussion/{RUN_ID}/council.json|md`
  - Purpose: product/architect/dev/qa independent review before convergence.
  - Rule: council output must be evidence-based (learn/ready/scope/verify/docs/queue pressure checks), not static templates.
- `S2.7 Arbiter gate`: `python3 tools/arbiter.py`
  - Input: `council.json` + `direction_contract.json`
  - Output: `reports/{RUN_ID}/execution_contract.json|md`
  - Purpose: converge independent views into one executable contract.
  - Rule: execution slices must reflect council blockers/warnings/role conditions.
- `S2.8 Slice gate`: `python3 tools/slice_task.py`
  - Input: `execution_contract.json`
  - Output:
    - `reports/{RUN_ID}/slice_state.json`
    - queue insertion into `TASKS/QUEUE.md` (idempotent by slice marker)
  - Purpose: turn contract into smallest executable queue tasks.
- `S2.9 Discuss shortcut`: `bash tools/legacy.sh discuss`
  - Purpose: one command to run discussion chain (`orient/choose/council/arbiter/slice`) and stop before execution.
  - Default target: `prepare` (prints `EXECUTE_STATUS: prepared` + next do command).
- `bash tools/legacy.sh plan [N]` (legacy helper)
  - Purpose: generate `TASKS/TODO_PROPOSAL.md` queue suggestions only.
  - Non-goal: this command is not the planning gate and does not authorize execution.
- `S3 Execute`: `bash tools/legacy.sh do queue-next`
  - Input: valid gates (`ready.json` + `orient_choice.json` + `council.json` + `execution_contract.json` + `slice_state.json`)
  - Output: task pick + evidence skeleton + execution trace updates
  - Task pick command: `tools/task.sh --next` (no `plan 20` dependency in critical path)
  - Queue pick policy: prefer unchecked item whose `Slice: run_id=<CURRENT_RUN_ID>` matches `TASKS/STATE.md`; fallback to first unchecked item.
  - Auto checkpoint: runs `bash tools/legacy.sh review RUN_ID=<picked-run> AUTO_FIX=1 NON_BLOCKING=1` to emit drift report early.
- `S2.5~S3 Orchestrator (optional)`: `bash tools/legacy.sh execute`
  - Purpose: low-friction single command to advance gate chain and execute.
  - Output visibility: prints `EXECUTE_STEP[<i>/<n>]` stage markers.
  - Default behavior: if no confirmed option, stop with actionable choose command.
  - Contract confirm gate for execution:
    - `TARGET=do` requires `reports/{RUN_ID}/execution_contract_confirm.json`.
    - quick confirm command: `bash tools/legacy.sh execute RUN_ID=<run-id> PROJECT_ID=<project-id> CONFIRM_CONTRACT=1 TARGET=do`.
    - automation mode: `QF_EXECUTE_AUTO_CONFIRM_CONTRACT=1 bash tools/legacy.sh execute`.
  - Auto mode: `QF_EXECUTE_AUTO_CHOOSE=1 bash tools/legacy.sh execute` uses orient recommended option and continues through `council->arbiter->slice->do`.
- `S3.5 Review`: `bash tools/legacy.sh review`
  - Input: run evidence (`summary/decision/ready/choice/contract`) and optional flags (`AUTO_FIX`, `STRICT`).
  - Output: `reports/{RUN_ID}/drift_review.json|md`; blockers additionally write `chatlogs/discussion/{RUN_ID}/drift_todo.md`.
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
  - `bash tools/legacy.sh snapshot RUN_ID=<run-id> NOTE="decision/next-step summary"`
- `/compact` policy:
  - Use when conversation/context becomes large or when moving to a new milestone.
  - Not a mandatory "every task" gate.
  - Always snapshot first, then compact.
- `bash tools/legacy.sh do` / `bash tools/legacy.sh resume` 自动记录执行轨迹到
  `reports/{RUN_ID}/execution.jsonl`（默认脱敏，可审计）。
- `bash tools/legacy.sh resume` 在同步回 `main` 前若检测到脏工作区，会自动 stash
  `legacy-resume-cleanup-run-{RUN_ID}-wip-*`，避免因自身日志写入导致 checkout 自阻塞。
- `python3 tools/ready.py` / `python3 tools/orient.py` / `python3 tools/choose.py` /
  `python3 tools/council.py` / `python3 tools/arbiter.py` / `python3 tools/slice_task.py` 默认写入
  `reports/{RUN_ID}/conversation.md` checkpoint（可用 `QF_AUTO_CONVERSATION=0` 关闭）。
- Discussion drafts are intentionally separated from execution evidence:
  - pre-confirmation drafts in `chatlogs/discussion/{RUN_ID}/`
  - post-confirmation execution evidence in `reports/{RUN_ID}/`
- 断线恢复建议先生成接班摘要：
  - `bash tools/legacy.sh handoff RUN_ID=<run-id>` -> `reports/{RUN_ID}/handoff.md`
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

## Readiness completion criteria (must be true before execution)
- `python3 tools/init.py` completed successfully.
- `python3 tools/learn.py` produced valid `learn/{project_id}.json` (model sync mandatory; `RUN_ID` not required).
- `python3 tools/ready.py` produced `reports/{RUN_ID}/ready.json`.
- `python3 tools/orient.py` produced `chatlogs/discussion/{RUN_ID}/orient.json`.
- `python3 tools/choose.py` produced `reports/{RUN_ID}/orient_choice.json`.
- `python3 tools/council.py` produced `chatlogs/discussion/{RUN_ID}/council.json`.
- `python3 tools/arbiter.py` produced `reports/{RUN_ID}/execution_contract.json`.
- `python3 tools/slice_task.py` produced `reports/{RUN_ID}/slice_state.json`.
- `bash tools/legacy.sh do queue-next` requires all gates above and then picks via `tools/task.sh --next`.
- `tools/task.sh --next` prioritizes queue blocks that match `CURRENT_RUN_ID` slice marker before generic first-unchecked fallback.
- Optional shortcut: `bash tools/legacy.sh execute` can run the same chain with explicit/auto option strategy.

## Codex session startup checklist
- Do not rely on chat/session memory; rely only on repo memory:
  `TASKS/STATE.md`, `TASKS/QUEUE.md`, `reports/{RUN_ID}/`.
- First read owner entrypoint: `AGENTS.md` + `docs/PROJECT_GUIDE.md`.
- Codex 参数/模式参考：`CODEX_CLI_PLAYBOOK.md`。
- Preferred entrypoint set:
  - `python3 tools/init.py`
  - `python3 tools/learn.py`
  - `python3 tools/ready.py`
  - `python3 tools/orient.py`
  - `python3 tools/choose.py`
  - `python3 tools/council.py`
  - `python3 tools/arbiter.py`
  - `python3 tools/slice_task.py`
  - `bash tools/legacy.sh <subcommand>` for legacy commands.
- Compatibility wrappers: `tools/enter.sh` and `tools/onboard.sh`.
- 1) 运行 `python3 tools/init.py`（环境体检；不自动改工作区，不自动 handoff）。
- 1.1) 只看状态可用：`python3 tools/init.py -status`（抑制 resume 提示文案）。
- 1.2) 强制 main 约束可用：`python3 tools/init.py -main`（不满足即失败）。
- 1.0) 若希望在终端消费结构化日志，可设置 `QF_EVENT_STREAM=1`（stdout 会追加 JSONL 事件）。
- 2) 若 `INIT_STATUS=needs_resume`/`blocked`，先执行 `bash tools/legacy.sh resume RUN_ID=<run-id>` 处理收尾问题。
- 2.1) `handoff` 改为显式动作：`bash tools/legacy.sh handoff RUN_ID=<run-id>`（按需调用）。
- 3) 按顺序阅读并复述：`AGENTS.md` -> `docs/PROJECT_GUIDE.md` -> `docs/WORKFLOW.md` -> `docs/ENTITIES.md` -> `TASKS/STATE.md` -> `TASKS/QUEUE.md`。
- 3.1) 运行 `python3 tools/learn.py` 固化“上岗学习”证据（项目+宪法+工作流+技能+session），默认打印分步日志。
  - `project_id` 只来自 `TASKS/STATE.md: CURRENT_PROJECT_ID`（缺省 `project-0`）。
  - 模型同频是硬门禁（不可降级）：内部固定 `MODEL_SYNC=1` + `PLAN_MODE=strong`。
  - `learn` 会强制校验模型 `files_read` 覆盖必读文件清单。
- 4) 运行 `python3 tools/ready.py` 完成复述上岗门禁（默认绑定 `CURRENT_RUN_ID`，默认可自动填充；默认缺失 learn 时可自动补跑）。
- 4.0) 若 `ready` 提示 unresolved run context，先二选一：
  - `bash tools/legacy.sh resume RUN_ID=<run-id>`（收尾）
  - `python3 tools/ready.py RUN_ID=<run-id> DECISION=abandon-new`（明确抛弃旧上下文后继续）
- 4.1) 运行 `python3 tools/orient.py` 生成方向候选与优先级（L1 方向层）。
- 4.2) 运行 `python3 tools/choose.py OPTION=<id>` 确认方向后再进入执行层（L2）。
- 4.2.1) 运行 `python3 tools/council.py` 生成产品/架构/研发/测试独立评审结果（讨论态）。
- 4.2.2) 运行 `python3 tools/arbiter.py` 收敛为统一执行契约（执行态）。
- 4.2.3) 运行 `python3 tools/slice_task.py` 把执行契约拆成最小 queue tasks（幂等入队）。
- 4.2.4) 低摩擦讨论收敛可用：`bash tools/legacy.sh discuss`（默认停在 prepare，不直接 do）。
- 4.3) 在关键决策点执行 `bash tools/legacy.sh snapshot NOTE="..."`，把“本轮结论/下一步”写入仓库证据，避免会话丢失。
- 5) 运行 `bash tools/legacy.sh do queue-next` 领取下一枪（内部强制 ready + choose + council + arbiter + slice 前置；并自动产出一次 non-blocking drift review）。
- 5.0) 低摩擦可选：`bash tools/legacy.sh execute`
  - 默认在缺少方向确认时停在 choose（保留人工确认）
  - 自动推进模式：`QF_EXECUTE_AUTO_CHOOSE=1 bash tools/legacy.sh execute`
- 5.1) 需求执行完成后，显式运行 `bash tools/legacy.sh review RUN_ID=<run-id> STRICT=1 AUTO_FIX=1`，清空 blocker 后再 ship。
- 6) Expand that item into `TASKS/TASK-*.md` (from template), then run:
  implement minimal diff -> `make verify` -> update reports -> `tools/task.sh` ship.
- Ship failure recovery: `tools/ship.sh` writes `reports/{RUN_ID}/ship_state.json`
  at key steps. On push/PR/merge/sync failure, run `bash tools/legacy.sh resume RUN_ID=...`.
- `bash tools/legacy.sh resume` 会先检查是否已存在同分支的已合并 PR；若已合并则跳过重复 `pr create/merge`，直接执行本地 `main` 同步收尾。
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
  - `docs/PROJECT_GUIDE.md` and `docs/LEARN_EXAM_*` when onboarding/learn semantics changed
  - `TASKS/STATE.md` pointers if run/task context changed
  - `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- If documentation is stale, do not ship.

## Codex governance and automation
- Session constitution and operation standard: `AGENTS.md` + `CODEX_CLI_PLAYBOOK.md`
- Default policy: PR-driven flow with local `make verify`; do not depend on GitHub Actions queues.
- If automation is ever re-enabled, it must be explicitly requested and documented in task acceptance.
- `tools/ship.sh` hard gate blocks `.github/workflows/*.yml|*.yaml` by default; explicit override required:
  - `SHIP_ALLOW_WORKFLOWS=1 tools/ship.sh "<msg>"`
- `tools/ship.sh` appends process mistakes to `reports/{RUN_ID}/mistake_log.jsonl` on retries/failures.
- `tools/observe.sh` summarizes these logs under `过程错题（执行/思考）`.
- Process mistake template reference: `docs/MISTAKES_TEMPLATE.md`.
