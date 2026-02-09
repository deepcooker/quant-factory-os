# Decision

RUN_ID: `run-2026-02-09-status-snapshot`

## Why
- Codex usage limits are opaque without a manual snapshot; requiring a `/status`
  paste reduces friction and improves shared visibility.

## Options considered
- Automate `/status` capture (rejected: no stable API and may leak secrets).
- Leave it informal (rejected: too easy to forget).

## Risks / Rollback
- Risks: extra manual step at run start.
- Rollback: remove the rule and guardrail test.
