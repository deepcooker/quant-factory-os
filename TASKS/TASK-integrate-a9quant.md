# TASK: integrate a9quant dry-run pipeline

RUN_ID: run-2026-02-09-integrate-a9
OWNER: codex
PRIORITY: P1

## Goal
Integrate a minimal dry-run path for /root/a9quant-strategy so we can validate
the pipeline without running a real backtest.

## Non-goals
- Running real trading/backtest logic.
- Modifying a9quant-strategy source.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-integrate-a9/summary.md` and `reports/run-2026-02-09-integrate-a9/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- /root/a9quant-strategy
- tools/run_a9.py

## Steps (Optional)
- Add run_a9 dry-run tool and log output to evidence.
- Add pytest coverage for missing/available a9 directory.

## Risks / Rollback
- Risks: dry-run check not representative of actual pipeline.
- Rollback plan: remove run_a9 tool and tests.
