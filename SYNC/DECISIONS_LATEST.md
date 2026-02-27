# DECISIONS_LATEST

Date: 2026-02-27
RUN_ID: `run-2026-02-27-sync-entrypoint-layer`

## Decision 1: Sync layer location
- Chosen: top-level `SYNC/`
- Why: `docs/` is too broad; `chatlogs/` is too noisy for rapid alignment.
- Impact: one explicit entrypoint for both CLI and web-model collaboration.

## Decision 2: Sync workflow priority
- Chosen: sync-first, execute-second.
- Why: session memory is unstable across `/quit`, account switch, and network.
- Impact: each session starts from `SYNC/READ_ORDER.md` before code actions.

## Decision 3: Wealth roadmap preservation
- Chosen: keep wealth/quant appendix untouched.
- Why: strategic content is valid; only handoff ergonomics needed upgrade.
- Impact: architecture direction preserved while improving operating continuity.
