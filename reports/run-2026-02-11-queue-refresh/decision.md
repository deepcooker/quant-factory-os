# Decision

RUN_ID: `run-2026-02-11-queue-refresh`

## Why
- `TASKS/QUEUE.md` was stale versus delivered workflow hardening changes.
- New Codex sessions need a true "next shot" list that is immediately actionable.

## Options considered
- Keep queue unchanged and only add new items.
- Mark completed items done and prepend new P0/P1 candidates.
- Chosen: mark done + prepend next-shot items, so history stays visible and
  startup selection is accurate.

## Risks / Rollback
- Risk: incorrect completion marking if repository state is misread.
- Mitigation: checked `tools/ship.sh` and `.codex_read_denylist` before updating queue.
- Rollback: revert `TASKS/QUEUE.md` and `TASKS/TASK-queue-refresh.md`, then rerun `make verify`.
