# Summary

RUN_ID: `run-2026-03-07-project-guide-mainline-reinforcement`

## What changed
- Created [docs/PROJECT_GUIDE_1.0_backup.md](/root/quant-factory-os/docs/PROJECT_GUIDE_1.0_backup.md) before editing the guide.
- Kept the `PROJECT_GUIDE` question-bank structure intact and only tightened:
  - `使用方式`
  - `Q1` standard answer
  - `Q4` standard answer and mainline meaning
  - `Q8` standard answer
  - `Q17` standard answer and required files
- Synced owner-doc anchors so the same rule is explicit in all three places:
  - [docs/PROJECT_GUIDE.md](/root/quant-factory-os/docs/PROJECT_GUIDE.md)
  - [AGENTS.md](/root/quant-factory-os/AGENTS.md)
  - [docs/WORKFLOW.md](/root/quant-factory-os/docs/WORKFLOW.md)
- The clarified rule is: `PROJECT_GUIDE` is a high-quality reverse-questioning course; when the model drifts, Codex CLI should go back to the question system and re-answer from evidence instead of continuing ad-hoc chat.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-03-07-project-guide-mainline-reinforcement`
- `make verify` -> `29 passed in 1.92s`
- `bash tools/legacy.sh review RUN_ID=run-2026-03-07-project-guide-mainline-reinforcement STRICT=1 AUTO_FIX=1` -> `REVIEW_STATUS: pass`
- `bash tools/smoke.sh RUN_ID=run-2026-03-07-project-guide-mainline-reinforcement TASK_FILE=TASKS/TASK-project-guide-mainline-reinforcement.md` -> `SMOKE_STATUS: pass`

## Notes
- This run intentionally did not restructure the guide or rewrite the question set.
- `docs/PROJECT_GUIDE.md` was edited only after a same-run backup was created.
