# PROJECT_GUIDE.md (v2) — quant-factory-os 自举式智能工厂操作系统

> 目的：让任何新开的 GPT 窗口 / 新启动的 Codex 会话，在**不依赖聊天历史**的情况下，快速对齐：
> 1) 我们最终要什么（北极星/终局）
> 2) 现在做到哪（阶段/能力）
> 3) 下一步怎么做（队列→任务→证据→交付）
> 4) 如何学习进步（手册/错题本/技能树）
> 5) 如何训练新智能体，并逐步多智能协作涌现智能

> v2.1 同频入口补充：新会话先读 `SYNC/`（尤其 `SYNC/01_阅读顺序.md`），
> 再进入本指南与深层文档。

---

## 0. 一句话北极星（你最终要什么）
quant-factory-os 是一个“自举式智能工厂操作系统”：它能**自动执行任务**、能**从证据链与错题本学习变强**、能**训练/引导新的智能体加入并理解因果链**、能**自我迭代升级工具与流程**、最终能**多智能协作形成涌现智能**，并把这些能力用于任何项目（最初是量化策略工厂，最终是通用项目底座）。

---

## 1. 五层终局目标（按优先级与阶段推进）

### 目标 1：自动化执行（Execution Autonomy）
- 系统能从队列（QUEUE）自动生成任务（TASK）与证据命名空间（RUN_ID），执行最小改动，跑验证，ship 成 PR。
- 关键：**可审计**（每次行动都能复现、能回放、能接力）。

### 目标 2：学习进步（Learning System）
- 系统能把“成功模式/失败模式”沉淀为：
  - 使用手册（WORKFLOW/ENTITIES/TOOLS）
  - 错题本（MISTAKES / failure playbook）
  - 周期性复盘报告（awareness/digest）
- 关键：学习来自 **repo 证据**（PR + reports），而不是聊天记忆。

### 目标 3：训练新智能体（Onboarding / Training New Agents）
- 新智能体能被“训练成合格执行者”：
  - 学会读 STATE / QUEUE / WORKFLOW / ENTITIES
  - 学会按 gate/证据链执行
  - 学会用错题本避免复发
  - 学会最小化改动 + 可验证交付
- 关键：训练必须**有可测验收**（复述/演练/小任务）。

### 目标 4：自我迭代升级（Self-Improvement / Tool Evolution）
- 系统能持续发现“摩擦点/失败点”，提出改进任务并合并进基座：
  - 更稳的 gate、更低摩擦的工具、更强的恢复能力
- 关键：自我升级必须遵守“天道=边界”：不可破坏因果链，不可跳过证据与验证。

### 目标 5：多智能协作涌现智能（Multi-agent Collaboration / Emergence）
- 多智能体在同一规则体系下分工协作：
  - Planner（规划/拆解）/ Implementer（实现）/ Reviewer（审查）/ Observer（只读觉察）/ Librarian（知识/错题本维护）
- 关键：协作只靠 PR/RUN_ID/evidence 接力，避免“隐形状态”。

> 备注：你提到的 EvoMap 类思路可以作为参考，但我们这里更强调“可审计的工程因果链 + 强门禁”，避免进化失控。

---

## 2. 系统因果链（必须守住的“天道”）
### 2.1 实体关系（Entity Model）
- Task：需求真相源（scope/goal/acceptance 是硬约束）
- PR：一次交付单元（1 task → 1 PR）
- RUN_ID：证据命名空间（reports/<RUN_ID>/）
- Evidence：summary/decision/meta（可复现可审计）
- STATE：全局进展基线（唯一“我们做到哪”的入口）
- QUEUE：下一枪队列（系统“将要做什么”的入口）
- MISTAKES：失败协议/复盘（防复发）
- Gate：门禁（enter/denylist/scope/single-run 等）

### 2.2 三条硬规则（端云/多窗口/多 agent 的生命线）
- 未提交=不存在（本地改动对其他 agent/云端不存在）
- 交接只认 PR/commit + reports/<RUN_ID>（聊天不算交接）
- 失败必须可复盘：写 evidence/必要时写 MISTAKES（否则等于没学到）

---

## 3. GPT vs Codex：角色分工与协作窗口

