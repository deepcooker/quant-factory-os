# TASK: add a9 probe mode to run_a9

RUN_ID: run-2026-02-09-a9-probe
OWNER: Codex
PRIORITY: P1

## Goal
Extend `tools/run_a9.py` with a probe mode that runs a9 help entrypoints and
records results in evidence logs.

## Non-goals
Do not change default dry-run behavior or execute real backtests.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-a9-probe/summary.md` and
  `reports/run-2026-02-09-a9-probe/decision.md`
- [ ] `tools/run_a9.py` supports `--mode probe` with help execution and logging
- [ ] Tests cover probe success and failure

## Inputs
- `TASKS/_TEMPLATE.md`
- `tools/run_a9.py`
- `tests/`

## Steps (Optional)
- Generate evidence skeleton.
- Add probe mode with logging updates.
- Add tests and verify.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: probe command may fail if a9 entrypoint changes.
- Rollback plan: revert probe mode and related tests.
