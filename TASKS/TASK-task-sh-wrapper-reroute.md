# TASK: task sh wrapper reroute

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-task-sh-wrapper-reroute
PROJECT_ID: quant-factory-os
STATUS: done
PRIORITY: P1

## Goal
把原 `tools/task.sh` wrapper 的最常用主线路径直接改为转到 Python-first 的 `taskclient`，进一步减少旧 shell task 入口继续充当正式主线。

## Scope
- `tools/task.sh`
- `tools/project_config.json`
- `AGENTS.md`
- `docs/FILE_INDEX.md`
- `docs/WORKFLOW.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写 `tools/backup/task.sh`。
- 不动旧 ship 链。
- 不删除所有历史对 `tools/task.sh` 的引用。

## Acceptance
- [x] `tools/task.sh --next` 直接转到 `python3 tools/taskclient.py --pick-next`
- [x] `tools/task.sh --pick queue-next` 直接转到 `python3 tools/taskclient.py --pick-next`
- [x] 其他旧参数仍回退到 `tools/backup/task.sh`
- [x] `tools/project_config.json` 的 active task 指针与当前 runtime task 一致
- [x] Command(s) pass: `bash tools/task.sh --next`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `tools/task.sh`
- `tools/taskclient.py`
- `tools/backup/task.sh`

## Risks / Rollback
- Risks: 少量遗留流程可能仍假设 `tools/task.sh --next` 会输出旧 shell 文案。
- Rollback plan: 恢复当前 wrapper 仅做 deprecation + 直通 backup 的行为。
