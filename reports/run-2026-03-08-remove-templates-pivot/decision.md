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
- Remove the separate `AUTOMATION_1_0` logic and wealth bootstrap guide, and keep only the four core owner docs as the active cognition surface.
- Treat `PROJECT_GUIDE` question design and structure as owner-fixed curriculum assets; only answers or minimal tuning may change.
- Clear old `reports/run-*` evidence as well, and keep only the current active run evidence.
- Remove `chatlogs/discussion` and `chatlogs/sync` as non-essential historical materials.
- Remove `CHARTER.md` and `CONTRIBUTING.md` as non-owner docs that no longer match the active process, and remove CI's dependency on `CHARTER.md`.
- Normalize the repo definition around one runtime split: CLI for development/debug takeover, app-server for programmatic runtime integration.

## Risks / Rollback
- Risk: deleting historical run evidence removes old in-repo audit trails and makes older references in task files point to non-existent paths.
- Rollback: restore deleted files from git history if the template route needs to be revisited.
