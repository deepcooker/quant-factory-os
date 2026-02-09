# TASK: 测试

RUN_ID: run-2026-02-09-test
OWNER: codex
PRIORITY: P1

## Goal
Allow non-interactive GitHub auth in tools/ship.sh using GH_TOKEN for automation.

## Non-goals
Do not change tools/ship.sh behavior when GH_TOKEN is not set.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-test/summary.md` and `reports/run-2026-02-09-test/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- tools/ship.sh
- AGENTS.md

## Steps (Optional)
- Run `make evidence RUN_ID=run-2026-02-09-test`
- Update tools/ship.sh to use GH_TOKEN for non-interactive auth when present
- Run `make verify`
- Update evidence reports
- Ship with SHIP_ALLOW_SELF=1

## Risks / Rollback
- Risks: auth flow regressions if GH_TOKEN handling is incorrect
- Rollback plan: revert tools/ship.sh
