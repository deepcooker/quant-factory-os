# PROJECT_GUIDE.md

## 一句话北极星
自动化 -> 自我迭代 -> 涌现智能。

## 使用方式
- 这是 `learn` 的主课程、问题库、标准答案和主线锚点。
- 题目本身与整体结构是 owner 精心挑选后的固定课程资产，不应被随意改写、重排或替换。
- 正常允许变化的是：项目变动后同步更新标准答案，或为保持同频质量做最小必要微调。
- `learn` 必须先阅读本文件，再按每题的 `必查文件` 与 `查找线索` 去读取证据。
- 这些题的目的不是“考试打分”，而是用高质量提问反向逼模型去读全量 owner docs、run evidence、session continuity 线索，并把主线固化成可复用的证据。
- 如果输出偏到具体细节、工具琐事或单一 bug，而没有回到项目目标、门禁、工作流、当前阶段，就说明已经偏离主线。
- 一旦漂移，不是继续闲聊，而是回到 `PROJECT_GUIDE` 的问题体系里重答，并重新引用证据把模型拉回主线。

### 建议入口顺序
- 新 agent 首轮同频，优先按 `Q1 -> Q2 -> Q5 -> Q6 -> Q7 -> Q8 -> Q17` 作答。
- 这组题的作用分别是：项目定位、当前阶段、宪法、工作流、当前局面、session continuity、最终主线回拉。
- 这组题答稳之后，再继续 `Q3/Q4/Q9...Q16`，避免一开始就陷进局部实现细节。

### Q1. 整个项目是做什么的，背景，目标是什么，我最终要什么，我是用什么开发方式来完成这个项目的？
#### 为什么问这题
这题决定 agent 是否理解项目的根目标。如果连项目定位都没对齐，后续所有流程都会变成“会跑命令，但不知道为什么要跑”。
#### 标准答案
`quant-factory-os` 是一个基建型执行与治理系统，目标是把 AI 协作从“依赖聊天记忆”改造成“依赖仓库内证据、门禁和工作流”的工程化闭环。它当前不是业务项目仓，而是在把 `tools` 自动化 AI 研发体系本身做稳。背景是多窗口、多会话、多 agent 协作时非常容易丢上下文、偏离主线、重复试错，所以需要把任务、决策、验证、错误和状态都沉淀到仓库里。你最终要的是：新 agent 上岗后能快速同频、知道项目主线、按规则执行、持续更新文档与证据，并最终让这套能力沉淀成普通窗口可执行的 Python 总入口，而 Codex 通过 app-server 在背后提供运行时智能能力。开发方式不是随手改代码，而是 `Task + Gate + Evidence + Verify + Ship` 的方式：先绑定任务和范围，再同频和规划，再执行最小改动，再验证，再更新证据与文档。`PROJECT_GUIDE` 在这里不是说明书，而是反向提问课程：它通过问题体系逼模型去读宪法、工作流、实体、证据和 session 线索，再把主线答出来。
#### 必查文件
- AGENTS.md
- docs/WORKFLOW.md
- docs/ENTITIES.md
#### 查找线索
- 先看 README 的项目定位。
- 再看 AGENTS 的硬规则和门禁要求。
- 再看 WORKFLOW 的状态机，确认这不是普通代码仓，而是流程仓。
- 最后用 ENTITIES 理清 task/run/project/evidence 这些名词。
#### 主线意义
- 这题是总开关，回答错了，后面所有题都会偏。
- 最常见漂移是把项目理解成“一个脚本工具集”或“一个普通自动化仓库”，忽略治理与同频。

