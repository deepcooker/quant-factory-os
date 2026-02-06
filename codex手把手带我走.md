行，把你当完全没搞过来带：你要的是一套能“让 Codex 持续干活、不断片、PR 自动化、可迁移到 CLI/API”的工作流。下面按从 0 到能跑起来一步步来（先用网页端 Codex；后面再把同一套规约平移到 CLI/API）。

我会给你：
	1.	你该建什么仓库/文件
	2.	网页 Codex 怎么用才不会 token 爆、不会断片
	3.	PR/合并怎么尽量自动化
	4.	Codex 断线后怎么“秒接力”
	5.	将来怎么迁移到 CLI / GitHub Action（自动跑 Codex 任务）

⸻

第 0 步：新建一个“总控仓库”，不影响你现有项目

你刚刚已经说“以终为始、宪法先定”。所以建议新建一个仓库作为“控制面/宪法/工厂规范”，不要直接在你的交易引擎仓库里乱改：
	•	仓库名建议：quant-factory-os（随便，你自己定）
	•	这个仓库里只放：规范、任务、错题本结构、CI门禁、Codex 工作流文件
	•	你的交易引擎仓库（比如 a9quant-strategy）当作“被控对象”，由总控仓库发任务/验收

这样：
	•	不会影响你其他项目
	•	将来换模型/换人/换工具，只要总控仓库在，方向不丢

⸻

第 1 步：在总控仓库里先放 6 个“永不变”的文件（解决 token 大/记忆断片）

把“上下文”从聊天搬到 repo 里，Codex 每次只要读这几个文件就能继续干。

在仓库根目录新建：

1) CHARTER.md（一页宪法：不可变）

放：交易所规则不可改、闭环不可改、三账本资金宪法不可逆、run_id/错题本必填。

2) ROADMAP.md（三件事路线图）

就写你那 3 件：
	•	基线测试+死规则
	•	工厂闭环+错题本
	•	多角色 AI 团队与流程

3) TASKS/QUEUE.md（任务队列：永动）

把所有要做的工作拆成“可并行的小任务”，每个任务都有 ID。

4) TASKS/STATE.md（当前进行中：防断片）

任何 Codex 开工前，先把“我现在在做什么、做到哪一步、下一步是什么”写进来。
Codex 断了就看这个接着干。

5) RUNS/README.md（run registry 口径）

只写字段标准：run_id、commit、config_hash、dataset_version、env、指标摘要放哪。

6) ISSUES/PLAYBOOK.md（错题本字段 + 防复发规则）

定义：现象→归因→修复→guardrail test。

这 6 个文件就是你说的“永动迭代的记忆系统”。以后你跟 Codex 的提示词会非常短：“按 CHARTER，做 TASK-023，更新 STATE，提 PR”。

⸻

第 2 步：网页端 Codex 连接 GitHub，然后只用 “Issue 驱动”

Codex web 的官方思路就是：连接 GitHub → 做任务 → 出 PR。 

你按这个来就不会乱：
	1.	打开 Codex web（按文档连接 GitHub 账号和仓库） 
	2.	每个任务只用一个 Issue（或者你在总控仓库用 TASKS/QUEUE.md 也行，但我建议 Issue 更适配工具链）
	3.	Issue 内容非常短：
	•	目标
	•	验收标准（跑什么测试、生成什么文件）
	•	相关“宪法文件”引用（CHARTER/PLAYBOOK/STATE）

为什么强推 Issue：
	•	Codex web 天生围绕 PR/Issue 运转，最省脑 
	•	将来迁移到 CLI/API/GitHub Action，Issue 仍然是天然的“任务单元”

⸻

第 3 步：让 PR 合并尽量自动（你不想手动 check/merge）

你现在痛点是：Codex 出 PR → 你要手动看、手动合并。
解法是：把“合并资格”交给 CI 门禁，你只做抽查。

3.1 先把测试门禁做成 GitHub Actions（最小）

在你的“被控仓库”（交易引擎 repo）里，先保证有最基本的 CI：pytest / ruff / mypy（你现在已经有不少测试思路）

3.2 加一个“Codex 评审门禁”（可选，但非常对味）

