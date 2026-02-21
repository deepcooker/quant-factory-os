# Decision

RUN_ID: `run-2026-02-12-entities-min-dict`

## Why
- `docs/ENTITIES.md` was only a placeholder and could not act as a practical
  dictionary for workflow entities.
- Need a minimal, evidence-backed dictionary that reflects only existing repo
  entities/constraints and provides a clear entrypoint from `TASKS/STATE.md`.

## Options considered
- Expand ENTITIES into a full workflow handbook.
  - Rejected: too broad for requested scope and duplicates `docs/WORKFLOW.md`.
- Keep only short one-line labels.
  - Rejected: not enough operational constraints for task/PR/evidence usage.
- Implement minimal structured dictionary with TODO for unknowns.
  - Chosen: smallest diff with explicit certainty boundaries.

## Risks / Rollback
- Risks:
  - `tools/run_a9` reference is currently unresolved as a readable file path.
  - RUN_ID naming remains convention-based without a strict global regex.
- Rollback plan:
  - Revert this task commit to restore previous `docs/ENTITIES.md` and
    `TASKS/STATE.md`.
