# Decision

RUN_ID: `run-2026-03-04-docs-cleanup-project-guide`

## Why
- User requested `PROJECT_GUIDE` to contain only question-and-answer content and remove all nonessential narrative.
- User also requested a dedicated guide for wealth-system new-project onboarding.
- Consolidating guidance into Q&A format improves learn/exam consistency and reduces sync noise for new AI sessions.

## Options considered
- Option A: Keep existing `PROJECT_GUIDE` structure and only trim some sections.
  - Rejected: still leaves mixed narrative and weak exam alignment.
- Option B: Fully rewrite `PROJECT_GUIDE` as Q&A-only and move project-bootstrap details into a separate file.
  - Selected: matches the request directly and keeps responsibilities clear.

## Risks / Rollback
- Risk: Some readers may miss removed background narrative previously embedded in `PROJECT_GUIDE`.
- Mitigation: Added dedicated wealth bootstrap file and preserved evidence pointers in each Q&A answer.
- Rollback: Restore previous `docs/PROJECT_GUIDE.md` from git history if mixed narrative format is needed again.
- Stop reason: `task_done`
