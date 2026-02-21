# TASK: queue pick lock (in-progress marker)

RUN_ID: run-2026-02-21-queue-pick-lock-in-progress-marker
OWNER: <you>
PRIORITY: P1

## Goal
when `tools/task.sh --next` picks the top item, mark it as in-progress (`[>]`) and record RUN_ID+timestamp to avoid duplicate picks across sessions.

## Scope (Required)
- `tools/task.sh`
- `TASKS/QUEUE.md`
- `tests/`


## Non-goals
What we explicitly do NOT do.

## Acceptance
- Picking changes `[ ]` -> `[>]` and appends `Picked: <RUN_ID> <timestamp>`.
- Re-running `--next` does not pick the same `[>]` item again.
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