### Q2. 项目有几个阶段性目标，现在完成到哪个阶段，每个阶段都完成了什么？
#### 为什么问这题
这题用来判断 agent 是否知道“我们现在在哪”，避免拿未来形态要求当前实现，或者拿历史方案约束当前方向。
#### 标准答案
这个项目是分阶段推进的。当前可以概括为：先把项目级同频学习基线和 session 基建做稳，再围绕 run 级需求方向 fork 多角色 session 拆最小 task 执行，最后用 `gitclient` 完成交付和回滚闭环。现在仍处于 foundation 强化阶段，重点不是扩业务，而是让 `init` 作为准备层稳定、让 `appserverclient` 承担正式主流程、让 `gitclient` 承担正式收尾层，并把这三层口径彻底统一。已经有的成果包括：项目级 baseline 学习、current fork/session 推进、Git 提交/回滚闭环、owner docs 主线统一；旧 shell 兼容入口则已开始降级到 `tools/backup/`。当前研发期主要通过 Codex CLI 暴露流程问题、观察日志和接管排障；终态目标则不是长期停留在 CLI，而是让这套基座逐步沉淀成“普通窗口执行的 Python orchestrator + Codex app-server 运行时”。
#### 必查文件
- docs/WORKFLOW.md
- tools/project_config.json
- TASKS/QUEUE.json
- reports/<RUN_ID>/summary.md
#### 查找线索
- 先看 WORKFLOW 的状态机和当前推荐路径。
- 再看 `tools/project_config.json -> runtime_state` 当前 run 和 task。
- 再看 QUEUE 判断还有哪些未完事项。
- 最后看当前 run summary，确认最近落地了什么。
#### 主线意义
- 这题负责时间定位。
- 最常见漂移是把“最终自动化蓝图”误当作“当前已经实现的能力”。

### Q3. 这个项目完成后会形成什么基座能力，接下来第一个落地项目会是什么，你准备怎么承接和落地？
#### 为什么问这题
这题是把“基座仓”与“业务仓”分开，防止把所有问题都堆在一个仓里，造成基建和业务互相污染。
#### 标准答案
基建项目做完后，它应作为 foundation repo，负责流程、门禁、同频和执行治理。它当前首先要产出的不是业务项目模板，而是一套更稳定的 `tools` 自动化 AI 研发团队运行层。研发期用 Codex CLI 来定义 agent 行为、检验 `PROJECT_GUIDE / ENTITIES / WORKFLOW / AGENTS` 是否足以约束研发流程，并通过日志暴露问题；成熟后，日常运行应主要在普通窗口通过 Python 总入口执行，而与 Codex 的程序化交互统一落在 app-server。原因是：当前最难的不是复用分发，而是正确理解需求、对齐主线、保证流程稳定。如果过早把未稳定流程包装成接口或模板，会放大耦合和返工。更合理的做法是：基座仓继续稳定 learn / ready / discuss / execute / review 机制，把 owner docs 和状态机打磨清楚；我的承接方式应该是先跑同频，再确认当前 run、任务和方向，然后才进入讨论和执行。
#### 必查文件
- docs/WORKFLOW.md
- docs/ENTITIES.md
- reports/<RUN_ID>/decision.md
#### 查找线索
- 看 WORKFLOW，确认基座提供的是流程骨架，不是业务实现。
- 看 ENTITIES，区分 project/run/task 的层级。
- 看当前 decision，确认近期对“基座 vs 业务”的判断。
#### 主线意义
- 这题防止把基建仓做成“所有事都往里塞”的大杂烩。
- 常见漂移是太早做插件化，忽视当前流程还没稳定。

### Q4. 如果把不同 AI 界面或运行时分别作为决策端和执行端，它们应如何保持同频，各自承担什么职责？
#### 为什么问这题
这题负责定义脑和手的协作边界，不然模型会把战略、评审、实现、修复混成一层。
#### 标准答案
不同 AI 界面和运行时可以分成“决策端”和“执行端”，但必须保持同频。当前项目里，网页端更适合做方向讨论、方案反驳、角色博弈和收敛决策；本地执行端更适合做项目级 baseline 学习、session/fork 推进、代码修改、验证和证据回写。它们保持同频的方式不是靠聊天记忆，而是靠 `AGENTS.md`、`PROJECT_GUIDE.md`、`WORKFLOW.md`、`FILE_INDEX.md`、`TOOLS_METHOD_FLOW_MAP.md`、`project_config.runtime_state` 和 run 证据同步；真正发生漂移时，不应该继续闲聊，而应该回到 `PROJECT_GUIDE` 的问题体系里按题重答并重新绑定证据。
#### 必查文件
- AGENTS.md
- docs/WORKFLOW.md
- docs/FILE_INDEX.md
- TOOLS_METHOD_FLOW_MAP.md
- tools/appserverclient.py
- tools/gitclient.py
- tools/project_config.json
#### 查找线索
- 看 AGENTS 的 session gate 和主流程分层。
- 看 WORKFLOW 的 state machine 和主线定义。
- 看 FILE_INDEX / TOOLS_METHOD_FLOW_MAP，确认学习、执行、收尾三层分别由哪些文件承担。
- 看 `tools/project_config.json -> runtime_state`，确认当前 run 和 task 指针。
#### 主线意义
- 这题直接决定“同频”是不是靠证据完成。
- 常见漂移是把网页端和 CLI 当成同一个东西，或者指望它们天然共享上下文。
- 真正的回拉动作不是补充闲聊，而是回到题库和证据重新答题。

