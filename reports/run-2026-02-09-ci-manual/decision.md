# Decision

RUN_ID: `run-2026-02-09-ci-manual`

## Why
- CI scheduling was unstable; manual dispatch avoids surprise triggers while keeping the file for future runners.
- Ship should not hang when no checks are reported shortly after PR creation.

## Options considered
- Keep automatic CI triggers and rely on required checks (rejected: unstable scheduling).
- Wait indefinitely for checks (rejected: hangs when no checks are configured).

## Risks / Rollback
- Risks: PRs may merge without checks unless branch protection enforces them.
- Rollback: restore original workflow triggers and revert ship changes.
