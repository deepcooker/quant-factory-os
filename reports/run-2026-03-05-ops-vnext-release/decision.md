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

## Incremental decision (rebuild learn around PROJECT_GUIDE course flow)
### Why
- The previous learn flow proved model interaction and anchors, but it still behaved like a partial exam gate rather than a full onboarding curriculum.
- The project goal is stronger: `learn` must really synchronize project goal, constitution, workflow, skills, project status, and session continuity through `PROJECT_GUIDE`, not through shallow chat memory.
- `exec` fallback also weakened the guarantee that learn was running under true plan mode.

### Decision
- Rebuild `tools/learn.py` so `PROJECT_GUIDE` becomes the primary onboarding course.
- Keep `AGENTS.md` and `docs/WORKFLOW.md` as owner docs, but let `PROJECT_GUIDE` drive all additional evidence reads through per-question `必查文件`.
- Remove `oral_exam` and require full-question oral restatement (`guide_oral`) across the entire question bank.
- Remove `exec` fallback; learn must now succeed only through `codex app-server` true plan mode.
- Treat `/compact` as a long-session recommendation, not as a learn gate.

### Evidence
- `tools/learn.py`
- `tools/codex_transport.py`
- `docs/PROJECT_GUIDE.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `CODEX_CLI_PLAYBOOK.md`
- `tools/ready.py`

### Risk / rollback
- Risk: full-question learn is now much heavier, especially at `-medium` and above.
- Risk: real model-sync completion time may still be too long for daily use until prompt/output size is tuned further.
- Rollback path: reduce `PROJECT_GUIDE` output verbosity or relax full-question oral scope only if runtime proves unacceptable in repeated real smokes.

### Current stop reason
- `needs_human_decision`
- Reason: implementation is landed, but real `-medium` onboarding runtime is still heavy enough that user should validate whether the full-question output shape matches desired day-to-day ergonomics.

## Incremental decision (separate learn parser bug from learn runtime weight)
### Why
- A real rerun after the latest workflow/ready cleanup exposed two different failure modes:
  - sandboxed Codex app-server attempts could fail on `~/.codex` cache writes
  - interrupted `model.raw.txt` content could begin with non-JSON process prose, which caused `tools/learn.py` to mis-parse the first `{...}` block instead of the intended onboarding packet
- The parser bug is a real code defect and should be fixed independently from the broader runtime-weight problem.

### Decision
- Remove dead legacy code from `tools/ready.py` and keep it as a pure gate only.
- Harden `tools/learn.py` so it scans `model.raw.txt` for the first JSON object that actually matches the learn packet shape (`mainline/current_stage/next_step/files_read`), rather than trusting the first decoded dict.
- Treat the remaining `learn -low/-medium` delay as a separate ergonomics/runtime problem to optimize next; do not conflate it with parser correctness.

### Evidence
- `tools/learn.py`
- `tools/ready.py`
- `learn/project-0.model.events.jsonl`
- `learn/project-0.model.stderr.log`

### Risk / rollback
- Risk: learn still remains too heavy for daily use until the prompt/tool loop is shortened.
- Rollback: none recommended for the parser change; the previous behavior was incorrect when raw output contained leading prose.

## Incremental decision (keep view.sh compatibility fix, reject hardcoded learn read script)
### Why
- The model naturally used `tools/view.sh -h` and `tools/view.sh <path> 120`. Rejecting those forms caused avoidable tool-loop noise during onboarding.
- A temporary hardcoded reading script reduced prompt drift during debugging, but it encoded current file layout and would make `learn` brittle as documents evolve.
- The latest failed real smoke was blocked by Codex quota (`usage_limit_exceeded`), so hardcoding reads would solve the wrong problem.

### Decision
- Keep the durable `tools/view.sh` compatibility improvements.
- Remove the hardcoded reading-plan prompt from `tools/learn.py`.
- Keep only strategy-level guidance in learn:
  - read owner docs first
  - read required files next
  - use `tools/view.sh`
  - prefer targeted section reads
  - avoid unnecessary exploration and rereads

### Evidence
- `tools/view.sh`
- `tools/learn.py`
- `learn/project-0.model.events.jsonl`

### Risk / rollback
- Risk: without a scripted read plan, learn may still spend too many tool turns on long docs until prompt strategy is tuned further.
- Rollback: only reintroduce a debugging-only scripted plan locally; do not make it part of the committed onboarding design.

### Current stop reason
- `infra_quota_or_auth`
- Reason: the latest live learn smoke was cut off by Codex usage limits after the prompt rollback, so final runtime verification must wait for quota reset.

## Incremental decision (accept strategy-based learn reads after real low-profile pass)
### Why
- After quota recovery, the real `learn -low` run completed end-to-end under app-server true plan mode and still preserved the full onboarding shape:
  - all required files read
  - all `PROJECT_GUIDE` questions answered
  - anchor remained on track
- This proves the rollback from a scripted read plan to a strategy-constrained read policy did not reduce onboarding quality.

### Decision
- Keep the current learn design:
  - strategy-based reading
  - no hardcoded line-by-line read script
  - full `Q1..Q17` oral sync
  - evidence-driven file coverage
- Treat `learn -low -> ready` as the first verified daily-use closure.
- Defer further work to ergonomics tuning for `-medium`, not to another architectural rewrite of onboarding.

### Evidence
- `learn/project-0.json`
- `learn/project-0.model.json`
- `learn/project-0.model.events.jsonl`
- `reports/run-2026-03-05-ops-vnext-release/ready.json`

### Risk / rollback
- Risk: `-medium` may still feel heavy in day-to-day use even though `-low` now closes successfully.
- Rollback: none recommended on the reading-strategy direction; only tune prompt/output ergonomics if daily latency remains too high.

### Current stop reason
- `needs_human_decision`

## Incremental decision (filter commentary at transport layer, do not weaken onboarding)
### Why
- The remaining learn bottleneck was no longer file coverage or prompt structure; it was app-server plan-mode process output.
- Local protocol/schema evidence shows app-server distinguishes `agentMessage.phase=commentary` from `agentMessage.phase=final_answer`.
- Treating both as one stream pollutes raw output and wastes parser work, but shrinking `PROJECT_GUIDE` or dropping questions would directly hurt onboarding quality.

### Decision
- Keep the full onboarding content unchanged:
  - `Q1..Q17`
  - must-read evidence coverage
  - mainline anchor and oral readout
- Fix transport instead:
  - ignore `commentary`
  - only accumulate `final_answer`
  - optimize final JSON extraction so parsing does not rescan the whole buffer on every delta
  - stop waiting when app-server exits without a usable packet

### Evidence
- `tools/codex_transport.py`
- `learn/project-0.model.events.jsonl`
- `learn/project-0.model.stderr.log`

### Risk / rollback
- Risk: app-server can still fail before final answer under quota pressure, so `-medium` remains dependent on account limits.
- Rollback: not recommended; the previous behavior mixed protocol phases and made final parsing slower and noisier.

### Current stop reason
- `infra_quota_or_auth`
- Reason: after the transport fixes, `learn -low -> ready` passes again, but `learn -medium` is currently blocked by `usage_limit_exceeded`, so the next action depends on quota recovery rather than more prompt compression.
- Reason: the learn/ready closure is now verified; next step is a product decision whether to continue tuning onboarding ergonomics or move forward into `orient`.
