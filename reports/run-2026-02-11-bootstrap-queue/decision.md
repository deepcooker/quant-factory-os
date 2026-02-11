# Decision

RUN_ID: `run-2026-02-11-bootstrap-queue`

## Why
- New Codex sessions need a deterministic, repo-native entrypoint for "what to
  do next" without depending on chat memory.
- Queue + startup checklist makes task pickup repeatable and auditable through
  `STATE`, `QUEUE`, and `reports/<RUN_ID>/`.

## Options considered
- Keep only `TASKS/STATE.md` for next-step discovery.
  - Rejected: mixes status and queue intent; less explicit for new sessions.
- Add a dedicated `TASKS/QUEUE.md` + startup checklist in workflow.
  - Chosen: clear separation of current state vs pending tasks, with explicit
    execution flow.

## Risks / Rollback
- Risk: checklist drift if not maintained with process changes.
- Rollback: revert `TASKS/QUEUE.md`, `docs/WORKFLOW.md`, and `TASKS/STATE.md`
  in a single follow-up task.
