# Summary

RUN_ID: `run-2026-02-21-task-bootstrap-next`

## What changed
- Added `next/bootstrap` mode in `tools/task.sh` with backward compatibility:
  - supports `tools/task.sh --next` and `tools/task.sh next`
  - reads first unchecked item (`- [ ]`) from `TASKS/QUEUE.md`
  - extracts `Title`, `Goal`, `Scope`, and `Acceptance` block
  - generates `RUN_ID` as `run-YYYY-MM-DD-<slug>` (no placeholder)
  - creates `TASKS/TASK-<slug>.md`
  - prints generated `TASK_FILE` and `RUN_ID` to stdout
  - optionally runs `make evidence RUN_ID=<RUN_ID>` when
    `TASK_BOOTSTRAP_EVIDENCE=1`
- Added regression test: `tests/test_task_bootstrap_next.py`.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-21-task-bootstrap-next`
  - wrote/ensured `meta.json`, `summary.md`, `decision.md`
- `make verify`
  - PASS: `30 passed in 1.34s`

## Notes
- Bootstrap mode intentionally does not call ship; it only generates executable
  task input (plus optional evidence).