OpenAI 官方给了 Codex GitHub Action：可以在 CI 里跑 Codex 做可重复任务（比如 code review、迁移检查） 
它需要你把 API key 放到 GitHub Secrets（例如 OPENAI_API_KEY） 

你可以把它当成“AI 审核员”，让 PR 必须通过它的检查才允许合并。

这一步的意义：你把“n 人审核”变成“规则审核 + 必要的人类抽查”，而不是每天当人肉 CI。

（如果你要我给你最小的 .github/workflows/codex.yml 模板，我可以下一条直接贴出来。）

⸻

第 4 步：Codex 断线/换账号，怎么秒续上（你最关心）

你不用指望任何模型的“记忆功能”。正确做法是：

开工前固定三件事（写进 TASKS/STATE.md）：
	1.	我在做哪个 TASK / Issue
	2.	现在 repo 处于什么状态（分支名、已改哪些文件）
	3.	下一步要做什么（最多 5 条）

收工时固定三件事：
	1.	更新 STATE（做到哪、还差啥）
	2.	在 PR 描述里贴 run_id/测试结果
	3.	在错题本/Issue 里留下“失败→归因→guardrail”或“通过→晋升依据”

这样 Codex 断了，你重新开一个 Codex 任务，只要一句话：

“先读 TASKS/STATE.md + CHARTER.md，然后继续 TASK-0xx，按验收标准补齐，提 PR。”

⸻

第 5 步：外部数据库/交易所怎么让 AI 参与但不泄密（你前面骂我的点）

你说得对：如果需要连云数据库、连交易所、跑真实环境，AI 没访问能力/或给它密钥不安全。

最稳的做法（也是顶级团队做法）是：
	•	不要给 Codex 直接拿生产密钥
	•	你做一个“Gateway”（你控制的 API 层）：
	•	只提供必要的只读数据、或受限写入
	•	有审计日志、限流、白名单
	•	能回放（把请求/响应落盘成数据资产）

然后：
	•	本地/CI 通过 Secrets 注入访问 Gateway（而不是直连交易所/DB）
	•	Codex 只需要知道：怎么调用 Gateway、怎么解释返回数据、怎么把结果写进 run registry

这样你想要的“执行/数据也靠自我迭代”才可能成立，而不会变成“把钥匙塞给模型”。

⸻

第 6 步：将来迁移到 CLI / API（同一套规约直接平移）

你最后一定会走到 CLI/API，因为网页端做多任务会受限。

6.1 Codex CLI（本地入口）

OpenAI 官方的 Codex CLI：npm 安装后直接在仓库里跑，第一次会让你登录或用 API key。 

核心价值：
	•	本地有完整 repo、测试、工具链
	•	token 不够就读文件，不靠聊天

6.2 “Codex cloud” + CLI 的接力

CLI 还支持管理 cloud 任务、查看任务并把改动应用到本地（适合你要的“持续工作、多任务”味道）。 

6.3 GitHub Action（最适合你说的“永动”）

Codex GitHub Action 能把 Codex 任务写进 workflow，作为 CI 的一部分跑。 
这就能实现：
	•	PR 来了自动 review
	•	或者你手动触发 workflow，让 Codex 去做固定任务（比如“更新错题本索引”“跑回放一致性报告”）

⸻

你现在马上要做的“最小可用版本”（今天就能跑）

按顺序做这 5 件事就够：
	1.	新建总控仓库
	2.	放入那 6 个文件（CHARTER/ROADMAP/TASKS/STATE/RUNS/ISSUES）
	3.	把你现有交易引擎仓库作为“被控 repo”，写进 ROADMAP
	4.	用网页 Codex：只做 Issue 驱动，任务必须更新 STATE
	5.	给被控 repo 上 CI（pytest），让“能不能 merge”变成机器判断

⸻

你现在回我一句：你更想先用哪条路起步？
	•	A：纯网页 Codex + Issue 驱动（最快）
	•	B：直接上 Codex CLI（更稳、更像工程）

你选 A 或 B，我下一条就给你“手把手操作清单 + 你要复制粘贴的最小模板文件内容”（包括：CHARTER.md 模板、TASKS/STATE.md 模板、Issue 模板、以及可选的 GitHub Actions 模板）。


