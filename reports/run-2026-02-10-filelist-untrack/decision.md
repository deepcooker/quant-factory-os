# Decision

RUN_ID: `run-2026-02-10-filelist-untrack`

## Why
- `project_all_files.txt` drift should not pollute PRs; it is a local context
  snapshot for external models.

## What
- Untracked the file, kept it ignored, and documented the explicit override
  steps in `docs/WORKFLOW.md`.

## Options considered
- Keep it tracked and rely only on ship guard (rejected: still risks drift).

## Risks / Rollback
- Risk: Contributors may forget the override steps when they need to update it.
- Rollback plan: Re-add the file to git and revert the doc section.

## Verify
- `make verify`
