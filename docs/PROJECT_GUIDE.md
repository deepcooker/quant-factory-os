# PROJECT_GUIDE.md

## 一句话北极星

自动化 -> 自我迭代 -> 涌现智能。

## 使用方式

* 这是 `learn` 的主课程、问题库、标准答案和主线锚点。
* 题目本身与整体结构是 owner 精心挑选后的固定课程资产，不应被随意改写、重排或替换。
* 正常允许变化的是：项目变动后同步更新标准答案，或为保持同频质量做最小必要微调。
* `learn` 必须先阅读本文件，再按每题的 `必查文件` 与 `查找线索` 去读取证据。
* 文件阅读统一走 `tools/view.sh`；当前正式支持 `tools/view.sh ...` 和 `python3 tools/view.sh ...`，并兼容历史 `--lines START:END`。
* 如果目标项目尚未接入这套基座、缺少 owner docs，先参考 `scripts/bootstrap_experiment_project.py` 与 `templates/experiment_project/` 做首轮项目学习与文档补齐，再继续使用本题库。
* 这些题的目的不是“考试打分”，而是用高质量提问反向逼模型去读全量 owner docs、run evidence、session continuity 线索，并把主线固化成可复用的证据。
* 如果输出偏到具体细节、工具琐事或单一 bug，而没有回到项目目标、门禁、工作流、当前阶段，就说明已经偏离主线。
* 一旦漂移，不是继续闲聊，而是回到 `PROJECT_GUIDE` 的问题体系里重答，并重新引用证据把模型拉回主线。

### 建议入口顺序

* 新 agent 首轮同频，优先按 `Q1 -> Q2 -> Q5 -> Q6 -> Q7 -> Q8 -> Q17` 作答。
* 这组题的作用分别是：项目定位、当前阶段、宪法、工作流、当前局面、session continuity、最终主线回拉。
* 这组题答稳之后，再继续 `Q3/Q4/Q9...Q16`，避免一开始就陷进局部实现细节。

---

### Q1. 整个项目是做什么的，背景，目标是什么，我最终要什么，我是用什么开发方式来完成这个项目的？

#### 为什么问这题

这题决定 agent 是否理解项目的根目标。如果连项目定位都没对齐，后续所有流程都会变成“会跑命令，但不知道为什么要跑”。

#### 标准答案

`quant-factory-os` 是一个基建型执行与治理系统，目标是把 AI 协作从“依赖聊天记忆”改造成“依赖仓库内证据、状态、门禁和工作流”的工程化闭环。它当前不是业务项目仓，而是在把自动化 AI 研发体系本身做稳，并逐步沉淀成普通窗口可调用的 Python orchestrator / runtime 基座，Codex 通过 app-server 在背后提供运行时智能能力。这个项目的背景是：多窗口、多会话、多 agent 协作时极易丢上下文、偏离主线、重复试错，导致任务、决策、验证、错误和状态散落在聊天里，无法复用，也无法恢复。因此项目要把这些关键内容沉淀进仓库，让新 agent 上岗后能快速同频、知道主线、按规则执行、持续更新文档与证据，并在漂移时被拉回主线。

你最终要的，不是一个“会跑命令的自动化脚本”，而是一套 **AI 研发基座**：它能够围绕主线稳定完成需求澄清、证据核验、任务规划、角色执行、质量治理、缺陷分流、返工 / 重规划 / 讨论、结果汇总、学习回流、恢复续跑、回归验证和新项目接入。开发方式也不是随手改代码，而是沿着正式主线推进：先初始化 baseline，再通过 coach 和问题体系澄清需求，再做 verification 收集证据，再进入需求博弈和校正，再拆 task，再进行多角色执行，再通过 defect triage 做质量治理，再做 merge 和 baseline refresh，最后把 state、evidence、checkpoints、events 和 gate 结果沉淀下来。`PROJECT_GUIDE` 在这里不是说明书，而是反向提问课程：它通过问题体系逼模型去读宪法、工作流、实体、证据和 session 线索，再把主线答出来。

#### 必查文件

* `AGENTS.md`
* `docs/WORKFLOW.md`
* `docs/ENTITIES.md`
* `tools/project_config.json`

#### 查找线索

* 先看项目入口说明，确认项目不是普通业务仓，而是基建/治理仓。
* 再看 `AGENTS.md` 的硬规则和门禁要求。
* 再看 `WORKFLOW` 的状态机，确认这不是普通代码仓，而是流程仓。
* 最后用 `ENTITIES` 理清 `task / run / project / evidence / claim / baseline` 这些名词，并用 `tools/project_config.json` 看当前运行骨架。

#### 主线意义

