# Decision

RUN_ID: `run-2026-03-07-project-guide-mainline-reinforcement`

## Why
- The user confirmed that `PROJECT_GUIDE.md` is a deliberately designed learn curriculum and that any change must preserve the question-bank structure.
- The narrowest useful update was to keep every question intact while making the guide more explicit about its actual role: use high-quality questioning to force reading owner docs, evidence, and session continuity; then use the same questions to pull the model back when it drifts.

## Options considered
- Leave `PROJECT_GUIDE.md` untouched and rely on `AUTOMATION_1_0.md` / chat-only explanation.
- Rewrite the guide structure around the new automation wording.
- Keep the guide structure intact, create a backup, and make only minimal wording updates where the learning semantics needed to be sharper.

Chosen:
- Keep the question-bank structure intact, back up the guide first, and make the smallest wording changes necessary to strengthen the reverse-questioning/mainline-recovery behavior.

## Risks / Rollback
- Risk: even small wording changes inside the guide can accidentally weaken the original learning rhythm if they spread beyond the anchor sections.
- Rollback: restore [docs/PROJECT_GUIDE.md](/root/quant-factory-os/docs/PROJECT_GUIDE.md) from [docs/PROJECT_GUIDE_1.0_backup.md](/root/quant-factory-os/docs/PROJECT_GUIDE_1.0_backup.md) and revert the paired owner-doc sync in [AGENTS.md](/root/quant-factory-os/AGENTS.md) and [docs/WORKFLOW.md](/root/quant-factory-os/docs/WORKFLOW.md).

## Stop Reason
- task_done
