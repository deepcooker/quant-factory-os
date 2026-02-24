# Summary

RUN_ID: `run-2026-02-25-make-evidence`

## What changed
- Updated `tools/task.sh` bootstrap flow so `--next` and `--pick queue-next` now:
  - auto-run evidence by default
  - support injectable evidence executor via `TASK_BOOTSTRAP_EVIDENCE_CMD`
  - rollback queue `[>]` marker when evidence execution fails
  - print a standard next-step checklist
- Updated `docs/WORKFLOW.md` startup checklist to state that pick now auto-creates evidence.
- Added regression tests:
  - `tests/test_task_next_auto_evidence.py`
  - updated existing `--next` tests to set `TASK_BOOTSTRAP_EVIDENCE_CMD=true`.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-25-make-evidence`
- `make verify` -> `47 passed in 1.95s`

## Notes
- Failure path now restores queue content, preventing stale `[>]` locks.
