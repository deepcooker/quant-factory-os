# Decision

RUN_ID: `run-2026-03-06-ship-post-sync-cleanliness`

## Why
- The real `tools/task.sh -> tools/ship.sh` smoke proved branch continuity was fixed, but also exposed a second issue: `write_ship_state("merged")` dirtied the working tree and immediately caused the post-ship sync guard to abort.

## Options considered
- Stop at documenting the resumed command.
- Ignore all dirty files during post-ship sync.
- Ignore only the current run's `ship_state.json` while preserving the dirty guard for every other file.

Chosen:
- Ignore only the current run's `ship_state.json` in the post-ship sync dirty check.

## Risks / Rollback
- Risk: if future ship metadata files also self-dirty the tree, they will need explicit treatment instead of piggybacking on this narrow exception.
- Rollback: revert to the previous guard and require a different write timing strategy if broader side effects appear.

## Stop Reason
- task_done
