# Decision

RUN_ID: `run-2026-03-11-vnext-release-baseline`

## a9quant-strategy init completion decision
- `/root/a9quant-strategy` 现在已经正式完成首轮初始化。
- 这意味着它不再卡在 `--init-project` 门禁上，可以进入下一阶段：
  - 最小 tools 下沉
  - `learn-baseline`
  - 真实项目主线逐步调试
- 这一步刻意只做初始化完成，不混入工具迁移，避免把“状态切换”和“能力迁移”混成一个动作。

## a9quant-strategy owner docs rewrite decision
- `/root/a9quant-strategy` 的 owner docs 现已按完成后的 init-project 理解重写，不再使用之前那版偏摘要化的草稿内容。
- 当前最合理的顺序继续保持不变：
  1. 先 owner docs
  2. 再 complete-init
  3. 再迁最小 tools
  4. 再一步步调试真实项目主线
- 这一步刻意没有自动执行 `--complete-init-project`，因为 owner docs 既然刚刚重写，应该先给 owner 一个确认窗口。
- 一旦 owner 确认文档方向没问题，下一步就应该不是再改文档，而是：
  - `--complete-init-project`
  - 然后开始最小 tools 下沉和真实项目调试

## a9quant-strategy foundation-parity decision
- `/root/a9quant-strategy` 的 init-project 17 问理解现在已经闭合。
- 通过“与 foundation 项目一致”的 owner 决策，原本剩余的：
  - `Q7`
  - `Q8`
  - `Q12`
  - `Q14`
 现在也可稳定回答。
- 当前状态因此变成：
  - `answered_questions = [Q1..Q17]`
  - `unclear_questions = []`
  - `must_read_next = []`
- 但我仍然保持 `ready_for_doc_write=false`，因为你前面明确要求初始化阶段和文档反写阶段分开，且要由 owner 明确确认是否进入下一步。
- 所以下一步不是继续 update-init-project，也不是继续读代码，而是由你明确一句：
  - 是否进入 owner docs 反写阶段。

## a9quant-strategy owner-rules decision
- `/root/a9quant-strategy` 的初始化理解现在已经从“技术证据补读”进入“owner 规则收口”阶段。
- 在 owner 给出项目阶段划分、基座/项目职责、协作主线和 gitclient 交付口径之后，当前可以稳定回答：
  - `Q1`
  - `Q2`
  - `Q3`
  - `Q4`
  - `Q5`
  - `Q6`
  - `Q9`
  - `Q10`
  - `Q11`
  - `Q13`
  - `Q15`
  - `Q16`
  - `Q17`
- 当前仍不能结束初始化，因为还缺 4 个 owner 规则面：
  - `Q7` 当前任务/批次真相源如何定义
  - `Q8` session 审计材料如何保留
  - `Q12` 准备完成后从哪一步进入需求讨论
  - `Q14` 任务完成后的固定收尾动作是否比基座默认流程更细
- 所以下一步不该写 docs，也不该 complete init；只需要继续补这 4 个 owner 规则即可。

## a9quant-strategy final technical update decision
- `/root/a9quant-strategy` 的初始化理解现在已经基本走完“代码与配置证据补读”阶段。
- 在最后一批配置与 replay 证据补齐之后，当前可以稳定上提到 `answered_questions` 的题目是：
  - `Q1`
  - `Q2`
  - `Q3`
  - `Q5`
  - `Q6`
  - `Q10`
  - `Q11`
  - `Q15`
- `must_read_next` 已经清空，这表示后续不再优先扫代码；剩余缺口主要来自 owner 规则：
  - AI 协作边界
  - 需求讨论流程
  - 分支/交付规则
  - 任务完成收尾动作
  - 当前主线优先级确认
- 因此下一步正确动作不是继续读实现文件，也不是 `--complete-init-project`，而是让 owner 直接补这些规则，再继续同一个 `init_project_session` 更新。

## a9quant-strategy second update decision
- `/root/a9quant-strategy` 的初始化理解已经从“宪法/工作流/对象”扩展到“整体定位、阶段、终局与一期承接、实施流程”这一层。
- 在第二批实现文件补读之后，当前可以稳定上提到 `answered_questions` 的题目是：
  - `Q1`
  - `Q2`
  - `Q3`
  - `Q5`
  - `Q6`
  - `Q10`
  - `Q11`
