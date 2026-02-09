# TASK: ignore local artifacts

RUN_ID: run-2026-02-09-ignore-local
OWNER: codex
PRIORITY: P1

## Goal
Ignore local run artifacts so enter/ship flows are not blocked by untracked noise.

## Non-goals
- Changing any runtime behavior outside .gitignore.
- Deleting existing local files.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-ignore-local/summary.md` and `reports/run-2026-02-09-ignore-local/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- .gitignore

## Steps (Optional)
- Add ignore rules for MISTAKES and PR body excerpts.

## Risks / Rollback
- Risks: missing needed artifacts in git.
- Rollback plan: remove ignore entries.
