# TASK: single run guard in ship

RUN_ID: run-2026-02-09-single-run-guard
OWNER: codex
PRIORITY: P1

## Goal
Add a guard in tools/ship.sh to prevent shipping when multiple RUN_IDs or task files
are present in the pending changes.

## Non-goals
- Changing existing ship behavior beyond the guard.
- Adding new CLI flags or changing PR body format.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-single-run-guard/summary.md` and `reports/run-2026-02-09-single-run-guard/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- tools/ship.sh
- AGENTS.md

## Steps (Optional)
- Implement single-run/task guard before commit/PR creation.
- Add pytest guardrail covering multiple RUN_ID / task file detection.

## Risks / Rollback
- Risks: false positives if file list detection misses edge cases.
- Rollback plan: revert guard block and test.
