# Summary

RUN_ID: `run-2026-02-27-governance-convergence-sync-priority`

## What changed
- Governance docs convergence (single-source model):
  - Added canonical strategy guide: `docs/PROJECT_GUIDE.md`.
  - Kept `chatlogs/PROJECT_GUIDE.md` as backward-compatible pointer only.
  - Converted `README.md` to index-only file with owner map.
  - Updated `AGENTS.md`, `docs/WORKFLOW.md`, `docs/ENTITIES.md`,
    `docs/CODEX_ONBOARDING_CONSTITUTION.md`, and `SYNC/*` to owner/reference pattern.
- Unified run pointer definition:
  - Added `CURRENT_RUN_ID`, `CURRENT_TASK_FILE`, `CURRENT_STATUS`,
    `CURRENT_UPDATED_AT` in `TASKS/STATE.md`.
- `tools/qf` run-id behavior upgrade:
  - Added `TASKS/STATE.md` parsing/writing helpers.
  - Commands `ready/snapshot/handoff/do/resume` now default to
    `CURRENT_RUN_ID` (with mismatch fail-fast, optional one-shot override).
  - `do queue-next` now updates `CURRENT_*` to picked task run/task file.
  - `resume` defaults to `CURRENT_RUN_ID` and marks current status done on completion.
  - `onboard/init` guide path updated to `docs/PROJECT_GUIDE.md`.
- Tests:
  - Added `tests/test_qf_current_run.py`.
  - Updated `tests/test_qf_handoff.py` to new default-ready suggestion wording.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-governance-convergence-sync-priority`
- `make verify` -> `69 passed in 6.35s`

## Notes
- Scope intentionally excludes wealth/quant strategic content edits.
