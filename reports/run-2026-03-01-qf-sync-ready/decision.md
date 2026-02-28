# Decision

RUN_ID: `run-2026-03-01-qf-sync-ready`

## Why
- The sync phase must be automatic, auditable, and explicit in output, not dependent on human reminders.
- Readiness (`tools/qf ready`) should enforce actual sync completion while keeping one-command ergonomics.
- Process memory needs timely updates in repo evidence, especially for session continuity (`conversation.md`).

## Options considered
- Keep manual sync reminders (rejected): repeats the same human coordination gap.
- Hard-fail `ready` when sync report is missing without automation (rejected): strict but higher friction and poorer UX.
- Default auto-sync + hard validation gate (chosen):
  - `ready` auto-runs `sync` when needed.
  - `ready` still fails if sync report remains invalid.
  - preserves strictness and improves usability.

## Risks / Rollback
- Risk: sync required-file list may drift when onboarding docs change.
  - Mitigation: owner docs (`AGENTS`/`WORKFLOW`/`SYNC`) updated in same run; `sync_passed` exposes missing files early.
- Risk: auto-stash in `qf plan` can hide unstaged work unexpectedly.
  - Mitigation: command prints stash name and restore instructions; behavior mirrors existing `qf init` ergonomics.
- Rollback:
  - Revert this RUN changes in `tools/qf`, tests, and owner docs to restore previous manual sync behavior.

## Stop reason
- `task_done`
