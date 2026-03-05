# Summary

RUN_ID: `run-2026-03-04-remove-sync-entry`

## What changed
- Re-generated `AGENTS.md` using the new mainline contract: startup anchor is `AGENTS.md + docs/PROJECT_GUIDE.md`.
- Removed remaining `SYNC`-entry semantics from hard-rule narrative in `AGENTS.md`.
- Kept workflow enforceable but lightweight: mandatory gate is `init -> learn -log -> ready`, then `Plan -> Confirm -> Execute`.
- Clarified owner-doc boundaries and anti-drift rule: when drift happens, return to `docs/PROJECT_GUIDE.md` question system before coding.
- Reduced test surface for qf lane:
  - removed all `tests/test_qf_*.py` files
  - removed `tests/test_run_a9_dryrun.py` and `tests/test_run_a9_probe.py`
  - added merged minimal test module `tests/task_qf.py`
- Followed request to drop sync-related gate tests by removing `tests/test_qf_sync_gate.py`.
- Merged all remaining `tests/test_*.py` modules into minimal `tests/task_*.py` modules:
  - added: `task_codex.py`, `task_docs.py`, `task_enter.py`, `task_observe.py`, `task_run.py`, `task_ship.py`, `task_start.py`, `task_task.py`, `task_view.py`
  - removed remaining split tests under `tests/test_*.py`
- Reworked `tools/qf init` to environment-diagnostic mode:
  - removed automatic side effects from init path (no auto-stash, no auto-sync-main, no auto-handoff)
  - added mode flags: `tools/qf init` (check), `tools/qf init -status` (status-only), `tools/qf init -main` (strict main-oriented gate)
  - added structured outputs: account/version, branch/upstream, diff summary, run/task state, last-change evidence, status/reason/next command
- Updated workflow docs to match the new init contract.
- Added AGENTS pointer to keep init detail ownership in `docs/WORKFLOW.md (S0 Environment)` and keep AGENTS gate-only.

## Commands / Outputs
- `tools/view.sh TASKS/STATE.md`
- `tools/view.sh TASKS/QUEUE.md`
- `tools/view.sh AGENTS.md`
- `tools/view.sh reports/run-2026-03-04-remove-sync-entry/summary.md`
- `tools/view.sh reports/run-2026-03-04-remove-sync-entry/decision.md`
- Updated file: `AGENTS.md`
- `git rm -f tests/test_run_a9_dryrun.py tests/test_run_a9_probe.py tests/test_qf_current_run.py tests/test_qf_execute.py tests/test_qf_execution_log.py tests/test_qf_handoff.py tests/test_qf_orient_and_do.py tests/test_qf_plan_clean.py tests/test_qf_ready_gate.py tests/test_qf_review.py tests/test_qf_stash_clean.py tests/test_qf_sync_gate.py`
- Added file: `tests/task_qf.py`
- `git rm -f tests/test_*.py`
- Added files:
  - `tests/task_codex.py`
  - `tests/task_docs.py`
  - `tests/task_enter.py`
  - `tests/task_observe.py`
  - `tests/task_run.py`
  - `tests/task_ship.py`
  - `tests/task_start.py`
  - `tests/task_task.py`
  - `tests/task_view.py`
- Verify attempt:
  - `pytest -q tests/task_qf.py` -> command not found
  - `python3 -m pytest -q tests/task_qf.py` -> `No module named pytest`
- `bash -n tools/qf` -> pass
- `tools/qf init -status` -> pass (`INIT_STATUS: needs_resume`, reminder text suppressed)
- `tools/qf init` -> pass (`INIT_STATUS: needs_resume`, emits resume hint)
- `tools/qf init -main` -> fail as expected (`INIT_STATUS: blocked` under dirty workspace)

## Notes
- This update is focused on hard-rule contract text for sharing with GPT web session.
- Full repo consistency verify is pending in this step (not run yet).
- Local environment currently lacks `pytest` runtime, so test execution could not be completed in this shell.
- `init` now acts as an environment health check only; continuity/learning/execution remain in `learn -> ready -> discuss/execute`.

## Incremental update (learn hard-sync enforcement)
- `tools/qf learn` is now hard-gated to real model sync:
  - `MODEL_SYNC` only accepts `1`
  - `PLAN_MODE` only accepts `strong`
  - `codex` CLI missing -> learn fails immediately
