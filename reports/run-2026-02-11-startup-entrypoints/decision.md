# Decision

RUN_ID: `run-2026-02-11-startup-entrypoints`

## Why
- New sessions can lose orientation; printing fixed entry links and current `RUN_ID`
  at startup reduces startup ambiguity with minimal behavior change.

## Options considered
- Add output in `tools/enter.sh` only.
- Also modify `tools/start.sh`.
- Decision: modify `tools/enter.sh` only, because `tools/start.sh` already delegates
  to `tools/enter.sh`, so this is the smallest diff.

## Risks / Rollback
- Risk: tests rely on output text and may need updates if wording changes intentionally.
- Rollback: revert `tools/enter.sh` output block and remove `tests/test_enter_entrypoints.py`.