- 这里仍然刻意没有把 `Q4/Q7-Q9/Q12-Q17` 一起提上去，因为这些题还缺 owner 规则、配置卫生或 replay 证据，不应为了推进速度而过度推断。
- 当前最正确的下一步不是 `--complete-init-project`，而是继续最后一批补读：
  - `config.json`
  - `replay_runner.py`
- 在这之前，目标项目的 owner docs 继续保持不变；只允许推进 `/root/a9quant-strategy/tools/project_config.json` 中的 `init_project_session`。

## a9quant-strategy first update decision
- `/root/a9quant-strategy` 的初始化理解现在不再停留在纯 intake 状态。
- 在第一批实现文件补读之后，当前可以稳定上提到 `answered_questions` 的题目是：
  - `Q5`
  - `Q6`
  - `Q11`
- 这里故意没有把 `Q1/Q2/Q3` 一起提上去，因为这些题还需要第二批主控、状态、契约和测试证据才能压实，不应为了推进速度而过度推断。
- 当前最正确的下一步不是 `--complete-init-project`，而是继续第二批补读：
  - `main_controller.py`
  - `data_synchronizer.py`
  - `account_state.py`
  - `contracts.py`
  - `test_integration.py`
  - `test_regression.py`
- 只要第二批证据补齐，就可以继续同一 `init_project_session` 再产出下一版 `--update-init-project` payload。

## Real a9quant-strategy init-project decision
- 真实 `/root/a9quant-strategy` 现在应按 session-first 初始化流继续，而不是再回到 phase2 writer 或本地 heuristic 方案。
- 本轮已经确认：
  - 目标项目可被重置为未初始化状态
  - `--init-project -new --instruction-text ...` 能把 owner 的一句高质量阅读顺序指令写进目标项目自己的 `init_project_session`
  - Phase 1 会 fail-closed 返回 `err_code=1012`，要求继续同一 init session，而不是假装初始化已经完成
- 因此下一步正确动作不是 `--learnbaseline`，而是：
  - 进入 `/root/a9quant-strategy` 的 `init_project_session`
  - 先按 `must_read_next` 补读关键实现
  - 然后产出一个 `--update-init-project --payload-json <path>` 的更新载荷
  - 只有当 `ready_for_doc_write=true` 且 owner 确认后，才允许执行 `--complete-init-project`
- 额外决策：
  - foundation 仓的 `required.project_root` 不得长期指向外部项目；每次真实外部初始化运行结束后，都必须切回 `/root/quant-factory-os`
  - `tools/init.py` 目前仍会在外部项目预检时混入 foundation bootstrap_state 元数据；这不是本轮阻塞项，但后续应收口

## Init-project real-material-derived validation decision
- `--init-project` 的 question-level reasoning 已在 richer in-repo fixture 上得到验证，不再只依赖 tiny toy fixture。
- 当前可稳定首轮答出的题目是：
  - `Q1`
  - `Q2`
  - `Q5`
  - `Q6`
  - `Q11`
- 继续保持 fail-closed 是刻意设计：
  - 即使这 5 题已稳定，Phase 1 仍返回非零 `err_code`
  - 只有在后续补读完成、`ready_for_doc_write=true` 后才允许继续到写入阶段
- 下一步不应再盲目堆 heuristic，而应优先降低 `readme_refs_missing_in_repo` 对 README 命令路径的误报。
- 这条误报现在已被处理：README 中的命令示例路径不再被当成仓库缺失文件引用。

## Init-project Q3 decision
- `Q3` 现在进入可稳定首轮回答集合。
- 触发条件被刻意收窄为两类显式原始文档证据同时存在：
  - 终局系统能力 / 三账本治理
  - 第一期落地目标 / 趋势+鲨鱼策略
- 这保证 `Q3` 不是靠泛化阶段猜测得出，而是靠明确文档表达得出。

## Init-project phase1 schema decision
- 不再把“owner docs 全为空”当成 `--init-project` 的通用项目硬门禁。
- `--init-project` 现在正式按“17 问完成度 + xhigh plan + 同一 init session 可续跑 + 人工确认后再写”建模。
- Phase 1 的正式对外输出收成：
  - `answered_questions`
  - `unclear_questions`
  - `customer_followups`
  - `document_priority_understanding`
  - `current_project_understanding`
  - `ready_for_doc_write`
