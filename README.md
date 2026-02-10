好，我按“现在仓库最终长什么样 + 我们到底做了什么 + 入口在哪 + 每一步怎么跑 + 进度到哪 + 下一阶段做什么”给你做一份**超细**总结（偏“交接文档”风格，方便你/AI接管）。

> 说明：我这边用网页工具看 GitHub 文件正文会被 GitHub 的“你在别的窗口登录/登出”提示挡住，**正文我无法稳定拉出来**；但仓库结构（有哪些目录/文件）能确认，且你在服务器里实际跑出来的日志、脚本内容我都有上下文，所以我会以“你已经跑通的真实行为”为准来总结。仓库顶层结构我用 GitHub 页面可见的文件树来核对。 ([GitHub][1])

---

## Quick start

无代理：

```bash
./tools/start.sh
```

有代理：

```bash
PROXY_URL=http://127.0.0.1:7890 ./tools/start.sh
```

## Next steps

1. Run a9 probe/help checks (see `docs/INTEGRATION_A9.md`).
2. Smoke small window backtest (minimal symbols/window).
3. Real backtest once smoke passes.

Note: capture `/status` output in evidence before each ship.

## 0）这个仓库到底是什么：quant-factory-os 的定位

它不是交易策略引擎本体（那个是 `a9quant-strategy`），它是**让 AI/Codex 能“安全、自动、可审计”接管开发的操作系统（OS）**：

* 把**改代码**这件事制度化：
  **任何变更必须走 PR → CI 绿灯 → 才能进 main**（你已经配置并验证过“直推 main 会被拒绝”）。
* 把“人肉点按钮”的动作自动化：
  本地一条命令，就能**建分支、提交、推送、建 PR、盯 CI、合并、删分支、回 main 同步**。
* 把 AI 的工作组织起来：
  用 `TASKS/QUEUE.md`（任务队列）+ `TASKS/STATE.md`（当前状态）作为**AI 可读、可接力**的工作台。

仓库当前顶层能确认存在这些：`.github/`、`ISSUES/`、`TASKS/`、`tests/`、`tools/`、`CHARTER.md`、`CONTRIBUTING.md`、`README.md`、`githubcli.txt`。 ([GitHub][1])

---

## 1）我们已经做成了什么（成果清单）

### A. “主分支门禁”已经落地（你已经验证过）

* `main` 受保护：**禁止直接 push**，必须 PR。
  你实际 `git push` 触发过远端拒绝：`Protected branch update failed... Changes must be made through a pull request.`（这就是门禁生效）
* CI check 作为“合并资格”：远端提示过 `Required status check "check" is expected.`
  这说明仓库的分支保护规则里已经把某个 check（名叫 `check`）设成必需。

### B. 最小 CI 已经跑通

* `.github/workflows/ci.yml` 已存在并能跑（你每个 PR 都看到 `ci/check` 绿灯）。
* 你的 `doctor.sh` 也能检测到 workflow 文件存在，并能调用 pytest（即便无测试会 rc=5，它也会解释“这不一定是坏事”）。

### C. Codex/AI 的“发货入口”已经统一成脚本（核心）

你现在有三个关键入口脚本（都在 `tools/`）：

1. **`tools/ship.sh`（最核心）**
   一键把“当前工作区改动”变成一个 PR，并自动合并（如果仓库允许 auto-merge）。

2. **`tools/task.sh`（任务驱动入口）**
   让你先选一个 `TASKS/*.md`，自动生成提交信息 `task: ...`，然后**内部调用 `tools/ship.sh` 发货**。
   所以你才会感觉：

   > “我怎么觉得已经做了 ship.sh 的事情？”
   > ——对的，因为 `task.sh` 本质就是 `ship.sh` 的“前置包装”。

3. **`tools/doctor.sh`（自检入口）**
   给 Codex 接管前/每次环境漂移时跑一下，确认：在 repo 根目录、remote、gh 登录、CI 是否存在、python/pytest 是否可用。

> 你已经跑通过：`tools/ship.sh` 能自动建 PR、盯 checks、合并、删分支、回 main；
> 你也跑通过：`tools/task.sh` 选 TASK 文件后同样完整走完这一套，并生成 PR（#15/#16/#17/#18/#19/#20 等）。

### D. 制度入口文件已经有了

