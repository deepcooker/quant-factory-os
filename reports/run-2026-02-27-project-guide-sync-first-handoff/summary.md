# Summary

RUN_ID: `run-2026-02-27-project-guide-sync-first-handoff`

## What changed
- Updated `chatlogs/PROJECT_GUIDE.md` to make "sync-first handoff" the primary logic before execution.
- Added section `4.4 同频优先接班协议`:
  - reconnect/session-start read order,
  - mandatory restatement before actions,
  - mandatory snapshot before quit.
- Reworked section `10. 新窗口对齐` into v2.1:
  - includes `handoff.md` and `conversation.md` in required reading order,
  - adds conflict rule (`decision.md` + latest PR as source of truth),
  - clarifies minimal next-step command output.
- Kept appendix A (wealth/quant project integration roadmap) unchanged.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-project-guide-sync-first-handoff`
- `make verify` -> `64 passed in 4.81s`

## Notes
- This task intentionally changes process documentation only (no tooling logic change).