- `ready_for_doc_write` 只表示可继续走向写入，不表示立即自动写。
- Phase 1 运行时也同步切到同一语义：
  - 未 ready 时返回 `err_code!=0`
  - 但把 Phase 1 payload 一起带回，供同一 `init_project_session` 继续补料和纠偏
  - 仍然保留 `bootstrap_state.is_inited` 作为 baseline 主线硬门禁
- 已用仓库内未初始化 fixture 做过一次真实验证；因此这条决策不再只是协议层约定，而是有实际 phase1 返回结果支撑。

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

## View tool decision
- 保留 `tools/view.sh` 作为正式长文件读取入口，不再引入第二个正式 `view.py` 入口。
- 实现改成 Python，以同时支持直接执行和 `python3 tools/view.sh ...`，从而消除历史误调用导致的 `SyntaxError`。
- 回归测试使用标准库 `unittest`，避免正式阅读工具依赖外部 `pytest` 安装。

## View usage docs decision
- 将 `tools/view.sh` 的正式调用方式最小同步到 `WORKFLOW`、`PROJECT_GUIDE` 和 `README`。
- 不改 `PROJECT_GUIDE` 题库结构，只补阅读协议说明和最小示例。

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

## Run summary risk near-duplicate merge decision
- `cross_task_risks` 的近义 blocked-gate 风险句不再并列堆叠；如果同时存在通用 blocked-gate 句与更具体的 blocked-gate 解释句，则优先保留更具体那条。
- 这条规则只作用于 run-level 风险表达，不挪动 `verification_overview` 的证据粒度，也不引入模型改写。
- 当前先把这类“通用句被更具体句覆盖”的最小策略写死，后续再决定哪些其他风险近义族值得按同样模式归并。

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

## Short stable mainline regression decision
- 当前最短稳定主线维持不变，继续作为默认推荐路径。
- `fork-current` 在当前会话环境里的失败被判定为沙箱访问 `/root/.codex/sessions` 的权限差异，不是 repo 主线逻辑失败。
- 本轮 stop reason 记为 `task_done`；后续处理方向不是改 formal mainline，而是在需要真实 session 文件访问的环境里继续执行或显式提权。

## Codex Full Access runtime prerequisite decision
- 对 Codex TUI 内的真实 session/runtime 调试，当前选择补充运行前提说明，而不是改 formal mainline。
- 在 `Default` 权限模式下，workspace 外的 `/root/.codex/sessions` 可能被外层权限边界拦住；切到 `/permissions -> Full Access` 后，`fork-current / summarize-current / refresh-baseline` 已真实通过。
- 因此这类失败应判定为外层会话权限问题，不应继续误判为 repo 主线逻辑问题。

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

## Dev role runtime merge decision
- `dev` 角色线程继续沿 `appserverclient` 的真实 runtime 路径推进，不单独开新客户端，也不把这一步并进 run-main/test gate 任务。
- `summarize-role dev` 现在会直接触发 `merge_role_summaries_into_task_summary`，再刷新 `gap_summary / escalation_summary / run_main_resolution`；这让 `dev` 真实执行结果能自动沉淀到 task 机器层。
- 当前把 `task-dev-role-runtime-merge-link` 收为完成，意味着多角色协作链已经具备 `dev`、`test`、`run-main` 三条真实 runtime 验证路径；下一步应在此基础上继续收多角色协同而不是再回头补单角色底座。

## Integrated multi-role runtime chain decision
- 当前把 `dev/test/run-main` 三条真实 runtime 线程首次收进同一个 task，并把结果定格成“可解释的 blocked 状态”，而不是强行追求一次性收成 `passed`。
- `test_gate=blocked`、`run_main_resolution=acknowledged`、`role_summary_evidence/source_threads` 三角色并存，证明当前系统已经能表达“多角色已收敛，但仍未放行”的真实主线状态。
- 这比只验证单角色成功更接近正式协作主线；下一步应该基于这个 integrated chain 往更高层聚合推进，而不是再回去重做单线程/单角色 plumbing。

## Run summary reconciliation decision
- `run_summary.json` 的 `active_tasks/completed_tasks/source_tasks` 不再继续靠历史写入结果维持，而是增加 `tools/evidence.py --reconcile-run-summary`，按同一 run 下的 task JSON 真相源重算。
- 这一步的目标是减少 run 层手工漂移，不是掩盖历史遗留 truth；因此如果 task JSON 本身仍残留多个 `active` 项，run summary 应如实暴露，并把清理责任留给后续 task truth cleanup。