* 这题是总开关，回答错了，后面所有题都会偏。
* 最常见漂移是把项目理解成“一个脚本工具集”或“一个普通自动化仓库”，忽略治理、同频、证据和恢复。
* 另一种常见漂移是只看到代码与工具，不看到问题方法论和主线校正机制。

---

### Q2. 项目有几个阶段性目标，现在完成到哪个阶段，每个阶段都完成了什么？

#### 为什么问这题

这题用来强制区分 5 个层次：项目愿景、当前阶段、已经验证的能力、正在试点验证中的能力、以及尚未闭合的能力。若这 5 层混在一起，agent 就会把“未来蓝图”误答成“当前已实现”，或者把“试点中”误答成“已稳定可复用”。

#### 标准答案

这个项目当前必须按“愿景 / 当前阶段 / 已验证 / 试点中 / 未闭合”五层来回答。愿景上，它最终要沉淀成普通窗口可执行的 Python orchestrator + app runtime 基座。当前阶段上，它已经从单纯的流程设计推进到**实验线状态机阶段**：需求澄清、verification、correction、planning、角色执行、defect triage、repair / replan / discussion、merge、baseline refresh、resume、events、checkpoints、smoke、gate、bootstrap 都已经在根目录实验线中成形。已验证的能力上，当前已经通过 fake smoke 和 gate 验证了：happy path、major defect -> replan -> targeted rerun、merged -> resume、send_back_to_dev repair、critical discussion block、cycle limit block，以及最小 app runtime contract。试点中的能力上，bootstrap 已经能生成最小可运行接入骨架，并进入 runtime-bundle 模式验证。尚未闭合的能力上，真实 app-server 下整条主链的长期稳定实跑、subagents 真执行、queue/event source、human gates、独立 implementation-critic / review-mediator 仍未完全闭合。因此不能把“实验线已经形成完整状态机样机”误说成“整条正式主线已经在真实环境下长期稳定全自动运行”。

#### 必查文件

* `docs/WORKFLOW.md`
* `tools/project_config.json`
* `TASKS/QUEUE.json`
* `reports/<RUN_ID>/summary.md`
* `tests/run_gate.py`
* `scripts/bootstrap_experiment_project.py`
* `templates/experiment_project/`

#### 查找线索

* 先看 `WORKFLOW.md`，确认 formal mainline 与边界。
* 再看 `tools/project_config.json`，确认当前 skills、thread policy、verification policy、human gates 等配置。
* 再看 `TASKS/QUEUE.json` 和当前 `reports/<RUN_ID>/summary.md`，确认最近一批工作实际推进到了哪。
* 最后看 `tests/run_gate.py`、`scripts/bootstrap_experiment_project.py` 和 `templates/experiment_project/`，确认哪些能力已经进入可验证、可接入阶段。

#### 主线意义

* 这题负责时间定位。
* 最常见漂移是把“最终自动化蓝图”误答成“当前已经实现的能力”，或者把“实验线已证明”误答成“真实环境已长期闭合”。

---

### Q3. 这个项目完成后会形成什么基座能力，接下来第一个落地项目会是什么，你准备怎么承接和落地？

#### 为什么问这题

这题是把“基座仓”与“业务仓”分开，防止把所有问题都堆在一个仓里，造成基建和业务互相污染。

#### 标准答案

基建项目做完后，`quant-factory-os` 这个仓会以 **AI 研发基座** 的形式对外提供：项目级 baseline 学习、需求澄清与证据核验、任务规划、多角色执行、质量治理、恢复续跑、回归 gate 和 bootstrap 接入能力。它当前首先要产出的不是某个具体业务模板，而是一套更稳定的执行与治理运行层，让第二个项目不必重新发明 owner docs、状态机、gate 和 bootstrap。接下来的第一个落地项目，不应理解成“直接把业务逻辑搬进本仓”，而应理解成：**让第二个 coding 项目接入这套基座骨架**，先通过 bootstrap 生成 skeleton / runnable / runtime-bundle，再补项目自己的 owner docs 和业务真相，然后沿基座主线执行。我的承接方式应该是：先确认目标项目是否已接入这套骨架；未接入则先 bootstrap 和补文档；已接入则先同频、确认当前 run 与方向，再进入讨论、规划和执行。

#### 必查文件

* `docs/WORKFLOW.md`
* `docs/ENTITIES.md`
* `scripts/bootstrap_experiment_project.py`
* `templates/experiment_project/`
* `reports/<RUN_ID>/decision.md`

#### 查找线索

* 看 `WORKFLOW`，确认基座提供的是流程骨架，不是业务实现。
* 看 `ENTITIES`，区分 `project / run / task / evidence` 的层级。
* 看 `bootstrap_experiment_project.py` 和 `templates/experiment_project/`，确认新项目是怎么接入这套基座的。
* 看当前 `decision`，确认近期对“基座 vs 业务”的判断。

