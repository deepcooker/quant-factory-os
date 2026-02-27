# TASK: p0-clean-garbage-reports-and-add-archive-structure

RUN_ID: run-2026-02-27-p0-clean-garbage-reports-and-add-archive-structure
OWNER: codex
PRIORITY: P0

## Goal
Remove high-confidence garbage report directories and add stable archive directory scaffolding without touching core workflow rules.

## Scope (Required)
- `TASKS/STATE.md`
- `TASKS/TASK-p0-clean-garbage-reports-and-add-archive-structure.md`
- `TASKS/archive/`
- `reports/`
- `reports/archive/`
- `reports/run-2026-02-27-p0-clean-garbage-reports-and-add-archive-structure/`

## Non-goals
- No business/strategy content changes.
- No command behavior changes.
- No test logic refactor in this run.

## Acceptance
- [x] Remove garbage report dirs with invalid naming or probe-only logs.
- [x] Add archive directory scaffolding under `TASKS/archive/` and `reports/archive/`.
- [x] `make verify` passes.
- [x] Evidence updated under `reports/{RUN_ID}/`.

## Inputs
- User approved P0 cleanup: delete high-confidence garbage dirs and build archive structure.

## Risks / Rollback
- Risk: deleting a mistakenly useful historical dir.
- Rollback: restore from git history for removed tracked files.
