# TASK: auto-mark queue done on successful ship

RUN_ID: run-2026-02-22-auto-mark-queue-done-on-successful-ship
OWNER: <you>
PRIORITY: P1

## Goal
after a successful ship/PR open (and/or merge), automatically mark the picked `[>]` queue item as `[x]` and append `Done: PR #<n>, RUN_ID=<id>`.

## Scope (Required)
- `tools/task.sh`
- `tools/ship.sh`
- `TASKS/QUEUE.md`
- `tests/`


## Non-goals
What we explicitly do NOT do.

## Acceptance
- When shipping a task created by `--next`, the corresponding queue item is updated from `[>]` to `[x]` with Done metadata.
- No effect if ship fails or no matching picked item exists.
- `make verify` passes and evidence recorded under `reports/<RUN_ID>/`.

## Inputs
- Links / files / references
- If data is needed, specify allowed sample constraints (max rows, time window)

## Steps (Optional)
Suggested approach, if you have one.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
- Rollback plan:
