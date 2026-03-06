# Summary

RUN_ID: `run-2026-03-06-automation-1-0-definition`

## What changed
- Added `docs/AUTOMATION_1_0.md` as the foundation-side definition of Automation 1.0.
- Fixed the 1.0 boundary to:
  - business project repo as the daily single-entry surface
  - foundation repo as the backstage capability/governance layer
  - 1.0 acceptance ending at delivery, not post-launch operate/iterate
- Kept current terminology aligned with `AGENTS / WORKFLOW / ENTITIES`:
  - `project`
  - `run`
  - `task`
  - `execution_contract`
  - `slice_state`
  - evidence
- Added the new doc to the AGENTS single-source map and linked it from WORKFLOW as a target-shape document, not the current state machine.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-03-06-automation-1-0-definition`
- `make verify` -> `28 passed in 1.67s`

## Notes
- This run intentionally does not claim that the current repo already has a business-project single entry.
- The document is a foundation-side success definition for when the base is mature enough to retreat to the background.
