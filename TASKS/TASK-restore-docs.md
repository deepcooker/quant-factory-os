# TASK: restore required docs for workflow/tests

RUN_ID: run-2026-02-10-restore-docs
OWNER: Codex
PRIORITY: P1

## Goal
Restore required workflow and integration docs so guardrail tests pass and
status rules remain visible.

## Non-goals
Do not change test expectations or adjust unrelated docs.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-10-restore-docs/summary.md` and
  `reports/run-2026-02-10-restore-docs/decision.md`
- [ ] Required docs exist with expected titles and `/status` rule

## Inputs
- `TASKS/_TEMPLATE.md`
- `tests/test_docs_exist.py`
- `tests/test_status_snapshot_rule.py`

## Steps (Optional)
- Generate evidence skeleton.
- Confirm test expectations for docs.
- Restore required docs with minimal content.
- Verify and document.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: docs drift if not maintained.
- Rollback plan: revert docs changes.
