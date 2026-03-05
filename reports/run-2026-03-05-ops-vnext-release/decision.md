# Decision

RUN_ID: `run-2026-03-05-ops-vnext-release`

## Why
- Current phase is development/design; old task/report history created noise and slowed execution.

## Decision
- Remove historical `TASKS/TASK-*` and previous `reports/*` content.
- Keep only minimal active pointers and one active task.
- Ship as a clean baseline version.

## Risk
- Historical audit trail is no longer available in-repo after this reset.

## Stop reason
- task_done


## Incremental decision (no single ops entrypoint)
### Why
- Single dispatcher `tools/ops` is unnecessary overhead for current development-design stage.

### Decision
- Remove `tools/ops` from the default workflow and delete the dispatcher file.
- Use direct Python scripts for migrated commands and `tools/ops_legacy.sh` for legacy commands.

### Risk / rollback
- Risk: old notes that mention `tools/ops` may become stale.
- Rollback: restore `tools/ops` thin dispatcher from git history if needed.