### Q5. 这个项目当前的宪法是什么样的？
#### 为什么问这题
这题判断 agent 是否知道谁是硬规则，谁只是说明文档。
#### 标准答案
当前项目的宪法是 `AGENTS.md`。它定义了任务入口、同频门禁、允许命令、执行流程、失败协议、文档新鲜度和 PR/ship 纪律。它不是可选参考，而是 agent 的硬契约。`docs/WORKFLOW.md` 负责补状态机和步骤细节，`PROJECT_GUIDE.md` 负责学习与主线锚点，但一切执行边界最终以 `AGENTS.md` 为准。
#### 必查文件
- AGENTS.md
- docs/WORKFLOW.md
#### 查找线索
- 看 AGENTS 里 task/run、learn、ship、docs freshness 的硬要求。
- 再看 WORKFLOW 理解哪些是流程细节，哪些是宪法。
#### 主线意义
- 这题负责分清“规则层”和“说明层”。
- 常见漂移是把任何文档都当宪法，或者只看流程图不看硬门禁。

### Q6. 这个项目当前工作流是什么样的？
#### 为什么问这题
这题用于确认 agent 是否知道从哪一步开始、什么时候停、什么时候不能直接改代码。
#### 标准答案
当前工作流已经收敛成三层。第一层是环境准备层：`init`，它只负责配置、项目骨架、Codex/Git 前提和现场诊断，不属于主业务流程。第二层是真正自动化主线：`run(appserverclient)`，先做项目级 `--learnbaseline` 同频学习，再确定本轮需求方向，然后从 baseline `fork` 多个角色 session，把需求拆成最小 task 逐个推进，并在阶段结束后把去噪结果回灌 baseline。第三层是 Git 收尾层：`gitclient` 负责提交、PR、合并、回滚和本地同步 main。复杂需求仍然遵守 `Plan -> Confirm -> Execute`，但主线不再是旧的长链，而是“准备层 -> 学习/执行层 -> Git 收尾层”。
#### 必查文件
- docs/WORKFLOW.md
- AGENTS.md
#### 查找线索
- 先看 WORKFLOW 的 session lifecycle state machine。
- 再用 AGENTS 核对哪些步骤是硬门禁，哪些是推荐路径。
#### 主线意义
- 这题负责把 agent 拉回流程，而不是细节。
- 常见漂移是把 `/plan`、`legacy plan`、`do`、`ship` 混在一起理解。

### Q7. 我们现在的项目有没有未完成的任务呢，最新的批次在讨论什么问题，你是怎么查的？
#### 为什么问这题
这题要求 agent 具备“看当前局面”的能力，而不是只会泛泛复述项目介绍。
#### 标准答案
要看当前有没有未完成任务，先看 `tools/project_config.json -> runtime_state` 当前指针，再看 `TASKS/QUEUE.json` 队列真相源，再看当前 `RUN_ID` 下的 `summary.md` 和 `decision.md`。`TASKS/QUEUE.md` 现在只是迁移期的人类可读视图。当前项目最近讨论的重点，已经从旧的长流程门禁转向更轻的主线：用 `appserverclient` 建立和维护项目级 baseline 学习、副本 fork 和当前工作 session，再用 `gitclient` 做提交与回滚收尾，让整个自动化真正围绕项目、run、task 这三层推进。
#### 必查文件
- tools/project_config.json
- TASKS/QUEUE.json
- reports/<RUN_ID>/summary.md
- reports/<RUN_ID>/decision.md
#### 查找线索
- 先看 `tools/project_config.json -> runtime_state` 的当前 run/task。
- 再看 QUEUE 有哪些未勾选项。
- 最后看当前 run 的 summary/decision 判断最近批次在推进什么。
#### 主线意义
- 这题把学习拉回“当前在做什么”。
- 常见漂移是只会讲历史和蓝图，不知道当前迭代目标。

