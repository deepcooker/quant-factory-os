# AGENTS.md (Hard Rules for Codex / Agents)

This repo is a quant-engineering OS. Follow deterministic workflow, not ad-hoc chat.

## 0) Scope
- Work only inside this repository.
- Never invent data. Never assume prod access.
- No secrets in files, logs, or commits.
- This repo's current goal is to harden the experimental orchestrator + skill runtime itself.
- Codex CLI is the development/debug/takeover interface; the current active mainline is the `tools` experimental line (`tools/main.py` / `tools/app.py` / `tools/project_config.json` / `schemas` / `tests` / `bootstrap`), and the long-term runtime target remains Python orchestrator + Codex app-server.

## 1) Entry Rule: Task + Run are mandatory
- All implementation starts from `TASKS/TASK-*.json`.
- If user did not give a task, pick next open item in `TASKS/QUEUE.json` and create/select a task first.
- `TASKS/TASK-*.md` are legacy human-readable views during transition, not machine truth.
- Never edit code/docs without an active `TASK_ID` / `RUN_ID` truth source. For the current experimental line, runtime truth is rooted in `tools/project_config.json`, `state/registry.json`, `state/events.jsonl`, `state/checkpoints/`, and `reports/<RUN_ID>/`.

## 2) Core onboarding principle (mainline anchor)
- Session startup is anchored by:
  - `AGENTS.md` (hard contract)
  - `docs/PROJECT_GUIDE.md` (learning curriculum + question bank + standard answers + mainline anchor)
- `PROJECT_GUIDE.md` is not a passive reference; it is the high-quality reverse-questioning course that forces reading owner docs, evidence, and session continuity before coding.
- `PROJECT_GUIDE.md` 的题目设计与结构是 owner 精选后的固定课程资产，不得随意重写、重排或替换题库。
- 允许的变更只有两类：
  - 因项目真实变化而更新标准答案
  - 为保持同频质量而做最小必要微调
- If the session drifts, return to `docs/PROJECT_GUIDE.md` questions and re-answer from evidence before coding.

## 3) Single source map (owner files)
- Hard rules: `AGENTS.md`
- Project cognition / Q&A anchor: `docs/PROJECT_GUIDE.md`
- Execution state machine: `docs/WORKFLOW.md`
- Entity dictionary: `docs/ENTITIES.md`
- Experimental file index: `docs/FILE_INDEX.md`
- Current experimental runtime truth: `tools/project_config.json`, `state/registry.json`, `state/events.jsonl`, `state/checkpoints/`
- Queue intent: `TASKS/QUEUE.json`
- Run evidence: `reports/<RUN_ID>/`

## 4) Mandatory session gate (once per session)
Before any implementation:
1. Read `AGENTS.md`
2. Read `docs/PROJECT_GUIDE.md`
3. Read `docs/WORKFLOW.md`
4. Confirm the current experimental runtime truth in:
   - `tools/project_config.json`
   - `state/registry.json`
   - `TASKS/QUEUE.json`
   - `reports/<RUN_ID>/`

Runtime note:
- The current active experimental mainline is:
  - learning baseline initialize / refresh
  - `project_coach` clarification
  - verification and evidence pack collection
  - correction (`demand_critic / solution_designer / risk_reviewer`)
  - planning (`run_manager`)
  - role execution (`dev_worker / test_worker / arch_reviewer`)
  - defect triage / repair / replan / discussion
  - merge
  - baseline refresh
  - state / events / checkpoints
  - smoke / gate / bootstrap as support layers
- `tools/` runtime commands remain compatibility assets and historical formal mainline references while the new orchestrator line hardens, but they no longer define the project cognition anchor.
- Historical Python-first commands such as `learn/ready/orient/choose/council/arbiter/slice_task` are archived compatibility assets, not the primary mainline contract or formal docs surface.
- Legacy shell entrypoints are archived under `chatlogs/backup/` and no longer belong to the formal tool surface.

`init` detailed step definitions, mode semantics (`-status` / `-main`), and output fields are owned by `docs/WORKFLOW.md` (`S0 Environment`). `AGENTS.md` keeps only gate-level contract.

Required visible progress:
- `INIT_STEP[<i>/<n>]`
- `APP_RUNTIME_STATE_START`
- `APP_RUNTIME_STATE_END`