#### 主线意义

* 这题防止把基建仓做成“所有事都往里塞”的大杂烩。
* 常见漂移是太早业务化，忽视当前更重要的是把接入方式、主线和 gate 做稳。

---

### Q4. 如果把不同 AI 界面或运行时分别作为决策端和执行端，它们应如何保持同频，各自承担什么职责？

#### 为什么问这题

这题负责定义脑和手的协作边界，不然模型会把战略、评审、实现、修复混成一层。

#### 标准答案

不同 AI 界面和运行时可以分成“决策端”和“执行端”，但必须保持同频。当前项目里，网页端更适合做方向讨论、方案反驳、角色博弈和收敛决策；本地执行端更适合做项目级 baseline 学习、session / fork 推进、代码修改、验证和证据回写。它们保持同频的方式不是靠聊天记忆，而是靠 `AGENTS.md`、`PROJECT_GUIDE.md`、`WORKFLOW.md`、`ENTITIES.md`、`tools/project_config.json`、run evidence、events 和 checkpoints 来同步；真正发生漂移时，不应该继续闲聊，而应该回到 `PROJECT_GUIDE` 的问题体系里按题重答并重新绑定证据。

#### 必查文件

* `AGENTS.md`
* `docs/WORKFLOW.md`
* `docs/ENTITIES.md`
* `tools/project_config.json`
* `tools/main.py`

#### 查找线索

* 看 `AGENTS` 的 session gate 和主流程分层。
* 看 `WORKFLOW` 的 state machine 和主线定义。
* 看 `tools/project_config.json` 的 policy 和 skills。
* 看 `tools/main.py` 里 `resume_job()`、events、checkpoints 如何维持同频。

#### 主线意义

* 这题直接决定“同频”是不是靠证据完成。
* 常见漂移是把网页端和 CLI 当成天然共享上下文，或者指望“聊一聊”就能自动对齐。

---

### Q5. 这个项目当前的宪法是什么样的？

#### 为什么问这题

这题判断 agent 是否知道谁是硬规则，谁只是说明文档。

#### 标准答案

当前项目的宪法是 `AGENTS.md`。它定义了任务入口、同频门禁、执行边界、失败协议、文档新鲜度和交付纪律。它不是可选参考，而是 agent 的硬契约。`docs/WORKFLOW.md` 负责补状态机和步骤细节，`PROJECT_GUIDE.md` 负责学习与主线锚点，`docs/ENTITIES.md` 负责名词系统和对象边界，但一切执行边界最终以 `AGENTS.md` 为准。

#### 必查文件

* `AGENTS.md`
* `docs/WORKFLOW.md`
* `docs/ENTITIES.md`

#### 查找线索

* 看 `AGENTS` 里对 learn、run、docs freshness、gate 的硬要求。
* 再看 `WORKFLOW` 理解哪些是流程细节，哪些是宪法。
* 用 `ENTITIES` 确认对象层级和状态边界。

#### 主线意义

* 这题负责分清“规则层”和“说明层”。
* 常见漂移是把任何文档都当宪法，或者只看流程图不看硬门禁。

---

### Q6. 这个项目当前工作流是什么样的？

#### 为什么问这题

这题用于确认 agent 是否知道从哪一步开始、什么时候停、什么时候不能直接改代码。

#### 标准答案

当前工作流已经收敛成一条正式主线：
**baseline 初始化 / 刷新 -> coach 澄清 -> verification -> correction -> planning -> role execution -> active results -> defect triage -> repair / replan / discussion -> merge -> baseline refresh -> state / events / checkpoints -> smoke / gate / bootstrap（配套层）**。
其中，运行主线负责从需求到学习回流；events / checkpoints / resume 是运行保障层；smoke / gate / bootstrap 是配套验证与接入层。复杂需求仍然遵守“先澄清、先证据、再执行”的原则，不能从准备工作直接跳到写代码。真正的主线不是旧的长流程口号，而是**问题驱动学习 + 证据核验 + 状态机执行 + 质量治理 + 学习回流**。

#### 必查文件

* `docs/WORKFLOW.md`
* `AGENTS.md`
* `tools/main.py`

#### 查找线索

* 先看 `WORKFLOW` 里的状态机和主阶段。
* 再看 `AGENTS` 里哪些步骤是硬门禁。
* 最后看 `tools/main.py` 的 `run_job()` / `resume_job()`，确认实验线当前实际怎么跑。

#### 主线意义

