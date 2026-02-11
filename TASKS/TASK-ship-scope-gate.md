# TASK: ship scope gate (validate staged files against task-declared scope)

RUN_ID: run-2026-02-11-ship-scope-gate
OWNER: codex
PRIORITY: P1

## Goal
Add a default-on scope gate in `tools/ship.sh` so staged files must stay within task-declared scope, preventing missing/extra files in PR delivery.

## Scope
- `tools/ship.sh`
- `TASKS/_TEMPLATE.md`
- `docs/WORKFLOW.md`
- `tests/`
- `TASKS/TASK-ship-scope-gate.md`

## Non-goals
No a9 integration changes or non-ship tooling refactors.

## Acceptance
- [ ] `tools/ship.sh` parses `## Scope` from task file and validates staged files against allowed scope.
- [ ] Out-of-scope files are rejected by default with clear file list; `SHIP_ALLOW_OUT_OF_SCOPE=1` is explicit escape hatch.
- [ ] Test-only mode exists (`SHIP_SCOPE_GATE_ONLY=1`) using env-provided task file + file list without git push/PR side effects.
- [ ] Minimal pytest added: in-scope pass + out-of-scope fail.
- [ ] `TASKS/_TEMPLATE.md` includes required `## Scope` guidance.
- [ ] `docs/WORKFLOW.md` documents scope declaration + ship gate expectation.
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-11-ship-scope-gate/summary.md` and `reports/run-2026-02-11-ship-scope-gate/decision.md`

## Inputs
- `TASKS/_TEMPLATE.md`
- `tools/ship.sh`
- `tests/test_ship_pr_body_excerpt.py`
- `docs/WORKFLOW.md`

## Steps (Optional)
1. Create task + evidence skeleton.
2. Add scope parser + scope gate to `tools/ship.sh`.
3. Add `SHIP_SCOPE_GATE_ONLY` mode for isolated tests.
4. Add pytest coverage for pass/fail scope validation.
5. Update template/workflow text for scope declaration.
6. Run `make verify`, update evidence, and ship.

## Reading policy
Use `tools/view.sh` by default. If larger ranges are needed, specify exact line ranges and reason.

## Risks / Rollback
- Risks: scope parsing assumptions may reject malformed task files.
- Rollback plan: revert this run's ship/template/workflow/test changes.
