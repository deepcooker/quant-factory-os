# TASK: make start.sh executable

RUN_ID: run-2026-02-09-start-exec
OWNER: Codex
PRIORITY: P1

## Goal
Ensure `tools/start.sh` is executable so it can be run directly as `./tools/start.sh`.

## Non-goals
Do not modify script contents or adjust permissions on any other files.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-start-exec/summary.md` and
  `reports/run-2026-02-09-start-exec/decision.md`
- [ ] `tools/start.sh` has executable bit set

## Inputs
- `TASKS/_TEMPLATE.md`
- `tools/start.sh`

## Steps (Optional)
- Generate evidence skeleton.
- Set executable bit on `tools/start.sh`.
- Verify and document changes.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: none beyond permission toggle.
- Rollback plan: `chmod -x tools/start.sh`.
