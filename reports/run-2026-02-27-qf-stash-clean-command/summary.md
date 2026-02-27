# Summary

RUN_ID: `run-2026-02-27-qf-stash-clean-command`

## What changed
- Added a new command: `tools/qf stash-clean [preview|apply] [KEEP=<n>]`.
- Behavior:
  - default `preview`: list qf/ship transient stash candidates and planned keep/drop.
  - `apply`: drop only recognized transient stash entries and keep the newest `KEEP` entries.
- Recognized transient stash patterns:
  - `ship-wip-*`
  - `qf-init-wip-*`
  - `resume-cleanup-run-*`
  - `tmp-ship-cleanup-*`
- Added regression tests for preview/apply behavior and no-candidate path.
- Updated workflow docs with optional stash-clean step.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-qf-stash-clean-command`
- `make verify`
  - Result: `73 passed`

## Notes
- Command is intentionally preview-first to avoid accidental stash deletion.
