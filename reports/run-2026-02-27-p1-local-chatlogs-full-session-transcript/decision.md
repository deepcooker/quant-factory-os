# Decision

RUN_ID: `run-2026-02-27-p1-local-chatlogs-full-session-transcript`

## Why
- User expectation is explicit: `SYNC/SESSION_LATEST.md` is not enough; complete
  session fallback is needed to reduce context-loss friction.
- Current policy forbids storing full transcripts in tracked repo files, so the
  correct location is local gitignored `chatlogs/`.

## Options considered
- Keep summary-only mode:
  - Pros: minimal change.
  - Cons: cannot recover full interaction context.
- Store full transcripts in repo:
  - Pros: easy sharing.
  - Cons: violates existing memory policy and increases repo noise.
- Chosen:
  - auto-log full startup session locally in `chatlogs/` via `tools/start.sh`,
    with explicit opt-out and fallback behavior.

## Risks / Rollback
- Risks:
  - `script` command may not exist in some environments.
  - local transcript files may grow over time.
- Mitigation:
  - runtime fallback to plain `codex` with warning if `script` missing.
  - transcript location remains outside git tracking (`chatlogs/`).
- Rollback plan:
  - revert this RUN diff.
