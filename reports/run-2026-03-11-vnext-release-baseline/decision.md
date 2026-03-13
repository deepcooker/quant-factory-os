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

## Run-main escalation resolution decision
- 在 task 层继续补 `run-main` 收到升级后的最小闭环，但不把它扩成新的 orchestrator。
- `run_main_resolution` 只负责：
  - 是否已收到/确认升级
  - 是否满足关闭升级项的条件
  - 记录最小 closing note
- 它不替代：
  - `refresh-task-escalation` 的升级判断
  - `run summary` 的聚合
  - 多角色调度器
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

## Entity layering decision
- 当前 `reports/<RUN_ID>/summary.md` 和 `decision.md` 继续保留，不否定现有表达价值，但明确它们目前更接近 run 容器下的 task-focused evidence。
- `session_registry.current_summary` 明确定义为 thread-level transitional summary，只是当前最小闭环的输入槽位，不等同于最终 run summary。
- 长期推荐的聚合链路定为：
  - `thread summary -> task summary -> run summary -> baseline refresh`
- baseline 当前允许暂时消费 `current_summary`，但后续应优先消费 run-level stable summaries，必要时再吸收经过筛选的 task summaries。

## Task summary bootstrap decision
- `task summary` 先不拆成独立文件，直接落在 `TASKS/TASK-*.json` 内，作为 task 层机器真相源的一部分。
- 这样可以避免再引入一套平行路径，同时保持 `task json -> task md` 的双层表达稳定。
- 当前只补最小入口：
  - `taskclient --set-task-summary` 负责写回
  - `taskclient --task-summary` 负责读取
- run summary 和 baseline 消费链路这轮不动，避免一次性跨三层对象重构。

## Run summary bootstrap decision
- `run summary` 的机器真相源定在 `reports/<RUN_ID>/run_summary.json`，因为它天然属于 run evidence 命名空间，而不是全局 runtime 指针。
- `summary.md / decision.md` 继续保留为 run 级 md 视图，不因机器真相源引入而被否定或替换。
- 本轮只补 schema 与自动落盘，不急着引入新的 run 级 CLI 写回入口，避免在模型刚定型时继续扩工具面。

## Run summary writeback decision
- 最小 run summary 写回入口不单独新建 `runclient`，而是并入 `tools/evidence.py`，因为它天然已经负责 run evidence 目录。
- 这样可以把 run-level machine truth 的创建、读取、更新都收在同一命名空间下，避免为单一对象过早扩工具面。
- baseline 消费链保持不变；当前只把 run summary 的 machine truth 读写路径先稳定下来。

## Baseline input priority decision
- `refresh-baseline` 现在优先消费 `run_summary.json`，只有在 run summary 缺失或为空时才回退到 `current_summary`。
- 这样 baseline 优先吸收 run-level stable summary，而不是直接依赖 thread-level transitional summary。
- 当前仍保留 fallback，是为了兼容过渡期和 run summary 尚未生成的场景。

## Requirement-analysis learning decision
- 传统需求分析文档对本项目有价值，但不整份照搬到 AI 主线。
- 当前选择是：只迁移其中适合 AI/Codex 的需求收敛原则，优先增强 `PROJECT_GUIDE` 的高质量提问与自我学习能力，再把稳定规则沉淀到 `WORKFLOW` 和 `ENTITIES`。
- 不回迁旧 `orient/choose/council/arbiter` 为正式主流程；相关方法仅作为新主线下 `run 主线程 -> task` 的需求收敛规则。

## Requirement-analysis role decision
- 当前更明确的角色结构是：
  - `run-main` 负责需求收敛、task 拆分和最终确认
  - `dev` 负责实现与单元/最小集成自证
  - `test` 负责独立验证
  - `arch` 只在复杂 task 下按需启用
- 这样做的原因是先保证 AI 学习协议和协作边界稳定，而不是过早扩大量角色或恢复旧流程节点。

## Project guide probing decision
- 当前继续优先增强 `PROJECT_GUIDE` 的高质量提问能力，而不是先做新的自动提示词层或额外客户端。
- 追问模板只落在 Q9-Q12 这类最直接承接需求收敛的题目下，避免为了补模板而改动题库结构或稀释课程主线。

## Project guide self-structuring decision
- 当前继续把 `PROJECT_GUIDE` 往“AI 自我梳理客户材料”的方向推进，但仍停留在协议层，不急着做自动生成器。
- 选择把最小输出骨架挂在 Q9-Q12 下，是因为这几题正好承接 run 方向收敛、角色分工、对象分层和 task 创建前置条件。

## Project guide markdown draft decision
- 在现阶段先把“AI 读完客户材料后先产出什么”收成标准化 Markdown 草稿模板，而不是立刻做自动生成器或跨项目复制实验。
- `Markdown intake draft` 只定义为 run 级协议层草稿，用来整理客户材料和收敛需求边界；它不替代 `run summary`、`TASKS/*.json` 或其他机器真相源。
- 这样可以先验证学习协议是否足够稳定，再决定后续是否把该模板抽成独立提示模板或跨项目 bootstrap 资产。

