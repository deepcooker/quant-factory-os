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
- `python3 tools/init.py -status`
- `python3 -m py_compile tools/init.py tools/learn.py tools/ready.py tools/orient.py tools/choose.py tools/council.py tools/arbiter.py tools/slice_task.py tests/task_ops.py tests/task_run.py tests/task_enter.py`

## Notes
- Historical evidence content was intentionally removed per request for development-design phase reset.


## Incremental update (remove single ops entrypoint)
- Removed `tools/ops` dispatcher file; no single CLI entrypoint remains.
- Default usage is now direct scripts:
  - `python3 tools/init.py`
  - `python3 tools/learn.py`
  - `python3 tools/ready.py`
  - `python3 tools/orient.py` / `choose.py` / `council.py` / `arbiter.py` / `slice_task.py`
  - legacy commands via `bash tools/legacy.sh <subcommand>`
- Updated wrappers (`enter.sh`, `onboard.sh`, `start.sh`) and docs/tests to remove `tools/ops` main-entry dependency.

### Verify (incremental)
- `python3 tools/init.py -status` -> pass
- `python3 -m py_compile tools/*.py tests/task_ops.py tests/task_run.py tests/task_enter.py` -> pass
- `bash -n tools/enter.sh tools/onboard.sh tools/start.sh tools/legacy.sh tools/ship.sh tools/task.sh` -> pass


## Incremental update (learn anti-water gates)
- Upgraded learn practice gate: command evidence must prove `tools/view.sh` actually covered every required file.
- Upgraded strong plan gate: `plan_protocol.evidence` must mention every required file.
- Upgraded oral gate: `oral_exam` now requires at least 2 `pass` items.
- Prompt updated to force file-grounded evidence format (`<path>#<section>: <concrete fact>`).

### Verify (incremental)
- `python3 -m py_compile tools/learn.py tools/ready.py tools/init.py` -> pass
- `python3 tools/learn.py PLAN_TRANSPORT=exec -log` -> expected fail (`expected auto|slash`)
- Source checks:
  - `required files not actually viewed via tools/view.sh`
  - `plan_protocol.evidence missing required files`
  - `oral_exam insufficient passes`

## Incremental update (model 5.4 switch attempt rejected by real runtime)
- Attempted to unify the learn default model with the current chat session model (`gpt-5.4-codex`).
- Real runtime verification failed in `tools/learn.py` model sync because the local Codex CLI account path rejected `gpt-5.4-codex`.
- Restored the executable baseline to `gpt-5.3-codex` so `learn` remains working by default.

### Verify (incremental)
- `python3 -m py_compile tools/learn.py tools/codex_transport.py tests/test_codex_transport.py CODEX_APP_SERVER_PYTHON_TEST.py` -> pass
- `python3 tools/learn.py -minimal` -> pass on restored `gpt-5.3-codex` baseline
- `learn/project-0.model.events.jsonl` captured hard failure for attempted `gpt-5.4-codex` switch:
  - `The 'gpt-5.4-codex' model is not supported when using Codex with a ChatGPT account.`

## Incremental update (app-server smoke bug fixed and re-tested)
- Found a false-positive bug in `CODEX_APP_SERVER_PYTHON_TEST.py`:
  - it marked `APP_SERVER_TURN_OK=true` as soon as it saw `turn/completed`
  - it did not check `turn.status` or `turn.error`
- Found a second bug:
  - artifact filenames used second-level timestamps, so concurrent runs could overwrite each other
- Fixed both:
  - `APP_SERVER_TURN_OK` now requires `turn.status=completed`
  - `APP_SERVER_EFFORT_VALIDATION_OK` is false when the turn did not complete
  - artifact names now use microsecond timestamps
- Re-tested serially:
  - `gpt-5.3-codex` -> pass
  - `gpt-5.4-codex` -> fail with explicit ChatGPT-account unsupported error

### Verify (incremental)
- `python3 -m py_compile CODEX_APP_SERVER_PYTHON_TEST.py` -> pass
- `timeout 50s python3 CODEX_APP_SERVER_PYTHON_TEST.py --mode plan --effort xhigh --model gpt-5.3-codex --timeout 25` -> pass
- `timeout 50s python3 CODEX_APP_SERVER_PYTHON_TEST.py --mode plan --effort xhigh --model gpt-5.4-codex --timeout 25` -> fail as expected
- Evidence:
  - `test_codex/app_server_runtime/20260305T210523151594Z.summary.json`
  - `test_codex/app_server_runtime/20260305T210546385697Z.summary.json`
  - `test_codex/app_server_runtime/20260305T210546385697Z.events.jsonl`

## Incremental update (learn default model simplified to gpt-5.4)
- Changed `tools/learn.py` default model from `gpt-5.3-codex` to `gpt-5.4`.
- Added one-shot model override:
  - `model=<slug>`
  - `-model <slug>`
- Fixed the log-mirror self-run so it preserves the selected model when `learn` re-executes itself for stdout logging.
- Updated workflow/playbook/guide/AGENTS text to match the new default and override usage.

### Verify (incremental)
- `python3 -m py_compile tools/learn.py tests/test_learn_cli.py tests/test_codex_transport.py` -> pass
- `python3 - <<'PY' ... parse_cli([] / model=... / -model ...)` -> pass
- `timeout 120s python3 tools/learn.py -minimal` -> pass on default `gpt-5.4`
- `timeout 120s python3 tools/learn.py -minimal -model gpt-5.3-codex` -> pass on override

## Incremental update (PROJECT_GUIDE-driven learn rewrite)
- Rebuilt `tools/learn.py` around `PROJECT_GUIDE` as the primary course file.
- `learn` now expands required reads from three owner docs:
  - `docs/PROJECT_GUIDE.md`
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  plus each question's `必查文件`.
- Removed `oral_exam` and replaced it with full-question `guide_oral` validation.
- Removed `exec` fallback from learn transport; learn now requires `codex app-server` true plan mode.
- Added `PROJECT_GUIDE` parser and strict validation for:
  - full Q1..Q17 coverage
  - fixed Q-order
  - per-question must-read evidence coverage
  - tools/view.sh command coverage for all required files
- Rewrote `docs/PROJECT_GUIDE.md` into course format:
  - question
  - why this matters
  - standard answer
  - must-read files
  - search hints
  - mainline meaning
- Updated `AGENTS.md`, `docs/WORKFLOW.md`, `CODEX_CLI_PLAYBOOK.md` to match the new learn semantics.
- Updated `tools/ready.py` to accept the new `qf_learn.v3` schema.
- Added/rewrote tests for:
  - CLI parsing
  - transport behavior
  - PROJECT_GUIDE parsing
  - learn model output parsing

### Verify (incremental)
- `python3 -m py_compile tools/codex_transport.py tools/learn.py tools/ready.py` -> pass
- `python3 -m py_compile tools/learn.py` -> pass after parser fix
- ad-hoc parser smoke:
  - `parse_project_guide(docs/PROJECT_GUIDE.md)` -> 17 questions detected
- `python3 -m pytest ...` could not run in this environment:
  - `No module named pytest`
- real smoke:
  - `python3 tools/learn.py -medium` now reaches true model-sync stage with 17-question course expansion and 16 required files
  - full completion is still heavy under current prompt shape; runtime optimization remains a follow-up item if medium-speed onboarding must finish faster
