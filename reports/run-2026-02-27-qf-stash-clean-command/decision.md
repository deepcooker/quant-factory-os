# Decision

RUN_ID: `run-2026-02-27-qf-stash-clean-command`

## Why
- Multiple `resume-cleanup-*` and `qf/ship` transient stashes were accumulating and adding manual cleanup friction.
- User asked to solidify stash cleanup into a single reusable command.

## Options considered
- Keep manual `git stash drop` only (rejected): repetitive and error-prone.
- Auto-clean on every init (rejected): too aggressive and can surprise users.
- Add explicit preview-first command with apply mode (chosen): safe and deterministic.

## Risks / Rollback
- Risk: matching patterns may include user stashes that reuse those prefixes.
- Mitigation: preview is default; deletion requires explicit `apply`.
- Rollback: revert this RUN diff to remove the command and tests.
