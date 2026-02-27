# Summary

RUN_ID: `run-2026-02-27-codex-ci-autofix-and-onboarding-constitution`

## What changed
- Updated `AGENTS.md` with mandatory session init gate and forced restatement readiness check before any coding.
- Added explicit governance defaults in `AGENTS.md`: PR-driven, local verify required, workflow changes blocked by default unless explicit override.
- Consolidated agent-facing entrypoints toward `tools/qf`:
  - `tools/qf` now has `onboard` subcommand.
  - `tools/enter.sh` is now a compatibility wrapper to `tools/qf init` (maps `ENTER_AUTOSTASH` to `QF_AUTOSTASH`).
  - `tools/onboard.sh` is now a compatibility wrapper to `tools/qf onboard`.
  - `tools/start.sh` now runs `tools/qf init` before launching Codex.
- Updated startup tests to assert wrapper/delegation behavior.
- Per owner request, removed historical backlog artifacts:
  - Deleted legacy `TASKS/TASK-*.md` files except current active task.
  - Deleted historical `reports/run-*` directories except current active RUN_ID.
  - Removed `TASKS/TODO_PROPOSAL.md` and `tests/__pycache__/`.
- Added onboarding constitution document `docs/CODEX_ONBOARDING_CONSTITUTION.md` with session gate, forced restatement, readiness checks, and rollback switches.
- Updated `docs/WORKFLOW.md` to reference governance/automation entrypoints.
- Set explicit repository policy: PR-driven, local `make verify` required, GitHub Actions optional/disabled by default.
- Added hard guard in `tools/ship.sh`: block `.github/workflows/*.yml|*.yaml` by default unless `SHIP_ALLOW_WORKFLOWS=1`.
- Added regression tests in `tests/test_ship_guard.py` for workflow guard block/override behavior.
- Updated `tools/qf` to proactively clean stale `reports/run-*-pick-candidate` directories in `init` and `do` (plan already cleaned).
- Removed stale local directory `reports/run-2026-02-27-pick-candidate/`.
- Fixed test-side artifact source in `tests/test_task_plan_pick.py` by setting `TASK_BOOTSTRAP_EVIDENCE=0` for `--pick queue-next` unit test, preventing repo-level evidence side effects.
- Hardened `tests/test_codex_read_denylist.py` to create and clean up `project_all_files.txt` during test execution for deterministic verify runs.
- Added task file `TASKS/TASK-codex-ci-autofix-and-onboarding-constitution.md` for this run.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-codex-ci-autofix-and-onboarding-constitution`
- `make verify` (first run failed on missing local `project_all_files.txt` fixture)
- `make verify` (final: `51 passed in 2.74s`)
- `make verify` (after policy update: `51 passed in 2.77s`)
- `make verify` (after ship workflow guard + tests: `53 passed in 3.40s`)
- `make verify` (after pick-candidate cleanup hardening: `53 passed in 3.15s`)
- `make verify` (after test artifact source fix + cleanup: `53 passed in 3.16s`)
- `make verify` (after AGENTS.md gate update: `53 passed in 3.55s`)
- `make verify` (after qf entrypoint consolidation: `53 passed in 3.43s`)
- `make verify` (after backlog cleanup: `53 passed in 3.45s`)

## Notes
- Automation strategy was revised to PR-only local-verify flow per owner preference.
- No business logic or production data paths were modified.
