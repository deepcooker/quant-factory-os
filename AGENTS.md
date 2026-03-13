# AGENTS.md (Hard Rules for Codex / Agents)

This repo is a quant-engineering OS. Follow deterministic workflow, not ad-hoc chat.

## 0) Scope
- Work only inside this repository.
- Never invent data. Never assume prod access.
- No secrets in files, logs, or commits.
- This repo's current goal is to harden the `tools` automation R&D system itself.
- Codex CLI is the development/debug/takeover interface; the long-term runtime target is Python orchestrator + Codex app-server.

## 1) Entry Rule: Task + Run are mandatory
- All implementation starts from `TASKS/TASK-*.json`.
- If user did not give a task, pick next open item in `TASKS/QUEUE.json` and create/select a task first.
- `TASKS/TASK-*.md` and `TASKS/QUEUE.md` are legacy human-readable views during transition, not machine truth.
- Never edit code/docs without active `RUN_ID` in `tools/project_config.json -> runtime_state`; when current work has been sliced, bind the active `TASK_ID` and `TASK JSON file` there too.

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
- Experimental flow map: `TOOLS_METHOD_FLOW_MAP.md`
- Experimental file index: `docs/FILE_INDEX.md`
- Current active pointers: `tools/project_config.json -> runtime_state`
- Queue intent: `TASKS/QUEUE.json`
- Run evidence: `reports/<RUN_ID>/`

## 4) Mandatory session gate (once per session)
Before any implementation:
1. `python3 tools/init.py`
2. `python3 tools/appserverclient.py --learnbaseline`
3. `python3 tools/appserverclient.py --fork-current`

Runtime note:
- `init` is preflight only. It is environment preparation / project skeleton / runtime checks, not the main business workflow.
- The current formal mainline is:
  - `python3 tools/appserverclient.py --learnbaseline`
  - determine run-level demand direction
  - role/session forks on top of baseline
  - `python3 tools/appserverclient.py --fork-role <dev|test|arch>` when a task needs a real role thread
  - minimal task execution inside forked sessions
  - `python3 tools/appserverclient.py --summarize-current`
  - `python3 tools/appserverclient.py --refresh-baseline`
  - `python3 tools/gitclient.py --commit` or rollback
- Historical Python-first commands such as `learn/ready/orient/choose/council/arbiter/slice_task` are archived compatibility assets, not the primary mainline contract.
- Legacy shell entrypoints are archived under `tools/backup/` and no longer belong to the formal tool surface.

`init` detailed step definitions, mode semantics (`-status` / `-main`), and output fields are owned by `docs/WORKFLOW.md` (`S0 Environment`). `AGENTS.md` keeps only gate-level contract.

Required visible progress:
- `INIT_STEP[<i>/<n>]`
- `APP_RUNTIME_STATE_START`
- `APP_RUNTIME_STATE_END`

`appserverclient` baseline/session pass criteria (minimum):
- Runtime implementation is Python-first (`tools/appserverclient.py`).
- `--learnbaseline` is the current project onboarding core:
  - owner files are `docs/PROJECT_GUIDE.md` + `AGENTS.md` + `docs/WORKFLOW.md`
  - `PROJECT_GUIDE.md` still drives what else must be read through each question's `必查文件`
- Baseline learning is mandatory:
  - session lifecycle is fixed internally: baseline -> fork-current -> current-turn -> summarize-current -> refresh-baseline
  - transport is fixed internally: `app-server`
  - baseline learning mode is fixed internally: `plan`
  - default model constant: `gpt-5.4`
  - baseline prompt is built from `tools/learnbaseline_prompt.md` plus dynamic project context
  - baseline creation must write `session_registry.learn_session_baseline`
  - current fork creation must write `session_registry.fork_current_session`
- Daily work should not keep using `plan`:
  - `--current-turn` is the normal default-mode session continuation path
- Denoise / refresh must write back through runtime truth:
  - `--summarize-current` must write `session_registry.current_summary`
  - `--refresh-baseline` must consume `session_registry.current_summary` instead of rebuilding baseline from scratch
- role-thread runtime currently also supports:
  - `python3 tools/appserverclient.py --role-turn <run-main|dev|test|arch> [text...]`
  - `python3 tools/appserverclient.py --summarize-role <run-main|dev|test|arch>`
