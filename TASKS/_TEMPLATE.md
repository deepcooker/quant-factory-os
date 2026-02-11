# TASK: <short-name>

RUN_ID: <YYYY-MM-DD-identifier>
OWNER: <you>
PRIORITY: P1

## Goal
What outcome do we want? (1-3 lines)

## Scope (Required)
- List allowed paths for this task using bullets and backticks, for example:
  - `tools/ship.sh`
  - `tests/`
- `tools/ship.sh` uses this section as the source of truth for scope gate checks.

## Non-goals
What we explicitly do NOT do.

## Acceptance
- [ ] Command(s) pass: `make verify`
- [ ] Evidence updated: `reports/<RUN_ID>/summary.md` and `reports/<RUN_ID>/decision.md`
- [ ] Regression guardrail added/updated if applicable

## Inputs
- Links / files / references
- If data is needed, specify allowed sample constraints (max rows, time window)

## Steps (Optional)
Suggested approach, if you have one.

## Reading policy
Use `tools/view.sh` by default. If you need to read larger ranges, specify the
exact line range and the reason.

## Risks / Rollback
- Risks:
- Rollback plan:
