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
- [ ] TODO Title: startup prints session entrypoints + active RUN_ID (P0)
  Goal: make `tools/start.sh` or `tools/enter.sh` print startup entrypoints
  (`TASKS/STATE.md`, `TASKS/QUEUE.md`, `docs/WORKFLOW.md`) and current `RUN_ID`.
  Scope: `tools/start.sh`, `tools/enter.sh`, startup docs/tests only as needed.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)

- [ ] TODO Title: ENTITIES.md minimal dictionary sync (P1)
  Goal: ensure `docs/ENTITIES.md` has minimal definitions for existing entities:
  Task, PR, RUN_ID, Evidence, STATE, MISTAKES, Gate, Tool.
  Scope: `docs/ENTITIES.md` and narrowly related docs references if required.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)

- [ ] TODO Title: add minimal regression tests for workflow gates (P1)
  Goal: cover scope gate / expected-files gate / single-run guard with small
  regression tests to prevent workflow regressions.
  Scope: ship/task tooling tests and minimal test fixtures.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)

- [x] TODO Title: ship allowlist includes docs
  Goal: update `tools/ship.sh` so untracked allowlist includes `docs/*`.
  Scope: `tools/ship.sh`, tests/docs directly related to this rule.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)

- [x] TODO Title: ship expected-files gate
  Goal: add expected-files guard so ship validates task-declared allowed files.
  Scope: ship/task tooling and related workflow docs/tests.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)

- [x] TODO Title: add `.codex_read_denylist` baseline
  Goal: add default read denylist to reduce noisy context snapshots.
  Scope: `.codex_read_denylist` and minimal workflow docs references only.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)
