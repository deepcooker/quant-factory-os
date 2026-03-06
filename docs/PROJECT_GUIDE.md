# PROJECT_GUIDE.md

## 一句话北极星
自动化 -> 自我迭代 -> 涌现智能。

## 使用方式
- 这是 `learn` 的主课程、问题库、标准答案和主线锚点。
- `learn` 必须先阅读本文件，再按每题的 `必查文件` 与 `查找线索` 去读取证据。
- 如果输出偏到具体细节、工具琐事或单一 bug，而没有回到项目目标、门禁、工作流、当前阶段，就说明已经偏离主线。

### Q1. 整个项目是做什么的，背景，目标是什么，我最终要什么，我是用什么开发方式来完成这个项目的？
#### 为什么问这题
这题决定 agent 是否理解项目的根目标。如果连项目定位都没对齐，后续所有流程都会变成“会跑命令，但不知道为什么要跑”。
#### 标准答案
`quant-factory-os` 是一个基建型执行与治理系统，目标是把 AI 协作从“依赖聊天记忆”改造成“依赖仓库内证据、门禁和工作流”的工程化闭环。背景是多窗口、多会话、多 agent 协作时非常容易丢上下文、偏离主线、重复试错，所以需要把任务、决策、验证、错误和状态都沉淀到仓库里。你最终要的是：新 agent 上岗后能快速同频、知道项目主线、按规则执行、持续更新文档与证据。开发方式不是随手改代码，而是 `Task + Gate + Evidence + Verify + Ship` 的方式：先绑定任务和范围，再同频和规划，再执行最小改动，再验证，再更新证据与文档。
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
这个项目是分阶段推进的。当前可以概括为：先做基座硬化和 learn 同频能力，再做讨论与执行闭环，再逐步走向多角色协作和具体业务项目承接。现在仍处于基座强化阶段，重点不是扩业务，而是让 `init / learn / ready / discuss / execute / review / ship` 这条链路足够稳，尤其是让 `learn` 真的完成项目目标、宪法、工作流、技能、项目现状和 session continuity 的同频。已经有的成果包括：Python-first 的核心命令、真实 Codex model sync、ready 门禁、讨论链路骨架、ship/verify 规则、文档 owner map。
#### 必查文件
- docs/WORKFLOW.md
- TASKS/STATE.md
- TASKS/QUEUE.md
- reports/<RUN_ID>/summary.md
#### 查找线索
- 先看 WORKFLOW 的状态机和当前推荐路径。
- 再看 STATE 当前 run 和 task。
- 再看 QUEUE 判断还有哪些未完事项。
- 最后看当前 run summary，确认最近落地了什么。
#### 主线意义
- 这题负责时间定位。
- 最常见漂移是把“最终自动化蓝图”误当作“当前已经实现的能力”。

### Q3. 这个基建项目做完之后，它会作为基座的项目，我们接下来第一个项目将完成什么，你会怎么去落地，我们现在设计的结构是把这个变成一个插件好呢还是独立项目好，项目最难的是读懂和同频我的意图，你读了项目后，你准备用什么样的方式来接？
#### 为什么问这题
这题是把“基座仓”与“业务仓”分开，防止把所有问题都堆在一个仓里，造成基建和业务互相污染。
#### 标准答案
基建项目做完后，它应作为基座仓，负责流程、门禁、同频和执行治理。接下来的第一个实际业务项目，是财富系统或类似真实业务项目的承接与落地，但应该以独立项目优先，而不是现在就插件化。原因是：当前最难的不是复用分发，而是正确理解需求、对齐主线、保证流程稳定。如果过早插件化，会把尚未稳定的基座规则固化成接口，放大耦合和返工。更合理的做法是：基座仓继续稳定 learn / ready / discuss / execute / review 机制，业务仓通过项目 guide 和集成合同接入。我的承接方式应该是：先跑同频，再确认当前 run、任务和方向，然后才进入讨论和执行。
#### 必查文件
- docs/WORKFLOW.md
- docs/ENTITIES.md
- reports/<RUN_ID>/decision.md
#### 查找线索
- 看 WORKFLOW，确认基座提供的是流程骨架，不是业务实现。
- 看 ENTITIES，区分 project/run/task 的层级。
- 看财富系统新建项目引导，确认业务项目的承接形态。
- 看当前 decision，确认近期对“基座 vs 业务”的判断。
#### 主线意义
- 这题防止把基建仓做成“所有事都往里塞”的大杂烩。
- 常见漂移是太早做插件化，忽视当前流程还没稳定。

