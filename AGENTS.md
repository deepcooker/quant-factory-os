# AGENTS.md (Hard Rules for Codex / Agents)

This repo is an OS for quant engineering. Agents MUST obey these rules.

## 0) Scope
- You work ONLY inside this repository.
- Never invent data. Never assume prod access.
- Prefer deterministic scripts + evidence, not long chat.

## 1) Entry: Tasks are syscall
- All work MUST start from a task file under /TASKS.
- If no task is provided, pick the next unchecked item in QUEUE.md and create a TASK file first.
- Never change code without an active task ID and RUN_ID.

## 2) Output: Evidence is memory
For each task you MUST create/update:
- reports/<RUN_ID>/meta.json
- reports/<RUN_ID>/summary.md
- reports/<RUN_ID>/decision.md

Optional:
- reports/<RUN_ID>/samples/*.csv.gz
- MISTAKES/<RUN_ID>.md (only if failure)

## 3) Constraints (Data / Size / Secrets)
- Never write or commit secrets. Never print secrets.
- Never commit production data. Use synthetic or reduced samples only.
- Hard limits:
  - Any single generated file <= 5MB
  - Any table-like output <= 500 rows unless explicitly requested by task

## 4) Allowed Commands (Default)
Use ONLY these unless task explicitly authorizes more:
- tools/qf
- tools/doctor.sh
- tools/enter.sh
- tools/task.sh
- tools/ship.sh
- tools/view.sh
- make evidence RUN_ID=...
- make verify
- make slice RUN_ID=... DAY=... SYMBOLS=... START=... END=...
- pytest -q

Notes:
- Primary agent entrypoint is `tools/qf` (`init/sync/ready/orient/choose/council/arbiter/slice/execute/do/review/resume`).
- Sync gate command: `tools/qf sync` (auto reading + sync report).
- `tools/enter.sh` and `tools/onboard.sh` are compatibility wrappers.
- Discussion drafts live in `SYNC/discussion/<RUN_ID>/`; execution evidence lives in `reports/<RUN_ID>/`.

## Single source map
- Session entrypoint owner: `SYNC/READ_ORDER.md`
- Hard rules owner: `AGENTS.md`
- Execution workflow owner: `docs/WORKFLOW.md`
- Entity definitions owner: `docs/ENTITIES.md`
- Strategy/vision owner: `docs/PROJECT_GUIDE.md`
- Codex operation owner: `docs/CODEX_CLI_OPERATION.md`

## Reading policy
- 长文件阅读必须使用 tools/view.sh 分段查看，不得直接使用 sed/cat/rg/grep/awk。

## 5) Workflow (Must follow)
1) Read TASKS/<task>.md and confirm acceptance criteria.
2) Run `make evidence RUN_ID=<RUN_ID>` (creates evidence skeleton).
3) Implement change in smallest diff possible.
4) Run `make verify` until green.
5) Write decision + update summary (what changed / why / risks / verify commands).
6) Ship via `tools/ship.sh` or `make ship` (if defined).

## 6) Failure protocol
If stuck or tests fail:
- Capture the failing command + minimal logs in reports/<RUN_ID>/summary.md
- Write MISTAKES/<RUN_ID>.md with:
  - symptom, root cause hypothesis, fix, guardrail test suggestion
  - process category: thinking_error / decision_error / execution_error / verification_error / recovery_error / business_error
- Add/strengthen a test to prevent regression.
- Treat mistakes as end-to-end process memory, not only business/domain errors.
- When pausing/stopping a run, record one stop reason in `reports/<RUN_ID>/decision.md`:
  - task_done
  - needs_human_decision
  - infra_network
  - infra_quota_or_auth
  - tool_or_script_error
  - verify_failed
  - external_blocked

## 7) PR discipline (Single-user but strict)
- One task -> one branch -> one PR
- PR title MUST include RUN_ID
- PR body MUST include:
  - Why / What / Verify
  - Evidence paths

## 8) Session init gate (Mandatory, once per session)
Before any implementation, you MUST complete init and pass readiness checks:
1) Run `tools/qf init` (environment prep only; this is NOT readiness pass).
   - Visible progress markers are required: `INIT_STEP[<i>/<n>]`.
   - `init` must not silently clean `reports/run-*-pick-candidate` directories.
   - `init` must not create a new business `RUN_ID`; run ownership starts at `learn/ready` (or existing `CURRENT_RUN_ID`).
   - Optional machine stream: set `QF_EVENT_STREAM=1` to emit JSONL step events to stdout.
2) If `CURRENT_RUN_ID` exists, run `tools/qf handoff` (context summary only; this is NOT readiness pass).
   - `tools/qf init` auto-runs this step by default for continuing runs.
   - To disable auto-handoff for one run: `QF_INIT_AUTO_HANDOFF=0 tools/qf init`
3) Read, in order:
   - `SYNC/READ_ORDER.md`
   - files listed in `SYNC/READ_ORDER.md` (strict order)
   - then run `tools/qf sync` to materialize read evidence (`sync_report.json/.md`)
   - exam package is v2 deep questionnaire (`SYNC/EXAM_PLAN_PROMPT.md`, `SYNC/EXAM_ANSWER_TEMPLATE.md`, `SYNC/EXAM_WORKFLOW.md`, `SYNC/EXAM_RUBRIC.json`)
4) Restate and get confirmation before coding:
   - Goal (1 sentence)
   - Scope (exact paths)
   - Acceptance (verify/evidence/scope)
   - Execution steps (evidence -> implement -> verify -> reports -> ship)
   - Stop condition (finish and wait)
5) Record readiness gate:
   - `CURRENT_PROJECT_ID` + `CURRENT_RUN_ID` source-of-truth is `TASKS/STATE.md`.
   - default `project_id` is `project-0` when missing.
  - Run `tools/qf learn` before `ready` to complete onboarding learning gate:
    - output: `reports/projects/<project_id>/session/learn.json|md` (project-scoped session memory)
    - model sync (Codex real interaction) options:
      - `MODEL_SYNC=0|auto|1` (or `QF_LEARN_MODEL_SYNC`), default `auto`
      - `MODEL_SYNC=1` is strict mode: learn fails if model sync fails
      - `PLAN_MODE=strong|basic` (or `QF_LEARN_PLAN_MODE`), default `strong`
      - timeout/model override: `MODEL_TIMEOUT_SEC=<n>` (default 180), `MODEL=<slug>`
      - invocation profile: `codex --search --ask-for-approval never exec --sandbox read-only --json --output-last-message ...`
      - model artifacts:
        - `reports/projects/<project_id>/session/learn.model.prompt.txt`
        - `reports/projects/<project_id>/session/learn.model.raw.txt`
        - `reports/projects/<project_id>/session/learn.model.json`
        - `reports/projects/<project_id>/session/learn.model.events.jsonl`
        - `reports/projects/<project_id>/session/learn.model.stderr.log`
    - `RUN_ID` is optional for `learn`:
      - with `RUN_ID`/`CURRENT_RUN_ID`: uses run-scoped sync/exam evidence.
      - without run context: enters `session-direct-read` mode (reads required docs directly; no implicit fallback to latest historical run).
      - without run context and no session exam result, exam requirement is downgraded for that learn pass (`LEARN_EXAM_BYPASS_NO_RUN_CONTEXT: true`).
    - optional stdout log mirror: `tools/qf learn -log` -> `reports/projects/<project_id>/session/learn.stdout.log` (or `LOG=<path>`)
    - Visible progress markers are required: `LEARN_STEP[<i>/<n>]`.
    - learn anchors are required in stdout:
      - `LEARN_MAINLINE`
      - `LEARN_CURRENT_STAGE`
      - `LEARN_NEXT_STEP`
      - `LEARN_REQUIRED_FILES_READ_LIST`
      - when model sync passes: `LEARN_MODEL_MAINLINE`, `LEARN_MODEL_CURRENT_STAGE`, `LEARN_MODEL_NEXT_STEP`, `LEARN_MODEL_FILES_READ_LIST`
      - when `PLAN_MODE=strong` and model sync passes:
        - `LEARN_MODEL_PLAN_GOAL`
        - `LEARN_MODEL_PLAN_NON_GOAL`
        - `LEARN_MODEL_PLAN_REBUTTAL`
        - `LEARN_MODEL_PLAN_DECISION_STOP`
        - `LEARN_MODEL_ORAL_PROJECT`
        - `LEARN_MODEL_ORAL_CONSTITUTION`
        - `LEARN_MODEL_ORAL_EVIDENCE`
        - `LEARN_MODEL_ORAL_SESSION`
        - `LEARN_MODEL_ORAL_CURRENT_FOCUS`
        - `LEARN_MODEL_ORAL_NEXT_ACTION`
        - `LEARN_MODEL_ORAL_EXAM_QA_COUNT`
    - Optional machine stream: set `QF_EVENT_STREAM=1` to emit JSONL step events to stdout.
  - Run `tools/qf ready` (or `tools/qf ready RUN_ID=<run-id>` for explicit override).
  - Visible progress markers are required: `READY_STEP[<i>/<n>]`.
  - Optional machine stream: set `QF_EVENT_STREAM=1` to emit JSONL step events to stdout.
  - `tools/qf ready` enforces learn gate by default when sync gate is enabled (`QF_READY_REQUIRE_LEARN=auto`).
    - auto recovery: `QF_READY_AUTO_LEARN=1` allows `ready` to auto-run `tools/qf learn` when missing/expired.
  - If unresolved run context is detected, `ready` MUST stop and require decision:
    - `DECISION=resume-close` (go close via `tools/qf resume`)
    - `DECISION=abandon-new` (explicitly continue as new direction cycle)
  - Resolution memory: after `DECISION=abandon-new`, the same RUN keeps this decision in `ready.json` and should not re-prompt on every `ready`.
   - `tools/qf ready` requires valid `reports/<RUN_ID>/sync_report.json`; by default it auto-runs `tools/qf sync` when missing (`QF_READY_AUTO_SYNC=1`).
  - `tools/qf ready` auto-fills restatement from active task contract by default.
  - To force manual-only input: `QF_READY_AUTO=0 tools/qf ready`
  - `tools/qf do` MUST fail if no valid `reports/<RUN_ID>/ready.json`.
  - After ready, orientation drafts are generated under `SYNC/discussion/<RUN_ID>/orient.json|md`.
  - Confirm direction with `tools/qf choose OPTION=<id>`:
    - confirmation result goes to `reports/<RUN_ID>/orient_choice.json`
    - direction contract goes to `reports/<RUN_ID>/direction_contract.json|md`
  - Generate independent multi-role reviews via `tools/qf council`.
  - Converge to execution contract via `tools/qf arbiter`:
    - output: `reports/<RUN_ID>/execution_contract.json|md`
  - Slice execution contract to queue tasks via `tools/qf slice`:
    - output: `reports/<RUN_ID>/slice_state.json`
    - queue insertion: `TASKS/QUEUE.md` (idempotent by slice marker)
  - Discussion-first shortcut (recommended): `tools/qf discuss`
    - default target is `prepare` (generates council/contract/slice, does not execute do)
    - next command is explicit `tools/qf do queue-next`
  - Queue pick policy (`tools/task.sh --next`):
    - prefer unchecked item whose `Slice: run_id=<CURRENT_RUN_ID>` matches `TASKS/STATE.md`
    - fallback to first unchecked item when no matching slice exists
  - Low-friction orchestrator (optional): `tools/qf execute`
    - default: stops at choose if no `OPTION` confirmed
    - for `TARGET=do`, execution requires contract confirmation evidence:
      - one-shot confirm: `tools/qf execute RUN_ID=<run-id> PROJECT_ID=<project-id> CONFIRM_CONTRACT=1 TARGET=do`
      - auto confirm mode: `QF_EXECUTE_AUTO_CONFIRM_CONTRACT=1 tools/qf execute`
    - auto mode: `QF_EXECUTE_AUTO_CHOOSE=1 tools/qf execute` auto-picks recommended option then runs `council->arbiter->slice->do`
  - `tools/qf do` MUST fail if any required gate is missing:
    - `reports/<RUN_ID>/orient_choice.json`
    - `SYNC/discussion/<RUN_ID>/council.json`
    - `reports/<RUN_ID>/execution_contract.json`
    - `reports/<RUN_ID>/slice_state.json`
  - After execution, run `tools/qf review` (or rely on `tools/qf do` auto-review checkpoint) and resolve drift blockers before ship.
  - Keep conversation evidence fresh: `tools/qf sync|ready|orient|choose|council|arbiter|slice` should append checkpoint notes into `reports/<RUN_ID>/conversation.md` (unless explicitly disabled).
   - At major checkpoints (and before `/quit`), run:
     `tools/qf snapshot NOTE="decision + next step"` to persist session fallback in repo.
   - `tools/qf do` / `tools/qf resume` must keep execution traces in
     `reports/<RUN_ID>/execution.jsonl` (default redaction on).
6) If restatement is missing or unclear, STOP and do not modify code.

## 9) Governance policy (Default)
- This repo is PR-driven and local-verify-first.
- Required before ship: local `make verify` is green and recorded in reports.
- Do not rely on GitHub Actions queues as required path.
- `.github/workflows/*.yml|*.yaml` is blocked by default in `tools/ship.sh`.
  To allow intentionally for one run:
  - `SHIP_ALLOW_WORKFLOWS=1 tools/ship.sh "<msg>"`

## 10) Documentation freshness gate (Hard rule)
- Any process/rule/tooling behavior change in this repo MUST update owner docs in the same RUN.
- Minimum required updates per process change:
  - `AGENTS.md` (hard rule layer)
  - `docs/WORKFLOW.md` (execution/state-machine layer)
  - `SYNC/*` entry docs if startup/order semantics changed
  - `TASKS/STATE.md` current pointers if active run/task changed
  - `reports/<RUN_ID>/summary.md` + `reports/<RUN_ID>/decision.md` evidence
- No doc update, no ship.