## Stale active task cleanup decision
- 在 `reconcile-run-summary` 暴露出历史遗留 `active` task 后，本轮继续直接清理 task JSON 真相源，而不是在 run summary 层做额外隐藏规则。
- 当前选择只关闭明显属于样例验证或被后续完成任务覆盖的条目，避免扩大为历史内容重写；这样 `run_summary.json` 才能自然收敛到 `active_tasks=[]` 和 `status=completed`。

## Run summary baseline refresh boundary decision
- `refresh-baseline` 的输入边界不再停留在“代码里隐式 if/else + prompt 里旧口径”，而是显式记录本次 baseline refresh 实际消费的是 `run_summary` 还是 `current_summary`。
- 当前仍保持最小实现：优先消费 `run_summary`，缺失时回退 `current_summary`；下一步优化不再是继续扩 fallback，而是提升 `run_summary` 本身的语义压缩质量。

## Run summary semantic compaction decision
- `run_summary` 继续保留宽表 machine truth，但 baseline refresh 不再直接吃整份宽表，而是新增 `baseline_ready_summary` 作为压缩视图。
- 当前 compaction 保持规则化最小实现：只提取 `run_goal/status/key_updates/decisions/risks/next_steps` 的小集合；这一步先解决 baseline 输入过宽问题，不引入新的 run client 或模型内聚合器。

## Baseline-ready summary quality decision
- 在 `baseline_ready_summary` 已存在后，下一步不是继续扩字段，而是提升表达质量，让 baseline 吃到的更像 run-level prose。
- 当前选择最小规则化改进：对常见 `task-...:` 前缀和工具路径语句做规范化，不引入新的 summarizer client，也不让 evidence.py 直接承担模型级改写责任。

## Task summary to run summary decision
- run-level 聚合继续收口在 `tools/evidence.py`，并通过 `--merge-task-summary` 直接提升稳定 task summary，不新增独立 run client。
- 当前聚合策略只做最小 append-dedup：把 task 的稳定 `key_updates / decisions / risks / verification / next_steps` 提升到 run 层，并维护 `source_tasks/completed_tasks`。
- 这一步让 run summary 首次开始真正消费 task summary，而不是只靠手工写回；下一步可以在此基础上再讨论更强的 run-level 归并与基线消费。

## Task-to-run merge rule decision
- 当前不再把 `task summary -> run summary` 的所有字段统一按 `task_id: ...` 前缀直接 append，而是显式分成三类：
  - `reconcile_only`
  - `append_dedup`
  - `merge_rewrite`
- 具体规则定为：
  - `active_tasks` / `completed_tasks` -> `reconcile_only`
  - `source_tasks` / `verification_overview` -> `append_dedup`
  - `key_updates` / `cross_task_decisions` / `cross_task_risks` / `next_run_or_next_tasks` -> `merge_rewrite`
- 当前 `merge_rewrite` 仍然只做规则化轻改写，不引入模型推理；这样先把 run-level 归并责任从 `baseline_ready_summary` 前移回 `run_summary.json` 本身。
- 当前已知风险是历史 run summary 中已有的 task 前缀条目不会自动清洗；只有后续 task 重新走 `merge_policy` 聚合时，新增项才会逐步进入更干净的 run-level 表达。

## Legacy prefix cleanup decision
- 对已经写入 `run_summary.json` 的历史 task 前缀语义项，不在普通 `merge-task-summary` 或 `reconcile-run-summary` 流程中自动重写。
- 当前改为显式维护动作：
  - `python3 tools/evidence.py --run-id <RUN_ID> --normalize-run-summary`
- 该动作只处理 run-level 语义字段，不处理证据粒度字段；也就是说：
  - 会清理 `key_updates / cross_task_decisions / cross_task_risks / next_run_or_next_tasks`
  - 不会重写 `verification_overview / source_tasks`
- 这样做的原因是：历史语义清理应可追踪、可控制，不应在正常聚合路径里静默改变已经落盘的证据表达。

## Run summary merge quality decision
- `merge_rewrite` 不再只做“去前缀 + humanize”，而是允许少量高频模式在进入 run-level 字段时直接归并成更稳定的 run-level 表达。
- 当前只收了高复用、低歧义的模式：
  - 多个 `<role> summary merged`
  - `test gate=blocked/passed`
  - `all three real summaries are preserved ...`
- 这样做的原因是：这些模式本来就属于 run-level 结构化结论，不应一直等到 `baseline_ready_summary` 才做最后一层修辞压缩。
- 当前仍然刻意不扩大到模型推理或通用文本改写，避免把 run truth 层重新做成不可控的黑箱 summarizer。

