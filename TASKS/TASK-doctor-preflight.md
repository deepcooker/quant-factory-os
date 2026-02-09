# TASK: doctor preflight checks

RUN_ID: run-2026-02-09-doctor-preflight
OWNER: codex
PRIORITY: P1

## Goal
Upgrade `tools/doctor.sh` into a codex preflight check with clearer failures
and remediation guidance, without changing success behavior.

## Non-goals
- Changing existing passing paths or adding new required checks.
- Modifying ship behavior.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-doctor-preflight/summary.md` and `reports/run-2026-02-09-doctor-preflight/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- tools/doctor.sh
- Makefile
- AGENTS.md

## Steps (Optional)
- Read Makefile PY to use same python as `make verify`.
- Add clearer failure messages (pytest/gh/view.sh exec).
- Keep passing path unchanged.

## Risks / Rollback
- Risks: overly strict checks block usage.
- Rollback plan: revert doctor.sh to previous behavior.
