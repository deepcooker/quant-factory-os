# TASK: qf-stash-clean-command

RUN_ID: run-2026-02-27-qf-stash-clean-command
OWNER: codex
PRIORITY: P1

## Goal
Add a small deterministic command to clean recurring qf/ship temporary stashes, with safe preview-first behavior.

## Scope (Required)
- `tools/qf`
- `tests/test_qf_stash_clean.py`
- `docs/WORKFLOW.md`
- `TASKS/STATE.md`
- `TASKS/TASK-qf-stash-clean-command.md`
- `reports/run-2026-02-27-qf-stash-clean-command/`

## Non-goals
- No business strategy or model behavior change.
- No change to ship/merge policy.
- No automatic deletion without explicit apply action.

## Acceptance
- [x] `tools/qf stash-clean` provides preview mode by default.
- [x] `tools/qf stash-clean apply` only drops recognized qf/ship transient stash entries.
- [x] `make verify` passes.
- [x] Evidence updated under `reports/{RUN_ID}/`.

## Inputs
- User confirmed to solidify stash cleanup policy into a command.

## Risks / Rollback
- Risk: pattern mismatch could drop unexpected stash entries.
- Rollback: revert this RUN diff; command removal restores previous behavior.
