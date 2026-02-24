# Summary

RUN_ID: `run-2026-02-24-run-id-pytest`

## What changed
- Added explicit cache ignore rules to `.gitignore`: `.pytest_cache/`, `.venv/`
  (while keeping existing Python cache and venv patterns).
- Replaced raw `<RUN_ID>` placeholders with `{RUN_ID}` in:
  - `TASKS/QUEUE.md`
  - `TASKS/_TEMPLATE.md`
  - `docs/WORKFLOW.md`
- Added regression test `tests/test_runid_placeholder_render.py` to assert:
  - no raw `<RUN_ID>` remains in the three files above
  - required cache ignore rules exist in `.gitignore`

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-24-run-id-pytest`
- `make verify` -> `40 passed in 1.50s`

## Notes
- The queue item stayed in-place as picked (`[>]`) for this active run; done-mark
  is expected after successful ship/PR flow.
