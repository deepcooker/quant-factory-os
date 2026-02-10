# TASK: add --find to view tool

RUN_ID: run-2026-02-10-view-find
OWNER: codex
PRIORITY: P1

## Goal
Add a `--find` option to `tools/view.sh` for locating patterns with optional
context, without changing existing range behavior.

## Non-goals
Change the default range output or add new dependencies.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-10-view-find/summary.md` and `reports/run-2026-02-10-view-find/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- tools/view.sh
- AGENTS.md reading policy

## Steps (Optional)
1. Extend `tools/view.sh` argument parsing for `--find` and `--context`.
2. Add tests for hit and miss cases.
3. Run `make verify` and update evidence.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Incorrect exit codes or unexpected output format.
- Rollback plan: Revert `tools/view.sh` changes and test file.
