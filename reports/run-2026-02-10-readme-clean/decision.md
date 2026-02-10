# Decision

RUN_ID: `run-2026-02-10-readme-clean`

## Why
- README needed to be a concise entrypoint without historical narrative.

## What
- Replaced README with a structured entrypoint including quickstart, workflow,
  concepts, docs index, troubleshooting, and checklists.

## Options considered
- Keep partial narrative and trim (rejected: still too long and noisy).

## Risks / Rollback
- Risk: Missing required strings could break tests.
- Rollback plan: Revert `README.md` to prior version if needed.

## Verify
- `make verify`
