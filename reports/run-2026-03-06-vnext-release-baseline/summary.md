# Summary

RUN_ID: `run-2026-03-06-vnext-release-baseline`

## What changed
- Promoted `vnext release baseline` into an active task/run:
  - `TASKS/TASK-vnext-release-baseline.md`
  - `TASKS/STATE.md`
  - `TASKS/QUEUE.md`
- Formalized the current delivery boundary in owner docs:
  - `smoke` is the pre-ship release-prep/readiness layer
  - `smoke` does not perform remote git / PR / merge
  - `ship` remains the formal git / PR / merge / sync layer
- Added a dedicated `smoke` section to `docs/WORKFLOW.md` and aligned the `AGENTS.md` workflow skeleton.
- Added a minimal `tools/smoke.sh` readiness command:
  - reads current `TASKS/STATE.md` / explicit `RUN_ID`
  - validates task contract, run evidence, and `drift_review`
  - writes `reports/<RUN_ID>/smoke.json`
- Added `tests/task_smoke.py` coverage for:
  - pass path with complete readiness materials
  - fail path when review artifacts are missing
- Completed the minimum discussion artifacts for this run:
  - `orient_choice.json`
  - `direction_contract.json`
  - `execution_contract.json`
- `bash tools/legacy.sh review ... STRICT=1 AUTO_FIX=1` now passes for this run.
- `bash tools/smoke.sh ...` passes for this run.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-03-06-vnext-release-baseline`
- `make verify` -> `27 passed in 1.62s`
- `python3 tools/orient.py`
- `python3 tools/choose.py RUN_ID=run-2026-03-06-vnext-release-baseline OPTION=execution-path-ergonomics`
- `python3 tools/council.py RUN_ID=run-2026-03-06-vnext-release-baseline`
- `python3 tools/arbiter.py RUN_ID=run-2026-03-06-vnext-release-baseline`
- `bash tools/legacy.sh review RUN_ID=run-2026-03-06-vnext-release-baseline STRICT=1 AUTO_FIX=1` -> `REVIEW_STATUS: pass`
- `bash tools/smoke.sh RUN_ID=run-2026-03-06-vnext-release-baseline TASK_FILE=TASKS/TASK-vnext-release-baseline.md` -> `SMOKE_STATUS: pass`

## Notes
- `docs/PROJECT_GUIDE.md` only received a minimal standard-answer sync in Q14 to reflect `smoke -> ship`; the question bank structure and learning intent were left intact.
- This run still does not have its own successful `ready.json`. Attempts to regenerate a fresh project-scoped learn packet for the new run re-entered the known app-server/model-packet completion issue, so `ready` remains a residual warning rather than a blocker for this slice.