* 这题负责把 agent 拉回流程，而不是局部实现细节。
* 常见漂移是还停留在旧流程叙述，或者把验证与接入层误当成每次 job 的主运行层。

---

### Q7. 我们现在的项目有没有未完成的任务呢，最新的批次在讨论什么问题，你是怎么查的？

#### 为什么问这题

这题要求 agent 具备“看当前局面”的能力，而不是只会泛泛复述项目介绍。

#### 标准答案

要看当前有没有未完成任务，先看 `tools/project_config.json` 的运行配置与当前约束，再看 `TASKS/QUEUE.json` 或当前 run 下的 `summary.md / decision.md / events / checkpoints`，最后再结合 gate 和 bootstrap 的最新验证结果。当前最近一批工作的重点，已经从“只讨论流程设计”推进到了“把实验线做成可恢复状态机样机”：主流程、defect triage、repair / replan / discussion、resume、smoke、gate、bootstrap 都已经接上。现在仍未完全闭合的重点主要是：真实 app-server 下的整条主链长期实跑、subagents 真执行、queue / event job source、human gates、以及更独立的 discussion 角色能力。也就是说，当前批次讨论的核心，不再是“要不要有这套主线”，而是“怎么把这套主线从实验线进一步做稳、做实、做成可复制基座”。

#### 必查文件

* `tools/project_config.json`
* `TASKS/QUEUE.json`
* `reports/<RUN_ID>/summary.md`
* `reports/<RUN_ID>/decision.md`
* `state/events.jsonl`
* `state/test_reports/gate_summary.json`

#### 查找线索

* 先看当前 run/task 指针和 queue。
* 再看 `summary / decision` 确认最近一批工作的方向。
* 再看 `events` 和 `gate_summary`，确认哪些已经真实过 gate，哪些还只是设计。

#### 主线意义

* 这题把学习拉回“当前在做什么”。
* 常见漂移是只会讲历史和蓝图，不知道当前批次到底在收什么口。

---

### Q8. 你查了最近的 session 说了什么，你是从哪里查的？

#### 为什么问这题

这题要求 agent 具备 session continuity，不然一换会话就会忘掉当前主线。

#### 标准答案

最近 session 的内容应该从仓库证据里查，不应该靠聊天记忆猜。最重要的来源是当前 `RUN_ID` 下的 `summary.md`、`decision.md`、`events`、`checkpoints`，必要时再看相关 `conversation` 沉淀。根据当前证据，最近 session 的主线已经明确为：实验线已经形成可恢复状态机，重点是继续把这条主线和接入方式做稳，而不是重新发明新流程。当前最近连续几轮已经把：需求澄清、verification、correction、planning、角色执行、defect triage、repair / replan / discussion、merge、baseline refresh、resume、smoke、gate、bootstrap 一路收上来了；接下来更像是在补剩余边界，而不是从零开始定义方法论。

#### 必查文件

* `reports/<RUN_ID>/summary.md`
* `reports/<RUN_ID>/decision.md`
* `state/events.jsonl`
* `state/checkpoints/`

#### 查找线索

* 优先看 summary 和 decision，而不是先读全量聊天记录。
* 再看 events / checkpoints 还原最近几轮实际推进。
* 对总结存疑时，再回溯 conversation 沉淀。

#### 主线意义

* 这题是“主线连续性”的核心。
* 常见漂移是把当前 session 理解成全新任务，忽略前面已经收敛的方向。

---

### Q9. 项目需求讨论应该使用什么流程？

#### 为什么问这题

这题负责把“讨论”和“执行”分开，防止先写代码后补理由。

#### 标准答案

项目需求讨论现在应挂在正式主线上做：先有 learning baseline，同频项目长期真相；再接收原始需求，通过 coach 做第一轮澄清，产出 `clarified_job_v1 + claims`；接着进入 verification，把猜测变成 evidence；证据回来后，再由 coach 二次修正，形成 `clarified_job_v2`；之后再进入 `demand_critic / solution_designer / risk_reviewer` 的需求博弈，最终形成 `corrected_job`，满足 planning gate 后才允许拆 task。run 级需求收敛至少要问清：背景与目标、必须做 / 应该做 / 可以做、明确不做项、影响模块与外部依赖、异常流与非功能约束、以及后续如何验收。

#### 必查文件

* `docs/WORKFLOW.md`
* `AGENTS.md`
* `PROJECT_GUIDE.md`
* correction 相关 skills

#### 查找线索

* 在 `WORKFLOW` 里找 coach、verification、correction、planning 的先后关系。
* 在 `AGENTS` 里看“先澄清、先证据、再执行”的门禁。
* 在 `tools/main.py` 里看 `coach_round_v1 / verification_round / coach_round_v2 / correction_round`。

