# Summary

RUN_ID: `run-2026-03-04-docs-governance-cleanup`

## What changed
- Added hard documentation-boundary rules to `AGENTS.md` (owner-only definition + anti-duplication policy).
- Updated `README.md` to be index-only with explicit boundary quick rules.
- Updated `docs/WORKFLOW.md` to remove stale constitution pointer and reference canonical owners (`AGENTS.md` + `docs/CODEX_CLI_OPERATION.md`).
- Updated `SYNC/README.md` and rewrote `SYNC/LINKS.md` to focus on current-run entrypoints and remove historical run noise.
- Updated `SYNC/CURRENT_STATE.md`, `SYNC/SESSION_LATEST.md`, and `SYNC/DECISIONS_LATEST.md` to the active docs-governance run context.
- Updated `TASKS/STATE.md` pointer to current task/run and removed deprecated boundary reference.
- Cleaned docs set:
  - removed stale `docs/BOUNDARY_A9.md`
  - removed stale `docs/CODEX_ONBOARDING_CONSTITUTION.md`
  - converted `docs/INTEGRATION_A9.md` into compatibility pointer (kept for test/tool compatibility only)
- Cleaned `docs/ENTITIES.md` by removing obsolete `tools/run_a9` reference.

## Commands / Outputs
- `tools/task.sh --next`
  - Created `TASKS/TASK-docs-governance-cleanup.md`
  - Created evidence scaffold under `reports/run-2026-03-04-docs-governance-cleanup/`
- `make verify` (run #1)
  - Failed: `tests/test_docs_exist.py::test_docs_exist_and_have_key_titles`
  - Cause: expected `docs/INTEGRATION_A9.md` to exist
- `make verify` (run #2)
  - Failed: expected substring `Integration: a9quant` in `docs/INTEGRATION_A9.md`
- `make verify` (run #3)
  - Passed: `123 passed in 55.53s`

## Notes
- Boundary determination method now enforced in `AGENTS.md`:
  - Keep: owner docs with active responsibilities
  - Delete: stale/placeholder docs with no owner path
  - Refine: documents that mix responsibilities or duplicate owner definitions
- This run intentionally keeps `docs/INTEGRATION_A9.md` as a compatibility pointer to satisfy existing regression tests while removing it from owner-doc responsibility.
