# Summary

RUN_ID: `run-2026-02-27-p0-clean-garbage-reports-and-add-archive-structure`

## What changed
- Removed two tracked garbage report directories with invalid `:` suffix naming:
  - `reports/run-2026-02-27-codex-ci-autofix-and-onboarding-constitution:`
  - `reports/run-2026-02-27-session-conversation-fallback-log:`
- Removed two probe-only untracked report directories:
  - `reports/run-probe-ok`
  - `reports/run-probe-missing-controller`
- Added archive scaffolding:
  - `TASKS/archive/README.md`
  - `TASKS/archive/2026-02/`
  - `reports/archive/README.md`
  - `reports/archive/2026-02/`

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-p0-clean-garbage-reports-and-add-archive-structure`
- `git rm -r -- "reports/run-2026-02-27-codex-ci-autofix-and-onboarding-constitution:" "reports/run-2026-02-27-session-conversation-fallback-log:"`
- `rm -rf reports/run-probe-ok reports/run-probe-missing-controller`
- `make verify` -> `73 passed`

## Notes
- This run intentionally limits scope to cleanup and archive structure only.
