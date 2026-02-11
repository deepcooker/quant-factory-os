# Summary

RUN_ID: `run-2026-02-11-bootstrap-queue`

## What changed
- Added `TASKS/TASK-bootstrap-queue.md` to define scope, acceptance, and RUN_ID.
- Added `TASKS/QUEUE.md` as the next-shot queue entrypoint with a minimal item
  schema and two TODO sample tasks.
- Updated `docs/WORKFLOW.md` with a new `Codex session startup checklist`
  section defining a 5-step bootstrap flow.
- Updated `TASKS/STATE.md` with explicit references to queue and startup
  checklist paths.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-11-bootstrap-queue`
  - wrote `reports/run-2026-02-11-bootstrap-queue/meta.json`
  - ensured `reports/run-2026-02-11-bootstrap-queue/summary.md`
  - ensured `reports/run-2026-02-11-bootstrap-queue/decision.md`
- `make verify`
  - `20 passed in 0.90s`

## Notes
- Scope intentionally limited to task/workflow/state/evidence files only.
