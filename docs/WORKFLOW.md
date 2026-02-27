# WORKFLOW

Standard start

This document describes the expected workflow for changes in this repository.

## Document ownership
- Session entrypoint owner: `SYNC/READ_ORDER.md`
- Hard rules owner: `AGENTS.md`
- Execution details owner: `docs/WORKFLOW.md` (this file)
- Entity definitions owner: `docs/ENTITIES.md`
- Strategy/vision owner: `docs/PROJECT_GUIDE.md`

## Session lifecycle state machine (single source)
- `S0 Environment`: `tools/qf init`
  - Input: local repo checkout
  - Output: synced main + doctor checks + onboard summary
  - Note: this is environment preparation only, not readiness pass.
  - Continuing runs: auto-handoff is executed by default (`QF_INIT_AUTO_HANDOFF=1`).
- `S1 Handoff`: `tools/qf handoff`
  - Input: `CURRENT_RUN_ID` (or explicit RUN_ID)
  - Output: `reports/{RUN_ID}/handoff.md`
  - Note: this is context reconstruction only, not readiness pass.
  - Format: concise session summary (main thread, key conclusions, small reflection, one next command).
- `S2 Ready gate`: `tools/qf ready`
  - Input: restatement fields (goal/scope/acceptance/steps/stop)
  - Output: `reports/{RUN_ID}/ready.json`
  - Low-friction mode: fields auto-fill from active task contract by default (`QF_READY_AUTO=1`).
  - Gate: `tools/qf do` must fail without valid `ready.json`.
- `S3 Execute`: `tools/qf do queue-next`
  - Input: valid ready gate
  - Output: task pick + evidence skeleton + execution trace updates
- `S4 Ship`: `tools/ship.sh` (or `make ship`)
  - Input: verified diff + in-scope task contract
  - Output: PR + merge + main sync
- `S5 Learn`: reports/mistakes updates
  - Input: execution and verification outcomes
  - Output: durable memory for next session handoff.

## Status snapshot rule
Before each ship, record `/status` output in the evidence for the active RUN_ID.

## File list rule
`project_all_files.txt` is a local generated artifact and is excluded from PRs by
default. Update it only with a dedicated task, and call out the change in the PR
body.

## Scope gate rule
Task files must declare a `## Scope` section with allowed change paths. `tools/ship.sh`
validates staged files against this declared scope by default.

## Context snapshot (for ChatGPT)
`project_all_files.txt` is a context index snapshot for external models. It is
not evidence and does not belong in PRs by default. If it must be updated,
create a dedicated task, set `SHIP_ALLOW_FILELIST=1`, and use
`git add -f project_all_files.txt`.

## Memory & Context (handoff rules)
- The following hard rules are handoff gates and apply to every delivery.
- Do not store full chat transcripts or raw logs in the repo. Keep them local
  under `chatlogs/` and ensure it is listed in `.gitignore`.
- Preferred startup for full local transcript fallback:
  - `./tools/start.sh` (default `START_SESSION_LOG=1`)
  - optional controls:
    - `START_SESSION_LOG=0` disable transcript logging
    - `START_SESSION_LOG_FILE=/abs/path/session.log` set explicit log file path
- For anti-loss fallback, store concise session checkpoints in
  `reports/{RUN_ID}/conversation.md` via:
  - `tools/qf snapshot RUN_ID=<run-id> NOTE="decision/next-step summary"`
- `tools/qf do` / `tools/qf resume` 自动记录执行轨迹到
  `reports/{RUN_ID}/execution.jsonl`（默认脱敏，可审计）。
- 断线恢复建议先生成接班摘要：
  - `tools/qf handoff RUN_ID=<run-id>` -> `reports/{RUN_ID}/handoff.md`
- Repo memory is limited to: `docs/` (rules), `TASKS/STATE.md` (current state),
  `reports/{RUN_ID}/decision.md` (key decisions), and `MISTAKES/` (postmortems
  when enabled).
- When sharing code with an external model, use `project_all_files.txt` as the
  context snapshot. It is ignored by default and must only be updated via a
  dedicated task with explicit approval to commit.
- Hard rule (gate): Uncommitted changes do not exist for other agents or cloud runs.
- Hard rule (gate): Handoff must be via PR or commit hash, with evidence under
  `reports/{RUN_ID}/`.
- Hard rule (gate): If local-only context is needed, record it as structured evidence
  (`summary.md`, `decision.md`, `MISTAKES/`) or in `TASKS/STATE.md`, not in chat.
- `TASKS/STATE.md` is the source-of-truth for `CURRENT_RUN_ID`.