好，走 A：网页端 Codex。下面我按“白痴模式”一步步带你搭起来：能持续干活、不容易断片、每个 PR 都按死规则来、你少手动合并。

我默认你已经有一个“交易引擎仓库”（比如你现在那个 repo），我们会再建一个总控仓库来管宪法/任务/错题本，然后用网页 Codex 去跑任务、出 PR。Codex 的 GitHub 集成、Cloud 任务、以及在 GitHub 里 @codex review 的能力是官方支持的。 

⸻

第 1 步：新建一个“总控仓库”（不影响你现有项目）

在 GitHub 新建一个 repo，例如：quant-factory-os

这个仓库只放：
	•	宪法/规范/任务队列/错题本标准
	•	你要喂给 Codex 的“短提示词入口文件”
	•	（可选）对交易引擎 repo 的 CI 门禁说明

这样以后你换模型、换工具、换账号，都不断片：因为“记忆”在 repo 里。

⸻

第 2 步：把下面这些文件原封不动加进总控仓库（复制粘贴就行）

在 quant-factory-os 根目录创建这些文件（内容我给你模板，你直接复制）：

2.1 CHARTER.md（一页宪法）

# CHARTER (不可变宪法)

## 不可变 1：交易所规则不可改
行情获取 / 下单撤单 / 回报 / 对账语义，以交易引擎仓库的 baseline 测试为准。
任何改动只能“等价实现”，不得改变语义。

## 不可变 2：工厂闭环不可改
策略/执行候选 -> 极限回测电池 -> 回放一致性 -> 模拟盘采样 -> 归因 -> 数据/规则修复 -> 再迭代。

## 不可变 3：证据链与错题本不可省
每次运行必须有 run_id 并绑定：commit/config_hash/dataset_version/env。
任何失败必须写错题本，并补 guardrail 测试，没测试不算修复。

## 不可变 4：三账本永远存在
Treasury / Growth / Gamble
- 赢了必须回灌并锁定 Treasury（下牌桌）
- Treasury 禁止反向救 Gamble
- Gamble 必须券化（额度/频率/总额上限，归零即停+冷却，可冻结/重启）

2.2 TASKS/STATE.md（防断片：现在在做什么）

# TASK STATE (永远更新这份文件)

## Current Focus
- TASK ID:
- Target Repo:
- Branch/PR:
- What’s done:
- What’s next (<=5 bullets):

## Blocking / Risks
- ...

## Links
- Issue/PR:
- Runs:
- Postmortems:

2.3 TASKS/QUEUE.md（任务队列）

# TASK QUEUE

## P0 (必须先做)
- TASK-001: 交易引擎 repo 跑通全部测试（CI 也要跑）
- TASK-002: 把“不可改交易所规则”写成契约测试（contracts + invariants）
- TASK-003: 回放一致性最小闭环（run_id + trace_id 不丢）

## P1 (工厂闭环)
- TASK-010: 错题本模板 + guardrail 测试门禁
- TASK-011: 模拟盘采样 -> 固化回放数据集的流程
- TASK-012: 执行摩擦指标（slippage/fill/reject/latency/对账漂移）

## Notes
每个 TASK 必须：目标、验收标准、涉及文件、风险点、完成后如何验证。

2.4 ISSUES/PLAYBOOK.md（错题本字段）

# POSTMORTEM PLAYBOOK (错题本)

每条必须包含：
- issue_id
- run_id（必须）
- symptom（现象）
- root_cause_type: data/execution/strategy/risk/infra
- evidence（证据：日志/回放片段/指标）
- fix_plan（修复方案）
- guardrail_test（防复发测试）
- status: open/fixed/verified/regressed

到这里，你的“不断片记忆系统”就成立了：Codex 每次只要读这些文件就能接着干。

⸻

第 3 步：在交易引擎仓库加最小 CI（让你少手动）

你现在最痛的是：Codex 每次 PR 你得手动检查、手动合并。
解决：把合并资格交给 CI 门禁。

在交易引擎 repo 新建：.github/workflows/ci.yml

