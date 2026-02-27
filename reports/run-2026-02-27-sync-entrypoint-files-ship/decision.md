# Decision

RUN_ID: `run-2026-02-27-sync-entrypoint-files-ship`

## Why
- `SYNC/*` was designed and validated but remained untracked in the previous ship.
- To ensure the sync-entrypoint strategy is actually usable, these files must be
  committed on `main`, not left in local stash/worktree.

## Options considered
- Option A: skip follow-up and keep local-only `SYNC/*`.
  - Rejected: defeats cross-session/cross-account sync purpose.
- Option B: create a dedicated recovery task and ship only `SYNC/*` + evidence.
  - Selected: clear audit trail and minimal-risk patch.

## Risks / Rollback
- Risks:
  - `SYNC/*` may become stale if session discipline is weak.
- Mitigation:
  - `SYNC/READ_ORDER.md` and `SYNC/SESSION_LATEST.md` define update points.
- Rollback:
  - Revert this RUN diff if needed.