## Run summary risk merge quality decision
- `cross_task_risks` 继续沿同一条规则化路线推进，只收高频、低歧义的 blocked-gate 风险模式。
- 当前先把 `test gate=blocked` 统一改写为 `test gate remains blocked`，以避免 run-level 风险字段继续保留实现型等号表达。
- 当前仍然不扩大到通用风险改写；如果后续出现更多重复模式，再逐步加稳定规则，而不是一次性做宽泛 NLP 清洗。

## Appserverclient task-rule boundary tightening decision
- 当前先不做新的 role/agent 配置系统，而是继续收紧四个主工具边界。
- `appserverclient` 不再显式了解 task 层的四步刷新链；task 协调刷新改由 `taskclient.refresh_task_coordination()` 统一承接。
- 这样 runtime 只负责真实线程生命周期和必要写回，task policy 继续优先归属 `taskclient`。
- 当前这一步仍保持最小实现：
  - 不改 role runtime 协议
  - 不引入新客户端
  - 不改变 formal mainline 命令面

## Appserverclient task-policy boundary tightening pass 2 decision
- 第二刀继续沿同一方向推进，但只处理 `summarize-role` 里的直接 task aggregate 写回。
- `appserverclient` 不再直接写 `task_summary.role_summary_evidence/source_threads`；该联动改由 `taskclient.update_role_summary_with_task_links()` 统一承接。
- 这样 role summary 到 task aggregate 的写回路径也回到 task truth 层，runtime 进一步收窄到“真实线程 + 必要调用”。
- 当前仍然保持最小实现：
  - 不改 role runtime 协议
  - 不新增 agent 配置系统
  - 不改变 formal mainline 命令面

## Appserverclient task-policy boundary tightening pass 3 decision
- 第三刀继续沿同一方向推进，但只处理 `mark-test-gate` 里的 test 证据拼接。
- `appserverclient` 不再直接读取 `role_summaries.test` 去拼 `test-summary-turn/test-thread` 证据；该逻辑改由 `taskclient.update_test_gate_from_test_summary()` 统一承接。
- 这样 `mark-test-gate` 也进一步收窄到“传状态和补充说明”，runtime 继续远离 task policy 细节。
- 当前仍然保持最小实现：
  - 不改 test gate 语义
  - 不引入新配置层
  - 不改变 formal mainline 命令面

## Appserverclient task-policy touchpoint audit decision
- 当前暂停第四刀最小解耦。
- 审计后剩余 touchpoints 主要已是 runtime 必需：
  - active task 定位
  - role thread 绑定读写
  - task-side helper 调用
- 如果继续为“更纯”而拆，会让主流程更长、更绕、更难定位问题，收益已经低于复杂度成本。
- 后续只在再次发现明显 task policy 泄漏时，再做新的最小下沉；当前阶段先保持这条边界。

## Shortest stable mainline documentation decision
- 当前把“最短稳定主线”正式写死成 owner docs，作为默认操作面。
- 原则是：
  - 不再为了理论纯度继续加中间步骤
  - 没有真实多角色需要时，不引入 role thread
  - 当前主线先以短、稳、好定位为第一优先级

## Task / queue truth reconciliation cleanup decision
- `TASKS/QUEUE.json` 继续作为唯一 queue 机器真相源，`TASKS/QUEUE.md` 降级为废弃兼容说明页，不再保留可被误读成真实 backlog 的历史文本。
- 当前新增 `python3 tools/taskclient.py --reconcile-task-queue-truth` 作为最小维护入口，用来统一收口：
  - `runtime_state`
  - `TASKS/QUEUE.json`
  - `TASKS/TASK-*.json`
- 这一步选择放在 `taskclient`，而不是 `evidence.py` 或 `appserverclient`，因为它本质上属于 task/queue truth maintenance，不属于 runtime transport，也不属于 run evidence 聚合。

## Run summary stale prose cleanup decision
- 已确认 baseline refresh 现在默认消费 `run_summary`，所以继续保留“baseline still does not consume run summary yet”会直接误导后续 session。
- 当前选择把这类修正继续放在 `tools/evidence.py --normalize-run-summary` 的窄规则里，而不是手工改 `run_summary.json` 或在别的层做补丁。
- 原则保持不变：只对已被当前代码和真实运行明确证伪的旧句子做窄规则替换，不把 `normalize-run-summary` 扩成泛化改写器。

