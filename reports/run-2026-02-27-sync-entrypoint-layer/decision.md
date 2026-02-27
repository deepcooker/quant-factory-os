# Decision

RUN_ID: `run-2026-02-27-sync-entrypoint-layer`

## Why
- Current collaboration pain is continuity loss across sessions/accounts/models.
- Existing docs are useful but scattered; they are not an explicit sync entrypoint.
- A dedicated sync layer enables fast alignment for both Codex CLI and web GPT.

## Options considered
- Option A: Keep only `docs/` + `chatlogs/` and improve discipline.
  - Rejected: high context scatter, too much reading overhead.
- Option B: Add top-level `SYNC/` as mandatory first read, with short curated files.
  - Selected: minimal change with high handoff reliability.

## Risks / Rollback
- Risks:
  - `SYNC/*` can become stale if not updated each session.
- Mitigation:
  - `SYNC/READ_ORDER.md` and `SESSION_LATEST.md` define explicit maintenance rules.
- Rollback:
  - Revert this RUN diff and continue using previous guide-only flow.
