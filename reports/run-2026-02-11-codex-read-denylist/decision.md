# Decision

RUN_ID: `run-2026-02-11-codex-read-denylist`

## Why
- Codex reading `project_all_files.txt` by default adds high-noise context that is not evidence and is already treated as a special local artifact in workflow rules.
- A clear default read policy with explicit override improves permission clarity and makes exceptions auditable.

## Options considered
- Add denylist enforcement in `tools/view.sh` only (chosen): smallest reliable fix for default read path.
- Add same guard in `tools/find.sh` if present: not applied because `tools/find.sh` is not a regular file in this repository.
- Hard-block without override: rejected because controlled, auditable emergency reads are still needed.

## Risks / Rollback
- Risk: simple glob matching may not cover every edge path form.
- Risk: denylist can block intentional reads unless override is set.
- Rollback plan: revert `.codex_read_denylist`, `tools/view.sh`, and `tests/test_codex_read_denylist.py`.
