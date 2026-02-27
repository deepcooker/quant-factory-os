# Decision

RUN_ID: `run-2026-02-28-sync-exam-assets-followup`

## Why
- Previous run merged core grader/docs changes but left `SYNC/EXAM_*` files untracked due ship allowlist behavior.
- These files are required for cross-surface exam workflow to be complete.

## Options considered
- Leave as-is and rely on ad-hoc prompts (rejected): breaks deterministic onboarding workflow.
- Follow-up patch run to ship missing files (chosen): minimal and auditable.

## Risks / Rollback
- Risk: very low (documentation-only files).
- Rollback: revert this follow-up RUN commit.
