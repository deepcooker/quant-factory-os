# Summary

RUN_ID: `run-2026-02-11-handoff-rule`

## What changed
- Added task file: `TASKS/TASK-handoff-rule.md`.
- Updated `docs/WORKFLOW.md` in `Memory & Context` to explicitly mark three handoff hard rules as delivery gates:
  - uncommitted changes do not exist for other agents/cloud runs
  - handoff only via PR/commit hash with evidence under `reports/<RUN_ID>/`
  - local-only context must be captured in evidence or `TASKS/STATE.md`, not chat
- Updated `TASKS/STATE.md` to add an explicit handoff hard-rule entry referencing `docs/WORKFLOW.md` -> `Memory & Context`.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-11-handoff-rule`
  - wrote `reports/run-2026-02-11-handoff-rule/meta.json`
  - ensured `reports/run-2026-02-11-handoff-rule/summary.md`
  - ensured `reports/run-2026-02-11-handoff-rule/decision.md`
- `make verify`
  - `20 passed in 0.88s`

## Notes
- Why: make handoff constraints auditable and enforceable at documentation level so future deliveries do not treat local/uncommitted context as transferable state.
