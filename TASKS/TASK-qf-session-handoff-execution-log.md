# TASK: qf-session-handoff-execution-log

RUN_ID: run-2026-02-27-qf-session-handoff-execution-log
OWNER: codex
PRIORITY: P1

## Goal
Implement minimal session full-trace persistence and disconnect recovery on top of
existing `tools/qf init/ready/do/resume` flow.

## Scope (Required)
- `tools/qf`
- `docs/WORKFLOW.md`
- `AGENTS.md`
- `tests/`
- `TASKS/TASK-qf-session-handoff-execution-log.md`
- `reports/run-2026-02-27-qf-session-handoff-execution-log/`

## Non-goals
- Storing full raw chat transcripts.
- Replacing existing evidence files (`summary.md`, `decision.md`, `ship_state.json`).

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- Approved implementation plan: P0/P1/P2 for execution logs + handoff + init hint.

## Steps (Optional)
1. Add automatic execution logging with default redaction.
2. Add `tools/qf handoff` to synthesize restart context.
3. Add init hint to continue from last active run.
4. Add focused regression tests and docs updates.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: noisy logs or accidental sensitive text in notes.
- Rollback plan: revert this task diff.