### Q4. 如果完成这个项目，我把 gpt 网页端当做大脑，codex cli 当做手脚，你是怎么让 codex cli 和 gpt 保持同频的，一样吗，如果不一样，都需要怎么做？
#### 为什么问这题
这题负责定义脑和手的协作边界，不然模型会把战略、评审、实现、修复混成一层。
#### 标准答案
GPT 网页端和 Codex CLI 不一样，但必须同频。网页端更适合做方向讨论、方案反驳、角色博弈和收敛决策；Codex CLI 更适合本地读仓、改代码、跑验证、写证据。它们保持同频的方式不是靠聊天记忆同步，而是靠仓库内的 owner docs、task/run 指针和执行证据同步。Codex CLI 在本地必须先执行 `python3 tools/init.py -> python3 tools/learn.py -> python3 tools/ready.py`，再进入讨论或执行链；日常默认建议用 `python3 tools/learn.py -daily`，它等价于 `-medium`，但不降低强同频门禁。网页端如果要作为大脑，也必须先看 `AGENTS.md`、`docs/PROJECT_GUIDE.md`、`docs/WORKFLOW.md`，再围绕当前 state/run 来讨论，而不是脱离仓库空谈。
#### 必查文件
- AGENTS.md
- docs/WORKFLOW.md
- CODEX_CLI_PLAYBOOK.md
- TASKS/STATE.md
#### 查找线索
- 看 AGENTS 的 session gate。
- 看 WORKFLOW 的 state machine。
- 看 PLAYBOOK，确认 Codex CLI 的正确使用方式和 plan/read-only/write 区分。
- 看 STATE，确认当前 run 和 task 指针。
#### 主线意义
- 这题直接决定“同频”是不是靠证据完成。
- 常见漂移是把网页端和 CLI 当成同一个东西，或者指望它们天然共享上下文。

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
当前工作流是分层状态机。主线是：`init -> learn -> ready -> orient -> choose -> council -> arbiter -> slice -> do -> review -> ship`。其中 `init/learn/ready` 是上岗和同频层；`orient/choose/council/arbiter/slice` 是讨论和合同收敛层；`do/review/ship` 是实现交付层。复杂需求必须先 `Plan -> Confirm -> Execute`，不能跳过讨论层直接写代码。
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
要看当前有没有未完成任务，首先看 `TASKS/STATE.md` 当前指针，再看 `TASKS/QUEUE.md` 队列，再看当前 `RUN_ID` 下的 `summary.md` 和 `decision.md`。当前项目最近讨论的重点，不是新业务功能，而是自动化流程本身，尤其是 `learn` 是否真的完成同频、`PROJECT_GUIDE` 如何成为学习课程、以及流程能否更简单、更自动化。
#### 必查文件
- TASKS/STATE.md
- TASKS/QUEUE.md
- reports/<RUN_ID>/summary.md
- reports/<RUN_ID>/decision.md
#### 查找线索
- 先看 STATE 的当前 run/task。
- 再看 QUEUE 有哪些未勾选项。
- 最后看当前 run 的 summary/decision 判断最近批次在推进什么。
#### 主线意义
- 这题把学习拉回“当前在做什么”。
- 常见漂移是只会讲历史和蓝图，不知道当前迭代目标。

### Q8. 你查了最近的 session 说了什么，你是从哪里查的？
#### 为什么问这题
这题要求 agent 具备 session continuity，不然一换会话就会忘掉当前主线。
#### 标准答案
最近 session 的内容应该从仓库证据里查，不应该靠聊天记忆猜。最重要的来源是 `TASKS/STATE.md`、当前 `RUN_ID` 下的 `reports/<RUN_ID>/summary.md` 和 `decision.md`，必要时再看 `conversation.md`。根据当前证据，最近 session 的主线是：继续压缩流程噪音，把 `learn` 做成真正的项目同频核心，并用 `PROJECT_GUIDE` 把模型拉回主线，而不是让它在单个技术细节里打转。
#### 必查文件
- TASKS/STATE.md
- reports/<RUN_ID>/summary.md
- reports/<RUN_ID>/decision.md
#### 查找线索
- 先看 STATE 决定去哪个 run 读证据。
- 优先看 summary 和 decision，而不是盲读全量聊天记录。
- 如果对总结存疑，再回溯 `conversation.md`。
#### 主线意义
- 这题是“主线连续性”的核心。
- 常见漂移是把当前 session 理解成新任务，忽略前面已经反复收敛的方向。

