# TASK: startup prints entrypoints + RUN_ID (if set)

RUN_ID: run-2026-02-11-startup-entrypoints
OWNER: codex
PRIORITY: P1

## Goal
Reduce new-session confusion by printing session entry points and current RUN_ID
at startup, after `tools/enter.sh` checks pass.

## Scope (Required)
- `tools/enter.sh`
- `tests/`
- `tools/start.sh` (only if needed)

## Non-goals
- No deep integration with `a9` or main project runtime behavior.
- No changes outside startup/task/evidence/test scope.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-startup-entrypoints/summary.md` and `reports/run-2026-02-11-startup-entrypoints/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `TASKS/_TEMPLATE.md`
- `tools/enter.sh`
- `tools/start.sh`
- User request in this session

## Steps (Optional)
1. Add startup entrypoint block output in `tools/enter.sh`.
2. Print `RUN_ID` value (or `(not set)` when absent).
3. Add minimal subprocess-based pytest for `tools/enter.sh` output checks.
4. Run `make verify` and update evidence docs.

## Reading policy
Use `tools/view.sh` by default. If larger ranges are required, specify exact line
ranges and reason.

## Risks / Rollback
- Risks: startup output assertion brittle if wording changes.
- Rollback plan: revert `tools/enter.sh` message block and the new test file.