### 3.1 GPT 窗口（“大脑/制度/路线图/外部知识”）
负责：
- 校准目标与方向（北极星）
- 拆任务、排优先级、写 QUEUE item（最小四元组）
- 把外部信息（上网查资料）变成可执行 task
- 复盘：把失败模式沉淀为“下一枪”

不负责：
- 不直接改仓库、不跑命令、不 ship（执行噪声留给 Codex）

### 3.2 Codex CLI（“执行器/改代码/跑验证/ship”）
负责：
- 严格按工作流执行：读→task→evidence→实现→verify→reports→ship
- 默认只用允许命令和工具脚本
- 每次行动必须产出证据链并可回放

---

## 4. 初始化与退出（普通窗口 vs Codex 窗口）

### 4.1 两种窗口
- 普通终端窗口：用来 `cd repo`，启动 Codex
- Codex 窗口：执行任务、改代码、跑 verify、ship

### 4.2 正确启动 Codex（必须）
1) 普通终端：
   - `cd ~/quant-factory-os`
   - `./tools/start.sh codex`
2) start.sh 会：
   - 激活 venv（确保 pytest 在 PATH）
   - 运行 enter.sh（必须工作区干净、pull、doctor）
   - 进入 codex 会话

### 4.3 退出/恢复
- 退出：在 codex 会话中 `/quit` 或 `exit`
- 恢复：重新从普通终端用 `./tools/start.sh codex`
- 若中断（余额/权益问题），恢复时只依赖 repo 记忆（STATE/QUEUE/reports），不要依赖 session。

### 4.4 同频优先接班协议（当前主策略）
> 核心原则：先同频，再执行；先接班，再新建动作。

每次新会话（含断线重连）先做 4 步，不要直接开改：
1) `tools/qf init`
2) 读取当前接班证据（按顺序）：
   - `TASKS/STATE.md`
   - `TASKS/QUEUE.md`
   - 最近一次 `reports/<RUN_ID>/handoff.md`（若存在）
   - 最近一次 `reports/<RUN_ID>/conversation.md`（若存在）
   - 最近一次 `reports/<RUN_ID>/decision.md`
3) 复述同频五项（目标/范围/验收/步骤/停止条件）
4) 复述通过后再进入执行命令（如 `ready/plan/do`）

退出前必须写“最新会话衔接摘要”（防账号/网络/session 丢失）：
- `tools/qf snapshot RUN_ID=<run-id> NOTE="本轮结论 + 下一步 + 阻塞"`

判断是否同频成功（DoD）：
- 新会话不依赖聊天历史，也能在 3 分钟内说清：
  - 上轮做到哪
  - 当前阻塞是什么
  - 下一步一条命令是什么

---

## 5. 如何判断“它真的理解了”（强制复述协议）
在让 Codex 执行任何任务前，必须要求它先复述（不复述不执行）：

**复述模板：**
1) 目标：一句话
2) Scope：将修改的文件列表（精确路径）
3) 验收：3 条（verify/evidence/scope）
4) 执行步骤：evidence→实现→verify→更新 reports→ship
5) 停止条件：完成后停下等待确认

**复述不合格的红旗：**
- 想动主项目、扩大 scope
- 想跳过 evidence/verify
- 想用未允许命令
- 想用 override 逃逸但不记录证据

---

## 6. 当前基座能力（你现在已达到的“自举底盘”）
> 这部分是“新窗口快速对齐现状”的必读摘要（以 repo 为准）。

- enter：要求干净工作区，pull + doctor，打印 entrypoints
- queue：`tools/task.sh --next` 能从 QUEUE 生成 TASK + RUN_ID，并标记 `[>] Picked: ...`
- ship：创建 PR、等 checks，并能自动把对应 `[>]` 改成 `[x] Done: PR #.. RUN_ID=..`
- denylist：`.codex_read_denylist` 默认阻止读某些文件，可 override 但需审计
- scope gate：以 task 的 `## Scope` 为准拦 out-of-scope（防混入/漏文件）
- 多次事故复盘：已通过门禁与工具改进修复（示例：Scope 自动化修复、QUEUE 自动 done）

---

## 7. 学习系统（手册 + 错题本 + 技能树）

