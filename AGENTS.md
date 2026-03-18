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
- `TASKS/TASK-*.md` are legacy human-readable views during transition, not machine truth.
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
- Experimental flow map: `docs/TOOLS_METHOD_FLOW_MAP.md`
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
  - `python3 tools/appserverclient.py --fork-role <run-main|dev|test|arch>` when a task needs a real role thread
  - minimal task execution inside forked sessions
  - `python3 tools/appserverclient.py --summarize-current`
  - `python3 tools/appserverclient.py --refresh-baseline`
  - `python3 tools/gitclient.py --commit` or rollback
- Historical Python-first commands such as `learn/ready/orient/choose/council/arbiter/slice_task` are archived compatibility assets, not the primary mainline contract or formal docs surface.
- Legacy shell entrypoints are archived under `chatlogs/backup/` and no longer belong to the formal tool surface.

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
  - default effort is `low`; use `-e <low|medium|high|xhigh>` to override when a heavier learning pass is needed
  - baseline prompt is built from `tools/prompts/learnbaseline_prompt.md` plus dynamic project context
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
- Historical `legacy.sh` behavior is reference-only under `chatlogs/backup/legacy.sh`; it does not open execute gate.
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
- `python3 tools/appserverclient.py --fork-role <run-main|dev|test|arch>`
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
- `tools/view.sh`
- `python3 tools/evidence.py --run-id <RUN_ID>`
- `pytest -q`
- `python3 tools/slice.py --run-id <RUN_ID> --day YYYY-MM-DD --symbols A,B --start HH:MM --end HH:MM`

## 9) Reading policy (hard)
- Long file reading must use `tools/view.sh` in chunks.
- `tools/view.sh` is the stable file reader and supports both direct execution and `python3 tools/view.sh ...`.
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
- `docs/TOOLS_METHOD_FLOW_MAP.md` (if formal mainline methods or call paths changed)
- `tools/project_config.json` (if active pointers changed)
- `TASKS/QUEUE.json` / `TASKS/TASK-*.json` (if task or queue truth changed)
- `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`

No doc update, no ship.

## 13) PR discipline
- One task -> one branch -> one PR.
- PR title must include `RUN_ID`.
- PR body must include: Why / What / Verify / Evidence paths.
补充初始化门禁：
- `tools/project_config.json -> bootstrap_state.is_inited` 是项目是否完成首轮接入的硬门禁。
- 只有 `is_inited = Y` 才允许直接执行 baseline 主线命令；其他任何值都视为未初始化。
- 首轮接入入口统一命名为 `python3 tools/appserverclient.py --init-project`。
- `session_registry.init_project_session` 是初始化过程的独立 thread 槽位；默认 `--init-project` 应续跑该 session，只有显式 `-new` 才允许重开。
- `--init-project` 的正式协议是：
  - Phase 1：`plan` 模式下的 17 问理解与补缺阶段，默认 effort 为 `low`，可通过 `-e <low|medium|high|xhigh>` 覆盖；输出 `answered_questions / unclear_questions / customer_followups / document_priority_understanding / current_project_understanding / ready_for_doc_write`
  - Phase 1 可保留内部辅助字段：`explicit_refs / light_repo_findings / implementation_gaps / must_read_next`
  - 当前允许通过 `--instruction-text/--instruction-file` 给同一 init session 注入补充执行指令；该指令应写回 `session_execution_instruction`
  - `--init-project` 当前必须先生成目标项目的 `tools/init_project.final_prompt.md`，再把这份最终 prompt 作为真实 init thread 的实际 turn 输入源；其内容顺序固定为：模板 -> 补充执行指令 -> 动态项目上下文 -> 输出约束
  - `-t` 是 `--instruction-text` 的短别名；`-p` 表示显式强制再走一次完整 prompt；`-new` 只负责重开 thread，不再隐式等于 prompt 模式
  - 如果当前已有真实 init thread，则不带 `-p` 的 `--init-project -t "..."` 默认是沿同一线程继续聊天微调，而不是重喂完整 prompt
  - 如果当前没有 init thread，则不带 `-p` 的 `--init-project -t "..."` 也必须创建新的真实 init thread，但只发送聊天文本，不重喂完整 prompt
  - 如果同一 init thread 仍有未闭合 turn，重复执行 `--init-project` 必须返回 `err_code = 0` + `status / next_action`，而不是生成重复线程；当前允许出现 `existing_thread_busy` / `rollout_pending` 作为忙态提示
  - 手工续跑与状态推进通过 `python3 tools/appserverclient.py --update-init-project --payload-json <path>` 完成
  - 初始化完成入口是 `python3 tools/appserverclient.py --complete-init-project`
- `--init-project` / `--update-init-project` 在“需要继续推进但并未出错”时必须返回 `err_code = 0`，并通过 `status / next_action` 指出下一步；只有真正异常才允许 `err_code <> 0`
- 如果当前 `init_project_session` 没有 `thread_id/thread_path`，则不带 `-new` 的 `--init-project` 也必须创建新的真实 init thread；`-new` 只用于显式推翻重来
