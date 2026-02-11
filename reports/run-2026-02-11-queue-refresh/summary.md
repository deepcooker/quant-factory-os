# Summary

RUN_ID: `run-2026-02-11-queue-refresh`

## What changed
- Added task definition file: `TASKS/TASK-queue-refresh.md`.
- Refreshed `TASKS/QUEUE.md`:
- Marked delivered items as done (`[x]`): `ship allowlist includes docs`,
  `ship expected-files gate`, `.codex_read_denylist` baseline.
- Added next-shot items at queue top (P0/P1):
  startup entrypoint print with RUN_ID, `docs/ENTITIES.md` minimal dictionary
  sync, and minimal workflow-gate regression tests.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-11-queue-refresh`
  - wrote/ensured `reports/run-2026-02-11-queue-refresh/{meta.json,summary.md,decision.md}`
- `make verify`
  - `25 passed in 1.10s`

## Notes
- Scope kept minimal to task file + queue file; no code/tool changes.