* `CONTRIBUTING.md`：告诉所有人/所有 AI **唯一入口就是 ship.sh**，禁止直推 main，标题前缀建议等。
* `.github/pull_request_template.md`：PR 模板（你希望中文）
* `CHARTER.md`：你这套 OS 的“宪法/章程”（至少文件已存在于仓库根目录） ([GitHub][1])

---

## 2）这套系统怎么“交互式工作”（你是小白版的运行流程）

### 2.1 日常改动（不管是你改，还是 Codex 改）

你在工作区改完任意文件后，只做这一句：

```bash
tools/ship.sh "一句话说明改动"
```

**ship.sh 会做这些动作（你日志里已经完整体现过）：**

1. **检测 gh 是否登录**（没登录直接失败，避免 PR 建不起来）
2. **检查工作区是否有未提交改动**

   * 有 → 自动 stash（包括未跟踪文件）
3. **切回 main 并更新到最新**
4. **用“提交信息 + 时间戳”生成新分支名**
   类似：`chore/docs-pr-20260202-204007`
5. **切到新分支，把 stash pop 回来**
6. `git add -A` + `git commit -m "..."` + `git push -u origin branch`
7. `gh pr create` 自动创建 PR
8. `gh pr merge --auto --squash --delete-branch` 尝试开启自动合并
9. `gh pr checks --watch` 盯 CI 直到出结果
10. 合并完成后：切回 main，同步最新，并清理本地/远端分支

> 你遇到过的典型坑：
>
> * “刚建 PR 显示 no checks reported” → 你后来在 ship.sh 加了等待逻辑（循环等 checks 出现）
> * “stash pop 报 stash@{0}: 冒号问题” → 你也修过（日志里有）

---

### 2.2 任务驱动模式（让 AI 有队列可读）

你运行：

```bash
tools/task.sh
```

它会列出 `TASKS/` 下可选的任务文件（你现在是 `QUEUE.md` 和 `STATE.md`），你输入序号。

然后它会：

1. 打印：选中的任务文件路径
2. 从该文件提取标题 → 自动生成提交信息：`task: ...`
3. **直接调用 `tools/ship.sh "$msg"`** 把这次变更发货

所以结论是：

✅ **用 `tools/task.sh` 就不需要再手动跑 `tools/ship.sh`**
因为 `task.sh` 就是“先选任务/生成 msg”，然后把活交给 ship 去做。

---

## 3）仓库里“哪些是系统工程文件”，哪些是“日常变动内容”

你可以按“变动频率 + 权限门禁”把文件分两类：

### 3.1 系统工程文件（低变动、要更谨慎）

这些是“让 AI 能接管”的底座，改它们要更谨慎：

* `.github/workflows/ci.yml`：CI 门禁（决定能不能合并）
* `.github/pull_request_template.md`：PR 结构（AI 写 PR 的格式）
* `tools/ship.sh`：核心发货流水线（最关键）
* `tools/task.sh`：任务入口（会影响 AI 如何组织工作）
* `tools/doctor.sh`：自检入口（保证环境可控）
* `CONTRIBUTING.md` / `CHARTER.md`：制度说明与宪法

> 你在 `ship.sh` 里做过“防误提交保险丝”（默认不允许顺带提交 ship.sh 本体），这就是典型的“系统工程防呆”。
> 你现在说 `SHIP_ALLOW_SELF=1` 不加也行——可以，但我建议**保留保险丝**，否则 Codex 很容易“顺手把 ship 改坏然后一键合并”。

### 3.2 日常变动内容（高变动、就是给 PR 用的）

* `TASKS/QUEUE.md`：任务队列（待做清单）
* `TASKS/STATE.md`：当前状态（正在做什么、做到哪一步、阻塞是什么）
* `ISSUES/`：问题记录、错题本、事故复盘（如果你后面要做）
* `tests/`：随着工程推进逐步加（先从 smoke test / guardrails 开始）
* `README.md`：随阶段更新

---

## 4）系统里已经使用的“概念词典”（你提到的 PR 任务队列等）

你现在这套 OS 已经落地的概念有：

1. **Branch Protection（主分支保护）**
   main 不允许直推；合并必须满足规则。

2. **CI Required Check（必须绿灯的检查）**
   你这里叫 `ci/check`（最终是否叫 `check` 取决于 workflow job 名/分支保护配置）。

