# Decision

RUN_ID: `run-2026-02-27-sync-learning-exam-cli-web`

## Why
- User requirement: onboarding must focus on thought-layer sync quality, not answer quantity.
- Need one exam flow compatible with both Codex CLI and web GPT, with machine judgement.

## Options considered
- Manual interviewer-only judgement (rejected): subjective and inconsistent across sessions.
- Pure multiple-choice quiz (rejected): measures memory, weak on causal alignment.
- Structured answer template + weighted required checks + auto-grader (chosen): auditable and repeatable.

## Risks / Rollback
- Risk: rubric may be too rigid and reject semantically-correct but differently phrased answers.
- Mitigation: keep rubric editable (`SYNC/EXAM_RUBRIC.json`) and review failed checks before adjusting.
- Rollback: revert this RUN to return to manual onboarding review.
