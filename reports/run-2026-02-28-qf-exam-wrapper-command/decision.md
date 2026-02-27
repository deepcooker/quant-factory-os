# Decision

RUN_ID: `run-2026-02-28-qf-exam-wrapper-command`

## Why
- User requested one-command operation for exam grading to reduce operational friction.
- Existing flow required manual invocation of `tools/sync_exam.py`, which increased command overhead.

## Options considered
- Keep direct python command only (rejected): still works but higher friction.
- Add `tools/qf exam` wrapper (chosen): keeps one entrypoint and consistent run-id semantics.

## Risks / Rollback
- Risk: argument parsing ambiguity with future qf subcommands.
- Mitigation: explicit `KEY=VALUE` args and strict unexpected-arg failure.
- Rollback: revert this RUN to remove `exam` subcommand and related tests/docs.
