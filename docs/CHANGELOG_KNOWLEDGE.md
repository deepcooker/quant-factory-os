# CHANGELOG_KNOWLEDGE

Purpose: track canonical knowledge updates so new sessions can trust repo memory over chat memory.

## Entry Template
- Date: `YYYY-MM-DD`
- RUN_ID: `run-...`
- Source:
  - Official docs links reviewed
  - Repo files reviewed
- Added:
  - New rules / workflows / constraints
- Changed:
  - Behavior changes and why
- Deprecated:
  - Old approach removed and replacement
- Verify:
  - Commands run (`make verify`, etc.)
- Risks:
  - Open risks and follow-up task link

## Log
- Date: `2026-02-27`
  - RUN_ID: `run-2026-02-27-codex-ci-autofix-and-onboarding-constitution`
  - Source:
    - Codex CLI docs and current repo workflow/tooling
  - Added:
    - `tools/qf ready` gate before `tools/qf do`
    - PR-only workflow policy with local verify baseline
  - Changed:
    - Primary entrypoint consolidated to `tools/qf`
  - Deprecated:
    - Direct use of legacy startup scripts as primary path
  - Verify:
    - `make verify` (`55 passed`)
  - Risks:
    - Large cleanup/override flows remain high-friction; improve with dedicated maintenance task mode.
