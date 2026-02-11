# Decision

RUN_ID: `run-2026-02-11-state-queue-startup-links`

## Why
- Session bootstrap should have explicit, in-repo entry references so new Codex runs do not depend on chat memory.
- `STATE` is the startup baseline; surfacing queue and checklist entrypoints there reduces ambiguity.

## Options considered
- Add entrypoint references in `Current conventions` (chosen): minimal diff and immediately visible in startup read flow.
- Add references in `Next steps`: possible, but less canonical for stable conventions.
- No-op because references already present: rejected for this task because explicitness reinforcement was requested.

## Risks / Rollback
- Risk: duplicated or redundant wording in `TASKS/STATE.md`.
- Rollback: revert this run's `TASKS/STATE.md` hunk and keep prior text.
