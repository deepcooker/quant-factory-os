# TASK: ship echo PR body excerpts

RUN_ID: run-2026-02-09-ship-echo-prbody
OWNER: codex
PRIORITY: P1

## Goal
Automatically print and archive the task/evidence sections from PR body after ship,
so reviewers do not need to request PR body reads.

## Non-goals
- Changing existing PR body content or formatting.
- Altering behavior when no task info or RUN_ID is present.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-ship-echo-prbody/summary.md` and `reports/run-2026-02-09-ship-echo-prbody/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- tools/ship.sh
- AGENTS.md

## Steps (Optional)
- Extract task/evidence sections from PR_BODY, print and write to reports.
- Add pytest to validate extraction and file output.

## Risks / Rollback
- Risks: incorrect parsing if PR body format changes.
- Rollback plan: remove excerpt extraction and test.
