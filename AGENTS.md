# AGENTS.md (Hard Rules for Codex / Agents)

This repo is a quant-engineering OS. Follow deterministic workflow, not ad-hoc chat.

## 0) Scope
- Work only inside this repository.
- Never invent data. Never assume prod access.
- No secrets in files, logs, or commits.

## 1) Entry Rule: Task + Run are mandatory
- All implementation starts from `TASKS/TASK-*.md`.
- If user did not give a task, pick next unchecked item in `TASKS/QUEUE.md` and create/select a task first.
- Never edit code/docs without active `TASK_ID` + `RUN_ID` from `TASKS/STATE.md`.

## 2) Core onboarding principle (mainline anchor)
- Session startup is anchored by:
  - `AGENTS.md` (hard contract)
  - `docs/PROJECT_GUIDE.md` (learning curriculum + Socratic question bank + mainline anchor)
- If the session drifts, return to `docs/PROJECT_GUIDE.md` questions and re-answer from evidence before coding.

## 3) Single source map (owner files)
- Hard rules: `AGENTS.md`
- Project cognition / Q&A anchor: `docs/PROJECT_GUIDE.md`
- Execution state machine: `docs/WORKFLOW.md`
- Entity dictionary: `docs/ENTITIES.md`
- Codex CLI operations: `CODEX_CLI_PLAYBOOK.md`
- Codex CLI source audit: `CODEX_CLI_SOURCE_AUDIT.md`
- Current active pointers: `TASKS/STATE.md`
- Queue intent: `TASKS/QUEUE.md`
- Run evidence: `reports/<RUN_ID>/`
- Discussion drafts (non-governance): `chatlogs/discussion/<RUN_ID>/`

## 4) Mandatory session gate (once per session)
Before any implementation:
1. `tools/qf init`
2. `tools/qf learn`
3. `tools/qf ready`

`init` detailed step definitions, mode semantics (`-status` / `-main`), and output fields are owned by `docs/WORKFLOW.md` (`S0 Environment`). `AGENTS.md` keeps only gate-level contract.

Required visible progress:
- `INIT_STEP[<i>/<n>]`
- `LEARN_STEP[<i>/<n>]`
- `READY_STEP[<i>/<n>]`

`learn` pass criteria (minimum):
- Must print:
  - `LEARN_MAINLINE`
  - `LEARN_CURRENT_STAGE`
  - `LEARN_NEXT_STEP`
  - `LEARN_REQUIRED_FILES_READ_LIST`
- Model sync is mandatory (no downgrade path):
  - `MODEL_SYNC=1` only
  - `PLAN_MODE=strong` only
- Must also print model anchors:
  - `LEARN_MODEL_MAINLINE`
  - `LEARN_MODEL_CURRENT_STAGE`
  - `LEARN_MODEL_NEXT_STEP`
  - `LEARN_MODEL_FILES_READ_LIST`
  - plan/oral packet anchors defined in `docs/WORKFLOW.md`

No coding until this gate is complete.

## 5) Working mode: Plan -> Confirm -> Execute
- Complex work must follow `Plan -> Confirm -> Execute`.
- Codex interactive `/plan` is planning protocol, not execution.
- `tools/qf plan` only drafts queue proposals; it does not open execute gate.
- `/compact` is milestone-based, not mandatory every task. Use before context grows too large or before switching milestone.

## 6) Workflow skeleton
1. Read task acceptance criteria.
2. `make evidence RUN_ID=<RUN_ID>`
3. Implement smallest safe diff.
4. `make verify` until green.
5. Update run evidence.
6. Ship.

Discussion-first recommended lane:
- `tools/qf discuss TARGET=prepare`
- `tools/qf choose OPTION=<id>`
- `tools/qf council`
- `tools/qf arbiter`
- `tools/qf slice`
- `tools/qf do queue-next` (or `tools/qf execute TARGET=do`)

Execution gate artifacts required before `do`:
- `reports/<RUN_ID>/ready.json`
- `reports/<RUN_ID>/orient_choice.json`
- `chatlogs/discussion/<RUN_ID>/council.json`
- `reports/<RUN_ID>/execution_contract.json`
- `reports/<RUN_ID>/slice_state.json`

## 7) Evidence is memory (hard gate)
Each run must update:
- `reports/<RUN_ID>/meta.json`
- `reports/<RUN_ID>/summary.md`
- `reports/<RUN_ID>/decision.md`

`meta.json` minimum fields:
- `run_id`
- `task_id`
- `stop_reason`
- `commands_run`
- `artifacts`

Optional failure memory:
- `MISTAKES/<RUN_ID>.md`

## 8) Allowed commands (default)
Use only these unless task explicitly authorizes more:
- `tools/qf`
- `tools/doctor.sh`
- `tools/enter.sh`
- `tools/task.sh`
- `tools/ship.sh`
- `tools/view.sh`
- `make evidence RUN_ID=...`
- `make verify`
- `make slice RUN_ID=... DAY=... SYMBOLS=... START=... END=...`
- `pytest -q`

## 9) Reading policy (hard)
- Long file reading must use `tools/view.sh` in chunks.
- `rg` / `grep` are allowed only for locating text with short output (line hits/snippets), not for full-file reading.
- Do not use `cat` / `sed` / `awk` to dump large files; use `tools/view.sh` chunked reading instead.

## 10) Constraints
- No secrets.
- No production data.
- Any generated single file <= 5MB unless task says otherwise.
- Table-like output <= 500 rows unless task says otherwise.

## 11) Failure protocol
If blocked or verify fails:
- Record failing command + minimal logs in `reports/<RUN_ID>/summary.md`.
- Write stop reason in `reports/<RUN_ID>/decision.md`:
  - `task_done`
  - `needs_human_decision`
  - `infra_network`
  - `infra_quota_or_auth`
  - `tool_or_script_error`
  - `verify_failed`
  - `external_blocked`
- Add regression test when applicable.

## 12) Documentation freshness gate
If process/rule/tool behavior changes in a run, update in the same run:
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `CODEX_CLI_PLAYBOOK.md` (if CLI usage/flags changed)
- `CODEX_CLI_SOURCE_AUDIT.md` (if CLI behavior/evidence baseline changed)
- `docs/PROJECT_GUIDE.md` (if learning/Q&A anchor changed)
- `TASKS/STATE.md` (if active pointers changed)
- `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`

No doc update, no ship.

## 13) PR discipline
- One task -> one branch -> one PR.
- PR title must include `RUN_ID`.
- PR body must include: Why / What / Verify / Evidence paths.
