# CODEX ONBOARDING CONSTITUTION

Purpose: enforce a repeatable, auditable startup gate for every new Codex session.

## Session Gate (run once per session)
1) Environment readiness
- Run `./tools/start.sh codex` from repo root.
- Confirm doctor/enter checks passed.
- Confirm working tree is clean before task execution.

2) Mandatory reading (in order)
- `SYNC/READ_ORDER.md`
- files listed in `SYNC/READ_ORDER.md` (strict order)
- `TASKS/STATE.md`
- `TASKS/QUEUE.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- Latest `reports/<RUN_ID>/decision.md`

3) Forced restatement (must pass before coding)
- Goal: one sentence for the active task.
- Scope: exact file paths allowed by task `## Scope`.
- Acceptance: verify/evidence/scope checks.
- Execution sequence: evidence -> implement -> verify -> reports -> ship.
- Stop condition: finish and wait for next instruction.

4) Skill readiness check
- Operator can explain Task/PR/RUN_ID/Evidence relations.
- Operator can run one safe dry cycle:
  - `tools/qf init`
  - `tools/qf ready`
  - `tools/qf plan 20`
  - `tools/qf do queue-next`
- Operator can explain failure protocol and `MISTAKES/<RUN_ID>.md`.

## Operational constitution
- No active TASK + RUN_ID: no code changes.
- No evidence: no memory.
- No verify green: no ship.
- No out-of-scope files in PR.
- No secret or production data in repo output.
- No workflow changes by default:
  - `.github/workflows/*.yml|*.yaml` is blocked by `tools/ship.sh` unless `SHIP_ALLOW_WORKFLOWS=1`.

## CI automation constitution
- This repository is PR-driven and local-verify-first by default.
- Do not rely on GitHub Actions as a required execution path.
- Required baseline before any PR merge:
  - Run `make verify` locally and record result in `reports/<RUN_ID>/summary.md`.
  - Keep evidence (`meta.json`, `summary.md`, `decision.md`) complete.
  - Keep scope gate and task/RUN_ID discipline.
- GitHub Actions are optional and remain disabled unless explicitly requested by the project owner.

## Rollback
- If any workflow automation is introduced later, disable it immediately and fall back to local verify + PR flow.