3. **PR 是唯一变更单元**
   AI 不再“直接改 main”，而是“产出 PR”。

4. **Auto-merge（自动合并）**
   目标：CI 绿灯即合并。你有一次遇到过 “Auto merge is not allowed”，后来你在 Settings 打开了它，并且后续日志显示可以自动合并。

5. **Task Queue / Task State（任务队列/状态机雏形）**

   * QUEUE：待做
   * STATE：在做 / 已做 / 阻塞
     task.sh 就是把“更新任务文档”这件事也纳入 PR 流水线。

6. **Doctor（环境自检）**
   用于 Codex 接管前先跑，避免“环境不对导致 PR 垃圾化”。

---

## 5）当前进度到哪一步了（很明确）

你现在已经完成了“让 AI 接管不翻车”的第一阶段底座：

* ✅ 主分支门禁已生效（必须 PR + 必须 CI）
* ✅ CI workflow 能跑且 PR 上能显示绿灯
* ✅ 本地一键发货脚本（ship）已跑通（含 stash、建 PR、盯 CI、合并、删分支、回 main）
* ✅ 任务入口（task）已跑通（并已产生多次 PR 合并）
* ✅ 自检入口（doctor）已跑通
* ✅ PR 模板、Contributing 已经挂上

仓库语言也印证了它现在主要是“工具仓库”（Shell 为主）。 ([GitHub][1])

---

## 6）下一阶段做什么（按优先级给你一条清晰路线）

> 你刚刚说“先不继续优化 task.sh 的‘无关改动提醒’”，我同意：先把主流程推进到“Codex 真能稳定干活”。

### 阶段 2：把 quant-factory-os 变成“AI 的工作台 + 发布总闸”

重点不是写更多脚本，而是把“AI 怎么接任务、怎么交付、怎么验收”固化下来。

**我建议你下一步按这个顺序：**

1. **把 TASKS/STATE.md 固化成“每天/每次 PR 都要更新”的格式**

   * 当前正在做什么（1-3 行）
   * 今天目标（可验收）
   * 阻塞（如果有）
   * 最近合并的 PR 列表（自动/手动补）
     这样 Codex 打开仓库第一眼就知道“现在该干嘛”。

2. **把 `a9quant-strategy` 的工作也纳入同一套 PR 流程**

   * 你现在 quant-factory-os 是“制度与工具仓”
   * a9quant-strategy 是“交易引擎仓”
     下一阶段要做的是：让 Codex 在 engine 仓也必须：
   * 走 PR
   * 走 CI
   * 用同样的 `ship.sh`（可以复制一份过去，或做成共享模板）

3. **给 CI 加一条最低成本的“护栏测试”**

   * 现在 pytest “no tests ran” CI 也会绿（或者 rc=5 你 doctor 会提示）
   * 你至少需要一个 smoke test：保证脚本可执行、关键文件存在、格式正确
     （这是“防止 AI 一把删掉 tools/ 还合并成功”的关键）

4. （可选）**CODEOWNERS / 审核策略**

   * 如果你未来要让多个 AI 角色并行（Planner/Verifier/Release Governor），这里会很有用。
   * 但你现在资源有限，可以先不做强审核，只保留 CI 门禁。

---

## 7）你刚才问的那个关键点：为什么你觉得 task.sh “已经做了 ship 的事情”？

因为它确实就是这么设计的：

* `ship.sh` = **通用发货流水线**
* `task.sh` = **先做一件事：选任务文件 + 生成提交信息**，然后把剩下所有流程交给 `ship.sh`

所以你以后形成习惯就行：

* 改代码/改文档/改工具：`tools/ship.sh "..."`
* 更新任务队列/状态：`tools/task.sh`

---

如果你愿意，我们下一步就别在“脚本优化细枝末节”上打转了，直接推进到阶段 2 的第 1 步：

**你把你想要的 `TASKS/STATE.md` 最终结构（你脑子里的“状态机字段”）告诉我**，我给你写一个“傻瓜模板”（中文），并告诉你：

* 这个文件每个字段怎么填
* Codex 每次 PR 必须怎么更新它
* 以及怎么用 CI 简单检查“STATE.md 没更新就不让合并”（如果你想要更强门禁的话）

[1]: https://github.com/deepcooker/quant-factory-os "GitHub - deepcooker/quant-factory-os: quant-factory-os"
