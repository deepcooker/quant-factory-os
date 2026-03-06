# Decision

RUN_ID: `run-2026-03-06-ship-post-commit-state-cleanliness`

## Why
- The previous fix removed success-path writes at `merged` and `synced`, but a real rerun showed the same continuity failure still happening.
- The deeper root cause is broader: once a local commit exists, any further success-path rewrite of tracked `ship_state.json` re-dirties the worktree and can block PR merge helpers or post-ship sync checkout.

## Options considered
- Keep trying to stash/restore `ship_state.json` around later ship phases.
- Stop all success-path `ship_state.json` rewrites after local commit while preserving failure/recovery writes.
- Move runtime success state into a separate sidecar file.

## Risks / Rollback
- This reduces success-path granularity inside `ship_state.json`, but keeps the pipeline stable and leaves failure-state recovery intact.
- Rollback is straightforward: restore the removed success-path `write_ship_state` calls if a later design adopts a non-tracked runtime state channel.

## Stop Reason
- task_done
