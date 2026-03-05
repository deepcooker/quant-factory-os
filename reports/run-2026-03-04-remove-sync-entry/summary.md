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
