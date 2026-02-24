# Decision

RUN_ID: `run-2026-02-24-run-id-pytest`

## Why
- Markdown rendering was swallowing raw `<RUN_ID>` placeholders in queue/template
  docs, producing ambiguous text like empty path segments. Also, pytest cache
  artifacts needed explicit ignore rules to keep the workspace clean.

## What
- Updated `.gitignore` to include `.pytest_cache/` and `.venv/` explicitly.
- Normalized placeholders from `<RUN_ID>` to `{RUN_ID}` in:
  `TASKS/QUEUE.md`, `TASKS/_TEMPLATE.md`, `docs/WORKFLOW.md`.
- Added `tests/test_runid_placeholder_render.py` for regression coverage.

## Verify
- `make verify` -> `40 passed in 1.50s`

## Risks / Rollback
- Risk: downstream docs/scripts expecting literal `<RUN_ID>` text may need sync.
- Rollback: revert this commit and reapply placeholder changes with alternate
  escaping strategy (`&lt;RUN_ID&gt;`) if required.
