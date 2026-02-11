# Summary

RUN_ID: `run-2026-02-11-handoff-rule-fix-placeholder`

## What changed
- Added task file: `TASKS/TASK-fix-placeholder-run-id.md`.
- Updated `TASKS/TASK-handoff-rule.md`:
  - `RUN_ID` set to `run-2026-02-11-handoff-rule`
  - Acceptance/Steps report paths aligned to `reports/run-2026-02-11-handoff-rule/*`
- Migrated evidence from placeholder-named reports directory to `reports/run-2026-02-11-handoff-rule/` by content copy:
  - `meta.json`
  - `summary.md`
  - `decision.md`
- Removed old placeholder-named files under legacy reports path.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-11-handoff-rule-fix-placeholder`
  - wrote `reports/run-2026-02-11-handoff-rule-fix-placeholder/meta.json`
  - ensured `reports/run-2026-02-11-handoff-rule-fix-placeholder/summary.md`
  - ensured `reports/run-2026-02-11-handoff-rule-fix-placeholder/decision.md`
- `tools/view.sh reports/run-2026-02-11-handoff-rule/{meta.json,summary.md,decision.md}`
  - all new target files readable
- `tools/view.sh reports/<legacy-placeholder-run-id>/{meta.json,summary.md,decision.md}`
  - all return `ERROR: path is not a regular file.`
- `make verify`
  - `20 passed in 0.87s`

## Notes
- Why: PR #67 used a placeholder RUN_ID token, which polluted handoff/audit naming and required deterministic normalization to the real RUN_ID.