Experimental orchestrator pass criteria (minimum):
- Runtime implementation is Python-first (`tools/main.py` + `tools/app.py` + `core/schema_utils.py`).
- `tools/app.py` is now the active app-server client core:
  - thread lifecycle (`new / resume / fork / rename`)
  - unified turn execution (`default / plan / optional skill`)
  - unified business entry via `run_business_turn(...)`
- `tools/main.py` now consumes `tools/app.py` as the default runtime client path; historical demo-only protocol verification has been archived.
- `tools/init.py` is the active preparation-layer entry:
  - ensure / validate `tools/project_config.template.json` and `tools/project_config.json`
  - verify Codex CLI, app-server capability, skills / schemas presence, and git worktree state
- `tools/sync_tools.py` is the active sync-layer entry:
  - sync docs, schemas, skills, runtime files, and tests into target projects
  - do not overwrite target-project `tools/project_config.json`
- Baseline learning, coach, verification, correction, planning, role execution, triage, merge and refresh are all schema-backed and state-backed.
- Runtime truth must be recoverable from:
  - `tools/project_config.json`
  - `state/registry.json`
  - `state/events.jsonl`
  - `state/checkpoints/`
- Quality gates must be runnable from:
  - `tests/run_smoke_suite.py`
  - `tests/run_gate.py`
- New project intake must be bootstrap-capable through:
  - `scripts/bootstrap_experiment_project.py`
  - `templates/experiment_project/`

No coding until this gate is complete.

## 5) Working mode: Plan -> Confirm -> Execute
- Complex work must follow `Plan -> Confirm -> Execute`.
- Codex interactive `/plan` is planning protocol, not execution.
- Historical `legacy.sh` behavior is reference-only under `chatlogs/backup/legacy.sh`; it does not open execute gate.
- `/compact` is milestone-based, not a `learn` hard gate. Use after long exchanges or before switching milestones.

## 6) Workflow skeleton
1. Read the owner docs anchor: `AGENTS.md` -> `docs/PROJECT_GUIDE.md` -> `docs/WORKFLOW.md`.
2. Initialize or refresh the learning baseline.
3. Accept `raw_request`.
4. Run coach clarification and claim generation.
5. Run verification and collect evidence packs.
6. Run correction and produce `corrected_job`.
7. Run planning and task generation.
8. Execute role threads and collect active results.
9. Pass through defect triage; if needed, enter repair / replan / discussion.
10. Merge, refresh baseline, persist state / events / checkpoints, then verify with smoke / gate.

Current boundary:
- `tools/` commands remain compatibility / historical mainline assets.
- `tools/main.py` + `tools/app.py` + skills + schemas + tests + bootstrap define the current experimental mainline.
- `gitclient` still remains the formal Git / PR / merge / rollback / sync layer when this line is later integrated into the shipping path.

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
- `python3 tools/main.py`
- `python3 tests/run_smoke_suite.py`
- `python3 tests/run_gate.py`
- `python3 tests/smoke_*.py`
- `python3 tests/integration_real_app_smoke.py`
- `python3 scripts/bootstrap_experiment_project.py <target>`
- `tools/view.sh`
- `pytest -q`

## 9) Reading policy (hard)
- Long file reading must use `tools/view.sh` in chunks.
- `tools/view.sh` is the stable file reader and supports both direct execution and `python3 tools/view.sh ...`.
- `tools/view.sh` 单次读取范围上限是 `260` 行；超过该范围必须继续分段，不允许一次请求更大区间。
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
- `docs/PROJECT_GUIDE.md` (if learning/Q&A anchor changed)
- `docs/FILE_INDEX.md` (if key file responsibilities or reading order changed)
- `docs/ENTITIES.md` (if object boundaries or truth sources changed)
- `tools/project_config.json` (if active policy or skill pointers changed)
- `TASKS/QUEUE.json` / `TASKS/TASK-*.json` (if task or queue truth changed)
- `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`

No doc update, no ship.

## 13) PR discipline
- One task -> one branch -> one PR.
- PR title must include `RUN_ID`.
- PR body must include: Why / What / Verify / Evidence paths.
Bootstrap / intake discipline:
- New project intake is now implemented by `scripts/bootstrap_experiment_project.py` and the templates under `templates/experiment_project/`.
- Bootstrap modes are:
  - `skeleton`
  - `runnable`
  - `runtime-bundle`
- Runtime-bundle mode must produce a self-verifiable target project with:
  - core skills
  - minimum runtime files
  - minimum schema set
  - `bootstrap_manifest.json`
