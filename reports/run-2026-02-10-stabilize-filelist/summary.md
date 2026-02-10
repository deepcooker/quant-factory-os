# Summary

RUN_ID: `run-2026-02-10-stabilize-filelist`

## What changed
- Ignored `project_all_files.txt` in `.gitignore` and documented the rule in
  `docs/WORKFLOW.md`.
- Added a ship guard that blocks staged `project_all_files.txt` unless explicitly
  allowed.

## Commands / Outputs
- `make verify`
  - `18 passed in 0.78s`

## Notes
- Evidence: `.gitignore`, `docs/WORKFLOW.md`, `tools/ship.sh`
