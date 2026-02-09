# TASK: add start.sh for venv+proxy+enter+codex

RUN_ID: run-2026-02-09-start
OWNER: Codex
PRIORITY: P1

## Goal
Provide a single entry script that activates the policy venv, applies proxy
settings when present, runs `tools/enter.sh`, and then launches codex.

## Non-goals
Do not modify `tools/enter.sh` or change existing workflows beyond adding the
new entry point.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-start/summary.md` and
  `reports/run-2026-02-09-start/decision.md`
- [ ] `tools/start.sh` activates venv, applies proxy when present, runs
      `tools/enter.sh`, and execs codex
- [ ] Dry-run mode supports test coverage for missing venv

## Inputs
- `TASKS/_TEMPLATE.md`
- `tools/enter.sh`
- `README.md`
- `tests/`

## Steps (Optional)
- Generate evidence skeleton.
- Add `tools/start.sh` with dry-run support.
- Update README quick start.
- Add pytest coverage and verify.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: `start.sh` may fail if policy venv is missing or misconfigured.
- Rollback plan: remove `tools/start.sh` and README/test changes.
