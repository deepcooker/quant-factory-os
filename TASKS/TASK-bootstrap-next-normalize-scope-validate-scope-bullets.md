# TASK: bootstrap next: normalize Scope + validate scope bullets

RUN_ID: run-2026-02-22-bootstrap-next-normalize-scope-validate-scope-bullets
OWNER: <you>
PRIORITY: P1

## Goal
`tools/task.sh --next` must render Scope as one-path-per-bullet and fail fast if Scope cannot be parsed into valid bullets.

## Scope (Required)
- `tools/task.sh`
- `tests/`
- `TASKS/QUEUE.md`


## Non-goals
What we explicitly do NOT do.

## Acceptance
- Generated task Scope is multi-line bullets (each bullet is a single backticked path).
- No non-path explanatory bullet is appended to Scope.
- If Scope has no valid bullet paths, `--next` exits non-zero with a clear error.
- `make verify` passes and evidence recorded under `reports/<RUN_ID>/`.

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
