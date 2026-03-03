# Decision

RUN_ID: `run-2026-03-02-qf-ready`

## Why
- Continue the user-selected path (`1`) by resuming the main `qf-ready` run and validating the full multi-role planning workflow before any new execution.

## Options considered
- Option A: resume with `tools/qf resume` directly.
  - Rejected because the run lacks `ship_state.json`; this path is not valid for this run state.
- Option B: re-enter via `tools/qf ready`, then run `choose/council/arbiter/slice/review`.
  - Chosen for deterministic gate checks and complete evidence refresh.

## Risks / Rollback
- Risk: stale `STATE` task pointer could cause audit drift and misleading review references.
- Mitigation: corrected `TASKS/STATE.md` to `CURRENT_TASK_FILE: TASKS/TASK-qf-ready.md` and reran strict review.
- Risk: no pending queue tasks may appear as "stuck".
- Mitigation: confirmed this is an expected boundary; next step is orientation choice for new direction.
- Rollback: revert `TASKS/STATE.md` and refreshed report artifacts for this run.

## Stop Reason
- task_done

## Iteration Decision: output mode optimization
- Chosen:
  - implement deterministic stage prints directly in `tools/qf` (`INIT_STEP` / `READY_STEP`) so users can see progress in Codex CLI without relying on model transcript behavior.
  - add optional machine-readable stdout stream (`QF_EVENT_STREAM=1`) to support downstream automation/parsing.
- Rejected:
  - relying on Codex-only display mode as the single solution, because it cannot guarantee this repo tool's semantic step boundaries.
  - keeping init's hidden cleanup in startup path, because it introduces implicit side effects and reduces product predictability.

## Iteration Decision: discussion/execution split with low friction
- Chosen:
  - add `tools/qf discuss` as a first-class shortcut for "讨论完成但不立刻执行 do" workflow.
  - keep `tools/qf execute` as full orchestrator, but add `EXECUTE_STEP` markers to improve runtime observability.
  - make ready validation stable by using persisted `ready.json.sync_gate.required` first, reducing env-dependent drift.
- Rejected:
  - forcing execute default to `prepare` globally in this iteration, to avoid broad behavior changes for existing callers.
  - adding another standalone state file for discuss phase; current artifacts (`council/execution_contract/slice_state`) are already sufficient as gate evidence.

## Iteration Decision: introduce `learn` as explicit onboarding gate
- Chosen:
  - add `tools/qf learn` as dedicated onboarding-learning gate (project + constitution + workflow + skills + session + exam evidence).
  - keep `ready` as aggregation gate and enforce learn first (`QF_READY_REQUIRE_LEARN=auto`, `QF_READY_AUTO_LEARN=1`).
  - keep full console visibility by adding deterministic `LEARN_STEP` and updating `READY_STEP` to 12-step flow.
  - update sync hint chain to `learn -> ready -> execute`, reducing ambiguity before execution.
- Rejected:
  - keeping learn/exam logic buried inside `ready` without standalone artifacts, because it weakens auditability and re-learn reusability.
  - including volatile `TASKS/STATE.md` in learn digest, because state timestamp churn caused false stale-digest failures.

## Iteration Decision: `init` does environment only, not run ownership
- Chosen:
  - enforce boundary that init does not create business RUN_ID.
  - when no CURRENT_RUN_ID, init runs in session-context-only mode and skips run-scoped execution event writes.
  - keep run ownership at `learn/ready` (or pre-existing CURRENT_RUN_ID), matching task-batch semantics.
- Rejected:
  - continuing synthetic `run-*-qf-init` generation, because it pollutes run evidence and blurs run vs environment boundaries.

## Iteration Decision: `tools/qf learn -log`
- Chosen:
  - add `-log` flag to mirror learn stdout into a file while preserving live terminal output.
  - default log target: `reports/session/learn.stdout.log`; override via `LOG=<path>`.
- Rejected:
  - forcing all learn runs to always log (would create noisy artifacts by default).

## Iteration Decision: learn gate should not be RUN_ID-owned
- Chosen:
  - move learn gate artifacts to session scope (`reports/session/*`) and make `ready` depend on session learn gate.
  - keep optional `RUN_ID` for `learn` only as context source (sync/exam), not as learn evidence namespace.
- Rejected:
  - keeping learn files under `reports/<RUN_ID>/` because it falsely couples onboarding memory to per-run execution state.

