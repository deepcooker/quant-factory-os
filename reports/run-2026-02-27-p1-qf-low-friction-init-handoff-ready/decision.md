# Decision

RUN_ID: `run-2026-02-27-p1-qf-low-friction-init-handoff-ready`

## Why
- User experience issue: startup sync was adding manual effort and command
  ambiguity (`init/handoff/ready` boundaries were clear in rules but frictionful in execution).
- Objective for this phase: reduce startup burden while preserving hard gates and
  existing `plan/do` behavior.

## Options considered
- Keep strict manual flow (`init -> handoff -> ready` all explicit):
  - Pros: very explicit.
  - Cons: repeated manual steps reduce adoption and speed.
- Auto-bypass readiness:
  - Pros: fastest path.
  - Cons: breaks sync gate guarantees; rejected.
- Chosen:
  - Auto-assist only on non-gate steps (`init` auto-handoff), keep `ready` as mandatory gate,
    and auto-fill restatement from task contract by default.

## Risks / Rollback
- Risks:
  - auto defaults may hide poor task contracts if task files are weak.
  - startup output changes may affect operator habits.
- Mitigation:
  - keep manual override flags:
    - `QF_INIT_AUTO_HANDOFF=0`
    - `QF_READY_AUTO=0`
  - retain strict do-gate on `ready.json`.
- Rollback plan:
  - revert this RUN diff.
