# Summary

RUN_ID: `run-2026-03-04-docs-cleanup-project-guide`

## What changed
- Rewrote `docs/PROJECT_GUIDE.md` into a strict Q&A-only format.
- Removed legacy narrative/noise sections and kept only structured question -> answer -> evidence items.
- Added `docs/WEALTH_SYSTEM_NEW_PROJECT_GUIDE.md` as the standalone guide for wealth-system project bootstrap.
- Added one queue item and bootstrapped this task/run via `tools/task.sh --next`.

## Commands / Outputs
- `tools/task.sh --next`
  - Created `TASKS/TASK-docs-cleanup-project-guide.md`
  - Created evidence skeleton under `reports/run-2026-03-04-docs-cleanup-project-guide/`
- `make verify`
  - Result: `123 passed in 55.08s`

## Notes
- Scope respected: `docs/PROJECT_GUIDE.md`, `docs/WEALTH_SYSTEM_NEW_PROJECT_GUIDE.md`, `reports/{RUN_ID}/`.
- This run focused on documentation structure and onboarding clarity; no runtime/business logic changed.
