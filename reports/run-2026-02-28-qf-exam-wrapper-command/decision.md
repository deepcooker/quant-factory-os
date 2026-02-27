# Decision

RUN_ID: `run-2026-02-28-qf-exam-wrapper-command`

## Why
- User requested lower-friction exam operation and onboarding continuity.
- Existing flow either required manual python invocation or failed immediately when answer file was missing.

## Options considered
- Keep direct python command only (rejected): still works but higher friction.
- Add `tools/qf exam` wrapper only (partial): simplifies grading but still requires manual answer file preparation.
- Add `tools/qf exam` + `tools/qf exam-auto` (chosen): keeps consistent run-id semantics and removes first-run friction via scaffold-then-grade.

## Risks / Rollback
- Risk: argument parsing ambiguity with future qf subcommands.
- Mitigation: explicit `KEY=VALUE` args and strict unexpected-arg failure.
- Rollback: revert this RUN to remove `exam-auto` additions and related tests/docs.
