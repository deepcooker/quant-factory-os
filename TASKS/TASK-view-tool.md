# TASK: add view.sh for read-only file viewing

RUN_ID: run-2026-02-09-view-tool
OWNER: codex
PRIORITY: P1

## Goal
Introduce a controlled read-only viewer (`tools/view.sh`) so agents can read file ranges
without direct `sed/cat/rg` usage, reducing permission friction.

## Non-goals
- Expanding allowed commands beyond `tools/view.sh`.
- Allowing unrestricted file access or writes.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-view-tool/summary.md` and `reports/run-2026-02-09-view-tool/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- AGENTS.md
- TASKS/_TEMPLATE.md
- tools/ship.sh

## Steps (Optional)
- Add `tools/view.sh` and enforce path/line limits.
- Update AGENTS Allowed Commands and reading policy.
- Update TASK template reading policy.
- Add pytest coverage for view.sh.

## Risks / Rollback
- Risks: view constraints too tight for future usage.
- Rollback plan: remove view.sh and related policy updates.

## Reading policy
After `tools/view.sh` is introduced, all long file reading must use `tools/view.sh`
with explicit ranges. Do not use `sed/cat/rg` for long reads.
