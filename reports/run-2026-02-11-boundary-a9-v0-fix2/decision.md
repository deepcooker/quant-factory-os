# Decision

RUN_ID: `run-2026-02-11-boundary-a9-v0-fix2`

## Why
- `TASKS/STATE.md` contains Boundary v0 entry (`docs/BOUNDARY_A9.md`) but the target file was missing in repository state.
- PR #62 merged with the STATE entry present, leaving a dangling documentation pointer.
- PR #63 was intended to fix it but the merged commit did not actually include `docs/BOUNDARY_A9.md`.
- Therefore fix2 must explicitly add `docs/BOUNDARY_A9.md` and gate delivery on verification.

## Options considered
- Option 1: Also edit `TASKS/STATE.md` to remove or change the pointer.
  - Rejected: violates minimal-diff goal and does not solve intended Boundary v0 doc completion.
- Option 2: Add only `docs/BOUNDARY_A9.md` plus required task/evidence updates.
  - Selected: directly resolves dangling entry with smallest scoped change.

## Risks / Rollback
- Risk: `docs/BOUNDARY_A9.md` could be omitted from staged files during ship, recreating prior failure mode.
- Mitigation: re-opened file with `tools/view.sh` before verify; acceptance requires PR changed files include `docs/BOUNDARY_A9.md`.
- Verify: `make verify` (passed).
- Rollback: revert this task branch/PR if acceptance fails, then re-run with the same RUN_ID gates.