## Run summary risk layering decision
- run-level 风险不再只用一个列表承载全部含义；当前显式拆成：
  - `cross_task_risks`：当前主线仍成立的运行风险
  - `audit_risks`：历史清理、审计残留、兼容资产风险
- `baseline_ready_summary` 只消费 `cross_task_risks`，避免把 audit/history 噪音继续带进 baseline refresh。
- 这一步保持最小规则化分类，不引入新 client，也不把语义过滤责任继续推给 baseline 侧。

## Tool surface and prompt asset cleanup decision
- 正式 prompt 模板不再散落在 `tools/` 顶层，当前统一迁到 `tools/prompts/`。
- 传统需求分析文档移到 `chatlogs/`，因为它属于学习/对话参考材料，不应继续占据正式工具目录。
- `TOOLS_METHOD_FLOW_MAP.md` 迁到 `docs/`，与其他 owner docs 保持一致。
- `tools/start.sh` 与 `tools/onboard.sh` 直接归档到 `chatlogs/backup/`；当前不保留新的 wrapper，因为正式入口已经是 `init/appserverclient/gitclient/taskclient/evidence`。
- 历史 task、learn 产物中的旧路径不做批量重写，避免把一次目录清理扩大成历史 evidence 重写工程。

## Unused top-level tool artifact cleanup decision
- `tools/console.txt` 删除，因为它不在正式主线或当前工具引用链内。
- 顶层 `tools/taskstore.py` 与 `tools/sync_exam.py` 归档到 `chatlogs/backup/`，因为它们不再属于正式工具面。
- `tools/slice.py` 保留，因为它仍然是独立的 Python 工具入口，而不是因为 `Makefile`。

## Unused shell helper and Make target cleanup decision
- `Makefile` 已删除，因为 `make evidence / make verify / make slice` 只是 Python/pytest 的薄包装，不再值得保留为正式入口。
- `tools/doctor.sh`、`tools/enter.sh`、`tools/smoke.sh` 不再属于正式主线，因此归档到 `chatlogs/backup/`。
- 正式命令面已统一收成：
  - `python3 tools/evidence.py --run-id <RUN_ID>`
  - `pytest -q`
  - `python3 tools/slice.py --run-id <RUN_ID> --day YYYY-MM-DD --symbols A,B --start HH:MM --end HH:MM`
- `pytest` 当前在本 shell 中未安装，因此本轮 verify 结果记录为环境缺口，而不是回退保留 `Makefile` 的理由。

## Relocate appserver logs and backup assets decision
- app-server Python 调试日志不再散落在仓库根目录；默认统一落到 `appserver_log/`。
- 历史兼容脚本与旧 Python 入口不再继续占据 `tools/` 命名空间；归档位置统一改为 `chatlogs/backup/`。
- 这一步只改正式运行时默认路径和 owner docs，不重写历史 checkpoint/审计残留。

## Cleanup stale tasks and reports artifacts decision
- `TASKS/QUEUE.md` 已删除；queue 现在只保留 `TASKS/QUEUE.json` 作为机器真相源。
- sample/demo task 和孤立旧 task md 已删除；真实历史 task 和 run evidence 保留。
- reports 下只清理 checkpoint 垃圾，不删除有真实 run 价值的历史目录。

## Archive stale blueprint and project guide backups decision
- `PROJECT_GUIDE_1.0_backup.md` 与 `TOOLS_REFACTOR_BLUEPRINT.md` 已退出正式 `docs/` 面，改存到 `chatlogs/`。
- `docs/` 现在只保留仍参与当前 owner docs / formal mainline 的文件。
- 这一步不改历史 checkpoint，只收正式面，避免把一次目录减负扩大成历史材料重写。

## Docs stale flow noise cleanup decision
- 正式 `docs/` 面不再继续保留旧阶段流程名作为当前主线说明。
- 归档资产仍存在于 `chatlogs/backup/`，但不再进入正式流程文档和正式阅读索引。
- 这一步只收正式文档口径，不重写 checkpoint、旧备份或历史 evidence。

