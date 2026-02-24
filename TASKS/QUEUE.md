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

- [x] TODO Title: auto-mark queue done on successful ship  Picked: run-2026-02-22-auto-mark-queue-done-on-successful-ship 2026-02-22T03:15:24+0800
  Done: PR #89, RUN_ID=run-2026-02-22-auto-mark-queue-done-on-successful-ship
  Goal: after a successful ship/PR open (and/or merge), automatically mark the picked `[>]` queue item as `[x]` and append `Done: PR #<n>, RUN_ID=<id>`.
  Scope: `tools/task.sh`, `tools/ship.sh` (if needed), `TASKS/QUEUE.md`, `tests/`
  Acceptance:
  - When shipping a task created by `--next`, the corresponding queue item is updated from `[>]` to `[x]` with Done metadata.
  - No effect if ship fails or no matching picked item exists.
  - `make verify` passes and evidence recorded under `reports/<RUN_ID>/`.
  RUN_ID: (optional)


- [x] TODO Title: bootstrap next: normalize Scope + validate scope bullets  Picked: run-2026-02-22-bootstrap-next-normalize-scope-validate-scope-bullets 2026-02-22T02:17:45+0800
  Goal: `tools/task.sh --next` must render Scope as one-path-per-bullet and fail fast if Scope cannot be parsed into valid bullets.
  Scope: `tools/task.sh`
  Acceptance:
  - Generated task Scope is multi-line bullets (each bullet is a single backticked path).
  - No non-path explanatory bullet is appended to Scope.
  - If Scope has no valid bullet paths, `--next` exits non-zero with a clear error.
  - `make verify` passes and evidence recorded under `reports/<RUN_ID>/`.
  RUN_ID: (optional)
  Done: PR #86, RUN_ID=run-2026-02-22-bootstrap-next-normalize-scope-validate-scope-bullets

- [x] TODO Title: add minimal regression tests for workflow gates (P1)
  Goal: cover scope gate / expected-files gate / single-run guard with small
  regression tests to prevent workflow regressions.
  Scope: ship/task tooling tests and minimal test fixtures.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)
  Done: PR #81, RUN_ID=run-2026-02-21-add-minimal-regression-tests-for-workflow-gates-p1

- [x] TODO Title: startup prints session entrypoints + active RUN_ID (P0)
  Goal: make `tools/start.sh` or `tools/enter.sh` print startup entrypoints
  (`TASKS/STATE.md`, `TASKS/QUEUE.md`, `docs/WORKFLOW.md`) and current `RUN_ID`.
  Scope: `tools/start.sh`, `tools/enter.sh`, startup docs/tests only as needed.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)
  Done: PR #78, RUN_ID=run-2026-02-21-startup-entrypoints-runid

- [x] TODO Title: ENTITIES.md minimal dictionary sync (P1)
  Goal: ensure `docs/ENTITIES.md` has minimal definitions for existing entities:
  Task, PR, RUN_ID, Evidence, STATE, MISTAKES, Gate, Tool.
  Scope: `docs/ENTITIES.md` and narrowly related docs references if required.
  Acceptance:
  - `make verify` passes.
  - Evidence recorded under `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`.
  - No changes outside declared scope.
  RUN_ID: (optional)
  Done: PR #77, RUN_ID=run-2026-02-12-entities-min-dict

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
  
- [x] TODO Title: queue pick lock (in-progress marker)
  Goal: when `tools/task.sh --next` picks the top item, mark it as in-progress (`[>]`) and record RUN_ID+timestamp to avoid duplicate picks across sessions.
  Scope: `tools/task.sh`, `TASKS/QUEUE.md`, minimal tests for queue parsing/locking.
  Acceptance:
  - Picking changes `[ ]` -> `[>]` and appends `Picked: <RUN_ID> <timestamp>`.
  - Re-running `--next` does not pick the same `[>]` item again.
  - `make verify` passes and evidence recorded under `reports/<RUN_ID>/`.
  RUN_ID: (optional)