### 7.1 使用手册（Manual）
最低要求：任何“新人/新智能体”必须能从 docs 与工具输出理解：
- WORKFLOW（怎么做、怎么交接）
- ENTITIES（名词表）
- TOOLS（start/enter/doctor/view/task/ship 的职责）
- 未来可加：PLAYBOOK（常见故障与恢复）

### 7.2 错题本（MISTAKES）
目标：让系统能“见一次坑，下次不再踩”。
建议结构（可用文件/目录）：
- MISTAKES/<RUN_ID>.md：复现、根因、修复、预防测试、如何恢复
- tags：scope/denylist/ship/queue/venv 等

### 7.3 技能树（Skill Tree）
把能力分层：
- L0：能读 STATE/QUEUE/WORKFLOW/ENTITIES
- L1：能做一枪“文档/测试”任务并 ship
- L2：能改工具脚本并加测试护栏
- L3：能复盘与提出流程改进（自我升级）
- L4：能作为 Reviewer/Observer 参与多智能协作

---

## 8. 多智能协作（如何协作不乱）
### 8.1 角色建议
- Planner：写 QUEUE item、验收、风险
- Implementer：按 Task 执行
- Reviewer：只看 PR diff + evidence + tests
- Observer：只读生成周报（不改代码）
- Librarian：维护 docs/与 MISTAKES

### 8.2 协作协议
- 协作只通过：PR/RUN_ID/reports/STATE/QUEUE
- 禁止：口头/聊天交接当真相源
- 并行冲突：以 queue `[>] Picked` 锁 + PR 合并冲突解决为准

---

## 9. QUEUE：文件 vs 中间件（你担心的“文件易错”）
当前选择文件是正确的（因为可审计、最低依赖、最适合自举）。
你已经通过：
- pick lock（[>] + Picked）
- auto done（[x] + Done）
- scope normalization & fail-fast
把“文件易错”降到很低。

何时升级到 DB/中间件：
- 并行 session 多到 PR 合并冲突成为常态
- 需要跨仓库统一调度（多项目统一 queue）
- 需要细粒度权限/审计/多租户
升级也应保持：PR/commit 仍是最终审计边界。

---

## 10. 新窗口对齐（最快方式，v2.1）
新 GPT 窗口 / 新 Codex 会话统一按“同频优先接班协议”执行，必读顺序：
1) `TASKS/STATE.md`
2) `TASKS/QUEUE.md`
3) `docs/WORKFLOW.md`
4) `docs/ENTITIES.md`
5) 最近 `reports/<RUN_ID>/handoff.md`（若存在）
6) 最近 `reports/<RUN_ID>/conversation.md`（若存在）
7) 最近 `reports/<RUN_ID>/decision.md`

然后必须输出：
- 3 行状态：做到哪 / 阻塞 / 下一枪
- 1 条衔接摘要：上一轮关键结论与当前边界
- 1 条可执行命令（只给当前最小下一步）

注意：
- 若 `handoff.md` 与 `decision.md` 冲突，以 `decision.md` + 最新 PR 状态为准。
- 若找不到会话证据，先补 `snapshot`/`handoff`，再进入新任务。

---

## 11. 未来路线图（按阶段推进，避免失控）
- Stage 0：基座硬化（门禁/工具/自举闭环）✅（你们已大幅完成）
- Stage 1：学习系统（错题本检索、周报/awareness、复盘自动化）
- Stage 2：训练系统（训练新智能体：演练任务、复述验收、技能树晋级）
- Stage 3：自我升级（Observer→提出改进→合并）
- Stage 4：多智能协作（分角色、并行执行、统一调度）
- Stage 5：接入具体项目（财富系统/量化系统）——在 Stage 0-2 稳定后推进



---

# 附录 A：具体项目（财富系统 / 量化系统）与基座集成策略（v3 增补）

> 目的：让新 GPT 窗口、新 Codex 会话不只“知道现在工具链怎么跑”，还知道**最终要落地的具体项目是什么、怎么接入、怎样避免基座与项目混淆**。

---

## A1. 两个具体项目的“工程定义”（不再抽象）

### A1.1 量化系统（Quant System）是什么
量化系统 = **策略研发与交易执行系统**，更像“研究院 + 执行台”。