- Model output is now validated against required-read coverage:
  - `files_read` must include all required onboarding files from learn context
- Learn validity gate strengthened:
  - `learn_file_is_valid` now requires `model_sync.status=pass`, `model_sync.passed=true`, `mode=1`, `plan_mode=strong`
  - required model result packets must exist (`plan_protocol`, `oral_restate`, `oral_exam`, etc.)
- Owner docs aligned with new policy:
  - `AGENTS.md` learn gate text updated to mandatory model sync
  - `docs/WORKFLOW.md` learn section updated (path moved to `learn/{project_id}.*`, mandatory sync semantics)
  - `docs/PROJECT_GUIDE.md` learn command updated to `tools/qf learn -log` (strong mode now default hard gate)

### Verify (this update)
- `bash -n tools/qf` -> pass
- `tools/qf learn PROJECT_ID=project-0 MODEL_SYNC=0` -> expected fail (`learn requires model sync`)
- `tools/qf learn PROJECT_ID=project-0 PLAN_MODE=basic` -> expected fail (`learn requires PLAN_MODE=strong`)
- `tools/qf learn PROJECT_ID=project-0 MODEL_TIMEOUT_SEC=120` -> pass (model anchors emitted)
- `tools/qf ready` -> pass (`READY_LEARN_REPORT: learn/project-0.json`)

## Incremental update (learn = plan packet + oral + practice + anchor)
- Strengthened `tools/qf learn` strong-schema:
  - Added mandatory `anchor_realign` packet (question_id/status/drift_detail/return_to_mainline)
  - Added mandatory `practice` packet derived from model events (`command_execution_count` + command samples)
- Console anchor outputs expanded:
  - `LEARN_MODEL_ANCHOR_QUESTION_ID`
  - `LEARN_MODEL_ANCHOR_STATUS`
  - `LEARN_MODEL_ANCHOR_DRIFT_DETAIL`
  - `LEARN_MODEL_ANCHOR_RETURN_ACTION`
  - `LEARN_MODEL_PRACTICE_COMMAND_COUNT`
  - `LEARN_MODEL_PRACTICE_SAMPLE_1..n`
- Learn validity gate upgraded (`learn_file_is_valid`):
  - requires `anchor_realign` + `practice` packets to exist and pass minimum checks
- Updated learning knowledge base docs:
  - removed Q18 from `docs/PROJECT_GUIDE.md` (not a mainline-realign question)
  - moved Q16 codex sample evidence off `reports/run-*` paths to `test_codex/artifacts/*` + codex docs
  - synced learn anchors section in `docs/WORKFLOW.md`
- Updated exam auto template wording in `tools/qf`:
  - Q16 evidence paths now point to `test_codex/artifacts/*` and codex docs
  - mainline next command updated to `tools/qf learn -log`

### Verify (this update)
- `bash -n tools/qf` -> pass
- `tools/qf learn PROJECT_ID=project-0 MODEL_TIMEOUT_SEC=120` -> pass
  - includes new anchor/practice stdout fields
- `tools/qf ready` -> pass (new learn gate accepted)

## Incremental update (learn console readability)
- Added a human-readable readout block in `tools/qf learn` output (no gate semantics changed):
  - `LEARN_READOUT_BEGIN` ... `LEARN_READOUT_END`
  - includes mainline/current stage/next step/oral focus/anchor/practice summary
- Existing machine anchors and strict validation remain unchanged.

### Verify (this update)
- `bash -n tools/qf` -> pass
- `tools/qf learn PROJECT_ID=project-0 MODEL_TIMEOUT_SEC=90` -> pass
  - confirms `LEARN_READOUT_*` block is printed

## Incremental update (learn defaults)
- Changed learn defaults for lower-friction onboarding:
  - `QF_LEARN_MODEL_TIMEOUT_SEC` default from `180` -> `300`
  - `QF_LEARN_LOG` default from `0` -> `1` (stdout mirror on by default)
- Updated docs and guide wording:
  - session gate command changed from `tools/qf learn -log` to `tools/qf learn`
  - workflow updated with default-on log behavior and `QF_LEARN_LOG=0` one-shot disable
  - timeout default updated to `300`
