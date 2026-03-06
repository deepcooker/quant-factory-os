# Summary

RUN_ID: `run-2026-03-06-slice-next-p0-learn-core-delivery`

## What changed
- Added a `-daily` alias in `tools/learn.py` that maps the standard day-to-day gate path to `medium` without weakening strong plan mode or app-server transport.
- Restored `ready.json` legacy compatibility fields in `tools/ready.py` so Python-first `ready` output can still satisfy `bash tools/legacy.sh do queue-next`.
- Updated owner docs to make the daily learn entrypoint explicit in `AGENTS.md`, `docs/WORKFLOW.md`, and `docs/PROJECT_GUIDE.md`.
- Refreshed regression coverage in `tests/task_ops.py` for both `ready.json` compatibility aliases and the new `learn -daily` mapping.

## Commands / Outputs
- `python3 - <<'PY' ... parse_cli(['-daily']) ... PY` -> `daily / medium / medium`
- `python3 tools/ready.py RUN_ID=run-2026-03-05-ops-vnext-release` -> pass after re-running learn gate
- `bash tools/legacy.sh do queue-next` -> pass; created `TASKS/TASK-slice-next-p0-learn-core-delivery.md`
- `make verify` -> `21 passed in 1.80s`

## Notes
- This run fixed a real bridge break between the new Python-first gate output and the legacy execution entrypoint.
- The `-daily` alias is ergonomic only; default no-flag behavior remains `-xhigh`, and hard learn requirements are unchanged.
