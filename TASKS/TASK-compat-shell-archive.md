# TASK: compatibility shell archive

RUN_ID: run-2026-03-11-vnext-release-baseline
TASK_ID: task-compat-shell-archive
PROJECT_ID: quant-factory-os
STATUS: done
PRIORITY: P1

## Goal
把已被正式主线淘汰的 shell 兼容脚本归档到 `tools/backup/`，并在原路径保留最小兼容壳层，避免当前仓库引用立即断裂。

## Scope
- `tools/backup/`
- `tools/legacy.sh`
- `tools/task.sh`
- `tools/observe.sh`
- `tools/ship.sh`
- `tools/project_config.json`
- `docs/`
- `AGENTS.md`
- `reports/run-2026-03-11-vnext-release-baseline/`

## Non-goals
- 不重写这些兼容脚本的内部逻辑。
- 不在本任务里删除所有历史引用。
- 不扩 `appserverclient` 或 `gitclient` 新能力。

## Acceptance
- [x] `tools/backup/` 收纳 `legacy.sh` / `task.sh` / `observe.sh` / `ship.sh`
- [x] 原路径只保留兼容壳层并可转发到 `tools/backup/`
- [x] formal mainline 文档说明这些 shell 脚本已降级为归档兼容资产
- [x] Command(s) pass: `bash tools/legacy.sh --help || true`
- [x] Command(s) pass: `python3 tools/project_config.py`
- [x] Evidence updated: `reports/{RUN_ID}/summary.md` and `reports/{RUN_ID}/decision.md`

## Inputs
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `docs/PROJECT_GUIDE.md`
- `TOOLS_METHOD_FLOW_MAP.md`
- `tools/project_config.json`
- `reports/run-2026-03-11-vnext-release-baseline/summary.md`
- `reports/run-2026-03-11-vnext-release-baseline/decision.md`

## Risks / Rollback
- Risks: 仍有历史脚本/文档直接假定这些文件包含完整实现。
- Rollback plan: 把 `tools/backup/` 中的脚本移回原路径，并撤销 wrapper/documentation 变更。
