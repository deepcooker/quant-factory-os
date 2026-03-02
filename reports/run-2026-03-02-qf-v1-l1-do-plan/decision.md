# Decision

RUN_ID: `run-2026-03-02-qf-v1-l1-do-plan`

## Why
- The prior flow was execution-first and low on direction consensus, causing poor UX and weak strategy alignment.
- `tools/qf do` had real friction in production flow:
  - logging before sync made tracked evidence files dirty before pull;
  - internal auto-plan removed proposal file before pick, causing chain breaks.
- Strong mode requires a dedicated direction confirmation layer before task execution.

## Options considered
- Keep current flow and only patch `do` bugs (rejected): fixes immediate pain but still lacks direction-layer confirmation.
- Add manual docs-only direction process (rejected): still relies on human memory and inconsistent execution.
- Implement tool-level direction gate + do stability fixes (chosen):
  - add `orient/choose` as L1 layer;
  - keep L2 execution serial for now;
  - repair `do` chain and queue-empty guidance.

## Risks / Rollback
- Risk: adding `orient/choose` introduces one extra step for users who only want immediate execution.
  - Mitigation: command output includes single next command and defaults to recommended option.
- Risk: heuristics for orientation ranking may be simplistic.
  - Mitigation: orientation output is explicit/auditable (`orient.json`), easy to iterate in follow-up runs.
- Rollback:
  - Revert this RUN to return to previous `ready->plan->do` behavior.
  - Keep existing `sync/ready` gates from prior run unchanged.

## Stop reason
- `task_done`
