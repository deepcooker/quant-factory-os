# TASK: record codex /status snapshot in evidence

RUN_ID: run-2026-02-09-status-snapshot
OWNER: Codex
PRIORITY: P1

## Goal
Standardize recording a Codex `/status` snapshot in evidence notes for each RUN.

## Non-goals
Do not automate `/status` collection or change Codex behavior.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/run-2026-02-09-status-snapshot/summary.md` and
  `reports/run-2026-02-09-status-snapshot/decision.md`
- [ ] Workflow docs require `/status` snapshot in evidence notes with example
- [ ] Guardrail test ensures `/status` rule remains documented

## Inputs
- `TASKS/_TEMPLATE.md`
- `README.md` or `docs/WORKFLOW.md`
- `reports/run-2026-02-09-status-snapshot/summary.md`

## Steps (Optional)
- Generate evidence skeleton.
- Document `/status` snapshot rule with example block.
- Add minimal guardrail test.
- Verify and document changes.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: Process adds a small manual step at run start.
- Rollback plan: remove the rule and guardrail test.
