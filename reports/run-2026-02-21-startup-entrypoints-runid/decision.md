# Decision

RUN_ID: `run-2026-02-21-startup-entrypoints-runid`

## Why
- Startup checklist requires selecting the top unfinished queue item and
  shipping a complete run with evidence.
- Queue goal ("startup prints session entrypoints + active RUN_ID") is already
  implemented in `tools/enter.sh`; adding a regression guardrail prevents drift.

## Options considered
- Change `tools/start.sh` or `tools/enter.sh` output.
  - Not chosen: behavior already satisfies requirement; extra edits add risk.
- Add regression tests only.
  - Chosen: smallest diff that still implements durable acceptance.

## Risks / Rollback
- Risks:
  - String-based contract test may need updates if wording intentionally changes.
- Rollback plan:
  - Revert this run commit to remove the new task/test/evidence files.
