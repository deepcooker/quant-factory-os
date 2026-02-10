# TASK: clean README as entrypoint

RUN_ID: run-2026-02-10-readme-clean
OWNER: codex
PRIORITY: P1

## Goal
Rewrite README into a concise entrypoint page with quickstart, workflow summary,
concepts, docs index, and troubleshooting.

## Non-goals
Retain historical narrative or long timelines in the README.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-10-readme-clean/summary.md` and `reports/run-2026-02-10-readme-clean/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- README.md
- docs/WORKFLOW.md
- tests/test_status_snapshot_rule.py

## Steps (Optional)
1. Draft new README sections per requirements.
2. Replace README content and ensure line count target.
3. Run `make verify` and update evidence.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Missing required content or command strings causes tests to fail.
- Rollback plan: Revert README changes.
