# Summary

RUN_ID: `run-2026-03-08-remove-templates-pivot`

## What changed
- Bound the repository to a new active task/run for the templates pivot.
- Removed the `templates/` route from the repo because it is no longer the desired foundation direction.
- Removed `imports/` content that had been created for the same discarded project-repo exploration.
- Removed the three scaffold-only regression tests that depended on `templates/`.
- Removed the project-repo / adoption docs that belonged to the same discarded direction.
- Removed `docs/AUTOMATION_1_0.md` and `docs/WEALTH_SYSTEM_NEW_PROJECT_GUIDE.md`.
- Removed the remaining repository test files and test caches entirely.
- Tightened the active owner-doc set back to four core files only: `AGENTS.md`, `docs/PROJECT_GUIDE.md`, `docs/ENTITIES.md`, `docs/WORKFLOW.md`.
- Updated `PROJECT_GUIDE.md` answers to keep the focus on high-quality questions, standard answers, oral restatement, and anchor-based mainline recovery.
- Wrote the owner rule explicitly: `PROJECT_GUIDE` question set and structure are fixed assets, and may only change when project facts change or when a minimal quality-preserving adjustment is necessary.
- Removed all historical `reports/run-*` directories and kept only the current active run evidence.
- Removed `chatlogs/discussion` and `chatlogs/sync` content.
- Removed `CHARTER.md` and `CONTRIBUTING.md`, and dropped the obsolete CI check that required `CHARTER.md`.
- Tightened the four owner docs around the runtime split:
  - Codex CLI is the R&D/debug/takeover interface
  - Python orchestrator + Codex app-server is the long-term runtime path
- Updated task state and queue to bind this pivot to its own run.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-03-08-remove-templates-pivot` -> created run evidence files
- `find templates -type f | sort` -> identified 16 tracked template files
- `find imports -maxdepth 3 -print` -> identified the imported `a9quant-strategy` source set
- `grep -R -n "templates/" ...` -> identified direct references in docs, task files, and reports
- `find templates -depth -type d -empty -delete` -> removed the now-empty directory tree
- `rm -rf imports` -> removed imported external project materials
- `rm -rf tests .pytest_cache` -> removed remaining test files and caches
- `find reports -maxdepth 1 -mindepth 1 -type d ! -name 'run-2026-03-08-remove-templates-pivot' -exec rm -rf {} +` -> removed historical run evidence directories
- `rm -rf chatlogs/discussion chatlogs/sync` -> removed discussion drafts and sync materials
- removed `CHARTER.md` / `CONTRIBUTING.md`, and updated `.github/workflows/ci.yml`
- `make verify` -> `VERIFY: no tests/task_*.py files present; skipping pytest`

## Notes
- This run replaces the prior assumption that reusable template directories are part of the Automation 1.0 output.
- This run also removes the separate `AUTOMATION_1_0` logic and the wealth bootstrap guide so the repo keeps only the four core owner docs.
- The repo now keeps only the current active run evidence under `reports/`; older run evidence is intentionally cleared.
