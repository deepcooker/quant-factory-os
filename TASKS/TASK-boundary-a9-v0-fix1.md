# TASK: add missing docs/BOUNDARY_A9.md (fix PR #62)

RUN_ID: run-2026-02-11-boundary-a9-v0-fix1
OWNER: codex
PRIORITY: P1

## Goal
Add the missing `docs/BOUNDARY_A9.md` file only, restoring the boundary doc
expected by `TASKS/STATE.md` without changing STATE.

## Non-goals
No changes to `TASKS/STATE.md` or any integration code.

## Acceptance
- [ ] New `docs/BOUNDARY_A9.md` exists with only sections A/B/C/D.
- [ ] Every rule in A/B/C includes a source filename; unsupported items go to D.
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-boundary-a9-v0-fix1/summary.md` and `reports/run-2026-02-11-boundary-a9-v0-fix1/decision.md`

## Inputs
- `docs/WORKFLOW.md`
- `TASKS/STATE.md`
- `AGENTS.md`
- `Makefile`
- `tools/*.sh`
- `tests/test_ship_guard.py`

## Steps (Optional)
1) Create evidence skeleton.
2) Add `docs/BOUNDARY_A9.md` with sourced rules.
3) Run `make verify`.
4) Update evidence and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Missing boundary doc continues to leave STATE link dangling.
- Rollback plan: Revert the boundary doc addition.
