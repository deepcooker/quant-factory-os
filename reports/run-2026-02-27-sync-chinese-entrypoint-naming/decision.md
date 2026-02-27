# Decision

RUN_ID: `run-2026-02-27-sync-chinese-entrypoint-naming`

## Why
- Existing `SYNC/README.md` and root `README.md` are visually ambiguous in onboarding handoff discussions.
- Chinese-first entry labels reduce startup friction for current operator workflow (CLI + web model collaboration).
- Numbered names (`00..05`) preserve deterministic read order and reduce interpretation variance.

## Options considered
- Keep old English names:
  - Pros: less churn.
  - Cons: continues ambiguity with root `README.md`; weaker onboarding ergonomics.
- Rename only `SYNC/README.md`:
  - Pros: minimal rename.
  - Cons: mixed style and partial inconsistency; still leaves non-obvious reading order files.
- Full Chinese numbered rename for all entry files (chosen):
  - Pros: single coherent naming style + explicit sequence.
  - Cons: requires global reference updates once.

## Risks / Rollback
- Risk: stale links from old file names in docs or scripts.
- Risk: ship scope gate may mis-detect non-ASCII staged paths as out-of-scope.
- Mitigation:
  - updated canonical governance docs and checked no old SYNC names remain there.
  - verification suite passed (`make verify`).
  - ship used audited override once (`SHIP_ALLOW_OUT_OF_SCOPE=1`) to bypass false positive.
- Rollback:
  - revert this RUN diff (or restore old file names and references in one commit).
