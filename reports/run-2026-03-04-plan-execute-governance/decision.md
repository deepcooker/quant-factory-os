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

## Addendum (AGENTS lightweight contract + sync navigation)
- Why:
  - Keep `AGENTS.md` as hard-contract layer while reducing ambiguity for read-only discussion and gate predicates.
  - Ensure new sessions can immediately find owner docs via explicit navigation pointers.
  - Align evidence field expectations across `AGENTS.md`, `docs/WORKFLOW.md`, and `docs/ENTITIES.md`.
- Decision:
  - Keep current architecture (`AGENTS` for hard rules, owner docs for details).
  - Add only minimum contract reinforcements:
    - read-only discussion exception before task binding
    - `meta.json` minimum gate fields
    - `tools/evidence.py` default scaffolding updated to include those fields
    - concise gate predicates and owner-doc freshness triggers
    - `PROJECT_GUIDE` navigation pointers
  - Keep strict review gate green: missing direction artifacts were fixed via `tools/qf choose`, then `tools/qf review STRICT=1 AUTO_FIX=1` passed.
- Risks:
  - `AGENTS.md` remains long; further slimming is still desirable.
  - Read-only exception can be abused if mutation boundary is not respected.
- Stop reason:
  - `task_done`
