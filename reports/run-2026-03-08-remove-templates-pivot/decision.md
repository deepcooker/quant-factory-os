# Decision

RUN_ID: `run-2026-03-08-remove-templates-pivot`

## Why
- The template-based direction is now considered wrong for the current foundation path.

## Options considered
- Keep `templates/` and merely de-emphasize it.
- Delete `templates/` and align docs/tests/evidence with the pivot.

## Chosen
- Delete `templates/` entirely.
- Delete imported external-project materials created for that route.
- Remove the directly dependent tests.
- Remove the rest of the repository tests as well, per current reset direction.
- Remove the project-repo / adoption docs instead of keeping them as dormant references.
- Keep only negative mentions in owner docs where needed to make the new direction explicit.
- Preserve prior run references as historical evidence rather than rewriting history.

## Risks / Rollback
- Risk: historical reports from the previous run will still mention template outputs that no longer exist in the worktree.
- Rollback: restore deleted files from git history if the template route needs to be revisited.
