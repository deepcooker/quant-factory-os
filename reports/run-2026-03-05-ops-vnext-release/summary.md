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

## Incremental update (learn parser hardening after real rerun)
- Removed dead legacy ready code from `tools/ready.py` so the file now only contains the pure-gate path.
- Hardened `tools/learn.py` model parsing:
  - when `model.raw.txt` contains process prose before the final JSON packet, learn now searches for the first JSON object that matches the onboarding schema instead of trusting the first `{...}` block.
- Re-ran real `learn` model-sync attempts:
  - sandboxed runs exposed `~/.codex` cache write failures (`Permission denied`) from Codex app-server
  - unsandboxed re-run removed the cache error, but `learn -low/-medium` still remained too heavy and did not finish in a practical time window
- Current conclusion:
  - one parser bug is fixed
  - the remaining blocker is onboarding prompt/runtime weight, not the learn gate schema itself

### Verify (incremental)
- `python3 -m py_compile tools/learn.py tools/ready.py` -> pass
- `python3 - <<'PY' ... parse_model_output(...) ...` on the interrupted raw artifact now fails later for incomplete JSON instead of mis-parsing the first non-target `{...}` block
- real rerun findings:
  - sandboxed `learn` showed `failed to renew cache TTL: Permission denied (os error 13)`
  - unsandboxed `learn` removed that permission error but still did not produce `model.raw.txt` within the observation window

## Incremental update (learn reading strategy rollback + view.sh compatibility)
- Kept the `tools/view.sh` interface fix because the model naturally called two forms that previously caused avoidable tool errors:
  - `tools/view.sh -h`
  - `tools/view.sh <path> 120`
- Rolled back the temporary hardcoded learn reading script. The fixed line-range plan was useful for debugging, but it is not acceptable as the long-term onboarding design because it overfits the current document layout.
- `tools/learn.py` now constrains reading strategy instead of hardcoding reading commands:
  - read owner docs first
  - then read additional required files
  - use `tools/view.sh` for all reads
  - prefer targeted section reads over whole-document sweeps
  - avoid extra exploration unless a required read was truncated or a question needs one short lookup
- Current conclusion:
  - `view.sh` ergonomics improved in a durable way
  - learn prompt direction is now back on the right architecture (`strategy`, not `script`)
  - the latest failed smoke was still blocked by Codex usage limits, not by repo logic

### Verify (incremental)
- `bash -n tools/view.sh` -> pass
- `bash tools/view.sh -h` -> pass
- `bash tools/view.sh docs/WORKFLOW.md 20` -> pass
- prompt inspection on `tools/learn.py` confirms:
  - no `Exact reading plan`
  - no hardcoded `--from/--to` read script
  - targeted-section read guidance remains
- latest model event stream ended with usage quota failure rather than prompt/schema failure:
  - `learn/project-0.model.events.jsonl` -> `usage_limit_exceeded`

## Incremental update (real learn -> ready closure passed after quota recovery)
- Re-ran the real onboarding flow after quota recovery:
  - `env PYTHONUNBUFFERED=1 QF_LEARN_LOG_ACTIVE=1 python3 tools/learn.py -low`
  - `python3 tools/ready.py`
- `learn -low` completed successfully under:
  - real Codex app-server
  - real plan mode
  - `gpt-5.4`
  - low reasoning effort
- The pass still preserved the intended onboarding depth:
  - required files read: `10/10`
  - full `PROJECT_GUIDE` oral coverage: `Q1..Q17`
  - practice evidence: `38` `tools/view.sh` command reads
  - anchor status: `on_track`
- `ready` then passed as a pure gate and wrote:
  - `reports/run-2026-03-05-ops-vnext-release/ready.json`
- Current conclusion:
  - the strategy-based reading prompt did not damage sync quality
  - the current blocker has shifted from “can it close at all” to simple daily ergonomics tuning for `-medium`

### Verify (incremental)
- `env PYTHONUNBUFFERED=1 QF_LEARN_LOG_ACTIVE=1 python3 tools/learn.py -low` -> pass
- `python3 tools/ready.py` -> pass
- key outputs:
  - `LEARN_MODEL_SYNC_STATUS: pass`
  - `LEARN_MODEL_ORAL_Q_COUNT: 17`
  - `LEARN_MODEL_ANCHOR_STATUS: on_track`
  - `READY_LEARN_STATUS: pass`
  - `READY_NEXT_COMMAND: python3 tools/orient.py`

## Incremental update (transport commentary filtering + final JSON hot-path fix)
- Hardened `tools/codex_transport.py` around app-server plan-mode output handling:
  - track `agentMessage.phase`
  - ignore `commentary` chunks
  - only accumulate `final_answer`
- Fixed the final JSON extraction hot path:
  - do not rescan the entire accumulated output on every delta
  - only attempt JSON extraction after seeing likely JSON-closing chunks or on item completion
- Added app-server exit detection so `learn` no longer risks waiting forever when the child process exits without a usable final packet.
- Re-ran the real onboarding flow after these transport changes:
  - `env PYTHONUNBUFFERED=1 QF_LEARN_LOG_ACTIVE=1 python3 tools/learn.py -low` -> pass
  - `python3 tools/ready.py` -> pass
- Tried the next daily-use profile:
  - `env PYTHONUNBUFFERED=1 QF_LEARN_LOG_ACTIVE=1 python3 tools/learn.py -medium`
  - result: model sync failed due Codex account quota, not due repo logic

### Verify (incremental)
- `python3 -m py_compile tools/codex_transport.py tools/learn.py` -> pass
- `env PYTHONUNBUFFERED=1 QF_LEARN_LOG_ACTIVE=1 python3 tools/learn.py -low` -> pass
- `python3 tools/ready.py` -> pass
- `env PYTHONUNBUFFERED=1 QF_LEARN_LOG_ACTIVE=1 python3 tools/learn.py -medium` -> fail with quota event
- key evidence:
  - `learn/project-0.model.events.jsonl` -> `item/started` shows `agentMessage.phase=commentary|final_answer`
  - `learn/project-0.model.events.jsonl` -> `usage_limit_exceeded`
  - `learn/project-0.model.stderr.log` -> app-server exits with quota-related failure during `-medium`
