# TASK: untrack project_all_files snapshot

RUN_ID: run-2026-02-10-filelist-untrack
OWNER: codex
PRIORITY: P1

## Goal
Stop tracking `project_all_files.txt` while keeping it as a local context
snapshot with an explicit override path for PRs.

## Non-goals
Change how the snapshot is generated or used by other tools.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-10-filelist-untrack/summary.md` and `reports/run-2026-02-10-filelist-untrack/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- .gitignore
- docs/WORKFLOW.md
- tools/ship.sh

## Steps (Optional)
1. Untrack `project_all_files.txt` while keeping it locally.
2. Document the context snapshot rules in `docs/WORKFLOW.md`.
3. Run `make verify` and update evidence.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Needed filelist updates require explicit override steps.
- Rollback plan: Re-add the file to git and remove the doc section.
