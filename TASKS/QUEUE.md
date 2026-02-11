# QUEUE

Purpose: this is the "next-shot" queue for new Codex sessions. On startup, only
`TASKS/STATE.md` + `TASKS/QUEUE.md` are used to decide what to do next.

## Item format (minimum)
- Title
- Goal (one sentence)
- Scope (allowed files/directories)
- Acceptance (3 checks: verify, evidence, scope)
- Optional: RUN_ID (if omitted, generate at execution time)

## Queue
- [ ] TODO Title: ship allowlist includes docs
  Goal: update `tools/ship.sh` so untracked allowlist includes `docs/*`.
  Scope: `tools/ship.sh`, tests/docs directly related to this rule.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)

- [ ] TODO Title: ship expected-files gate
  Goal: add expected-files guard so ship validates task-declared allowed files.
  Scope: ship/task tooling and related workflow docs/tests.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)
