# READ_ORDER

This order is mandatory for session handoff alignment.

## Step 0: Startup
1. `tools/qf init`

## Step 1: Sync Layer (must read in order)
1. `SYNC/README.md`
2. `SYNC/CURRENT_STATE.md`
3. `SYNC/SESSION_LATEST.md`
4. `SYNC/DECISIONS_LATEST.md`
5. `SYNC/LINKS.md`

## Step 2: Core Governance
1. `AGENTS.md`
2. `docs/WORKFLOW.md`
3. `docs/ENTITIES.md`
4. `docs/PROJECT_GUIDE.md`
5. `TASKS/STATE.md`
6. `TASKS/QUEUE.md`

## Step 3: Current Run Evidence
1. latest `reports/<RUN_ID>/handoff.md` (if exists)
2. latest `reports/<RUN_ID>/conversation.md` (if exists)
3. latest `reports/<RUN_ID>/decision.md`
4. latest `reports/<RUN_ID>/summary.md`

## Completion Criteria (must restate)
- Goal (1 sentence)
- Scope (exact paths)
- Acceptance (verify/evidence/scope)
- Next command (one command only)
