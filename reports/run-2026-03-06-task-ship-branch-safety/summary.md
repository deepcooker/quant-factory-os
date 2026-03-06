# Summary

RUN_ID: `run-2026-03-06-task-ship-branch-safety`

## What changed
- Updated `tools/ship.sh` to default to the current active branch as `base_branch` instead of unconditionally switching to `main`.
- Scoped `fetch/pull origin main` to the explicit `main` base case only, and made branch creation, PR base, diff stat, and post-ship sync follow `base_branch`.
- Updated `tools/task.sh` to pass the current branch to `tools/ship.sh` via `SHIP_BASE_BRANCH`.
- Added regression checks in `tests/task_ship.py` and `tests/task_task.py`, and documented the continuity rule in `docs/WORKFLOW.md` and `docs/PROJECT_GUIDE.md`.

## Commands / Outputs
- `bash -n tools/ship.sh && bash -n tools/task.sh` -> pass
- `python3 -m pytest -q tests/task_ship.py tests/task_task.py tests/task_run.py` -> failed in this environment: `No module named pytest`
- `make verify` -> `21 passed in 1.46s`
- `bash tools/legacy.sh review RUN_ID=run-2026-03-06-task-ship-branch-safety STRICT=1 AUTO_FIX=1` -> pass (`REVIEW_BLOCKERS: 0`, `REVIEW_WARNINGS: 1`)

## Notes
- This task was triggered by a real failure path: `tools/task.sh` moved the session from `run-2026-03-05-ops-vnext-release` to an outdated `main`, which then lacked Python-first files such as `tools/codex_transport.py`.
- The fix keeps branch continuity by default while still preserving the old `main`-based behavior when `SHIP_BASE_BRANCH=main`.
- Strict review required run-level direction artifacts, so this run also includes minimal `orient_choice.json` and `direction_contract.json` to preserve governance lineage.
