# Summary

RUN_ID: `run-2026-02-11-state-queue-startup-links`

## What changed
- Added task definition: `TASKS/TASK-state-queue-startup-links.md`.
- Updated `TASKS/STATE.md` under `Current conventions` to make startup entrypoints explicit via:
  - `Queue: TASKS/QUEUE.md`
  - `Startup checklist: docs/WORKFLOW.md#Codex-session-startup-checklist`
- Generated evidence skeleton under `reports/run-2026-02-11-state-queue-startup-links/`.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-11-state-queue-startup-links`
  - OK: wrote `meta.json`, ensured `summary.md` and `decision.md`.
- `make verify`
  - `20 passed in 0.88s`

## Notes
- Scope kept minimal: only task file, `TASKS/STATE.md`, and run evidence files.