#### 高质量追问模板

* 这次需求真正要解决的业务问题是什么，为什么现在必须做？
* 本轮 run 的必须做 / 应该做 / 可以做分别是什么，哪些明确不做？
* 影响到哪些模块、数据、外部系统或角色，边界在哪里？
* 如果不按用户原话里的实现方案做，是否有更简单、更低耦合的系统实现？
* 后续怎么验收，哪些异常流、非功能约束和风险必须提前写清？

#### 自我梳理输出骨架

* `run_goal`: 这轮 run 真正要解决的问题
* `scope`: 当前明确纳入范围的模块、流程、数据和角色
* `non_goals`: 本轮明确不做的内容
* `impacted_modules`: 受影响模块、外部系统或依赖
* `risks`: 已知风险、异常流、潜在冲突
* `non_functional_constraints`: 性能、稳定性、安全、审计、环境约束
* `acceptance`: 后续如何判断这轮 run 可以进入 task 拆分

#### 主线意义

* 这题负责守住“讨论先于执行”。
* 常见漂移是跳过 coach / verification / correction，直接把原始需求推进成实现任务。

---

### Q10. 项目实施流程是什么，需要哪些角色协作，如何保证角色独立思考，目前实现到了什么程度？

#### 为什么问这题

这题不是让 agent 列角色，而是确认它是否真正区分了三件事：当前已经正式化的实施流程、当前只具备最小实现的角色能力、以及仍属于未来态 / 理想态的协作能力。若这三层混在一起，agent 就会把“希望中的多角色协作结构”误答成“当前已经稳定落地的实施能力”。

#### 标准答案

当前项目的实施流程，正式化部分已经收敛为：baseline 学习 -> coach / verification / correction -> task planning -> role execution -> defect triage -> repair / replan / discussion -> merge -> baseline refresh -> state / audit / resume。角色协作能力上，当前已正式化的是：

* `run_manager`：当前 job 的项目经理与汇总者
* `project_coach`：需求澄清与主线纠偏
* `dev_worker`：实现与修复
* `test_worker`：独立质量验证
* `arch_reviewer`：架构与边界评估
* `demand_critic / solution_designer / risk_reviewer`：需求博弈与路径选择
* `defect_triage`：质量分流

其中，`test_worker` 不是 `dev_worker` 的附庸，而是独立质量角色，它应从需求、功能、流程、数据/状态、非功能几个维度审视结果。角色独立性主要靠：session/thread 隔离、schema 化输出、merge 前的 defect triage、以及最终由 `run_manager` 去噪汇总。当前仍属于未来态或继续硬化中的，是：真实运行时下的长期稳定多角色 orchestration、subagents 真并行、以及更独立的 implementation-critic / review-mediator 角色。

#### 必查文件

* `docs/WORKFLOW.md`
* `AGENTS.md`
* `tools/project_config.json`
* role worker / correction / defect triage 相关 skills

#### 查找线索

* 先看 `WORKFLOW`，确认当前 formal mainline 和角色链。
* 再看 `tools/project_config.json`，确认正式注册了哪些 skills。
* 再看 `tools/main.py`，确认 triage、repair、replan、discussion 的真实执行边界。

#### 高质量追问模板

* 这次 task 是否只需要 `dev/test`，还是已经复杂到需要额外 `arch`？
* 哪些判断应该由 run 层拍板，哪些必须让角色独立结论后再回收？
* `test` 需要独立覆盖哪些功能、流程、数据、非功能验证面？
* 当前系统已经实现到了角色链的哪一层，哪些还只是目标态？

#### 自我梳理输出骨架

* `role_plan`: 本次是否只需要 `dev/test`，还是需要增加 `arch`
* `role_responsibilities`: run-main / coach / dev / test / arch / triage 各自负责什么
* `verification_axes`: 这次至少要覆盖哪些验证面
* `current_capability_gap`: 当前仓库已经实现到哪一层，哪些仍是目标态

#### 主线意义

* 这题负责防止 agent 把“理想协作结构”误说成“当前实现程度”。
* 只要回答里没有区分正式化流程、已实现角色能力、和未来态能力，就说明它还没有真正理解项目实施边界。

---

### Q11. 项目中的核心对象、关键状态和交付单元分别是什么，它们的生命周期是怎样的？

#### 为什么问这题

这题负责统一名词系统，避免 agent 在 task、run、project 这些层级上混乱。

#### 标准答案

