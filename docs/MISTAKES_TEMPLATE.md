# MISTAKE TEMPLATE (PROCESS + BUSINESS)

RUN_ID: `run-...`
DATE: `YYYY-MM-DD`
TASK: `TASK-...`

## Symptom
- What failed (short, concrete).

## Category
- [ ] thinking_error (assumption / reasoning / problem framing)
- [ ] decision_error (wrong option or priority)
- [ ] execution_error (command/code/tooling operation failure)
- [ ] verification_error (test/acceptance/gate miss)
- [ ] recovery_error (resume/rollback/handoff failure)
- [ ] business_error (domain logic or data issue)

## Root Cause Hypothesis
- Why this happened.

## Evidence
- command:
- key output:
- related files:

## Fix
- What was changed.

## Guardrail
- Test/rule/tool gate to prevent recurrence.

## Rollback
- How to safely revert if needed.

## Next Action
- Follow-up task link or queue item.
