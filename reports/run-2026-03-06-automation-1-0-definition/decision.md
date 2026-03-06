# Decision

RUN_ID: `run-2026-03-06-automation-1-0-definition`

## Why
- The user clarified that Automation 1.0 should not be defined as “continue explaining the base”.
- The correct target is:
  - one business-project entry
  - project learn as the daily sync focus
  - foundation repo hidden behind a stable pipeline
- The smallest safe implementation in this repo is to formalize that target in foundation documentation before attempting a fake `factory.py` in the base repo.

## Options considered
- Rewrite `docs/PROJECT_GUIDE.md` to turn the course directly into the 1.0 definition.
- Add a placeholder `tools/factory.py` in the current repo.
- Add a dedicated `docs/AUTOMATION_1_0.md` and keep the current repo explicitly positioned as the foundation repo.

## Risks / Rollback
- This run defines the target shape but does not yet create the separate business project repo.
- If the wording later proves too strong, rollback is simple: remove `docs/AUTOMATION_1_0.md` and the minimal references from `AGENTS.md` / `docs/WORKFLOW.md`.
