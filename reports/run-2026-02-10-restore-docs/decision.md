# Decision

RUN_ID: `run-2026-02-10-restore-docs`

## Why
- Guardrail tests require the docs and the `/status` rule to be visible.

## Options considered
- Relax tests (rejected: would weaken enforcement).
- Restore docs with minimal accurate content (selected).

## Risks / Rollback
- Risks: docs may drift if not updated.
- Rollback: revert docs changes.
