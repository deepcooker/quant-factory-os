# Decision

RUN_ID: `run-2026-03-06-slice-next-p0-learn-core-delivery`

## Why
- The selected direction was `learn-daily-ergonomics`, and the first concrete friction found on the critical path was that Python-first `ready.py` produced a minimal `ready.json` no longer accepted by `legacy do`.
- A bounded ergonomics improvement was also needed so day-to-day learn usage has a canonical entrypoint instead of forcing users to remember which reasoning tier to pick.

## Options considered
- Patch only `legacy.sh` to accept the new minimal `ready.json`.
- Patch only `tools/ready.py` to re-emit the legacy compatibility fields.
- Add a dedicated daily learn alias and update owner docs so the recommended day-to-day path is explicit.

Chosen:
- Re-emit legacy compatibility aliases from `tools/ready.py` so the Python-first gate and legacy execution path interoperate during migration.
- Add `learn -daily` as an ergonomic alias to `-medium` and document it in owner files.

## Risks / Rollback
- Risk: compatibility aliases can linger longer than intended and hide stale readers.
- Rollback: remove the aliases only after all `legacy.sh` readers stop depending on `restatement_passed`, `learn_passed`, and `sync_passed`.
- Risk: `-daily` could be misread as a weaker gate.
- Rollback: keep the alias mapped to `medium` only, and keep `AGENTS.md` explicit that strong plan mode and app-server remain mandatory.

## Stop Reason
- task_done