### Q9. 基建项目讨论项目应该用哪个流程？
#### 为什么问这题
这题负责把“讨论”和“执行”分开，防止先写代码后补理由。
#### 标准答案
基建项目讨论需求应该走讨论优先流程：`orient -> choose -> council -> arbiter -> slice`。这个流程的目的，是先生成方向草案，再由用户确认，再做多角色独立评审，再收敛为执行合同，最后切成最小 task。只有这一层完成后，才允许进入 `do`。`legacy plan` 只是提队列建议，不等于 Codex `/plan`，也不等于执行许可。
#### 必查文件
- docs/WORKFLOW.md
- AGENTS.md
#### 查找线索
- 在 WORKFLOW 里找 `Direction gate`、`Council gate`、`Arbiter gate`、`Slice gate`。
- 在 AGENTS 里看 Plan -> Confirm -> Execute 约束。
#### 主线意义
- 这题负责守住“讨论先于执行”。
- 常见漂移是把讨论代理和执行代理混成同一轮输出。

### Q10. 基建项目的代码实施流程是什么样的，它需要哪些 agent 进行协作呢，怎么保证这些角色都是独立思考的，他们每一个角色的定义是什么样子的，怎么保证其独立思考的，我们现在都实现了吗，怎么实现的？
#### 为什么问这题
这题用来区分“多角色讨论能力”和“单一实现能力”，避免只靠一个视角拍脑袋出方案。
#### 标准答案
代码实施流程是：讨论收敛成合同后，再进入 `do -> verify -> review -> ship`。多角色协作的理想角色包括产品、架构、研发、测试。产品负责目标、边界和优先级；架构负责影响面、模块边界、数据流和约束；研发负责实现路径、回滚和最小改动；测试负责用例、失败路径和回归验证。独立思考不是靠口头要求，而是靠 `council` 先分别产出，再由 `arbiter` 收敛成单一合同。当前基础版已经有 `orient / council / arbiter / slice` 骨架，但还在强化阶段，并没有做到真正高并发独立 agent 团队。
#### 必查文件
- docs/WORKFLOW.md
- AGENTS.md
#### 查找线索
- 看 WORKFLOW 中 council/arbiter 的职责定义。
- 看工具文件名称和输出物，确认当前实现到什么程度。
#### 主线意义
- 这题防止把“多角色评审”说成已经完整实现。
- 常见漂移是把角色分工说得很理想，但忽略当前还只是流程骨架。

### Q11. 项目基建里的 task，pr，run，project 的都是什么意思，还有其他的概念吗，他们的生命周期管理是怎么样的？
#### 为什么问这题
这题负责统一名词系统，避免 agent 在 task、run、project 这些层级上混乱。
#### 标准答案
`project` 是最高层项目维度，当前基座默认是 `project-0`；`run` 是一次执行或讨论周期对应的证据命名空间，主要落在 `reports/<RUN_ID>/`；`task` 是当前要做的具体合同，落在 `TASKS/TASK-*.md`；`PR` 是交付与审查单元。除此之外，还有 `queue` 作为待办入口，`gate` 作为门禁，`evidence` 作为仓库内记忆。生命周期一般是：`QUEUE -> TASK -> RUN evidence -> verify -> ship/PR -> state update`。
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
准备工作完成后，需求讨论方向应从 `orient` 开始，而不是直接 `do`。之后是 `choose -> council -> arbiter -> slice`。讨论阶段的草案和中间产物应该先放在 discussion 或方向合同里，等方向被确认、执行合同生成后，再进入执行阶段。讨论不是实现，讨论的结果必须能转成最小 task。
#### 必查文件
- docs/WORKFLOW.md
- AGENTS.md
- reports/<RUN_ID>/summary.md
#### 查找线索
- 看 WORKFLOW 的 direction gate 到 slice gate。
- 看当前 run summary 中有没有对方向讨论的近期结论。
#### 主线意义
- 这题负责接上岗后的下一步。
- 常见漂移是把 `ready` 误当“可以直接改代码”。

### Q13. 我们分支代码的管理是怎么样的，现在满足需求吗？
#### 为什么问这题
这题用于校准交付纪律，避免“本地能跑就行”而没有分支/PR 约束。
#### 标准答案
当前代码管理规则是“一任务一分支一 PR”，PR 标题必须带 `RUN_ID`，正文需要包含 Why / What / Verify / Evidence paths。这个纪律在当前基建阶段是够用的，重点不是复杂分支模型，而是保证每次改动都能回到 task、run 和验证证据。后续并行度上来时，再补更细的分支策略即可。
#### 必查文件
- AGENTS.md
- docs/WORKFLOW.md
#### 查找线索
- 看 AGENTS 的 PR discipline。
- 看 ship.sh 的行为边界，理解它何时适合、何时不适合补跑。
#### 主线意义
- 这题负责交付边界。
- 常见漂移是只关注本地改动，不关注如何形成干净可审计的交付单元。