- Synced helper answer template text inside `tools/qf`:
  - next-step command uses `tools/qf learn` (without `-log`)

### Verify (this update)
- `bash -n tools/qf` -> pass
- `tools/qf learn PROJECT_ID=project-0` -> pass
  - confirms `LEARN_LOG_FILE: learn/project-0.stdout.log`
  - confirms `LEARN_MODEL_TIMEOUT_SEC: 300`

## Incremental update (learn /plan wrapper + QID-bound oral exam)
- Reworked learn plan transport to be explicit and auditable:
  - `PLAN_TRANSPORT=auto|slash|exec` supported (`auto` default)
  - `auto` now checks PTY capability:
    - PTY available -> `slash`
    - no PTY devices -> `exec`
  - console now prints:
    - `LEARN_MODEL_PLAN_TRANSPORT`
    - `LEARN_MODEL_PLAN_TRANSPORT_AUTO_REASON` (when auto)
    - `LEARN_MODEL_PLAN_TRANSPORT_EFFECTIVE`
- Strengthened model prompt contract:
  - forbids calling `tools/qf init/learn/ready` during model-sync pass
  - requires minimal read-only evidence gathering only
- Upgraded strong oral exam schema:
  - each `oral_exam` item must include `question_id`
  - `question_id` must map to `Q1..Q17` in `docs/PROJECT_GUIDE.md`
  - stdout now prints `LEARN_MODEL_ORAL_EXAM_QID1..N`
- Updated owner docs to match behavior:
  - `AGENTS.md` learn gate transport/strictness notes
  - `docs/WORKFLOW.md` transport and QID anchor requirements

### Verify (this update)
- `bash -n tools/qf` -> pass
- `tools/qf learn MODEL_TIMEOUT_SEC=120 -log` -> pass
  - observed `LEARN_MODEL_PLAN_TRANSPORT: auto`
  - observed `LEARN_MODEL_PLAN_TRANSPORT_AUTO_REASON: no_pty_devices`
  - observed `LEARN_MODEL_PLAN_TRANSPORT_EFFECTIVE: exec`
  - observed `LEARN_MODEL_ORAL_EXAM_QID1: Q1`, `QID2: Q2`, `QID3: Q6`
- `tools/qf learn PLAN_TRANSPORT=slash MODEL_TIMEOUT_SEC=30` -> expected fail
  - observed `LEARN_MODEL_SYNC_REASON: no-pty-for-slash`
  - stderr evidence: `learn/project-0.model.stderr.log`
- `make verify` -> pass (`19 passed`)

## Incremental update (learn Python-first implementation)
- Added new Python runtime implementation: `tools/qf_learn.py`.
- Converted `tools/qf` `cmd_learn` to delegate to Python first; Bash now keeps compatibility wrapper/fallback role.
- Kept CLI contract compatible (same env vars and args), including:
  - `PROJECT_ID=...`, `TTL_DAYS=...`, `MODEL_SYNC=1`, `PLAN_MODE=strong`
  - `PLAN_TRANSPORT=auto|slash|exec`, `MODEL_TIMEOUT_SEC=...`, `MODEL=...`
  - `-log` / `LOG=<path>`
- Preserved strong learn outputs and gates:
  - `LEARN_STEP[1/4..4/4]`
  - model plan/oral/anchor/practice anchors
  - `LEARN_MODEL_ORAL_EXAM_QID1..N`
  - strict failure for `PLAN_TRANSPORT=slash` when host has no PTY devices.
- Improved `-log` streaming behavior:
  - child learn process now runs with `PYTHONUNBUFFERED=1`
  - console and log file receive line-by-line output in near real-time.
- Updated docs:
  - `docs/WORKFLOW.md` records Python-first learn implementation.
  - `AGENTS.md` records Python-first runtime note in learn gate criteria.

### Verify (this update)
- `python3 -m py_compile tools/qf_learn.py` -> pass
- `bash -n tools/qf` -> pass
- `tools/qf learn MODEL_TIMEOUT_SEC=120 -log` -> pass
- `tools/qf learn PLAN_TRANSPORT=slash MODEL_TIMEOUT_SEC=20` -> expected fail (`no-pty-for-slash`)
- `make verify` -> pass (`19 passed`)

