# TASK: session-conversation-fallback-log

RUN_ID: run-2026-02-27-session-conversation-fallback-log
OWNER: codex
PRIORITY: P1

## Goal
Add a repo-level fallback so important Codex conversations can be snapshotted
into versioned files, reducing loss from `/quit`, account switch, or network issues.

## Scope (Required)
- `tools/qf`
- `docs/WORKFLOW.md`
- `AGENTS.md`
- `tests/`
- `reports/run-2026-02-27-session-conversation-fallback-log/`

## Non-goals
- Building a full automatic transcript hook inside Codex runtime internals.
- Uploading chat logs to external services.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- User request in current session: "这次对话必须记录到仓库里，万一丢失很麻烦"
- Existing workflow: `tools/qf init/ready/do`, evidence-first process.

## Steps (Optional)
1. Add a dedicated command to persist conversation snapshots under `chatlogs/`.
2. Document when to run it in startup/ready workflow.
3. Add tests and evidence.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks: over-logging or accidental secret capture in free-form text.
- Rollback plan: revert this task diff and remove added command/tests/docs.
