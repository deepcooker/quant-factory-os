# Summary

RUN_ID: `run-2026-02-26-tools-qf-init-plan-do-git-sync-retry-resume`

## What changed
- 新增可执行脚本 `tools/qf`，实现四个子命令：
  - `init`：dirty 自动 stash（打印恢复指令）+ 强制 sync main + 执行 `tools/doctor.sh` 与 `tools/onboard.sh`。
  - `plan [N]`：强制 sync main，执行 `tools/task.sh --plan N`，复制 proposal 到 `/tmp/qf_todo_proposal.md`，`git restore TASKS/TODO_PROPOSAL.md`，并清理 `reports/run-*-pick-candidate/`，最后强制校验工作区干净。
  - `do queue-next`：强制 sync main，dirty 自动 stash，必要时自动 `plan 20`，随后 `tools/task.sh --pick queue-next` 并透传 `TASK_FILE/RUN_ID/EVIDENCE_PATH`。
  - `resume RUN_ID=...`：读取 `reports/{RUN_ID}/ship_state.json`，对 push/PR/merge/sync 进行重试恢复，失败打印单行恢复命令。
- 增强 `tools/ship.sh`：
  - 新增关键路径重试（`git push` / `gh pr create` / `gh pr merge` / post-ship sync）。
  - 新增阶段断点 `reports/{RUN_ID}/ship_state.json`（`branch/commit/pr_url/step/last_error/msg`）。
  - 失败统一输出 `tools/qf resume RUN_ID=...`。
  - 在“无变更可提交”及若干 guard 失败路径清理空分支，避免生成空分支残留。
- 更新 `docs/WORKFLOW.md`：对外入口收敛为 `tools/qf init/plan/do`，并补充 `resume` 失败恢复路径。
- 新增测试：
  - `tests/test_qf_plan_clean.py`（`qf plan` 不污染工作区 + 清理 pick-candidate）。
  - `tests/test_ship_retry_resume_state.py`（ship 的 retry/state/resume 关键标记）。

## Commands / Outputs
- `make verify`
  - `51 passed in 3.20s`
- Demo（临时 git repo，`QF_SKIP_SYNC=1`）：
  - `tools/qf init`：输出自动 stash、恢复指令、doctor/onboard 与下一步提示。
  - `tools/qf plan 20`：输出 `PROPOSAL_COPY: /tmp/qf_todo_proposal.md` 与 `CLEANED: reports/run-*-pick-candidate`。
  - `tools/qf do queue-next`：输出 `TASK_FILE` / `RUN_ID` / `EVIDENCE_PATH`。

## Notes
- 本次实现遵循任务 Scope：仅修改 `tools/`、`tests/`、`docs/WORKFLOW.md` 与 `reports/run-2026-02-26-tools-qf-init-plan-do-git-sync-retry-resume/`。
