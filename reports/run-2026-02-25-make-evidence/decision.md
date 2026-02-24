# Decision

RUN_ID: `run-2026-02-25-make-evidence`

## Why
- Picking tasks still required manual evidence and could leave queue items stuck
  in `[>]` if evidence failed, creating friction and manual repair work.

## What
- In `tools/task.sh`:
  - defaulted bootstrap evidence to enabled (`TASK_BOOTSTRAP_EVIDENCE=1`).
  - added `TASK_BOOTSTRAP_EVIDENCE_CMD` for testable/custom evidence execution.
  - added queue backup/restore logic so evidence failure rolls queue marker back.
  - added standardized next-step checklist output with `TASK_FILE`, `RUN_ID`,
    and `EVIDENCE_PATH`.
- Updated `docs/WORKFLOW.md` to reflect auto evidence on `--next/--pick`.
- Added `tests/test_task_next_auto_evidence.py` covering success and failure rollback.
- Updated existing bootstrap tests to inject `TASK_BOOTSTRAP_EVIDENCE_CMD=true`.

## Verify
- `make verify` -> `47 passed in 1.95s`

## Risks / Rollback
- Risk: custom `TASK_BOOTSTRAP_EVIDENCE_CMD` may contain unexpected shell behavior.
- Rollback: revert this run commit; behavior is localized to task bootstrap/docs/tests.

## Evidence paths
- `reports/run-2026-02-25-make-evidence/meta.json`
- `reports/run-2026-02-25-make-evidence/summary.md`
- `reports/run-2026-02-25-make-evidence/decision.md`
