# Decision

RUN_ID: `run-2026-03-04-plan-execute-governance`

## Why
- Current docs had semantic ambiguity between Codex `/plan` and `tools/qf plan`.
- Workflow clarity required a hard distinction between:
  - planning protocol (`/plan`)
  - queue proposal helper (`tools/qf plan`)
  - execution gate chain (`ready -> discuss/execute -> do`)
- `/compact` was previously discussed as if mandatory per task; official semantics indicate it is context-size driven, so policy needed correction.

## Options considered
- Option A: keep current wording and rely on chat convention.
  - Rejected: high drift risk; new agents will continue conflating plan commands.
- Option B: docs-only governance fix (owner docs + run evidence), no script behavior changes.
  - Chosen: fastest low-risk alignment; preserves current automation while removing semantic confusion.
- Option C: immediate script refactor (`tools/qf plan` rename + runtime hard gate).
  - Deferred: valuable but should be a dedicated follow-up task to avoid coupling policy and behavior change in one run.

## Risks / Rollback
- Risks:
  - Existing habits may still use `tools/qf plan` as if it were `/plan`.
  - Without script-level hard enforcement, misuse is still possible.
- Rollback plan:
  - Revert this RUN’s doc diffs and restore previous `TASKS/STATE.md` pointer.
- Stop reason:
  - `task_done`
  - Follow-up remains optional: script-level rename/hard-gate for `tools/qf plan`.
