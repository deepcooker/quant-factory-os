# Decision

RUN_ID: `run-2026-02-10-stabilize-filelist`

## Why
- `project_all_files.txt` drift was causing accidental PR noise.

## What
- Ignored the file by default, documented the exception workflow, and added a
  ship guard that requires `SHIP_ALLOW_FILELIST=1` when it is staged.

## Options considered
- Only ignore in `.gitignore` (rejected: extra guard helps when file is
  explicitly added).

## Risks / Rollback
- Risk: Legit updates will be blocked unless the env override is set.
- Rollback plan: Remove ignore and ship guard, revert docs.

## Verify
- `make verify`

## Tests
- No new tests. Behavior is shell-guarded and covered by `make verify` smoke.
