# Decision

RUN_ID: `run-2026-03-11-vnext-release-baseline`

## Why
- 旧的 `TASKS/STATE.md` 已经与当前 run/task 设计冲突，继续保留会让 runtime 指针再次分叉。

## Options considered
- 保留 `TASKS/STATE.md` 作为镜像兼容层。
- 直接改为 `tools/project_config.json -> runtime_state` 唯一真相源，并先扶正 `run`。

## Chosen
- 先扶正 `run`，再逐步重做 `task`。
- `runtime_state` 成为唯一运行时真相源。
- 当前 formal mainline 文档和入口只围绕这一真相源更新。
- 本轮只修 formal mainline 和直接依赖真相源的 Python 工具，不顺手重写 `legacy.sh` / `task.sh` 等兼容链路。

## Risks / Rollback
- 风险：历史兼容脚本仍可能依赖 `TASKS/STATE.md`。
- 回滚：恢复 `project_config.py` 的镜像逻辑，并临时回补 `TASKS/STATE.md`。

## Next decision
- 对已被正式主线淘汰的 shell 入口采用“归档到 `tools/backup/` + 原路径保留 wrapper”的迁移策略，先降级而不一次性硬删除。

## Applied
- 已执行上述迁移策略。
- 这样可以让正式主线继续聚焦 `init / appserverclient / gitclient`，同时不给历史引用制造一次性硬断裂。

## Additional decision
- task/queue 的长期真相源切到 JSON，而不是继续让 Markdown 承担机器写回。
- 原因是 task/queue 需要结构化校验、稳定字段更新和后续 Python orchestrator 自动处理；`jsonl` 更适合事件流，不适合作为 task/queue 主格式。

## Task binding
- 本轮后续改动不再继续挂在 `task-compat-shell-archive` 下，已切到新的 `task-task-queue-json-bootstrap`。

## Taskstore decision
- 在真正改写更多调用方之前，先补一个最小 `tools/taskstore.py` 作为公共层。
- 这样后面 `appserverclient`、`gitclient`、未来 task picker 都可以在不直接碰散落 JSON 路径的前提下逐步迁移。

## Task binding
- 本轮后续改动已从 `task-taskstore-bootstrap` 切到新的 `task-gitclient-taskstore-integration`。

## Gitclient decision
- `gitclient` 先只接入 task JSON 的读取，不改 commit/PR 主流程。
- 这样可以先把“任务上下文来源”扶正，再逐步继续收更大的交付链。

## Appserverclient decision
- `appserverclient` 这一轮只补 active task JSON 感知和日志，不直接承担 task/queue 编排。
- 这样可以先让 runtime/session 主线与 taskstore 对齐，同时保持 app-server 协议调用面稳定。

## Taskclient decision
- 先用一个很薄的 Python picker 替掉 `task.sh` 里最关键的 queue 选择和 runtime 绑定能力。
- task 模板生成、ship、PR 等剩余职责后续再拆，不在这一刀里混进来。

## Task bootstrap decision
- 继续沿同一条线，把最小 task bootstrap 也收进 `taskclient`，但只保留结构化参数版，不复刻旧 shell 交互。
- 这样后面你我可以在 JSON schema 稳定后再一起优化体验层，而不是继续把自动化绑死在 Markdown 模板上。

## Schema decision
- 先把 task schema 和 create-task 参数收紧到一版稳定字段集，再继续做体验优化。
- 当前策略仍然是“约定式最小校验”，先追求稳定落盘和低歧义，不上完整 schema engine。

## UX decision
- 在 schema 稳住后，先做 create-task 的轻量体验优化，而不是回到 shell 交互。
- 方向是减少重复输入，同时保持参数仍然显式、可脚本化、可自动化。

## Wrapper decision
- 继续沿“wrapper 只做过渡，不做主线”的原则，把 `tools/task.sh` 最常用的主线路径直接改成转到 `taskclient`。
- 这样可以逐步清空旧 shell 入口的主线职责，同时保留其余遗留参数的兼容逃生口。

## Task entry decision
- 不再把 `taskstore` 维持成独立用户入口，公共读写方法直接合入 `tools/taskclient.py`，把 task 的正式入口收成一个。
- `tools/taskstore.py` 只保留兼容转发价值，历史实现移到 `tools/backup/taskstore.py`；正式文档和主流程不再把它当主线工具。

## Shell deprecation decision
- `tools/task.sh` 不再继续承担任何主线职责，也不再回退执行 `tools/backup/task.sh`。
- 后续 shell 文件只按历史参考或安装/bootstrap 资产处理，不再作为“等待迁移”的正式设计对象。

## Legacy entrypoint archive decision
- 不再把旧 `learn/ready/orient/choose/council/arbiter/slice_task/run_main` 或顶层 `legacy/observe/ship/task` 视为仍在正式 `tools/` 层占位的兼容入口。
- 本轮直接把这些文件移入 `tools/backup/`，正式主流程只保留 `init / appserverclient / gitclient / taskclient / project_config`。
- 这样后续讨论主流程时不会再被历史入口干扰，也避免继续围绕它们做二次重构。

## Appserverclient summarize / refresh decision
- 不做假 summary 或本地拼接基线快照，而是继续沿真实 `codex app-server` session 生命周期补闭环。
- `--summarize-current` 必须直接在 current fork thread 上生成去噪结论，并把结果写入 `session_registry.current_summary`。
- `--refresh-baseline` 必须只消费 `session_registry.current_summary`，而不是重新扫描全部 run 聊天历史。
- 这样 formal mainline 现在明确收成：
  - `--learnbaseline`
  - `--fork-current`
  - `--current-turn`
  - `--summarize-current`
  - `--refresh-baseline`
