# TASK: housekeeping-clean-transient-reports

RUN_ID: run-2026-02-27-housekeeping-clean-transient-reports
OWNER: codex
PRIORITY: P1

## Goal
Restore a clean working tree after ship by removing transient report artifacts and adding minimal ignore guardrails for recurring transient files.

## Scope (Required)
- `.gitignore`
- `TASKS/STATE.md`
- `TASKS/TASK-housekeeping-clean-transient-reports.md`
- `reports/run-2026-02-27-housekeeping-clean-transient-reports/`

## Non-goals
- No business logic changes.
- No workflow redesign.
- No edits to shipped task evidence except removing untracked transient leftovers.

## Acceptance
- [x] Transient untracked artifacts from previous run are cleaned.
- [x] `.gitignore` includes minimal patterns for recurring transient files only.
- [x] `make verify` passes.
- [x] Evidence updated under `reports/{RUN_ID}/`.

## Inputs
- Post-ship state has recurring transient untracked files under `reports/` causing friction.

## Risks / Rollback
- Risk: over-broad ignore pattern may hide useful evidence unintentionally.
- Rollback: revert this RUN diff and remove added ignore entries.
