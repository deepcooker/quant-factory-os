# Decision

RUN_ID: `run-2026-02-27-p0-clean-garbage-reports-and-add-archive-structure`

## Why
- Root `reports/` had obvious garbage/noise artifacts (invalid suffix names and probe logs) that hurt readability for continuity.
- User requested P0 cleanup first, then later consolidation.

## Options considered
- Keep all historical directories untouched (rejected): noise remains and blocks clarity.
- Full immediate archive migration for all runs/tasks (rejected for P0): higher risk and larger blast radius.
- Minimal P0 cleanup + archive scaffolding (chosen): safe, reversible, and aligns with user request.

## Risks / Rollback
- Risk: deleted directories might contain niche forensic details.
- Mitigation: only removed high-confidence garbage/probe dirs and kept normal run evidence untouched.
- Rollback: restore deleted tracked files from git history if needed.
