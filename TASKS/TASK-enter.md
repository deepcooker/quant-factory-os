# TASK: add enter.sh preflight entry

RUN_ID: run-2026-02-09-enter
OWNER: codex
PRIORITY: P1

## Goal
Provide a one-shot `tools/enter.sh` to sync and preflight the repo before work,
reducing manual steps when starting a codex session.

## Non-goals
- Auto-stashing/committing or modifying the worktree beyond `git pull --rebase`.
- Replacing `tools/task.sh` or `tools/doctor.sh` workflows.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-enter/summary.md` and `reports/run-2026-02-09-enter/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- tools/enter.sh
- tools/doctor.sh
- AGENTS.md

## Steps (Optional)
- Add enter.sh with repo root checks, clean worktree guard, pull + doctor.
- Update Allowed Commands to include enter.sh.
- Add smoke pytest coverage for non-root and dirty states.

## Risks / Rollback
- Risks: overly strict checks block onboarding.
- Rollback plan: remove enter.sh and policy change.
