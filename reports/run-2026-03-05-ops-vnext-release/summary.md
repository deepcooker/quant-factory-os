# Summary

RUN_ID: `run-2026-03-05-ops-vnext-release`

## What changed
- Cleared historical task files under `TASKS/TASK-*`.
- Cleared historical report artifacts under `reports/*`.
- Rebuilt minimal active task baseline:
  - `TASKS/STATE.md`
  - `TASKS/QUEUE.md`
  - `TASKS/TASK-vnext-release-cleanup.md`
- Removed single-entry requirement; direct script calls are now the default.

## Verify
- `python3 tools/ops_init.py -status`
- `python3 -m py_compile tools/ops_init.py tools/ops_learn.py tools/ops_ready.py tools/ops_orient.py tools/ops_choose.py tools/ops_council.py tools/ops_arbiter.py tools/ops_slice.py tests/task_ops.py tests/task_run.py tests/task_enter.py`

## Notes
- Historical evidence content was intentionally removed per request for development-design phase reset.


## Incremental update (remove single ops entrypoint)
- Removed `tools/ops` dispatcher file; no single CLI entrypoint remains.
- Default usage is now direct scripts:
  - `python3 tools/ops_init.py`
  - `python3 tools/ops_learn.py`
  - `python3 tools/ops_ready.py`
  - `python3 tools/ops_orient.py` / `ops_choose.py` / `ops_council.py` / `ops_arbiter.py` / `ops_slice.py`
  - legacy commands via `bash tools/ops_legacy.sh <subcommand>`
- Updated wrappers (`enter.sh`, `onboard.sh`, `start.sh`) and docs/tests to remove `tools/ops` main-entry dependency.

### Verify (incremental)
- `python3 tools/ops_init.py -status` -> pass
- `python3 -m py_compile tools/ops_*.py tests/task_ops.py tests/task_run.py tests/task_enter.py` -> pass
- `bash -n tools/enter.sh tools/onboard.sh tools/start.sh tools/ops_legacy.sh tools/ship.sh tools/task.sh` -> pass


## Incremental update (learn anti-water gates)
- Upgraded learn practice gate: command evidence must prove `tools/view.sh` actually covered every required file.
- Upgraded strong plan gate: `plan_protocol.evidence` must mention every required file.
- Upgraded oral gate: `oral_exam` now requires at least 2 `pass` items.
- Prompt updated to force file-grounded evidence format (`<path>#<section>: <concrete fact>`).

### Verify (incremental)
- `python3 -m py_compile tools/ops_learn.py tools/ops_ready.py tools/ops_init.py` -> pass
- `python3 tools/ops_learn.py PLAN_TRANSPORT=exec -log` -> expected fail (`expected auto|slash`)
- Source checks:
  - `required files not actually viewed via tools/view.sh`
  - `plan_protocol.evidence missing required files`
  - `oral_exam insufficient passes`
