# TASK: make CI manual and ship tolerant of no checks

RUN_ID: run-2026-02-09-ci-manual
OWNER: Codex
PRIORITY: P1

## Goal
Disable automatic GitHub Actions triggers and make ship tolerant when no checks
appear shortly after PR creation.

## Non-goals
Do not remove CI workflow file or alter CI job content beyond triggers.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-ci-manual/summary.md` and
  `reports/run-2026-02-09-ci-manual/decision.md`
- [ ] Workflow only triggers on `workflow_dispatch`
- [ ] `tools/ship.sh` no longer hangs when no checks appear, and continues
      auto-merge attempt with clear guidance if blocked by required checks

## Inputs
- `TASKS/_TEMPLATE.md`
- `.github/workflows/ci.yml`
- `tools/ship.sh`

## Steps (Optional)
- Generate evidence skeleton.
- Update CI triggers to manual dispatch only.
- Add no-checks fast-path in `tools/ship.sh`.
- Verify and document changes.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: CI no longer runs automatically; merges rely on manual dispatch or
  other checks.
- Rollback plan: restore previous `on:` triggers and revert ship changes.
