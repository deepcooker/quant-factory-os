# TASK: fix required docs and status rule

RUN_ID: run-2026-02-10-fix-docs-readme
OWNER: codex
PRIORITY: P1

## Goal
Restore green `make verify` by adding required docs and documenting the `/status` rule.

## Non-goals
Rewrite the README or expand docs beyond what tests require.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-10-fix-docs-readme/summary.md` and `reports/run-2026-02-10-fix-docs-readme/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- tests/test_docs_exist.py
- tests/test_status_snapshot_rule.py
- README.md

## Steps (Optional)
1. Create missing docs with required titles and keywords.
2. Add minimal `/status` mention in README.
3. Run `make verify` and update evidence.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Missing required strings causes tests to fail.
- Rollback plan: Remove added files/edits if needed.