### Q8. 你查了最近的 session 说了什么，你是从哪里查的？
#### 为什么问这题
这题要求 agent 具备 session continuity，不然一换会话就会忘掉当前主线。
#### 标准答案
最近 session 的内容应该从仓库证据里查，不应该靠聊天记忆猜。最重要的来源是 `tools/project_config.json -> runtime_state`、当前 `RUN_ID` 下的 `reports/<RUN_ID>/summary.md` 和 `decision.md`，必要时再看 `conversation.md`。根据当前证据，最近 session 的主线已经明确为：`init` 只是准备层，真正主流程由 `appserverclient` 承担，用 `--learnbaseline` 建项目级同频基线，再 fork 多角色 session 做最小 task 处理，最后通过 `gitclient` 完成提交、PR、合并、回滚和主线同步。
#### 必查文件
- tools/project_config.json
- reports/<RUN_ID>/summary.md
- reports/<RUN_ID>/decision.md
#### 查找线索
- 先看 `tools/project_config.json -> runtime_state` 决定去哪个 run 读证据。
- 优先看 summary 和 decision，而不是盲读全量聊天记录。
- 如果对总结存疑，再回溯 `conversation.md`。
#### 主线意义
- 这题是“主线连续性”的核心。
- 常见漂移是把当前 session 理解成新任务，忽略前面已经反复收敛的方向。

### Q9. 项目需求讨论应该使用什么流程？
#### 为什么问这题
这题负责把“讨论”和“执行”分开，防止先写代码后补理由。
#### 标准答案
项目需求讨论现在更适合挂在 `appserverclient` 的 run/session 体系上做：先有项目级 baseline，同频当前主线和证据；再在 run 级别明确本轮需求方向；再从 baseline fork 多个角色 session 去做需求分析、方案评审、实现设计和验证拆分，最后把方向收敛成最小 task。旧的 `orient -> choose -> council -> arbiter -> slice` 可以视为兼容性的讨论链骨架，但主流程重心已经转到 baseline/fork/session 的分层运行方式。
#### 必查文件
- docs/WORKFLOW.md
- AGENTS.md
#### 查找线索
- 在 WORKFLOW 里找 `Direction gate`、`Council gate`、`Arbiter gate`、`Slice gate`。
- 在 AGENTS 里看 Plan -> Confirm -> Execute 约束。
#### 主线意义
- 这题负责守住“讨论先于执行”。
- 常见漂移是把讨论代理和执行代理混成同一轮输出。

### Q10. 项目实施流程是什么，需要哪些角色协作，如何保证角色独立思考，目前实现到了什么程度？
#### 为什么问这题
这题用来区分“多角色讨论能力”和“单一实现能力”，避免只靠一个视角拍脑袋出方案。
#### 标准答案
项目实施流程现在更适合理解成：项目级 baseline 学习一次建好后，围绕当前 run 的需求方向 fork 多个角色 session，各角色互不干扰地推进自己的最小 task，再把结论去噪收口回 baseline。多角色协作的理想角色仍然包括产品、架构、研发、测试，但独立性不再主要靠旧讨论链文字约束，而是靠 session 隔离：每个角色在自己的 fork thread 里独立思考，减少互相污染。当前已经具备 baseline、current fork 和普通 turn 这类核心 session 能力，但“多角色 fork -> 去噪总结 -> baseline 回灌”这条线还在继续强化。
#### 必查文件
- docs/WORKFLOW.md
- AGENTS.md
#### 查找线索
- 看 WORKFLOW 里 baseline、fork session 和角色推进的职责边界。
- 看工具文件名称和输出物，确认当前实现到什么程度。
#### 主线意义
- 这题防止把“多角色评审”说成已经完整实现。
- 常见漂移是把角色分工说得很理想，但忽略当前还只是流程骨架。

