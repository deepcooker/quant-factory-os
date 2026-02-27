# Decision

RUN_ID: `run-2026-02-27-codex-ci-autofix-and-onboarding-constitution`

## Why
- The project needs a stable large-project collaboration loop: policy and onboarding guardrails plus CI-level Codex assistance.
- Safe defaults are required to prevent unintended autonomous write actions in shared repositories.
- Owner requires PR-only workflow due GitHub Actions queue latency; ship path must enforce this as a hard gate.

## Options considered
- Enable full autofix by default:
  - Rejected due to risk of unsolicited commits before branch protection is validated.
- Add review-only automation first:
  - Accepted as baseline with explicit opt-in variables.
- Keep manual-only process:
  - Rejected because it does not solve consistency and drift at scale.
- Add ship-time hard gate for `.github/workflows/*`:
  - Accepted. Default deny with explicit one-shot override preserves control and auditability.
- Remove stale `run-*-pick-candidate` artifacts permanently:
  - Accepted. Delete existing directory and expand `tools/qf` cleanup to `init/do/plan`.
- Prevent test-induced repo artifact regeneration:
  - Accepted. Unit test for `tools/task.sh --pick` now disables auto evidence to keep tests side-effect free.
- Constitution placement strategy:
  - Accepted. Put hard, enforceable operating rules in `AGENTS.md`; keep long-form training/background in `docs/` and `chatlogs/PROJECT_GUIDE.md` referenced by AGENTS init gate.
- Tool consolidation strategy:
  - Accepted. Keep `tools/qf` as primary agent entrypoint; retain `enter/onboard/start` as backward-compatible wrappers to avoid breaking existing habits/scripts.
- Backlog retention strategy:
  - Accepted (owner preference). Keep only active task and active RUN evidence; remove older task/report backlog to reset baseline under new architecture.

## Risks / Rollback
- Risk: misconfigured repository permissions/variables can prevent workflows from executing.
- Risk: overly broad prompts may generate noisy PR suggestions.
- Risk: future workflow maintenance requires explicit override during ship.
- Rollback:
  - Revert workflow guard section in `tools/ship.sh` and matching tests if policy changes.
  - Keep PR + local verify baseline regardless of automation toggles.
