# TASK: ship-runid-normalization

RUN_ID: run-2026-02-27-ship-runid-normalization
OWNER: codex
PRIORITY: P1

## Goal
Fix `tools/ship.sh` RUN_ID parsing so trailing punctuation in commit message
does not leak into `reports/<RUN_ID>/...` paths.

## Scope (Required)
- `tools/ship.sh`
- `tests/`
- `TASKS/TASK-ship-runid-normalization.md`
- `reports/run-2026-02-27-ship-runid-normalization/`

## Non-goals
- Refactor unrelated ship logic.
- Change PR/merge strategy.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- PR #115 generated path anomaly: `reports/run-...:/ship_state.json`

## Steps (Optional)
1. Add RUN_ID normalization helper in `tools/ship.sh`.
2. Ensure message extraction excludes trailing punctuation.
3. Add regression test for parser path edge case.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: over-strict normalization might drop valid IDs.
- Rollback plan: revert this task diff.
