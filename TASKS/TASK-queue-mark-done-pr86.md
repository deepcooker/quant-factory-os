# TASK: queue mark done for bootstrap next scope normalize (PR #86)

RUN_ID: run-2026-02-22-queue-mark-done-pr86
OWNER: <you>
PRIORITY: P1

## Goal
Mark the completed queue item for bootstrap Scope normalization from `[>]` to `[x]`
and record its completion metadata (PR and RUN_ID).

## Scope (Required)
- `TASKS/QUEUE.md`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
Do not modify other queue items or task execution logic.

## Acceptance
- [ ] Target queue item is marked `[x]`.
- [ ] Target queue item includes:
  `Done: PR #86, RUN_ID=run-2026-02-22-bootstrap-next-normalize-scope-validate-scope-bullets`
- [ ] `make verify` passes.
- [ ] Evidence updated under `reports/run-2026-02-22-queue-mark-done-pr86/`.

## Inputs
- `TASKS/QUEUE.md`

## Steps (Optional)
1. Locate the `[>] bootstrap next: normalize Scope ...` queue item.
2. Mark it as `[x]` and add the Done line.
3. Run `make verify`.
4. Update summary and decision evidence.
5. Ship with task metadata.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: accidental edits to adjacent queue entries.
- Rollback plan: restore prior `TASKS/QUEUE.md` content and reapply only target lines.