## Iteration Decision: decouple learn from implicit latest-run binding
- Chosen:
  - `tools/qf learn` resolves run context from explicit `RUN_ID` or `TASKS/STATE.md` only.
  - if no run context exists, learn still passes via `session-direct-read` (direct required-doc reads) and writes session evidence.
  - no implicit fallback to historical latest run; avoid stale run contamination of onboarding.
- Rejected:
  - forcing hard run requirement in learn, because onboarding capability is session-level and should not be blocked by task/run ownership.
  - silently attaching learn to "latest reports run", because this can mis-route context in resumed/rebased repositories.

## Iteration Decision: introduce `project_id` namespace before orchestration upgrade
- Chosen:
  - add `project_id` baseline (`CURRENT_PROJECT_ID`, default `project-0`) without breaking existing `RUN_ID` flow.
  - migrate learn artifacts to `reports/projects/<project_id>/session/*` while keeping legacy read compatibility.
  - inject `project_id` into sync/ready/orient/choose/council/arbiter/slice artifacts for downstream execute orchestration.
  - keep directory migration for run evidence deferred (still `reports/<RUN_ID>/...`) to minimize risk in this slice.
- Rejected:
  - immediate full physical migration of all run evidence under `reports/projects/<project_id>/runs/...` in one step (too disruptive for current baseline).
  - dropping legacy `reports/session/learn.json` read path immediately (would break existing evidence continuity).

## Iteration Decision: keep full automation chain but add execution contract confirm gate
- Chosen:
  - keep `execute` as the single orchestrator entry and preserve full chain (`orient->choose->council->arbiter->slice->do`).
  - add a mandatory confirmation checkpoint before `TARGET=do` via `execution_contract_confirm.json`.
  - support both manual and automatic confirmation:
    - manual: `CONFIRM_CONTRACT=1`
    - auto: `QF_EXECUTE_AUTO_CONFIRM_CONTRACT=1`
  - preserve discussion-first ergonomics:
    - `TARGET=prepare` remains non-executing and does not force confirmation.
- Rejected:
  - always auto-confirm by default (would remove explicit final checkpoint and reduce governance control).
  - introducing a separate new command instead of evolving `execute` (would fragment operator UX).

## Iteration Decision: hard cleanup for baseline signal-to-noise
- Chosen:
  - apply hard deletion for stale/historical reports and task contracts to keep baseline workspace minimal and readable during init/learn/ready optimization.
  - keep current run evidence and current task contract as single active source of truth.
  - keep test source files; delete only generated caches/checkpoints.
- Rejected:
  - soft-archive approach in this iteration (still leaves navigation and review noise).
  - deleting test source files (would reduce regression guardrails for upcoming workflow refactor).

## Iteration Decision: learn 强同频必须“真实模型交互 + 可见锚点 + 严格门禁”
- Chosen:
  - 在 `tools/qf learn` 增加真实 Codex 模型交互链路，并保存 prompt/raw/json/events/stderr 全部证据。
  - 默认 `MODEL_SYNC=auto`，在 `MODEL_SYNC=1` 下强制失败即阻断 learn。
  - 强模式要求输出 `plan_protocol + oral_restate + oral_exam`，并在控制台打印 `LEARN_MODEL_PLAN_*` 与 `LEARN_MODEL_ORAL_*`。
  - 对 `codex exec` 非零退出（如 rollout recorder 关闭异常）采用“结果文件+schema校验”判定，而非仅看退出码。
- Rejected:
  - 仅依赖本地脚本拼接 learn 内容（不可证明模型同频）。
  - 仅依赖退出码判定模型同步是否成功（在当前环境下会误判）。

## Iteration Decision: 同频考试升级为 15+2 深度问卷（v2）
- Chosen:
  - 用你的 15+2 问卷替换旧考试模板与评分规则。
  - 要求每题包含证据路径；推理问题必须写依据。
  - `pass_score` 提升为 85，强化上岗门槛。
- Rejected:
  - 保留旧“8段模板”并只做局部修补（覆盖不足）。

## Iteration Decision: 旧答卷自动迁移
- Chosen:
  - `exam-auto` 在自动模式下检测旧格式答卷并自动重填，避免 learn 自动流程被历史文件卡住。
- Rejected:
  - 强制人工先删除旧答卷再重跑（体验差，自动化不足）。

## Iteration Decision: Codex 操作手册入库并纳入必读链
- Chosen:
  - 新增 `docs/CODEX_CLI_OPERATION.md`，统一讨论/执行模式与参数语义。
  - 将该文件纳入 sync/learn 必读链与文档 owner map。
- Rejected:
  - 把 Codex 参数经验分散在聊天或临时报告中（不可持续复用）。

## Stop Reason
- task_done