它至少包含以下工程模块（不等于一次性都做完）：
1) **数据摄取**：市场数据 / 指标数据 / 交易数据（含指针化与校验）
2) **回测实验室**：可复现 backtest（费用/滑点/撮合假设明确）
3) **参数/模型优化**：可审计的搜索（不追求花哨，追求可复现与可回放）
4) **模拟盘/纸交易**：与真实交易接口一致的 shadow 环境
5) **小资金实盘**：受控风险，强监控
6) **复盘系统**：交易回放、性能归因、异常检测、形成下一轮任务输入

量化系统的“成功信号”不是一时收益，而是：
- 同一策略在不同环境/不同 agent 执行下**可复现**
- 回测→模拟→实盘的落差有明确解释与证据链
- 失败能产出 MISTAKES 并让系统变强

### A1.2 财富系统（Wealth System）是什么
财富系统 = **资产与收益的全生命周期操作系统**。量化系统是其中一个“收益引擎”，但财富系统更大：它还要管理资金、风险、账户、仓位、税务/合规（视地区）、以及“多策略/多资产”的组合治理。

最低模块拆解：
1) **资金与账户**：多账户/多交易所/多链钱包的统一资产视图
2) **组合与风控**：仓位上限、回撤阈值、风险预算、相关性约束
3) **收益引擎**：量化策略只是其中一种（也可能是套利、做市、被动、RWA 等）
4) **监控与告警**：异常成交、接口故障、资金异动、风控触发
5) **审计与报表**：每一次变更、每一笔交易、每一次策略切换都有证据链
6) **治理**：什么能自动执行、什么必须人类确认（源觉/天道边界）

财富系统的“成功信号”是：
- 资金安全与可审计优先（先活着）
- 收益引擎可插拔、可比较、可退场（可控）
- 系统能持续迭代，不靠人肉运营

> 关系总结：量化系统更像“发动机与实验室”；财富系统是“整车 + 仪表盘 + 安全系统”。

---

## A2. 基座如何接入项目：三种架构选择（避免混淆）

你担心的核心：  
**基座要读懂项目，但又不能把任务/PR/证据链搞混。**

这里给出三种架构，并明确“现在用哪个、未来什么时候切换”。

### A2.1 方案 1：基座独立（Orchestrator Repo）— 推荐当前阶段
- quant-factory-os **独立仓库**，负责“任务/证据/门禁/训练/学习系统”。
- 项目仓库（量化/财富）是“业务代码与数据合同”的所在地。
- 基座通过 **集成合同（Integration Contract）** 调用项目的“受控入口”。

优点：
- 因果链更干净：基座的 Task/PR/evidence 不会污染项目
- 训练新智能体更清晰：先学基座规则，再学项目业务
- 基座没稳定前不会拖累项目；项目也不会拖基座门禁

缺点：
- 跨 repo 协作需要清晰的链接/指针（但这是可控成本）

### A2.2 方案 2：基座插件化（Embed / Package）— 未来阶段
- 把基座工具链打包成一个可安装组件（例如 python package / binary / submodule）
- 每个项目仓库引入这个组件，项目内直接执行“task/ship/verify”

优点：
- 单仓执行便利（项目内就能跑完整流水线）

缺点：
- 容易把“基座升级”变成“所有项目升级”，早期极不稳定
- 证据链/门禁容易被项目需求破坏（混淆更严重）

### A2.3 方案 3：单体大仓（Monorepo）— 不建议现阶段
- 基座和项目都在一个 repo
- 最容易“做着做着又混回去”，不利于你坚持的“先基座后项目”

**当前推荐选择：方案 1（独立 Orchestrator）**  
等 Stage 2/3 稳定后，再考虑方案 2 作为“分发形态”。

---

## A3. 最容易搞混的点：Task/PR/Evidence 跨 repo 如何分离

### A3.1 基本原则：每个 repo 有自己的 Task/PR；跨 repo 只能用“指针”
- quant-factory-os 的 Task/PR：只用于**基座工具链与制度升级**
- 项目 repo 的 Task/PR：只用于**项目业务代码**
- 基座与项目之间的链接，必须用：
  - PR 链接（URL）
  - commit hash pin（SHA）
  - 以及在 reports/<RUN_ID>/decision.md 中记录这些 pin

### A3.2 “跨 repo 大任务”怎么做才不会乱
用 **Coordinator Task（协调任务）** 的模式：

