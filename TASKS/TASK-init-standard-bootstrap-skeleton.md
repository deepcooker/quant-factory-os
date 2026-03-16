# TASK-init-standard-bootstrap-skeleton

## Goal
把 `init` 扩成最小标准协议骨架创建入口，确保新项目缺少 owner docs 与最小目录时也能先建协议壳。

## Scope
- `tools/init.py`
- `docs/WORKFLOW.md`
- `docs/FILE_INDEX.md`
- `TASKS/QUEUE.json`

## Acceptance
- init 自动创建最小标准协议骨架目录和文件
- docs 明确 init 的 bootstrap 范围

## Task Summary
- `init` 现在会自动创建最小标准协议骨架目录和文件。
- `tools/project_config.json` 缺失时会先由 `init` bootstrap 最小配置。
- `docs/TOOLS_METHOD_FLOW_MAP.md` 缺失时会创建为空文件，等待后续反写。
