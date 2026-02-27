# Decision

RUN_ID: `run-2026-02-27-project-guide-sync-first-handoff`

## Why
- Current pain is alignment drift across sessions/accounts, not command availability.
- The highest leverage first step is to lock sync/handoff policy as source-of-truth docs before changing automation.
- User explicitly requested preserving wealth project content while refreshing top-level sync logic.

## Options considered
- Option A: change scripts first (`qf ready/handoff/do`) then update docs.
  - Rejected for now: would risk implementing against unstable rules.
- Option B: update PROJECT_GUIDE sync policy first, keep wealth roadmap intact, then iterate tooling.
  - Selected: clearer baseline for future code changes.

## Risks / Rollback
- Risks:
  - Guide may temporarily diverge from current CLI ergonomics.
- Mitigation:
  - Keep changes narrow to "sync-first handoff" behavior and explicit read order.
  - Preserve appendix A content unchanged.
- Rollback:
  - Revert this RUN diff for `chatlogs/PROJECT_GUIDE.md` and evidence files.