### Q14. 每次做完任务，你必须要做什么事情？
#### 为什么问这题
这题是执行闭环问题，用来确认 agent 知道“写完代码不是结束”。
#### 标准答案
每次做完任务，必须做验证、更新证据、同步 owner docs（如果流程/规则/工具行为变了）、再 ship。最少要更新 `reports/<RUN_ID>/summary.md`、`decision.md`、`meta.json`，把 Why / What / Verify / Risk 写清楚。如果流程规则变了，还必须同步 `AGENTS.md`、`docs/WORKFLOW.md`、`docs/PROJECT_GUIDE.md`、`CODEX_CLI_PLAYBOOK.md` 等 owner docs。没有文档更新和验证，就不算完成。
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

### Q15. 这个项目是基建项目吗，如果我要的体验是为了用起来很爽，完全自动化，有哪些必要的需要优化的？
#### 为什么问这题
这题用来防止局部最优。项目是基建，就必须优先优化通用流程，而不是只修某一个具体命令。
#### 标准答案
这个项目就是基建项目。你要的“用起来很爽、自动化程度很高”并不等于命令越多越好，而是底层组件稳定、编排层清晰、同频质量足够高。必要优化的优先级应是：第一，`learn` 的同频质量必须做真；第二，流程要少噪音、少分叉、少手工；第三，文档更新要硬门禁；第四，失败恢复要清晰；第五，再考虑更强的 orchestrator 和多角色并行。
#### 必查文件
- docs/WORKFLOW.md
- AGENTS.md
- reports/<RUN_ID>/decision.md
#### 查找线索
- 看 WORKFLOW 的主路径是否简单清晰。
- 看 AGENTS 的门禁是否支持自动化而不是阻碍自动化。
- 看当前 decision 是否已经把重心放在 learn 上。
#### 主线意义
- 这题负责产品视角。
- 常见漂移是为了“爽”去堆功能，而不是收敛结构和减少噪音。

### Q16. 这个项目 codex 的正确打开方式你会吗，所有的 codex 正确的方法你会使用，我们项目中用到了哪些，你能列出来吗？
#### 为什么问这题
这题是技能题，确认 agent 不是只知道项目流程，还知道 Codex CLI 这个执行器该怎么正确使用。
#### 标准答案
会。当前项目中，Codex 的正确打开方式至少包括：讨论模式使用 `codex --sandbox read-only --ask-for-approval never --search`；执行模式使用 `codex --sandbox workspace-write --ask-for-approval on-request --search`；`learn` 使用 `codex app-server` 的 `plan` 协作模式完成真实模型同频；非交互审计和补充能力需要参考 `CODEX_CLI_PLAYBOOK.md` 与 `CODEX_CLI_SOURCE_AUDIT.md`。本项目强调的不是背所有子命令，而是分清讨论、执行、plan、review、ship 的边界，并用官方文档和本地实测来校对用法。
#### 必查文件
- CODEX_CLI_PLAYBOOK.md
- CODEX_CLI_SOURCE_AUDIT.md
- AGENTS.md
#### 查找线索
- 看 PLAYBOOK 里的默认流程和 learn 同频模式。
- 看 SOURCE AUDIT 里的本地源码与官方核对结论。
- 用 AGENTS 核对这些能力在项目中分别处于哪一层。
#### 主线意义
- 这题负责技能上岗。
- 常见漂移是把 Codex CLI 的所有功能都当项目必须路径，或者反过来只会最基本的 chat 用法。

### Q17. 根据最新的 session，你现在做的东西是否偏离了我们现在最重要的任务，你是否认为我们偏离了主线，为什么，接下来我们应该怎么做？
#### 为什么问这题
这题是最终回拉题。它不问知识点，而是判断 agent 能不能把当前执行重新拉回最重要的方向。
#### 标准答案
当前最重要的任务不是扩功能，而是把自动化流程做顺，尤其是把 `learn` 做成真正的同频核心。只要当前动作不能提升 `learn` 的真实性、主线回拉能力、流程自动化体验或文档一致性，就有偏离主线的风险。接下来应该优先做的，是：用 `PROJECT_GUIDE` 作为课程入口，强制 `learn` 用真 Plan 模式完成全量逐题口述和证据引用；同步更新 AGENTS、WORKFLOW、PLAYBOOK；再跑真实 smoke，确认它在实际模型交互里可用。
#### 必查文件
- TASKS/STATE.md
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
