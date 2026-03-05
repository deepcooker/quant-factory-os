# Decision

RUN_ID: `run-2026-03-05-ops-vnext-release`

## Why
- Current phase is development/design; old task/report history created noise and slowed execution.

## Decision
- Remove historical `TASKS/TASK-*` and previous `reports/*` content.
- Keep only minimal active pointers and one active task.
- Ship as a clean baseline version.

## Risk
- Historical audit trail is no longer available in-repo after this reset.

## Stop reason
- task_done


## Incremental decision (no single ops entrypoint)
### Why
- Single dispatcher `tools/ops` is unnecessary overhead for current development-design stage.

### Decision
- Remove `tools/ops` from the default workflow and delete the dispatcher file.
- Use direct Python scripts for migrated commands and `tools/legacy.sh` for legacy commands.

### Risk / rollback
- Risk: old notes that mention `tools/ops` may become stale.
- Rollback: restore `tools/ops` thin dispatcher from git history if needed.


## Incremental decision (learn evidence hardening)
### Why
- Existing learn gate could pass with weak command evidence and generic plan evidence, causing low-quality sync summaries.

### Decision
- Require `tools/view.sh`-based required-file coverage in practice evidence.
- Require `plan_protocol.evidence` to cover every required file.
- Require oral exam minimum pass threshold (>=2 pass).

### Risk / rollback
- Risk: stricter gate may fail more often when model output is incomplete.
- Rollback: relax each gate in `tools/learn.py` if needed.

## Incremental decision (do not switch learn default model to gpt-5.4-codex yet)
### Why
- The current chat session may use `gpt-5.4-codex`, but the local Codex CLI account path used by `tools/learn.py` rejected that model at runtime.
- Real verification produced a hard API error during model sync, so changing the default would leave `learn` broken by default.

### Decision
- Keep the automation default model at `gpt-5.3-codex`.
- Treat `gpt-5.4-codex` as unsupported for this local Codex CLI account path until a later verification proves otherwise.

### Evidence
- `learn/project-0.model.events.jsonl` recorded:
  - `The 'gpt-5.4-codex' model is not supported when using Codex with a ChatGPT account.`
- Re-run on `gpt-5.3-codex` passed:
  - `learn/project-0.stdout.log` -> `LEARN_MODEL_SYNC_STATUS: pass`

### Risk / rollback
- Risk: session model and automation model stay split for now.
- Rollback path: switch the constant only after a successful real `python3 tools/learn.py -minimal` verification on `gpt-5.4-codex`.

## Incremental decision (fix app-server smoke false positive before trusting 5.4 tests)
### Why
- `CODEX_APP_SERVER_PYTHON_TEST.py` incorrectly treated any matching `turn/completed` notification as success.
- That produced a false positive: summary said `APP_SERVER_TURN_OK: true` for `gpt-5.4-codex`, while the corresponding `events.jsonl` clearly showed `turn.status=failed` with a 400 model-support error.
- The script also used second-level artifact timestamps, so concurrent runs could overwrite each other.

### Decision
- Tighten the smoke verdict: `APP_SERVER_TURN_OK` is only true when `turn.status=completed`.
- Surface `turn.error` in `checks.detail`.
- Mark `APP_SERVER_EFFORT_VALIDATION_OK` false when the turn does not complete successfully.
- Use microsecond-level artifact timestamps to avoid output collisions.

### Evidence
- Successful `gpt-5.3-codex` app-server run:
  - `test_codex/app_server_runtime/20260305T210523151594Z.summary.json`
- Rejected `gpt-5.4-codex` app-server run under ChatGPT login:
  - `test_codex/app_server_runtime/20260305T210546385697Z.summary.json`
  - `test_codex/app_server_runtime/20260305T210546385697Z.events.jsonl`

### Risk / rollback
- Risk: existing notes that assumed `APP_SERVER_TURN_OK` meant only "saw turn/completed" are now stale.
- Rollback: not recommended; the old behavior was factually incorrect.

## Incremental decision (make learn default to gpt-5.4 but keep one-shot model override)
### Why
- Official Codex direction and local CLI config have moved to `gpt-5.4`, so keeping `learn` pinned to `gpt-5.3-codex` adds unnecessary friction.
- The workflow still needs a simple escape hatch when a run must target another supported model.

### Decision
- Change `tools/learn.py` default model constant to `gpt-5.4`.
- Allow one-shot model override via either `model=<slug>` or `-model <slug>`.
- Preserve the existing strong-mode and reasoning controls unchanged.

### Evidence
- Default run passed on `gpt-5.4`:
  - `learn/project-0.stdout.log` -> `LEARN_MODEL: gpt-5.4`
  - `learn/project-0.stdout.log` -> `LEARN_MODEL_SYNC_STATUS: pass`
- Override run passed on `gpt-5.3-codex`:
  - `learn/project-0.stdout.log` -> `LEARN_MODEL: gpt-5.3-codex`
  - `learn/project-0.stdout.log` -> `LEARN_MODEL_SYNC_STATUS: pass`

### Risk / rollback
- Risk: slower completion on some prompts when using `gpt-5.4`.
- Rollback: invoke `python3 tools/learn.py -model gpt-5.3-codex` or revert the default constant if needed.