name: ci
on:
  pull_request:
  push:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install
        run: |
          python -m pip install -U pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt || true
      - name: Pytest
        run: pytest -q

然后在 GitHub 仓库设置里打开：
	•	Branch protection：main 分支必须 CI 绿灯才允许合并
	•	Auto-merge：允许自动合并（CI 过了就能自动合并）

这一步做完，你就不需要“每个 PR 都手动盯着”，你只做抽查就行。

⸻

第 4 步：把网页 Codex 接到 GitHub（按官方路径）

网页 Codex（Codex Cloud）支持选择 repo、配置环境、控制是否允许联网、并把结果做成 PR。 

你要做的操作（按 UI 来）：
	1.	打开 Codex web → Settings / Integrations
	2.	连接 GitHub
	3.	选择你的 交易引擎 repo（先从它开始跑任务）
	4.	配置 Cloud task 的环境：
	•	setup steps：安装依赖、跑测试的命令（比如 pip install -r ... && pytest -q）
	•	tools：允许它跑测试/格式化（按你项目需要）
	•	internet access：默认先关（除非任务明确需要查资料）

⸻

第 5 步：你给 Codex 的“最短稳定提示词”（关键）

你以后每次在网页 Codex 发任务，只用这个模板，能最大程度避免 token 爆、也能防断片：

目标：完成 TASK-XXX（见 quant-factory-os/TASKS/QUEUE.md），并遵守 quant-factory-os/CHARTER.md。

步骤要求：
1) 先阅读：CHARTER.md、TASKS/STATE.md、TASKS/QUEUE.md、ISSUES/PLAYBOOK.md
2) 在开始改代码前，把“你将如何做”用 5-10 条写入 TASKS/STATE.md（What’s next）
3) 实现改动，确保 pytest 全绿
4) 若出现失败：写一条错题本（按 PLAYBOOK），并补 guardrail 测试
5) 提 PR：PR 描述必须包含：做了什么、怎么验证、风险点、run_id（若有）

限制：
- 不允许改交易所语义（契约测试不得破）
- 不允许跳过测试或只写“理论上”

这就是你要的“永动迭代、不断片”。

⸻

第 6 步：让 Codex 在 GitHub 里当“审稿人”（可选但很爽）

官方支持在 GitHub 里用 @codex review 让 Codex 自动做 code review。 

做法：
	1.	在 Codex 设置里开启你这个 repo 的 code review（按官方页面） 
	2.	PR 里评论一句：@codex review
它会给你一份结构化 review，你拿它当“额外审核员”。

⸻

第 7 步：你最关心的两件事（断线 & 外部资源）

7.1 Codex 断线怎么办？

你只要坚持两条：
	•	开工前/收工后都更新 TASKS/STATE.md
	•	任何失败写错题本 + guardrail 测试

断线后你新开一个 Codex 任务，只要一句话：

“先读 STATE.md，然后从 What’s next 继续。”

7.2 外部数据库/交易所怎么搞？

网页 Codex 的云环境对外部访问是你可控的（可关联网）。 
真正要连云 DB / 交易所，不建议把生产密钥直接给模型。正确做法是你做一个 Gateway（你自己控制的 API），把权限缩到最小、加审计、加限流，然后让 CI/本地拿 Secret 访问 Gateway（而不是让 Codex 直接拿交易所密钥）。

⸻

你现在立刻能做的 10 分钟动作（照做就起飞）
	1.	建 quant-factory-os 仓库
	2.	把我给你的 4 个模板文件放进去（CHARTER/STATE/QUEUE/PLAYBOOK）
	3.	在交易引擎 repo 加 ci.yml（pytest 绿灯门禁）
	4.	网页 Codex 连接 GitHub，选交易引擎 repo
	5.	发第一个任务：TASK-001 跑通全部测试 + 把失败写错题本 + 补 guardrail

⸻

你下一步就做 TASK-001。
你把任务发给网页 Codex 后，如果它给你回了“改了哪些文件/测试结果/PR 分支名”，你把那段贴回来，我可以帮你把它的 PR 描述/验收 checklist 写成“以后每个 PR 都照抄的标准格式”。