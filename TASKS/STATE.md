# STATE

CURRENT_RUN_ID: run-2026-03-01-qf-sync-ready
CURRENT_TASK_FILE: TASKS/TASK-qf-sync-ready.md
CURRENT_STATUS: done
CURRENT_UPDATED_AT: 2026-02-28T17:40:31+00:00












## Current baseline
- Core tooling available: `tools/start.sh`, `tools/enter.sh`, `tools/doctor.sh`,
  `tools/view.sh`, `tools/find.sh`.
- Documentation baseline in place: `docs/WORKFLOW.md`, `docs/ENTITIES.md`,
  `docs/README.md` (if present).

## Current conventions
- Task = requirement definition (source of truth for scope).
- PR = delivery artifact for one task.
- RUN_ID = evidence namespace under `reports/<RUN_ID>/`.
- Handoff rule: `docs/WORKFLOW.md` Memory & Context.
- Handoff hard rules (gate): `docs/WORKFLOW.md` -> Memory & Context.
- Boundary v0: `docs/BOUNDARY_A9.md`.
- Session startup entrypoints:
- Queue: `TASKS/QUEUE.md`.
- Entities: `docs/ENTITIES.md`.
- Startup checklist: `docs/WORKFLOW.md#Codex-session-startup-checklist`.

## Next steps
- Finish baseline hardening, then begin main project integration.
- Define external data ingestion strategy and constraints (sources, format,
  retention).
- Define database/storage strategy and interfaces.
- Confirm OSS dependency policy and allowlist.
- Add minimal regression tests for core tooling and workflow enforcement.

## Current blockers / risks
- External data and database/OSS integration policies are not yet defined.


## Risk guardrails

- Queue-add 只是“入队草稿”，必须 PR merge 到 main 才算存在；未 merge 前不要 pick。
- Pick 后 QUEUE 变为 `[>]` 是正常锁；完成后 ship 才会回写 `[x] Done`。
- Ship / enter / pull 前先 `git status --porcelain`：
  - 若出现不属于当前 RUN 的 `?? reports/run-*/`，先删除或 stash，否则容易触发 “working tree is not clean”。
- 遇到 `enter.sh` 因 dirty 拦截：
  - 严谨做法：先清理/commit/stash
  - 单人省事：`ENTER_AUTOSTASH=1 ./tools/enter.sh`（会打印 stash 名与恢复指令）
