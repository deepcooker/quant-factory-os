# Decision

RUN_ID: `run-2026-02-09-start`

## Why
- Provide a single entry point that ensures environment activation, optional proxy
  configuration, and repository checks before starting codex.

## Options considered
- Keep manual multi-step setup (rejected: higher friction and inconsistent setup).
- Skip proxy/venv handling (rejected: increases operator errors).

## Risks / Rollback
- Risks: start fails if policy venv is missing or codex is unavailable.
- Rollback: remove `tools/start.sh` and related README/test changes.
