# Decision

RUN_ID: `run-2026-02-27-sync-filename-rollback-keep-chinese-content`

## Why
- User clarified intended change scope: only comments/notes should be Chinese.
- Renaming filenames introduced unnecessary path churn and friction.
- Stable canonical paths are better for scripts, references, and handoff continuity.

## Options considered
- Keep Chinese filenames:
  - Pros: visual distinction from root README.
  - Cons: path churn, quoting/encoding friction, higher maintenance.
- Revert only some filenames:
  - Pros: partial compromise.
  - Cons: mixed naming style and extra confusion.
- Revert all SYNC filenames to original English and keep Chinese content (chosen):
  - Pros: path stability + readable Chinese notes.
  - Cons: no filename-level visual cue.

## Risks / Rollback
- Risk: stale references to Chinese SYNC paths in historical notes/evidence.
- Risk: `tools/ship.sh` scope gate may false-positive on quoted non-ASCII source paths during rename commits.
- Mitigation: canonical docs and active SYNC references fully switched back.
- Mitigation: used audited override `SHIP_ALLOW_OUT_OF_SCOPE=1` once for this run.
- Rollback plan: revert this RUN diff if needed.
