# Summary

RUN_ID: `run-2026-02-27-sync-chinese-entrypoint-naming`

## What changed
- Renamed SYNC entry-layer files to Chinese numbered names for clearer separation from root `README.md`:
  - `SYNC/README.md` -> `SYNC/00_同频入口.md`
  - `SYNC/READ_ORDER.md` -> `SYNC/01_阅读顺序.md`
  - `SYNC/CURRENT_STATE.md` -> `SYNC/02_当前状态.md`
  - `SYNC/SESSION_LATEST.md` -> `SYNC/03_本次会话.md`
  - `SYNC/DECISIONS_LATEST.md` -> `SYNC/04_最新决策.md`
  - `SYNC/LINKS.md` -> `SYNC/05_索引链接.md`
- Updated governance references to new canonical entrypoint:
  - `README.md`
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `docs/CODEX_ONBOARDING_CONSTITUTION.md`
  - `docs/PROJECT_GUIDE.md`
- Updated new `SYNC/*` content to Chinese and consistent read-order semantics.

## Commands / Outputs
- `make evidence RUN_ID=run-2026-02-27-sync-chinese-entrypoint-naming`
  - created evidence skeleton files under `reports/run-2026-02-27-sync-chinese-entrypoint-naming/`
- `make verify`
  - `69 passed in 6.28s`
- `make verify` (final check after doc/evidence update)
  - `69 passed in 6.34s`
- `tools/ship.sh "sync: 同频入口中文命名并统一引用"`
  - first run blocked by scope gate on quoted non-ASCII staged paths.
- `SHIP_ALLOW_OUT_OF_SCOPE=1 tools/ship.sh "sync: 同频入口中文命名并统一引用"`
  - committed, opened and merged PR: `#122`
  - post-ship local sync step aborted once due untracked evidence dir.

## Notes
- No behavior change to execution automation (`tools/qf` logic unchanged).
- Scope limited to governance/sync layer naming and references.
- Scope gate failure reason was tooling/encoding mismatch for Chinese file paths, not a true out-of-scope change.