### Q11. 项目中的核心对象、关键状态和交付单元分别是什么，它们的生命周期是怎样的？
#### 为什么问这题
这题负责统一名词系统，避免 agent 在 task、run、project 这些层级上混乱。
#### 标准答案
`project` 是最高层项目维度，负责项目级配置、baseline 学习和长期主线；`run` 是一次需求方向或执行周期，对应 run 级证据和 session 推进；`task` 是从 run 中拆出来的最小执行单元；`PR` 是 Git 交付与审查单元。除此之外，还有 `runtime_state` 作为当前活动指针，`session_registry` 作为 baseline/current session 记录，`evidence` 作为仓库内记忆。生命周期更接近：`PROJECT baseline -> RUN direction -> role fork sessions -> TASK execution -> Git PR -> baseline refresh`。
#### 必查文件
- docs/ENTITIES.md
- docs/WORKFLOW.md
- AGENTS.md
#### 查找线索
- 先看 ENTITIES 的名词定义。
- 再看 WORKFLOW 里的状态流转。
- 最后用 AGENTS 理解这些概念如何形成硬规则。
#### 主线意义
- 这题负责名词统一。
- 常见漂移是把 run 当需求方向、把 task 当 run、把 project 当 session。

### Q12. 我们在项目的准备工作做好后，我们一个需求讨论方向，从流程的哪一步开始？
#### 为什么问这题
这题确认“准备完成后做什么”，避免 learn/ready 做完还直接跳到写代码。
#### 标准答案
准备工作完成后，应该进入 `run(appserverclient)`，而不是直接写代码。先确认或建立 `--learnbaseline`，再在 run 级别明确这次需求方向，然后从 baseline fork 当前工作 session 和角色 session，把方向拆成最小 task 逐个推进。也就是说，准备工作之后的第一步不再是旧链里的 `orient`，而是进入项目级 baseline/session 主线。
#### 必查文件
- docs/WORKFLOW.md
- AGENTS.md
- reports/<RUN_ID>/summary.md
#### 查找线索
- 看 WORKFLOW 里 `appserverclient --learnbaseline / --fork-current / --current-turn` 的主流程说明。
- 看当前 run summary 中有没有对方向讨论的近期结论。
#### 主线意义
- 这题负责接上岗后的下一步。
- 常见漂移是把 `ready` 误当“可以直接改代码”。

### Q13. 项目的分支与交付管理规则是什么，当前是否满足需求？
#### 为什么问这题
这题用于校准交付纪律，避免“本地能跑就行”而没有分支/PR 约束。
#### 标准答案
当前交付主线已经收敛成 `gitclient`：从当前工作面建分支、提交、push、创建 PR、合并或 auto merge、最后同步本地 `main`。它和 task 是解耦的：有 task 时优先用 task 作为提交说明，没有 task 也可以直接手动提交。当前规则重点不是复杂分支模型，而是保证每次交付都能对应回项目、run、task 和证据；回滚也由 `gitclient` 统一处理。若 PR 当前不可 clean merge，应明确返回状态并等待处理，而不是隐藏失败。
#### 必查文件
- AGENTS.md
- docs/WORKFLOW.md
#### 查找线索
- 看 AGENTS 的 PR discipline。
- 看 `tools/gitclient.py` 的提交、PR、合并、回滚和主线同步行为边界。
#### 主线意义
- 这题负责交付边界。
- 常见漂移是只关注本地改动，不关注如何形成干净可审计的交付单元。

### Q14. 每次做完任务，你必须要做什么事情？
#### 为什么问这题
这题是执行闭环问题，用来确认 agent 知道“写完代码不是结束”。
#### 标准答案
每次做完任务，必须做验证、更新证据、同步 owner docs（如果流程/规则/工具行为变了），再通过 `gitclient` 做提交、PR、合并或回滚。最少要更新 `reports/<RUN_ID>/summary.md`、`decision.md`、`meta.json`，把 Why / What / Verify / Risk 写清楚。如果流程规则变了，还必须同步 `AGENTS.md`、`docs/WORKFLOW.md`、`docs/PROJECT_GUIDE.md`、`docs/FILE_INDEX.md`、`TOOLS_METHOD_FLOW_MAP.md` 等主线文档。没有验证、证据和文档更新，就不算完成。
#### 必查文件
- AGENTS.md
- docs/WORKFLOW.md
- reports/<RUN_ID>/summary.md
- reports/<RUN_ID>/decision.md
#### 查找线索
- 看 AGENTS 的 evidence gate 和 docs freshness gate。
- 看 WORKFLOW 的 ship 前提。
- 看当前 run 证据文件长什么样。
#### 主线意义
- 这题负责把“完成”定义清楚。
- 常见漂移是把“代码写完”误当“任务完成”。