## Incremental update (init Python-first implementation)
- Added new Python runtime implementation: `tools/qf_init.py`.
- Converted `tools/qf` `cmd_init` to delegate to Python first; Bash now keeps compatibility wrapper/fallback role.
- Kept `init` CLI contract compatible:
  - `tools/qf init`
  - `tools/qf init -status`
  - `tools/qf init -main`
- Preserved output schema and behavior:
  - `INIT_STEP[1/7..7/7]`
  - same status fields (`INIT_STATUS`, `INIT_REASON_CODES`, `INIT_NEXT`, `INIT_HINT`)
  - same mode behavior (`-status` suppress hint, `-main` strict non-zero on blocked)
  - same recommendation block in default check mode.
- Updated owner docs:
  - `docs/WORKFLOW.md` S0 now records Python-first implementation.
  - `AGENTS.md` mandatory gate notes init Python runtime.

### Verify (this update)
- `python3 -m py_compile tools/qf_init.py` -> pass
- `bash -n tools/qf` -> pass
- `tools/qf init -status` -> pass
- `tools/qf init` -> pass
- `tools/qf init -main` -> expected fail in dirty/non-main context (`RC=1`, `INIT_STATUS: blocked`)
- `make verify` -> pass (`19 passed`)

## Incremental update (ready Python-first implementation)
- Added new Python runtime implementation: `tools/qf_ready.py`.
- Converted `tools/qf` `cmd_ready` to delegate to Python first; Bash now keeps compatibility wrapper/fallback role.
- Kept ready gate behavior and outputs compatible:
  - same 12-step markers (`READY_STEP[1/12..12/12]`)
  - same run decision handling (`resume-close` / `abandon-new` / `continue`)
  - same restatement defaults and auto-fill semantics (`QF_READY_AUTO=1`)
  - same output artifacts (`ready.json`, `ready_brief`, `orient` draft)
  - same checkpoint writes (`execution.jsonl`, `conversation.md`, `TASKS/STATE.md`)
- In Python ready implementation, preserved:
  - learn gate auto-run behavior
  - optional sync gate compatibility behavior
  - orientation draft scoring + recommended option output.
- Updated owner docs:
  - `docs/WORKFLOW.md` S2 now records Python-first ready implementation.
  - `AGENTS.md` mandatory gate notes ready Python runtime.

### Verify (this update)
- `python3 -m py_compile tools/qf_ready.py` -> pass
- `bash -n tools/qf` -> pass
- `tools/qf ready` -> pass
- `tools/qf ready DECISION=abandon-new` -> pass
- `make verify` -> pass (`19 passed`)

## Incremental update (orient/choose/council/arbiter/slice Python-first)
- Added new Python runtime implementations:
  - `tools/qf_orient.py`
  - `tools/qf_choose.py`
  - `tools/qf_council.py`
  - `tools/qf_arbiter.py`
  - `tools/qf_slice.py`
- Converted `tools/qf` command handlers to delegate Python first for:
  - `cmd_orient`
  - `cmd_choose`
  - `cmd_council`
  - `cmd_arbiter`
  - `cmd_slice`
- Preserved behavior/output contracts:
  - discussion artifacts in `chatlogs/discussion/<RUN_ID>/...`
  - contract artifacts in `reports/<RUN_ID>/...`
  - queue slicing markers in `TASKS/QUEUE.md`
  - execution/conversation checkpoints and `TASKS/STATE.md` updates.

### Verify (this update)
- `python3 -m py_compile tools/qf_orient.py tools/qf_choose.py tools/qf_council.py tools/qf_arbiter.py tools/qf_slice.py` -> pass
- `bash -n tools/qf` -> pass
- `tools/qf orient RUN_ID=run-2026-03-04-remove-sync-entry` -> pass
- `tools/qf choose RUN_ID=run-2026-03-04-remove-sync-entry` -> pass
- `tools/qf council RUN_ID=run-2026-03-04-remove-sync-entry` -> pass
- `tools/qf arbiter RUN_ID=run-2026-03-04-remove-sync-entry` -> pass
- `tools/qf slice RUN_ID=run-2026-03-04-remove-sync-entry` -> pass
- `make verify` -> pass (`19 passed`)
