# TASK: codify boundary contract (base vs a9) v0

RUN_ID: run-2026-02-11-boundary-a9-v0
OWNER: codex
PRIORITY: P1

## Goal
Codify a base vs a9 boundary v0 using only repo evidence, without touching
main project integration.

## Non-goals
No deep a9 integration or changes outside the allowed doc and STATE updates.

## Acceptance
- [ ] New `docs/BOUNDARY_A9.md` exists with only sections A/B/C/D.
- [ ] Every rule in A/B/C includes a source filename; unsupported items go to D.
- [ ] `TASKS/STATE.md` includes an entry point for the boundary doc.
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-boundary-a9-v0/summary.md` and `reports/run-2026-02-11-boundary-a9-v0/decision.md`

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
3) Add boundary entry to `TASKS/STATE.md`.
4) Run `make verify`.
5) Update evidence and ship.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Ambiguous boundary rules if sources are missing.
- Rollback plan: Revert the doc and STATE entry.
