# TASK: document workflow and entity model

RUN_ID: run-2026-02-09-docs-foundation
OWNER: Codex
PRIORITY: P1

## Goal
Capture a concise operating manual and concept model so new agents can take over
without context gaps.

## Non-goals
Do not alter runtime scripts or automate integrations beyond documentation.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-docs-foundation/summary.md` and
  `reports/run-2026-02-09-docs-foundation/decision.md`
- [ ] Workflow, entities, and integration docs added/updated
- [ ] Guardrail test ensures docs presence

## Inputs
- `TASKS/_TEMPLATE.md`
- `docs/WORKFLOW.md`
- `README.md`
- `tools/run_a9.py`

## Steps (Optional)
- Generate evidence skeleton.
- Update workflow doc and add entities/integration docs.
- Update README quickstart and next steps.
- Add guardrail test and verify.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: docs drift from reality if not maintained.
- Rollback plan: revert docs/test changes.