### Q15. 如果目标体验是高质量、低噪音、强自动化，当前最需要优先优化什么？
#### 为什么问这题
这题用来防止局部最优。项目是基建，就必须优先优化通用流程，而不是只修某一个具体命令。
#### 标准答案
当前最需要优先优化的，不是继续堆命令，而是把两条真正的底层能力收稳：第一，`appserverclient` 的项目级同频学习、baseline、fork、current session 和去噪回灌；第二，`gitclient` 的提交、PR、合并、回滚和主线同步。只要这两条底层稳定，其他流程就会自然压缩和解耦。之后再继续优化 `PROJECT_GUIDE`、文件索引、方法流图和多角色 baseline 刷新即可。
#### 必查文件
- docs/WORKFLOW.md
- AGENTS.md
- reports/<RUN_ID>/decision.md
#### 查找线索
- 看 WORKFLOW 的主路径是否简单清晰。
- 看 AGENTS 的门禁是否支持自动化而不是阻碍自动化。
- 看 `tools/appserverclient.py` 和 `tools/gitclient.py`，确认真正底层能力是否已经收稳。
- 看当前 decision 是否已经把重心放在 baseline/session/git 这三条主能力上。
#### 主线意义
- 这题负责产品视角。
- 常见漂移是为了“爽”去堆功能，而不是收敛结构和减少噪音。

### Q16. 这个项目中 AI/工具系统的正确打开方式是什么，当前用到了哪些能力，你能列出来吗？
#### 为什么问这题
这题是技能题，确认 agent 不是只知道项目流程，还知道 Codex CLI 这个执行器该怎么正确使用。
#### 标准答案
会。当前项目中，AI/工具系统的正确打开方式已经收敛成三层：`init` 是准备层，只做配置、结构、Codex/Git 前提和现场诊断；`appserverclient` 是主流程层，负责项目级 `--learnbaseline`、run/session、fork、current-turn 和 baseline 回灌；`gitclient` 是收尾层，负责提交、回滚、PR、合并和本地同步。关键不是背全部子命令，而是知道什么问题该交给哪一层解决，以及 baseline 用 `plan`、日常 session 用 `default` 的模式切换原则。
#### 必查文件
- AGENTS.md
- docs/WORKFLOW.md
- tools/appserverclient.py
- tools/gitclient.py
#### 查找线索
- 看 AGENTS 和 WORKFLOW，确认当前主流程分层。
- 看 `appserverclient.py`，确认 baseline / fork / current-turn 的能力边界。
- 看 `gitclient.py`，确认 commit / rollback / PR / merge / sync 的收尾能力。
#### 主线意义
- 这题负责技能上岗。
- 常见漂移是把 Codex CLI 的所有功能都当项目必须路径，或者反过来只会最基本的 chat 用法。

### Q17. 根据最新的 session，你现在做的东西是否偏离了我们现在最重要的任务，你是否认为我们偏离了主线，为什么，接下来我们应该怎么做？
#### 为什么问这题
这题是最终回拉题。它不问知识点，而是判断 agent 能不能把当前执行重新拉回最重要的方向。
#### 标准答案
当前最重要的任务不是继续扩散旧流程，而是把新主线打扎实：项目级 baseline 学习、run 级需求方向收敛、baseline fork 多角色 session 做最小 task、去噪回灌 baseline，以及 `gitclient` 的交付闭环。只要当前动作不能提升这条主线、不能让 `PROJECT_GUIDE` 更像通用学习协议、不能让 `appserverclient` 和 `gitclient` 更稳定，就有偏离风险。接下来应该优先做的，是继续把 `PROJECT_GUIDE`、`FILE_INDEX`、`TOOLS_METHOD_FLOW_MAP` 等文档收成通用学习底座，同时让 baseline/session/git 这三条底层能力真正可复用。
#### 必查文件
- tools/project_config.json
- reports/<RUN_ID>/summary.md
- reports/<RUN_ID>/decision.md
- docs/WORKFLOW.md
#### 查找线索
- 看当前 run 的 summary/decision，确认最近连续几轮都在收敛什么。
- 看 WORKFLOW，确认最关键的瓶颈是不是 learn。
- 用这题检查自己当前做的事，是否真的在强化主线。
#### 主线意义
- 这题就是主线回拉器。
- 常见漂移是被单个实现细节拖住，忘了这轮迭代真正要交付的是更强的同频流程。
