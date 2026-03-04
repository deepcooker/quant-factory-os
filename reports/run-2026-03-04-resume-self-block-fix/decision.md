# Decision

RUN_ID: `run-2026-03-04-resume-self-block-fix`

## Why
- `tools/qf resume` could fail during merged-PR closeout because it appends run traces
  and then attempts `git checkout main` with a dirty workspace.
- This created an operational deadlock requiring manual stash or `QF_LOG_DISABLE=1`.
- The fix needed to preserve execution logging while keeping resume one-shot reliable.

## Options considered
- Option A: disable resume execution logging around checkout.
  - Rejected: violates evidence-first traceability requirements.
- Option B: keep current behavior and rely on operator manual recovery.
  - Rejected: poor automation reliability; known self-block remains.
- Option C: auto-stash dirty workspace right before checkout-main in resume.
  - Chosen: minimal diff, preserves logs, and removes self-blocking failure path.

## Risks / Rollback
- Risks:
  - auto-stash may add temporary stash noise in long sessions.
  - operators must know these stashes are cleanup artifacts.
- Mitigation:
  - `tools/qf stash-clean` now recognizes `qf-resume-cleanup-run-*`.
  - docs updated in `AGENTS.md` and `docs/WORKFLOW.md`.
- Rollback:
  - revert this run’s `tools/qf` and test/doc updates.
- Stop reason:
  - `task_done`