`project` 是最高层项目维度，负责项目级配置、baseline 学习和长期主线；`job` 是一次进入系统的工作单；`run` 是一次需求方向或执行周期；`task` 是从 `corrected_job` 中拆出来的最小执行单元；`thread` 是一个会话运行单元；`claim` 是待验证判断；`evidence` 是支持或反驳 claim 的证据；`merge_result` 是项目级收敛结果；`baseline_snapshot` 是长期真相快照；`PR` 是 Git 交付单元。关键状态至少包括：`NEW / COACHED / VERIFIED / CORRECTED / PLANNED / EXECUTING / MERGED / DONE / BLOCKED...` 以及 defect 侧的 `DEFECT_REPAIRING / DEFECT_REPLANNING / DEFECT_DISCUSSING / DEFECT_BLOCKED / READY_TO_MERGE`。生命周期更接近：
`PROJECT baseline -> RUN / JOB intake -> claims & evidence -> corrected job -> task plan -> role execution -> defect governance -> merge -> baseline refresh -> ship / gate / history`

#### 必查文件

* `docs/ENTITIES.md`
* `docs/WORKFLOW.md`
* `tools/main.py`

#### 查找线索

* 先看 `ENTITIES` 的名词定义。
* 再看 `WORKFLOW` 里的状态流转。
* 最后用 `tools/main.py` 看 Job / Thread / state / defect_status 实际如何落盘。

#### 高质量追问模板

* 这次信息属于 project、job、run、task 还是 thread summary，放错层会造成什么混乱？
* 哪些边界应该属于 run，哪些验证与修复细节应该属于 task？
* 当前更该沉淀的是 thread result、task summary 还是 run/merge summary？

#### 自我梳理输出骨架

* `object_layer`: 当前信息属于哪一层
* `run_fields`: 应沉淀到 run 的边界与聚合字段
* `task_fields`: 应沉淀到 task 的实现、风险和验证字段
* `summary_target`: 当前更适合生成什么层级的总结

#### 主线意义

* 这题负责名词统一。
* 很多漂移不是逻辑错，而是对象层级搞混了。

---

### Q12. 我们在项目的准备工作做好后，我们一个需求讨论方向，从流程的哪一步开始？

#### 为什么问这题

这题确认“准备完成后做什么”，避免准备完成后还直接跳到写代码。

#### 标准答案

准备工作完成后，分两种情况。若目标项目已经完成首轮接入，则从**主运行流程**开始：接收 `raw_request`，进入 coach 澄清、verification、correction，满足 planning gate 后再拆 task。若目标项目尚未完成首轮接入，则第一步不是直接 baseline 学习或实现，而是先按 `scripts/bootstrap_experiment_project.py` 做 bootstrap：先生成 skeleton / runnable / runtime-bundle 骨架，补 owner docs，确认最小 core skills 和最小 gate 能跑，再进入正式主运行流程。也就是说，准备工作之后的第一步始终是：**先建立理解和边界，再进入执行**，而不是一准备好就写代码。

#### 必查文件

* `docs/WORKFLOW.md`
* `AGENTS.md`
* `scripts/bootstrap_experiment_project.py`
* `templates/experiment_project/`
* 当前 `reports/<RUN_ID>/summary.md`

#### 查找线索

* 看 `WORKFLOW` 里的正式主线入口。
* 看 `bootstrap_experiment_project.py` 和 `templates/experiment_project/` 区分 skeleton / runnable / runtime-bundle。
* 看当前 run summary 是否已经有方向收敛结果。

#### 高质量追问模板

* 在创建 task 之前，这轮 run 的背景目标、范围边界、不做项和验收条件是否已经清楚？
* 还有哪些影响模块、依赖、异常流或非功能要求没有在 run 层说明白？
* 如果现在直接进入实现，最可能漏掉的边界和回归面是什么？

#### 自我梳理输出骨架

* `task_ready`: 当前是否已经满足创建 task 的前提
* `missing_boundaries`: 仍未说清的边界、依赖、异常流、非功能要求
* `first_task_candidate`: 最小可执行 task 候选是什么
* `why_not_code_yet`: 如果还不能进实现，当前阻塞点是什么

#### 标准化 Markdown 草稿模板

当 AI 读完杂乱输入后，先输出一版标准化 intake 草稿，再进入 run 方向收敛与 task 拆分；这一步是协议层草稿，不是机器真相源。

