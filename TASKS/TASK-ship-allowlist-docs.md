# TASK: ship allowlist includes docs for untracked files

RUN_ID: run-2026-02-11-ship-allowlist-docs
OWNER: codex
PRIORITY: P1

## Goal
Include `docs/*` in `tools/ship.sh` untracked allowlist so new docs files are staged and shipped by default.

## Non-goals
Do not change shipping flow, PR generation behavior, or non-allowlist logic.

## Acceptance
- [ ] `tools/ship.sh` untracked allowlist includes `docs/*`
- [ ] Add/update pytest regression test that asserts allowlist contains `docs/*`
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-ship-allowlist-docs/summary.md` and `reports/run-2026-02-11-ship-allowlist-docs/decision.md`

## Inputs
- `TASKS/_TEMPLATE.md`
- `tools/ship.sh` (`stage_changes()` untracked allowlist)
- `tests/*` minimal regression coverage for allowlist text

## Steps (Optional)
1. Create task and evidence skeleton.
2. Update `tools/ship.sh` allowlist to include `docs/*`.
3. Add minimal pytest to assert allowlist case includes `docs/*`.
4. Run `make verify`.
5. Update evidence with why/what/verify.
6. Ship with `SHIP_ALLOW_SELF=1 RUN_ID=run-2026-02-11-ship-allowlist-docs tools/task.sh TASKS/TASK-ship-allowlist-docs.md`.

## Reading policy
Use `tools/view.sh` by default. If larger ranges are needed, provide explicit line ranges and reason.

## Risks / Rollback
- Risks: allowlist assertion too brittle to formatting changes.
- Rollback plan: revert this run's changes in `tools/ship.sh` and related test/evidence files.