- practice evidence must show `tools/view.sh` coverage for every required file listed by the dynamic baseline prompt

No coding until this gate is complete.

## 5) Working mode: Plan -> Confirm -> Execute
- Complex work must follow `Plan -> Confirm -> Execute`.
- Codex interactive `/plan` is planning protocol, not execution.
- Historical `legacy.sh` behavior is reference-only under `tools/backup/legacy.sh`; it does not open execute gate.
- `/compact` is milestone-based, not a `learn` hard gate. Use after long exchanges or before switching milestones.

## 6) Workflow skeleton
1. Run `python3 tools/init.py` as preflight / environment preparation.
2. Run `python3 tools/appserverclient.py --learnbaseline` to ensure project baseline learning exists.
3. Determine the run-level demand direction (human-injected intent).
4. Run `python3 tools/appserverclient.py --fork-current` to create the working session from baseline.
5. Split work into minimal role/task units inside forked sessions; when a task needs real role thread binding, use `python3 tools/appserverclient.py --fork-role <run-main|dev|test|arch>`, continue role work with `python3 tools/appserverclient.py --role-turn <role> [text...]`, and denoise one role thread with `python3 tools/appserverclient.py --summarize-role <role>`.
6. Run `python3 tools/appserverclient.py --summarize-current` to denoise the current session.
7. Run `python3 tools/appserverclient.py --refresh-baseline` to feed the denoised summary back into baseline.
8. Finish with `python3 tools/gitclient.py --commit` or rollback commands.

Current boundary:
- `init` is not the mainline; it is preparation only.
- `appserverclient` is the formal runtime/session mainline.
- `gitclient` is the formal git / PR / merge / rollback / sync layer.
- Historical `learn/ready/orient/choose/council/arbiter/slice_task` flow remains only as compatibility material while the new mainline hardens.

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
- `python3 tools/init.py`
- `python3 tools/appserverclient.py --learnbaseline`
- `python3 tools/appserverclient.py --fork-current`
- `python3 tools/appserverclient.py --fork-role <dev|test|arch>`
- `python3 tools/appserverclient.py --role-turn <run-main|dev|test|arch> [text...]`
- `python3 tools/appserverclient.py --summarize-role <run-main|dev|test|arch>`
- `python3 tools/appserverclient.py --current-turn`
- `python3 tools/appserverclient.py --summarize-current`
- `python3 tools/appserverclient.py --refresh-baseline`
- `python3 tools/gitclient.py --commit`
- `python3 tools/gitclient.py --rollback-last`
- `python3 tools/gitclient.py --rollback-commit <sha>`
- `python3 tools/taskclient.py --next`
- `python3 tools/taskclient.py --create ...`
- `python3 tools/taskclient.py --merge-role-summaries`
- `python3 tools/taskclient.py --refresh-task-gaps`
- `python3 tools/taskclient.py --refresh-task-escalation`
- `python3 tools/taskclient.py --run-main-resolution`
- `python3 tools/taskclient.py --set-run-main-resolution`
- `python3 tools/taskclient.py --refresh-run-main-resolution`
- `python3 tools/evidence.py --merge-task-summary --run-id <RUN_ID> --task-json-file TASKS/TASK-*.json`
- `python3 tools/evidence.py --reconcile-run-summary --run-id <RUN_ID>`
- `python3 tools/evidence.py --normalize-run-summary --run-id <RUN_ID>`
- `python3 tools/evidence.py --compact-run-summary --run-id <RUN_ID>`
- `tools/doctor.sh`
- `tools/enter.sh`
- `tools/smoke.sh`
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
- `docs/PROJECT_GUIDE.md` (if learning/Q&A anchor changed)
- `docs/FILE_INDEX.md` (if key file responsibilities or reading order changed)
- `TOOLS_METHOD_FLOW_MAP.md` (if formal mainline methods or call paths changed)
- `tools/project_config.json` (if active pointers changed)
- `TASKS/QUEUE.json` / `TASKS/TASK-*.json` (if task or queue truth changed)
- `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`

No doc update, no ship.

## 13) PR discipline
- One task -> one branch -> one PR.
- PR title must include `RUN_ID`.
- PR body must include: Why / What / Verify / Evidence paths.
