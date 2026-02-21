# Summary

RUN_ID: `run-2026-02-22-bootstrap-next-normalize-scope-validate-scope-bullets`

## What changed
- Normalized Scope output for `tools/task.sh --next`: Scope is now rendered as one-path-per-bullet.
- Added fail-fast validation: invalid Scope text (e.g. natural language with spaces) causes `--next` to exit non-zero with a clear error.
- Removed non-path explanatory text from generated Scope.

## Verification
- make verify (34 passed)


## Commands / Outputs
- 

## Notes
- 
