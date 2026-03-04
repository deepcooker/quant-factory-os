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

## Commands / Outputs
- `tools/view.sh TASKS/STATE.md`
- `tools/view.sh TASKS/QUEUE.md`
- `tools/view.sh AGENTS.md`
- `tools/view.sh reports/run-2026-03-04-remove-sync-entry/summary.md`
- `tools/view.sh reports/run-2026-03-04-remove-sync-entry/decision.md`
- Updated file: `AGENTS.md`
- `git rm -f tests/test_run_a9_dryrun.py tests/test_run_a9_probe.py tests/test_qf_current_run.py tests/test_qf_execute.py tests/test_qf_execution_log.py tests/test_qf_handoff.py tests/test_qf_orient_and_do.py tests/test_qf_plan_clean.py tests/test_qf_ready_gate.py tests/test_qf_review.py tests/test_qf_stash_clean.py tests/test_qf_sync_gate.py`
- Added file: `tests/task_qf.py`
- Verify attempt:
  - `pytest -q tests/task_qf.py` -> command not found
  - `python3 -m pytest -q tests/task_qf.py` -> `No module named pytest`

## Notes
- This update is focused on hard-rule contract text for sharing with GPT web session.
- Full repo consistency verify is pending in this step (not run yet).
- Local environment currently lacks `pytest` runtime, so test execution could not be completed in this shell.
