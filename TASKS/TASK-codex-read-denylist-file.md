# TASK: ship allowlist includes .codex_read_denylist (make denylist effective)

RUN_ID: run-2026-02-12-codex-read-denylist-file
OWNER: codex
PRIORITY: P1

## Goal
Ensure `.codex_read_denylist` is a tracked, shippable repository file so denylist
behavior is stable across sessions and CI.

## Scope (Required)
- `tools/ship.sh`
- `.codex_read_denylist`
- `TASKS/TASK-codex-read-denylist-file.md`
- `reports/run-2026-02-12-codex-read-denylist-file/`

## Non-goals
- No a9 integration or runtime trading behavior changes.
- No broad allowlist relaxation for all dotfiles.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-12-codex-read-denylist-file/summary.md` and `reports/run-2026-02-12-codex-read-denylist-file/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- `tools/ship.sh`
- `tools/view.sh`
- `tests/test_codex_read_denylist.py`
- `TASKS/_TEMPLATE.md`

## Steps (Optional)
1. Add `.codex_read_denylist` to untracked allowlist logic in `tools/ship.sh`.
2. Add tracked root file `.codex_read_denylist` with baseline deny pattern and note.
3. Run `make verify` and update evidence files.

## Reading policy
Use `tools/view.sh` by default. If larger ranges are required, specify exact line
ranges and reason.

## Risks / Rollback
- Risks: accidental edits to denylist content could block intended reads.
- Rollback plan: revert `tools/ship.sh` and `.codex_read_denylist` changes.
