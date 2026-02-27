# Summary

RUN_ID: `run-2026-02-27-qf-handoff-session-summary-format`

## What changed
- Updated `tools/qf handoff` template from detailed dump style to concise session summary style.
- New handoff output now emphasizes:
  - main communication thread
  - key conclusions
  - small reflection summary
  - one recommended next command
- Preserved missing-input robustness and run-state update behavior.
- Updated `tests/test_qf_handoff.py` assertions to match the new summary contract.
- Updated `docs/WORKFLOW.md` S1 handoff description to document concise summary format.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-qf-handoff-session-summary-format`
  - created evidence skeleton files
- `bash tools/qf handoff RUN_ID=run-2026-02-27-qf-handoff-session-summary-format`
  - output: `reports/run-2026-02-27-qf-handoff-session-summary-format/handoff.md`
- `make verify`
  - result: `71 passed`

## Notes
- Intent is UX-first continuity: summary page for fast handoff, not transcript-level detail.
- Full transcript fallback remains local under `chatlogs/` (not committed).
