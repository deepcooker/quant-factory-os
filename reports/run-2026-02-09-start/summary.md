# Summary

RUN_ID: `run-2026-02-09-start`

## What changed
- Added `tools/start.sh` for venv activation, optional proxy setup, `tools/enter.sh`, and codex launch.
- Documented quick start commands in `README.md`.
- Added pytest coverage for missing venv behavior.

## Commands / Outputs
- `make verify`

## Notes
- `tools/start.sh` expects `/root/policy/venv` by default or `START_VENV_PATH`.
