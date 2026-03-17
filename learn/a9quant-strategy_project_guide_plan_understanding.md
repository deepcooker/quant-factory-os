# a9quant-strategy PROJECT_GUIDE 理解稿

## 说明
- 这是针对 `/root/a9quant-strategy` 的 plan 级理解稿。
- 它不是最终 owner doc，也不会在这一步直接覆盖目标项目文件。
- 它的作用是：先按 `PROJECT_GUIDE` 题目结构把理解摊开给 owner 审，再决定如何逐题改目标项目的 `PROJECT_GUIDE.md`。

## 一句话北极星
把当前这套以 Bitget 为首个落地场景的交易运行时系统讲清楚、守住风险与执行边界、用 owner docs 把实现证据沉淀成可维护知识。

## 使用方式
- 这不是最终答案，而是“按题理解”的审稿版本。
- 每题都保留问题导向，但当前先展示“我现在的理解”和它依赖的证据。
- owner 应优先判断：题目是否还需要调整、当前理解是否正确、哪些证据还不够。

### Q1. 整个项目是做什么的，背景，目标是什么，我最终要什么，我是用什么开发方式来完成这个项目的？
#### 为什么问这题
这题决定 AI 是否知道这个仓库到底是“纯愿景文档”“单一策略脚本”还是“已经存在真实运行时骨架的交易系统”。
#### 当前理解答案
`a9quant-strategy` 不是通用 AI 流程仓，也不是只停留在策略想法层的仓库。它本质上是一个以 Bitget 为第一落地场景、带有机构级资管愿景的交易运行时项目，正在把更大的“中央银行式资管体系”愿景压缩进已经实现的控制器、状态、风控、策略、OMS 和交易所桥接架构里。它当前最重要的目标，不是从零发明新架构，而是把现有实现讲清楚、守住 live/risk/config 边界，并逐步沉淀成可维护 owner docs。
#### 必查文件
- `README.md`
- `main_controller.py`
- `advanced_risk.py`
- `tiny_oms.py`
#### 查找线索
- 看 README 里对“机构级量化交易基座”和“Bitget 首个落地交易所”的表述。
- 看 `main_controller.py` 是否真的是系统组合根。
- 看 `advanced_risk.py` 和 `tiny_oms.py` 是否构成真实风控门与执行门。
#### 主线意义
- 这题是总开关，答错了会把项目误当成概念仓或策略脚本仓。
#### 证据锚点
- `README.md`
- `main_controller.py`
- `advanced_risk.py`

### Q2. 项目有几个阶段性目标，现在完成到哪个阶段，每个阶段都完成了什么？
#### 为什么问这题
这题负责时间定位，避免把终极愿景和当前实现态混成一层。
#### 当前理解答案
这个项目至少有三层阶段：第一层是顶层愿景与资管哲学；第二层是把愿景压成控制器、同步层、状态账本、风控、策略引擎、OMS 和桥接层的实现骨架；第三层是做 owner docs、配置卫生、交易门禁和验证面的持续加固。当前它显然已经越过“只有想法”的阶段，因为主入口、同步层、状态对象、风险门、执行边界和测试都已经存在。现在更准确的位置是“实现骨架已成型，但文档、配置卫生和交易所抽象还没跟上”。
#### 必查文件
- `README.md`
- `docs/中央银行设计.md`
- `main_controller.py`
- `test_integration.py`
- `test_regression.py`
#### 查找线索
- 从原始 docs 看愿景和制度层。
- 从主入口和 tests 看当前真实落地层。
#### 主线意义
- 这题用来防止把风险和耦合写成“尚未实现”，也防止把愿景写成“已经交付”。
#### 证据锚点
- `README.md`
- `docs/中央银行设计.md`
- `main_controller.py`
- `test_integration.py`
- `test_regression.py`

### Q3. 这个项目完成后会形成什么系统能力，接下来第一个落地目标会是什么，你准备怎么承接和落地？
#### 为什么问这题
这题是为了区分“长期系统能力”和“当前最现实的落地目标”。
#### 当前理解答案
如果这个项目继续走对方向，它形成的将是一套真实可解释、可验证、可控门的交易运行时基础，而不是空泛的“量化平台”。眼下最现实的落地目标不是再扩大愿景，而是把当前 Bitget 中心化 runtime 讲清楚、跑稳、把配置与环境耦合清理出来。承接方式也不应该是先加功能，而是先收 owner docs、再明确本轮需求落在哪一层、再切最小 task。
#### 必查文件
- `README.md`
- `config.json`
- `replay_runner.py`
- `test_regression.py`
#### 查找线索
- 看当前 config、回放和测试更像是在证明“可运行”和“可维护”，还是在证明“平台化分发”。
#### 主线意义
- 这题负责避免继续把项目拉回抽象平台叙事。
#### 证据锚点
- `README.md`
- `config.json`
- `replay_runner.py`
- `test_regression.py`