```md
# Run Intake Draft

## 1. Background
- 业务背景：
- 当前痛点：
- 为什么现在要做：

## 2. Run Goal
- 本轮 run 要解决的问题：
- 期望产出：

## 3. Scope
- 明确纳入范围：
- 涉及模块/流程/数据：
- 外部系统/依赖：

## 4. Non-Goals
- 本轮明确不做：

## 5. Impacted Modules
- 模块：
- 数据面：
- 角色面：

## 6. Risks And Abnormal Flows
- 已知风险：
- 异常流：
- 仍不清楚的边界：

## 7. Non-Functional Constraints
- 性能：
- 稳定性：
- 安全/审计：
- 环境/部署：

## 8. Acceptance
- 如何判断 run 已收敛到可以拆 task：
- 必要验证面：

## 9. Role Plan
- run-main：
- coach：
- dev：
- test：
- arch（如需要）：

## 10. Task Candidates
- 候选 task 1：
- 候选 task 2：
- 为什么它们是最小切片：

## 11. Open Questions
- 还需要用户或 owner 明确什么：

## 12. Summary Target
- 当前应先形成：
  - clarified_job / corrected_job / task_plan
- 暂不进入实现的原因：
```

#### 主线意义

* 这题负责接上岗后的下一步。
* 常见漂移是把环境准备、bootstrap 或 baseline 学习误当成“已经可以直接改代码”。

---

### Q13. 项目的分支与交付管理规则是什么，当前是否满足需求？

#### 为什么问这题

这题用于校准交付纪律，避免“本地能跑就行”而没有分支/PR 约束。

#### 标准答案

当前交付层的原则仍然是：每次可交付改动都应能对应回项目、job/run、task 和证据。实验线当前的重心虽然放在状态机、gate、bootstrap 和运行主线上，但交付纪律并没有消失：验证、证据、文档、gate 通过后，再进入 Git/PR 交付层；若 PR 当前不可 clean merge，应明确返回状态，而不是隐藏失败。当前项目真正强调的不是复杂分支模型，而是**可审计、可回滚、可对齐证据的交付单元**。

#### 必查文件

* `AGENTS.md`
* `docs/WORKFLOW.md`
* 交付层相关脚本或文档
* `state/test_reports/gate_summary.json`

#### 查找线索

* 看 `AGENTS` 的 PR discipline。
* 看 `WORKFLOW` 里 ship/gate/交付边界。
* 看当前是否已经把验证与文档更新纳入交付前提。

#### 主线意义

* 这题负责交付边界。
* 常见漂移是只关注本地改动，不关注如何形成干净、可回滚、可审计的交付单元。

---

### Q14. 每次做完任务，你必须要做什么事情？

#### 为什么问这题

这题是执行闭环问题，用来确认 agent 知道“写完代码不是结束”。

#### 标准答案

每次做完任务，至少必须完成这些动作：

1. 验证结果是否满足需求、功能、流程、数据/状态和非功能要求；
2. 更新证据、events、checkpoints 和必要的 state；
3. 如果主线、规则、文件映射、接入方式或验证方式改变了，更新 owner docs；
4. 运行最小 smoke / gate，确认没有把实验线打坏；
5. 若进入交付层，再做 Git/PR 相关动作。

最少要把 Why / What / Verify / Risk 说清楚，把结果沉淀到 run evidence 和文档里。没有验证、没有证据、没有文档更新，就不算完成。

#### 必查文件

* `AGENTS.md`
* `docs/WORKFLOW.md`
* `reports/<RUN_ID>/summary.md`
* `reports/<RUN_ID>/decision.md`
* `tests/run_gate.py`

#### 查找线索

* 看 `AGENTS` 的 evidence gate 和 docs freshness gate。
* 看 `WORKFLOW` 的 merge / baseline refresh / ship 前提。
* 看 gate 文档与测试入口，确认最小验证怎么跑。

#### 主线意义

* 这题负责把“完成”定义清楚。
* 常见漂移是把“代码写完”误当“任务完成”。

---

### Q15. 如果目标体验是高质量、低噪音、强自动化，当前最需要优先优化什么？

#### 为什么问这题

这题用来防止局部最优。项目是基建，就必须优先优化通用流程，而不是只修某一个具体命令。

#### 标准答案

当前最需要优先优化的，不是继续堆新功能，而是把已经成立的新主线在真实运行环境里继续收稳。优先级更像：

1. 真实 app-server 下整条主线的长期稳定验证；
2. 把现有状态机、defect 治理、resume、gate 保持一致，不让实验线文档与代码脱节；
3. 逐步补齐 subagents、queue / event source、human gates 等尚未闭合能力；
4. 继续把 bootstrap / runtime-bundle 做成更稳的可复制接入层。

也就是说，当前最值钱的不是“再加命令”，而是把 baseline / session / role execution / quality governance / gate 这条底层结构继续做稳。

#### 必查文件

* `docs/WORKFLOW.md`
* `AGENTS.md`
* `reports/<RUN_ID>/decision.md`
* `tests/run_gate.py`
* `scripts/bootstrap_experiment_project.py`
* `templates/experiment_project/`

#### 查找线索

