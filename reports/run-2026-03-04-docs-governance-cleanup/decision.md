# Decision

RUN_ID: `run-2026-03-04-docs-governance-cleanup`

## Why
- The user requested a full audit/cleanup of sync docs and logic (`AGENTS`, `README`, `docs/`, `SYNC/`) with explicit decisions on what to delete, adjust, and detail.
- Current pain point is documentation overlap and stale references, which lowers sync quality even when content volume is high.
- To improve onboarding quality, boundary rules must become hard constraints rather than oral guidance.

## Options considered
- Option A: Keep all files and only append more guidance.
  - Rejected: increases noise and does not resolve owner conflicts.
- Option B: Aggressive delete of stale docs without compatibility fallback.
  - Partially rejected: broke regression tests expecting legacy integration file.
- Option C (selected): owner-boundary hardening + targeted pruning + compatibility pointer for legacy test coupling.
  - Selected because it reduces noise while preserving current verification stability.

## Risks / Rollback
- Risk: deleting legacy docs may break scripts/tests that still hard-code old file names.
- Mitigation:
  - run `make verify` after each cleanup pass
  - keep compatibility pointer file when test coupling still exists
- Rollback:
  - restore removed files from git history if downstream tooling requires temporary compatibility.
- Stop reason: `task_done`
