# Decision

RUN_ID: `run-2026-03-06-task-ship-branch-safety`

## Why
- The previous task exposed a high-risk workflow bug: `tools/task.sh` delegated to `tools/ship.sh`, which always rebased onto `main` before creating the shipping branch.
- In the real session this destroyed active-run continuity and moved the repo onto an older baseline that did not contain the Python-first toolchain.

## Options considered
- Keep `ship.sh` main-based and only document that users should not invoke it from active run branches.
- Patch only `task.sh` and leave `ship.sh` hardcoded to `main`.
- Make `ship.sh` branch-aware by default and let `task.sh` pass the current branch explicitly.

Chosen:
- Make `ship.sh` branch-aware by default.
- Keep `main` sync only for the explicit `main` base case.
- Make `task.sh` pass `SHIP_BASE_BRANCH` explicitly so task handoff and ship use the same base.

## Risks / Rollback
- Risk: branch-aware shipping can change PR base for users who implicitly relied on `main`.
- Rollback: set `SHIP_BASE_BRANCH=main` / `SHIP_PR_BASE_BRANCH=main` explicitly, or revert the branch-aware default after a dedicated migration.
- Risk: source-level regression tests are weaker than full integration tests.
- Rollback: add repo-isolated fake-git/fake-gh integration tests in a follow-up task if this area changes again.

## Stop Reason
- task_done