* 看 `WORKFLOW` 的主路径是否简单清晰。
* 看 `decision` 是否已经把重心放在收稳主线而不是堆功能。
* 看 `run_gate` 和 bootstrap 是否已经成为正式入口。

#### 主线意义

* 这题负责产品视角。
* 常见漂移是为了“看起来更强”去堆功能，而不是收敛结构、减少噪音和补稳闭环。

---

### Q16. 这个项目中 AI/工具系统的正确打开方式是什么，当前用到了哪些能力，你能列出来吗？

#### 为什么问这题

这题不是让 agent 背命令，而是确认它是否真正理解项目中的 AI/工具系统分层。只知道命令名不代表知道“什么问题该交给哪一层解决”；如果把运行主线、验证层、接入层混在一起，agent 就会误用工具，或者把过渡态能力误说成已经正式化。

#### 标准答案

当前项目中的 AI/工具系统，正确打开方式不是先背命令，而是先分层。
第一层是**运行主线层**：由 `orchestrator + app runtime + skills + schemas + state` 组成，负责 baseline、coach、verification、correction、planning、角色执行、defect triage、merge、baseline refresh、resume。
第二层是**验证与发布层**：由 smoke、gate、integration real app smoke 组成，负责证明主线没坏。
第三层是**接入层**：由 bootstrap、skeleton / runnable / runtime-bundle 组成，负责把第二个项目接进来。

当前已经正式化的能力，是这三层的基本边界与实验线主线本身。当前仍属于边界或过渡态的，是：真实全链路长期运行、subagents 真执行、queue / event source、human gates 和更独立的 discussion 角色能力。正确打开方式的关键不是把所有脚本背全，而是先判断：这是运行主线问题、验证问题，还是接入问题；只有弄清这一层，才知道该用哪部分系统。

#### 必查文件

* `AGENTS.md`
* `docs/WORKFLOW.md`
* `tools/project_config.json`
* `tools/main.py`
* `tests/run_gate.py`
* `scripts/bootstrap_experiment_project.py`
* `templates/experiment_project/`

#### 查找线索

* 先看 `WORKFLOW`，确认运行主线是什么。
* 再看 `tools/project_config.json`，确认 skills 和 policy。
* 再看 `tools/main.py`，确认主入口状态机。
* 再看 `run_gate`、`bootstrap_experiment_project.py` 和 `templates/experiment_project/`，确认验证层与接入层。

#### 主线意义

* 这题负责“正确打开方式”的分层判断，不负责命令清单介绍。
* 只要回答仍停留在“有哪些命令”，却没有说清运行主线、验证层、接入层三层边界，就说明 agent 还没有真正吃透项目中的 AI/工具系统分层。

---

### Q17. 根据最新的 session，你现在做的东西是否偏离了我们现在最重要的任务，你是否认为我们偏离了主线，为什么，接下来我们应该怎么做？

#### 为什么问这题

这题是最终回拉题。它不问知识点，而是判断 agent 能不能把当前执行重新拉回最重要的方向。

#### 标准答案

当前最重要的任务，不是重新发明流程，也不是继续堆很多新层，而是把已经成立的实验线主线收稳，并把文档、代码、gate、bootstrap 持续保持一致。只要当前动作不能提升这条主线、不能让 `PROJECT_GUIDE` 更像通用学习协议、不能让运行主线 / defect 治理 / resume / gate / bootstrap 更稳定，就有偏离风险。当前并不算已经偏离主线，因为最近连续几轮工作确实都在围绕主线收口；但如果接下来继续大幅扩散概念、跳过真实验证、或者重新改写题库而不是更新答案，就很容易偏。接下来应该优先做的，是继续把：

* `PROJECT_GUIDE`
* `WORKFLOW`
* `ENTITIES`
* gate
* bootstrap
* 真实 app-server 验证
  这些东西收成一致的基座资产，同时有选择地补齐剩余未闭合能力，而不是再随意开新主线。

#### 必查文件

* `tools/project_config.json`
* `reports/<RUN_ID>/summary.md`
* `reports/<RUN_ID>/decision.md`
* `docs/WORKFLOW.md`
* `tests/run_gate.py`
* `scripts/bootstrap_experiment_project.py`
* `templates/experiment_project/`

#### 查找线索

* 看当前 run 的 summary/decision，确认最近连续几轮都在收敛什么。
* 看 `WORKFLOW` 和 `PROJECT_GUIDE` 是否已经同步。
* 用这题检查自己当前做的事，是否真的在强化主线，而不是制造新的偏移。

#### 主线意义

* 这题就是主线回拉器。
* 常见漂移是被单个实现细节、新想法或旧版流程拖住，忘了当前最重要的任务是把已经成立的新主线做稳、做实、做成可复制基座。