- 在基座 repo 创建一个 Task（Coordinator）
  - 只写目标、阶段、验收、以及“将产生哪些项目 repo PR”
- 项目 repo 各自有子任务 PR
- 基座的 reports/<RUN_ID>/decision.md 记录：
  - project repo PR# / commit sha
  - 验证方式（在项目 repo 的 verify 结果链接或日志摘要）
  - 是否允许进入下一阶段

这样即使 agent 中断 5 小时，新的 agent 也只要看 decision pin 就能接上。

### A3.3 Evidence 放哪里？（关键）
推荐当前阶段：
- **基座 repo 存“协调证据与指针”**
  - reports/<RUN_ID>/decision.md：记录“项目 PR/sha/验证结果摘要”
  - 大日志/数据：用 URI + checksum + 生成脚本（指针化合同）
- 项目 repo 存“业务实现与项目内测试证据”（如果项目也要有自己的 reports，那是项目内的事）

一句话：  
**基座 evidence = orchestration/治理证据；项目 evidence = 业务运行证据。**

---

## A4. 集成合同（Integration Contract）是什么（让基座能“读懂项目”但不混）

每个项目 repo 必须提供一个“受控入口”，让基座能做最小验证而不是随意执行。

建议项目 repo 提供：
- `make verify`（或等价命令）跑最小测试
- `make dryrun` / `python -m ... --dry-run`（只跑管线，不跑真实资金）
- 输出一个结构化结果（JSON 或 log），可被基座收集为 evidence 指针

基座 repo 对每个项目写一份合同文档（示例命名）：
- `docs/INTEGRATION_WEALTH.md`
- `docs/INTEGRATION_QUANT.md`

合同内容只包含：
- 允许调用的命令入口
- 允许读取/写入的输出目录
- 必须记录的 pin（repo url + sha）
- 禁止事项（例如未稳定前禁止实盘/禁止修改主项目）

---

## A5. 训练新智能体：它必须学会的三件事（从基座到项目）

### A5.1 新智能体的最小入门考试（必须能通过）
1) 复述：当前北极星 + 三条硬规则 + 自己角色（Planner/Implementer/Reviewer/Observer）
2) 演练：从 QUEUE 领取 → 生成 TASK → make evidence → make verify → ship → 自动 [x] Done
3) 复盘：把一次失败写成 MISTAKES，并能从 MISTAKES 提炼下一枪

### A5.2 从“只会跑工具”到“会看数据”
训练路径：
- 先学：证据链（reports/decision/summary + PR diff）
- 再学：数据合同（指针化、checksum、生成脚本）
- 最后学：项目业务数据（回测/模拟/实盘的观测指标）

---

## A6. 你的五层目标如何映射为可执行里程碑（避免空转）

### Stage 0（已基本完成）
- 自举闭环：QUEUE → TASK → RUN_ID → verify → ship → 自动 mark done
- 门禁：denylist + scope gate + single-run guard
- 入口：start/enter/doctor/view

### Stage 1（学习系统）
- 增加“错题本检索 + 周报/觉察报告”（只读 observer）
- 固化“常见故障恢复手册”（从 MISTAKES 自动归档）

### Stage 2（训练系统）
- 新 agent 入门考试脚本化（Checklist + 演练任务）
- 技能树/角色化（Planner/Implementer/Reviewer/Observer）

### Stage 3（自我升级）
- observer 输出下一枪建议（但不自动合并）
- 系统能提出“工具改进 PR”并通过门禁

### Stage 4（多智能协作涌现）
- 角色并行：多 PR 并行，但以 queue lock + PR 合并解决冲突
- 统一调度：必要时再考虑 DB/中间件

### Stage 5（接入具体项目：量化/财富）
- 先接 Integration Contract（dry-run/probe）
- 再接数据合同（指针化 + checksum）
- 再接模拟盘/小实盘（强治理边界）

---

## A7. 关键提醒：基座“知道自己在干嘛”的工程定义
不是写“我在挣钱”的宣言，而是：
- STATE/QUEUE 清晰表达目的与阶段
- 每次 PR 的 decision.md 写清 why/what/verify/next
- observer 周报能回答：我们离财富系统/量化系统的哪个里程碑更近了？

---

# 附录结束