## Init standard bootstrap skeleton decision
- `init` 应负责建立最小标准协议骨架，而不是只检查 `AGENTS.md` 和 `PROJECT_GUIDE.md` 是否存在。
- 这些骨架文件先只放空内容或极小占位，不预写新项目业务内容；后续由原始材料、代码现状和 `PROJECT_GUIDE` 高质量追问反写。
- `docs/TOOLS_METHOD_FLOW_MAP.md` 也纳入标准骨架，但缺失时只创建空文件，避免提前写死新项目流程。
- `tools/project_config.json` 缺失时，由 `init` 从模板 bootstrap 最小配置；`init` 仍然只属于准备层，不替代 baseline 学习和 owner docs 同频过程。

## Init-project gate and bootstrap state decision
- 项目首轮接入需要单独门禁，不能直接让未初始化项目进入 baseline 主线。
- 硬门禁定为：
  - `tools/project_config.json -> bootstrap_state.is_inited`
  - 只有 `is_inited = Y` 才允许 baseline 主线
  - 入口统一命名为 `python3 tools/appserverclient.py --init-project`
- `--init-project` 当前只做预检，不做反写；后续真正的初始化反写仍应走 plan 模式
- 为保护 `PROJECT_GUIDE` 等关键 owner docs，只要任一 owner doc 非空，就必须手动清空，禁止自动覆盖

## Init-project phase protocol decision
- `--init-project` 的首轮学习和反写不再模糊处理，而是正式拆成两阶段：
  - Phase 1: JSON-first 的 plan/gating
  - Phase 2: Markdown-first 的 owner-doc writing
- `session_registry.init_project_session` 负责保存初始化过程本身的 session 指针；默认 `--init-project` 必须 resume 这个 session，只有显式 `--init-project -new` 才允许重开。
- 默认 intake 顺序固定为：`README.md -> docs/**/*.md|txt|doc|docx -> 显式线索提取 -> 轻量仓库探测结果 -> must_read_next`。当前 owner docs 目标文件一律从原始输入集合中排除。
- Phase 1 的正式职责是判断“证据是否足以进入反写”；在 `can_write_owner_docs = true` 之前，禁止输出 owner docs 正文。
- Phase 2 的正式职责是按目标文件逐个生成详细 markdown 草稿，而不是把所有详细内容再次塞进一个大 JSON。

## Init-project phase-1 intake implementation decision
- 当前先只落 phase-1 的最小实现，不假装已经接通完整 init-project runtime。
- `appserverclient --init-project` 现在会真实生成：
  - `light_repo_findings`
  - `explicit_refs`
  - `must_read_next`
  - `can_write_owner_docs`
  - `why_not_ready`
- 第一轮文件发现明确走“程序轻探测 + 文档显式匹配”，不依赖 NLP 猜测文件路径。
- 下一步应先把 phase-1 输出接到 `init_project_session` 的续跑机制里，再讨论 phase-2 owner-doc reverse-writing。

## Init-project session resume semantics decision
- `init_project_session` 当前先收成“本地 phase-1 session 记录”，而不是伪造一个已经存在的 app-server thread。
- 默认 `--init-project` 必须复用这个本地 session 记录，只有显式 `--init-project -new` 才生成新的 session id。
- 这样可以先把 session 续跑语义稳定下来，再决定是否真的需要把 init-project 提升成完整 app-server lifecycle。

## Init-project phase-2 writer decision
- `--init-project` 先继续走本地 phase-2 writer，而不是立刻接 app-server init thread。
- 当前最小正确路径是：Phase 1 负责 gating，Phase 2 负责在 owner docs 全为空且 `can_write_owner_docs=true` 时，把 6 份 markdown 草稿分别写入目标文件。
- `bootstrap_state.is_inited` 必须只在全部目标文件写入成功后才切到 `Y`；不能在 phase-1 通过时提前放行 baseline 主线。

## Real a9quant-strategy phase-1 run decision
- 当前 `init -> --init-project` 主线已经可以真实跑到外部项目 `/root/a9quant-strategy`，说明 bootstrap gate 和 phase-1 intake 不是只在 foundation repo 内自洽。
- 为了让这条主线成立，`init` 必须把新项目 owner docs 骨架创建为空文件，而不是写占位文本；否则 `--init-project` 会被自己的空文件门禁挡住。
- 下一步不该急着对 `/root/a9quant-strategy` 做 phase-2 反写，而应先收一刀 intake 噪音：排除 `docs/.ipynb_checkpoints` 这类非原始材料目录，避免 phase-1 被 checkpoint 文件污染。

