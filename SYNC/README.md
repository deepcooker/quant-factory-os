# SYNC Entry Layer

Purpose: this is the **single sync entrypoint** for any model/session (Codex CLI
or web GPT) to align in minutes without relying on chat history.

If you only read one folder before action, read `SYNC/`.

## Start Here
1. `SYNC/READ_ORDER.md`
2. `SYNC/CURRENT_STATE.md`
3. `SYNC/SESSION_LATEST.md`
4. `SYNC/DECISIONS_LATEST.md`
5. `SYNC/LINKS.md` (for deep dive)

## Rules
- Sync first, execute later.
- If `SYNC/*` conflicts with deeper evidence, trust latest:
  - `reports/<RUN_ID>/decision.md`
  - merged PR state on `main`
- Before quit, update `SYNC/SESSION_LATEST.md`.
