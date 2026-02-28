# Decision

RUN_ID: `run-2026-02-28-qf-exam-auto`

## Why
- User pain point: `tools/qf exam-auto` still required manual answer editing before grading, which breaks expected one-command automation.
- Objective: keep onboarding exam in the flow but remove avoidable operator steps.

## Options considered
- Keep scaffold-only default (rejected): still requires two human actions (edit + rerun).
- Remove exam step entirely (rejected): weakens sync/onboarding gate.
- Default to auto-fill + grade, with opt-out manual mode (chosen): matches automation expectation while preserving strict/manual path.

## Risks / Rollback
- Risk: generated answer may become stale relative to rubric updates.
- Mitigation: deterministic template includes required rubric keywords and tests cover both default and manual branches.
- Rollback: revert this RUN to restore previous scaffold-only `exam-auto` behavior.