## Project bootstrap protocol decision
- 面对还没接入基座的新项目，先补一份独立的 bootstrap 学习协议，而不是直接把当前仓的自动化主线强行复制过去。
- 通用 `PROJECT_GUIDE` 继续承担跨项目学习协议角色；项目化 owner docs 则通过 bootstrap 协议逐步补齐。
- 这样可以把“学习协议层”和“自动化实现层”分开，先验证 AI 是否真的能从陌生项目材料中自我学习、自我建模，再决定后续接入深度。

## Multi-thread collaboration minimum-chain decision
- 当前先不实现完整多 agent orchestration，而是先把最小可用协作链落到 task 机器层：`run-main -> dev/test -> thread summary -> task summary`。
- `test` 的独立性先通过 `test_gate` 固化为 task 内质量门，而不是继续停留在口头规则；`dev` 与其他角色线程通过 `role_threads` 留下最小绑定关系。
- app-server 侧真实 role thread 生命周期和自动 summary 聚合后续再接，不在这一刀里混入。

## Appserverclient fork-role decision
- 在 task 机器层具备 `role_threads` 之后，下一刀优先接真实 runtime，而不是先做更多文档或更多抽象层。
- `--fork-role` 被定义为最小 role binding 命令：它只负责从当前 run-main thread 派生真实 role thread，并回写当前 task；不承担 thread summary 自动聚合。
- 当前先验证 `test` 这类关键独立角色，后续再扩到 `dev` 的真实绑定和 role thread 上的 current-turn / summarize。

## Appserverclient role-turn decision
- 在 `--fork-role` 成功之后，优先补 `--role-turn`，让已绑定 role thread 能直接在真实 runtime 中执行 turn，而不是先设计 thread summary 自动回收。
- 这样可以先把多线程协作链打通到“真实线程可执行”，再继续往上补 `thread summary -> task summary` 聚合。
- 当前最小验证角色仍选择 `test`，因为它承担独立质量门，最能验证多角色协作的关键边界。

## Role thread summary decision
- 在 role thread 已可真实执行之后，下一刀直接补 `--summarize-role`，让单个 role thread 能先形成稳定的 role-level summary。
- 当前选择把 role summary 直接落在 task JSON 的 `role_summaries`，并只向 `task_summary` 追加 `source_threads` 与 `role_summary_evidence`，不在这一轮引入更重的自动聚合器。
- 这样可以先确认最小回收链真实可用，再讨论多角色 summary 的去重、优先级和 task-level merge 策略。

## Task role summary merge decision
- 在 role summary 已真实落盘之后，先补 `taskclient --merge-role-summaries` 作为最小 task-level 聚合入口。
- 当前只做去重追加，不做复杂语义 merge；这样可以先稳定 task 机器层，再讨论多角色冲突时的优先级与缺口合并。

## Task role summary conflict decision
- 在最小 merge 稳定后，继续把冲突优先级和缺口汇总显式写成 task 机器层字段，而不是继续依赖口头约定。
- 当前优先级顺序定为 `run-main -> test -> arch -> dev`；如果冲突仍然存在，后续应升级给 `run-main` 收敛。
- 当前 `refresh-task-gaps` 只做最小缺口刷新，不做更重的语义判决。

## Task escalation decision
- 在有了冲突优先级和缺口汇总后，继续把“是否必须升级给 run-main”收成 task 机器层规则，而不是靠人工记忆判断。
- 当前先收最小升级条件，不引入新的 orchestration 层；只有当 `run-main summary missing`、`test_gate` 未通过或仍有 blocking issue 时，才标记 `needs_run_main=true`。

## Run-main role runtime decision
- 继续沿 `appserverclient` 现有 role runtime 往前收，不为 `run-main` 新开客户端。
- `run-main` 现在和 `dev/test/arch` 一样，可以通过真实 `fork-role / role-turn / summarize-role` 路径参与 task 升级处理。
- `summarize-role run-main` 后自动刷新 task 层的 gap/escalation/resolution，说明 run-main 的真实线程已经进入正式主线，而不是只靠 task JSON 手工模拟。
- 当前先停在 `run-main` 已确认、`test_gate` 仍待通过的状态；下一步继续接 `test` 角色线程与真实 `test_gate` 联动，避免提前关闭升级项。

## Test gate runtime decision
- `test_gate` 的真实写回入口继续放在 `appserverclient`，命令为 `--mark-test-gate`。
- 这样 `test` 线程的真实 summary 证据可以直接进入 `test_gate.evidence`，并立刻联动刷新 `gap_summary / escalation_summary / run_main_resolution`。
- 在同一 task 中补齐 `run-main` 和 `test` 两条真实链后，升级项已自动收成 `needs_run_main=false`；说明“独立测试通过 + run-main 确认”这条关闭链已经可执行。
