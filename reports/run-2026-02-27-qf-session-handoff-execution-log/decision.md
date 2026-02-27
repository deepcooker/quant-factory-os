# Decision

RUN_ID: `run-2026-02-27-qf-session-handoff-execution-log`

## Why
- Session interruptions (`/quit`, account switch, network) require deterministic in-repo recovery that does not depend on volatile chat memory.
- Existing evidence was strong at task level but lacked unified execution trace and restart summary.

## Options considered
- Option A: Store full raw transcripts in repo.
  - Rejected due noise, privacy risk, and low audit signal density.
- Option B: Keep concise conversation checkpoints + structured execution events + generated handoff summary.
  - Selected as minimal and auditable approach, aligned with current repo governance.

## Risks / Rollback
- Risks:
  - Over-logging could reduce readability.
  - Sensitive text may appear in command outputs.
- Mitigation:
  - Default redaction for common secret patterns in execution logs.
  - Optional log disable switch (`QF_LOG_DISABLE=1`) for exceptional scenarios.
  - Keep full transcript out of repo; use concise snapshots.
- Rollback:
  - Revert `tools/qf`, docs entries, and added tests in this RUN diff.