### Q4. 如果把不同 AI 界面或运行时分别作为决策端和执行端，它们应如何保持同频，各自承担什么职责？
#### 为什么问这题
这题负责把“看文档做判断”和“改代码做验证”分开，避免混成一个聊天输出。
#### 当前理解答案
决策端 AI 更适合做文档理解、主线对齐、风险识别和边界拆分；执行端 AI 更适合读代码、跑验证、做最小改动和补证据。它们保持同频的方式不应该是记聊天，而应该是共同依赖 owner docs、代码证据和测试证据。对这个项目来说，任何一端都不应该绕开风险门、状态真相源和测试面直接下结论。
#### 必查文件
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`
- `test_integration.py`
#### 查找线索
- 看规则、主线、对象和验证面是否已经能支持“先判断、后执行”的协作。
#### 主线意义
- 这题负责脑手分工，避免把局部代码感觉当整体判断。
#### 证据锚点
- foundation 的 owner docs
- 目标项目的 tests 与关键 runtime 文件

### Q5. 这个项目当前的宪法是什么样的？
#### 为什么问这题
这题确保 AI 先知道哪些边界不能破，再进入实现。
#### 当前理解答案
这个项目当前真正的宪法是运行时边界：`main_controller.py` 是组合根，`data_synchronizer.py` 是原始状态真相源，`account_state.py` 是业务状态账本，`advanced_risk.py` 是集中审批门，`tiny_oms.py` 是唯一应该被接受的执行边界，真实交易必须经过 config + env 双门。当前还必须把 sandbox credentials、proxy defaults 和 Bitget 中心化耦合当成显式风险，而不是当成默认安全状态。
#### 必查文件
- `advanced_risk.py`
- `tiny_oms.py`
- `data_synchronizer.py`
- `config.json`
#### 查找线索
- 看这些门是否被主线真实使用，而不是只在文档里存在。
#### 主线意义
- 这题是进入实现前的硬边界题。
#### 证据锚点
- `main_controller.py`
- `advanced_risk.py`
- `tiny_oms.py`
- `config.json`

### Q6. 这个项目当前工作流是什么样的？
#### 为什么问这题
这题确认 AI 是否知道真实 runtime mainline，而不只是会列模块清单。
#### 当前理解答案
这个项目的真实工作流已经是已实现主线：读取配置，构建控制器，初始化交易所适配器、同步层、状态账本、风险层、行情层、OMS、WS 桥和策略引擎，再通过主循环完成状态刷新、策略评估、intent 生成、风险审批、OMS 执行和回补。这个流程是已实现主线，不是未来设计图。
#### 必查文件
- `main_controller.py`
- `data_synchronizer.py`
- `advanced_risk.py`
- `tiny_oms.py`
#### 查找线索
- 看主循环、状态更新、审批和执行之间是否真的闭合。
#### 主线意义
- 这题负责 runtime 主线对齐。
#### 证据锚点
- `main_controller.py`
- `data_synchronizer.py`
- `advanced_risk.py`
- `tiny_oms.py`

### Q7. 我们现在的项目有没有未完成的任务呢，最新一批在补什么问题，你是怎么查的？
#### 为什么问这题
这题负责区分“已有实现”和“仍需治理/补证据”的部分。
#### 当前理解答案
当前未完成的重点，并不是“交易系统还没搭起来”，而是“治理和说明层还没收稳”。更具体地说，未完成项集中在 owner docs 质量、config/credential 卫生、Bitget 中心化假设，以及当前环境下我们还没真正执行目标测试。
#### 必查文件
- `config.json`
- `ccxt_utils.py`
- `test_integration.py`
- `test_regression.py`
#### 查找线索
- 看 sample config、测试块和回放验证面还存在哪些环境耦合或未验证路径。
#### 主线意义
- 这题防止把“主循环存在”误当成“项目已经收完了”。
#### 证据锚点
- `config.json`
- `ccxt_utils.py`
- 当前 owner docs 生成过程暴露的问题

### Q8. 你查了最近的学习/讨论线索说了什么，你是从哪里查的？
#### 为什么问这题
这题负责 session continuity，避免每次都像第一次接触项目。
#### 当前理解答案
这个目标项目当前的连续性主要来自 README、原始设计文档、代码读取和本轮生成的 owner docs 草稿，而不是像 foundation 仓那样已经有长期 run summary / decision history 可依赖。也就是说，这个项目当前的 continuity 还是“文档 + 代码 + 本轮理解证据”，不是“成熟 evidence 仓”。
#### 必查文件
- `README.md`
- `docs/*.md`
- 当前 owner docs
#### 查找线索
- 优先看 README、原始 docs、代码与当前生成草稿，不要假设已经存在成熟 run evidence。
#### 主线意义
- 这题防止伪造不存在的仓库记忆结构。
#### 证据锚点
- `README.md`
- `docs/梦想中的交易资管财富系统想法.md`
- `docs/资管双向原始想法.md`
- `docs/中央银行设计.md`

### Q9. 项目需求讨论应该使用什么流程？
#### 为什么问这题
这题负责把需求讨论拉回“先定层、先定边界”，而不是直接谈怎么改。
#### 当前理解答案
这个项目的需求讨论首先要判断改动落在哪一层：controller、synchronizer、typed state、risk gate、engine、OMS、exchange adapter、config hygiene，还是 tests/replay。只有层级清楚了，后面才好切最小 task。
#### 必查文件
- `docs/中央银行设计.md`
- `main_controller.py`
- `advanced_risk.py`
- `tiny_oms.py`
#### 查找线索
- 先判断是策略问题、风控问题、状态问题、执行问题还是配置/验证问题。
#### 主线意义
- 这题负责把讨论收成边界，而不是直接跳实现。
#### 证据锚点
- `docs/中央银行设计.md`
- `main_controller.py`
- `advanced_risk.py`
- `tiny_oms.py`

### Q10. 项目实施流程是什么，需要哪些角色协作，如何保证角色独立思考，目前实现到了什么程度？
#### 为什么问这题
这题负责把实现视角和验证视角拆开，避免单线程盲改。
#### 当前理解答案
即使目标项目自身还没有 foundation 仓那种成熟自动化治理层，实施时也应该保持 `run-main / dev / test` 的视角分离。`run-main` 负责范围和方向收敛，`dev` 负责实现与局部验证，`test` 负责独立挑战与回归。当前实现已经有主入口、风险门、状态层、执行边界和测试面，但 owner docs 和治理层仍然偏弱。
#### 必查文件
- `test_integration.py`
- `test_regression.py`
- `replay_runner.py`
#### 查找线索
- 看现有测试是否足以支持独立 test 视角，而不是只做开发自证。
#### 主线意义
- 这题负责防止把“已有测试”误当成“角色协作已经完美落地”。
#### 证据锚点
- `test_integration.py`
- `test_regression.py`
- `replay_runner.py`

### Q11. 项目中的核心对象、关键状态和交付单元分别是什么，它们的生命周期是怎样的？
#### 为什么问这题
这题负责统一对象语言，避免 `controller/state/risk/intent/order` 混成一层。
#### 当前理解答案
这个项目的核心对象语言是运行时对象语言，而不是抽象平台语言：`MainController`、`DataSynchronizer`、`AccountState`、`RiskManager`、`MarketDataHub`、`TrendEngine`、`SharkEngine`、`TinyOMS`、`BitgetWSBridge/BaseBitgetWsClient`，以及 `contracts.py` 里的 typed objects。状态流是：交易所 WS/REST -> synchronizer 原始真相 -> typed state -> 风控/策略快照 -> intent -> OMS -> 回补同步。
#### 必查文件
- `contracts.py`
- `account_state.py`
- `data_synchronizer.py`
- `tiny_oms.py`
#### 查找线索
- 看 typed contracts 和状态快照边界是怎么形成的。
#### 主线意义
- 这题负责对象去混乱。
#### 证据锚点
- `contracts.py`
- `account_state.py`
- `data_synchronizer.py`
- `tiny_oms.py`

### Q12. 准备工作做好后，一个需求讨论方向，从流程的哪一步开始？
#### 为什么问这题
这题确认“进入改动前”的第一动作，避免准备完就盲改。
#### 当前理解答案
准备工作做完后，第一步不是写代码，而是先做 run 方向收敛：这次要动哪一层、边界是什么、什么必须不动、验证要覆盖什么，再决定最小 task。对这个项目来说，常见切口是 controller、synchronizer、state、risk、engine、OMS、config 或 tests。
#### 必查文件
- 当前 `FILE_INDEX` / `TOOLS_METHOD_FLOW_MAP` 草稿
- `main_controller.py`
- tests
#### 查找线索
- 先按阅读顺序找最短路径，再根据 flow map 决定最先补的证据。
#### 主线意义
- 这题负责把准备层接到执行层。
#### 证据锚点
- `main_controller.py`
- `test_integration.py`
- `test_regression.py`

### Q13. 项目的分支与交付管理规则是什么，当前是否满足需求？
#### 为什么问这题
这题负责交付纪律，避免“本地能跑就行”。
#### 当前理解答案
这个目标项目目前还没有像 foundation 仓那样成熟写清的分支和交付治理文档。现阶段最稳的规则应该是：任何实质改动都要能对回对象层、风险门和验证面；高风险变更必须配测试或回放证据；配置和凭据类清理必须与功能改动边界分清。
#### 必查文件
- `README.md`
- `test_integration.py`
- `test_regression.py`
#### 查找线索
- 看当前是否已经有足够验证面支撑安全交付。
#### 主线意义
- 这题负责把代码变动变成可审计交付。
#### 证据锚点
- `test_integration.py`
- `test_regression.py`

### Q14. 每次做完任务，你必须要做什么事情？
#### 为什么问这题
这题负责定义“完成”，防止把编码结束当交付结束。
#### 当前理解答案
在这个项目里，“完成一个任务”至少意味着：确认是否触碰 live gate / risk gate / synchronizer truth / OMS boundary，补足对应验证面，更新 owner docs，并显式保留当前仍存在的风险。代码变了但这些没回收，就不能算闭环。
#### 必查文件
- `advanced_risk.py`
- `tiny_oms.py`
- tests 和 replay 文件
#### 查找线索
- 看这次改动动的是哪个门，再回头检查验证和文档是否收回。
#### 主线意义
- 这题负责闭环。
#### 证据锚点
- `advanced_risk.py`
- `tiny_oms.py`
- `test_integration.py`
- `test_regression.py`

### Q15. 如果目标体验是高质量、低噪音、强自动化，当前最需要优先优化什么？
#### 为什么问这题
这题防止继续堆功能，而不先收真正的底层问题。
#### 当前理解答案
当前最该优先优化的，不是继续扩策略，而是收稳三件底层事：owner docs 质量、config 卫生、controller/sync/risk/OMS 主链的验证面。只要这三件事没稳，继续堆新能力只会让系统更难维护。
#### 必查文件
- `config.json`
- `ccxt_utils.py`
- tests
- 当前 owner docs
#### 查找线索
- 看最大的噪音到底落在文档、配置还是验证层。
#### 主线意义
- 这题负责产品视角的优先级判断。
#### 证据锚点
- `config.json`
- `ccxt_utils.py`
- 当前 `PROJECT_GUIDE` 质量偏差

### Q16. 这个项目中 AI/工具系统的正确打开方式是什么，当前用到了哪些能力，你能列出来吗？
#### 为什么问这题
这题确认 AI 是按正确方式接管项目，而不是把仓库当聊天上下文池。
#### 当前理解答案
这个项目里 AI/工具的正确打开方式应该是 evidence-first：先看 README 和原始 docs，再确认主入口和关键模块，再用 `FILE_INDEX` 和 `TOOLS_METHOD_FLOW_MAP` 引导补读代码证据，最后才讨论改动。当前最重要的不是新增自动化层，而是保证理解路径正确。
#### 必查文件
- `README.md`
- 当前 owner docs
- `main_controller.py`
- tests
#### 查找线索
- 看当前学习路径是不是已经建立在文档线索、对象边界和验证面上。
#### 主线意义
- 这题负责上岗方式。
#### 证据锚点
- `README.md`
- 当前 owner docs
- 主入口与测试面

### Q17. 根据最新的学习线索，你现在做的东西是否偏离了当前最重要的任务，你是否认为我们偏离了主线，为什么，接下来我们应该怎么做？
#### 为什么问这题
这题是最终回拉器，用来判断当前动作是否仍然服务于项目最重要方向。
#### 当前理解答案
当前最重要的任务不是继续发散系统愿景，而是把这个已实现的交易 runtime 讲清楚、守住风险和执行边界、收 owner docs、清配置、稳验证。如果当前动作不能提升这几件事，就已经偏离主线。对这次工作来说，真正偏离的地方不是题目结构，而是我先前没有用 plan 级理解方法去重建答案。
#### 必查文件
- 当前 owner docs
- `config.json`
- tests
- 关键 runtime 文件
#### 查找线索
- 看当前动作是否真正服务于“讲清主线、守住边界、降低风险、提高验证”。
#### 主线意义
- 这题就是主线回拉器。
#### 证据锚点
- controller/sync/state/risk/OMS/tests 都已存在
- 本轮最大问题暴露在 `PROJECT_GUIDE` 答案理解质量上

## 总结
- 这次真正的问题不是题目结构，而是答案理解方法不对。
- 后续应保留题目结构不动，只在经过 plan 级理解之后重写答案。
- 这份理解稿就是后续逐题修正 `/root/a9quant-strategy/docs/PROJECT_GUIDE.md` 的基底。