## Sync completion criteria (must be true before execution)
- `tools/qf init` completed successfully.
- `tools/qf handoff` completed for continuing runs (auto by init unless explicitly disabled).
- `tools/qf ready` produced `reports/{RUN_ID}/ready.json`.
- `tools/qf do queue-next` no longer fails on readiness gate.

## Codex session startup checklist
- Do not rely on chat/session memory; rely only on repo memory:
  `TASKS/STATE.md`, `TASKS/QUEUE.md`, `reports/{RUN_ID}/`.
- First read owner entrypoint: `SYNC/READ_ORDER.md`.
- Preferred entrypoint: `tools/qf` (`init/plan/do/resume`).
- Compatibility wrappers: `tools/enter.sh` and `tools/onboard.sh` forward to `tools/qf`.
- 1) 运行 `tools/qf init`（自动 stash 可恢复 + sync main + doctor + onboard）。
- 1.1) 可选清理历史临时 stash：先预览 `tools/qf stash-clean`，确认后执行 `tools/qf stash-clean apply KEEP=0`。
- 2) 若为接力会话（`CURRENT_RUN_ID` 已存在），`tools/qf init` 默认自动执行 `handoff`。
- 2.1) 如需手动控制，可用：`QF_INIT_AUTO_HANDOFF=0 tools/qf init` 后再手动 `tools/qf handoff`。
- 3) 按 `SYNC/READ_ORDER.md` 顺序完成阅读与复述。
- 3.1) 新/陌生 agent 建议先完成同频考试：
  - `/plan` 题面：`SYNC/EXAM_PLAN_PROMPT.md`
  - 按 `SYNC/EXAM_ANSWER_TEMPLATE.md` 输出到 `reports/{RUN_ID}/onboard_answer.md`
  - 用 `tools/sync_exam.py` 评分，结果写入 `reports/{RUN_ID}/sync_exam_result.json`
- 4) 运行 `tools/qf ready` 完成复述上岗门禁（默认绑定 `CURRENT_RUN_ID`，默认可自动填充）。
- 4.1) 在关键决策点执行 `tools/qf snapshot NOTE="..."`，把“本轮结论/下一步”写入仓库证据，避免会话丢失。
- 5) 运行 `tools/qf plan 20` 生成候选；该命令会复制 proposal 到 `/tmp`（并打印路径）且保持工作区干净。
- 6) 运行 `tools/qf do queue-next` 领取下一枪（内部确保 ready + plan 前置、自动 evidence）。
- 7) Expand that item into `TASKS/TASK-*.md` (from template), then run:
  implement minimal diff -> `make verify` -> update reports -> `tools/task.sh` ship.
- Ship failure recovery: `tools/ship.sh` writes `reports/{RUN_ID}/ship_state.json`
  at key steps. On push/PR/merge/sync failure, run `tools/qf resume RUN_ID=...`.
- Ship success behavior: after merge, ship auto-syncs local `main` to `origin/main`.
- 8) On failure, write failure reason, repro, and next step in
  `reports/{RUN_ID}/summary.md` + `reports/{RUN_ID}/decision.md` (and `MISTAKES/`
  or `TASKS/STATE.md` when needed).

## Pause/stop reason taxonomy (required in decision.md)
- Use one canonical stop reason when pausing/stopping a run:
  - `task_done`
  - `needs_human_decision`
  - `infra_network`
  - `infra_quota_or_auth`
  - `tool_or_script_error`
  - `verify_failed`
  - `external_blocked`

## Documentation freshness gate (hard rule)
- Process/rule/tooling behavior changed in this RUN => update owner docs in this RUN.
- Minimum documentation set for process changes:
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - `SYNC/*` startup docs if order/semantics changed
  - `TASKS/STATE.md` pointers if run/task context changed
  - `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`
- If documentation is stale, do not ship.

## Codex governance and automation
- Session constitution: `docs/CODEX_ONBOARDING_CONSTITUTION.md`
- Default policy: PR-driven flow with local `make verify`; do not depend on GitHub Actions queues.
- If automation is ever re-enabled, it must be explicitly requested and documented in task acceptance.
- `tools/ship.sh` hard gate blocks `.github/workflows/*.yml|*.yaml` by default; explicit override required:
  - `SHIP_ALLOW_WORKFLOWS=1 tools/ship.sh "<msg>"`
- `tools/ship.sh` appends process mistakes to `reports/{RUN_ID}/mistake_log.jsonl` on retries/failures.
- `tools/observe.sh` summarizes these logs under `过程错题（执行/思考）`.
- Process mistake template reference: `docs/MISTAKES_TEMPLATE.md`.
