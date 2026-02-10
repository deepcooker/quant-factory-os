# Decision

RUN_ID: `run-2026-02-10-fix-docs-readme`

## Why
- `make verify` was failing due to missing docs and missing `/status` documentation.

## What
- Added required docs with mandated titles/keywords and documented `/status` rule.
- Added minimal `/status` mention to `README.md` to satisfy fallback documentation.

## Options considered
- Document `/status` only in README (rejected: workflow doc now exists and should carry the rule).

## Risks / Rollback
- Risk: Future doc edits remove required keywords and break tests.
- Rollback plan: Revert the added docs/README line if needed.

## Verify
- `make verify`
