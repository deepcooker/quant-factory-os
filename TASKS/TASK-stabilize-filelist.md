# TASK: prevent project_all_files drift

RUN_ID: run-2026-02-10-stabilize-filelist
OWNER: codex
PRIORITY: P1

## Goal
Prevent accidental PR noise from `project_all_files.txt` drift by ignoring it
by default and documenting the exception workflow.

## Non-goals
Change how file lists are generated or add new automation around them.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-10-stabilize-filelist/summary.md` and `reports/run-2026-02-10-stabilize-filelist/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- .gitignore
- tools/ship.sh
- docs/WORKFLOW.md

## Steps (Optional)
1. Ignore `project_all_files.txt` in `.gitignore`.
2. Document the rule in `docs/WORKFLOW.md`.
3. Add a minimal ship guard for staged `project_all_files.txt` (opt-out via env).

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Legit filelist updates require explicit override.
- Rollback plan: Remove ignore/guard and revert doc rule.