## Checkpoint noise cleanup decision
- `--init-project` 的第一轮 intake 继续坚持“轻、硬、稳”，所以 checkpoint 目录应直接在程序扫描层排除，而不是留给模型自己忽略。
- 这样 Phase 1 的 `raw_docs_read/docs_files` 会更贴近真正的原始材料，也更适合作为后续第二轮代码读取的计划输入。

## a9quant-strategy second-round code reads decision
- `/root/a9quant-strategy` 已被证实不是“只有文档、几乎没实现”的项目；当前 owner-doc 反写必须建立在“已有实现”而非“纯设计愿景”的前提上。
- 当前决定是继续停在 Phase 1，不进入 Phase 2 owner-doc 写入。
- 进入 Phase 2 前的最小补证据范围定为：
  - `main_controller.py`
  - `account_state.py`
  - `contracts.py`
  - selected tests
- 额外记录一条真实风险：`ccxt_utils.py` 的 `__main__` 测试块仍包含硬编码 Bitget sandbox credentials；即使是模拟盘，也应在后续项目治理中优先清理。

## a9quant-strategy mainline and test-surface decision
- 现在 `/root/a9quant-strategy` 的真实主线已经足够清楚：主入口是 `main_controller.py`，状态账本是 `account_state.py`，对象契约边界在 `contracts.py`，并且已有真实测试面约束 live gate、risk gate、OMS 幂等、reconnect 校准和 replay 链路。
- 因此，是否进入 Phase 2 的剩余判断不再取决于“项目有没有主线”，而只取决于最后一轮依赖/配置证据是否齐全。
- 当前决定仍是不进入 Phase 2；Phase 1 再补：
  - `data_synchronizer.py`
  - `config.json`
- 补完这两项后，再决定是否进行 owner-doc reverse-writing。

## a9quant-strategy synchronizer and config decision
- `data_synchronizer.py` 与 `config.json` 的证据现已补齐，因此 Phase 1 对 `/root/a9quant-strategy` 的主线理解已经基本闭合。
- 当前决定可以进入“是否执行 Phase 2 owner-doc reverse-writing”的判断阶段。
- 但如果进入 Phase 2，必须显式保留两类现实风险：
  - sample config 中仍有 hard-coded sandbox credentials / proxy defaults
  - synchronizer 仍带 exchange-specific 假设和简化的 `margin_ratio` 处理
- 也就是说，Phase 2 现在可以考虑做，但不能把目标项目写成一个已经完全抽象化、完全清洁的运行时系统。

## a9quant-strategy phase-2 draft payload decision
- 当前先生成 phase-2 draft payload，而不直接执行写入目标项目。
- 这样可以先审 payload 的 owner-doc 内容是否符合项目真实实现，再决定是否对 `/root/a9quant-strategy` 运行 `--init-project --phase2-json`。
- 当前选择保留的关键边界是：
  - draft is reviewable
  - target project is not mutated yet
  - real hygiene and coupling risks remain explicit in the draft

## init-project session-first simplification decision
- 当前决定正式移除 `--init-project` 的项目化 heuristics 和旧的 `--phase2-json` runtime 路径。
- init-project 现在只保留：
  - `bootstrap_state`
  - `session_registry.init_project_session`
  - `xhigh plan` 的 17 问初始化理解
  - `--update-init-project --payload-json <path>`
  - `--complete-init-project`
- 当前不再把 owner-doc 自动写入当作 formal init-project runtime contract；初始化完成后，才允许进入后续 baseline 学习主线。
- stop_reason: `task_done`

## init-project session instruction decision
- 当前决定把“一句话 owner 执行指令”正式纳入 `--init-project`，而不是继续靠代码里硬编码的项目语义。
- 新增的正式做法是：
  - `--instruction-text`
  - `--instruction-file`
- 这些补充指令现在写回 `init_project_session.session_execution_instruction`，人工纠偏备注写回 `operator_notes`。
- 这样后续无论是手工模式还是 SaaS 页面化流程，都可以围绕同一个 init session 继续推进，再决定何时完成初始化。

## init-project fixture validation decision
- 当前已用仓库内未初始化 fixture 真实验证 `init -> --init-project --instruction-text`。
- 这轮确认：
  - instruction payload 会进入 `err_code=1012` 返回结果
  - instruction 与 continuation state 会写回目标项目自己的 `init_project_session`
  - foundation 仓的默认 `project_root` 已在验证后恢复，不会把 fixture 留成当前项目
- 因此当前决定是：这条初始化 session 手工续跑链已经成立，可以继续迁移到真实未初始化项目上使用。
