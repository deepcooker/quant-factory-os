# Decision

RUN_ID: `run-2026-03-07-ship-retry-success-state-cleanliness`

## Why
- Real ship validation showed the previous cleanup was incomplete: the generic retry helper still rewrote `ship_state.json` on every successful step.
- Once a local commit exists, those helper-level success writes dirty the tracked evidence file again and can block PR automation or post-ship branch sync.

## Options considered
- Continue removing individual explicit `write_ship_state` success calls one by one.
- Add a helper-level gate that disables success-state writes after `git commit`, while preserving all failure and recovery writes.
- Move runtime success-state tracking into a different non-tracked file.

## Risks / Rollback
- This reduces success-step detail inside `ship_state.json` after commit, but keeps the important failure-state recovery breadcrumbs.
- Rollback is straightforward: re-enable helper success writes if a future design introduces a safe non-tracked success-state channel.

## Stop Reason
- task_done
