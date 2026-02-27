# DECISIONS_LATEST

Date: 2026-02-27
RUN_ID: `run-2026-02-27-governance-convergence-sync-priority`

## Decision 1: PROJECT_GUIDE canonical location
- Chosen: `docs/PROJECT_GUIDE.md`
- Why: governance/strategy docs must live under canonical docs ownership.
- Impact: `chatlogs/PROJECT_GUIDE.md` remains as compat pointer only.

## Decision 2: CURRENT_RUN_ID source-of-truth
- Chosen: `TASKS/STATE.md`
- Why: active run pointer must be in one stable, versioned state file.
- Impact: `qf` defaults should bind to `CURRENT_RUN_ID` unless explicitly overridden.

## Decision 3: Wealth roadmap preservation
- Chosen: keep wealth/quant appendix untouched.
- Why: strategic content is valid; only handoff ergonomics needed upgrade.
- Impact: architecture direction preserved while improving operating continuity.
