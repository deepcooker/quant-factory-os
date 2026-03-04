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
