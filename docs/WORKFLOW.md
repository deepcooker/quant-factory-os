# WORKFLOW

本文件定义本仓的状态机。

它回答的是：
- 当前流程分几层
- 每一层的目标是什么
- 每一层的输入、输出、门禁和下一跳是什么

它不负责重复解释所有命令参数。
对象定义以 `docs/ENTITIES.md` 为准，硬规则以 `AGENTS.md` 为准。

补充定位：
- 本文件描述的是 foundation repo 当前状态机。
- 自动化 1.0 的“business project repo 单入口目标形态”见 `docs/AUTOMATION_1_0.md`。

## 1. 设计原则

### 1.1 流程分层
流程固定分为五层：

1. 上岗层
   - `init`
   - `learn`
   - `ready`
2. 讨论层
   - `orient`
   - `choose`
   - `council`
   - `arbiter`
3. 拆解层
   - `slice`
   - `queue`
   - `task`
4. 执行层
   - `do`
   - `verify`
   - `review`
5. 交付层
   - `ship`
   - `run close`
   - `state update`

### 1.2 边界原则
- `init` 不学习，不讨论，不执行。
- `learn` 不决定方向，不授权执行。
- `ready` 只做 Go/No-Go 门禁。
- discussion 先于 execution。
- `queue` 在 discussion 之后，不在 discussion 之前。

### 1.3 对象原则
- `project_id`：长期上下文
- `run_id`：一轮周期容器
- `task_id`：run 内最小执行切片
- discussion artifacts：方向到合同的中间对象

对象边界见：
- [docs/ENTITIES.md](/root/quant-factory-os/docs/ENTITIES.md)

## 2. 状态机总览

```text
project
  -> init
  -> learn
  -> ready
  -> orient
  -> choose
  -> council
  -> arbiter
  -> slice
  -> queue/task
  -> do
  -> verify
  -> review
  -> ship
  -> run close
```

## 3. S0 上岗层

### 3.1 `init`

命令：
- `python3 tools/init.py`

目标：
- 诊断环境和现场

输入：
- 当前仓库
- `TASKS/STATE.md`
- git branch / worktree / remote 状态

输出：
- 控制台状态打印

关键输出锚点：
- `INIT_PROJECT_ID`
- `INIT_RUN_ID`
- `INIT_TASK_FILE`
- `INIT_BRANCH`
- `INIT_DIFF_SUMMARY`
- `INIT_STATUS`
- `INIT_NEXT`

职责：
- 打印账号、版本、分支、工作区差异
- 确认当前 `project/run/task`
- 判断当前是正常、脏工作区、还是需要 resume

非职责：
- 不创建业务 `RUN_ID`
- 不做项目同频
- 不生成讨论产物
- 不授权执行

下一跳：
- 若 `INIT_STATUS=needs_resume`，先处理恢复
- 否则进入 `learn`

### 3.2 `learn`

命令：
- `python3 tools/learn.py`

目标：
- 完成项目同频和主线回拉

输入：
- `docs/PROJECT_GUIDE.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`
- 由 `PROJECT_GUIDE` 引导出的必查文件
- 当前 `TASKS/STATE.md`
- 当前 run evidence（若存在）

输出：
- `learn/<project_id>.json`
- `learn/<project_id>.md`
- `learn/<project_id>.stdout.log`
- `learn/<project_id>.model.*`

职责：
- 通过真实 Codex Plan 模式读取课程与证据
- 输出主线、当前阶段、下一步
- 对 `PROJECT_GUIDE` 全量逐题口述
- 判断是否偏离主线并给出回拉动作

固定规则：
- 真模型交互是硬门禁
- transport 固定为 `app-server`
- 必须是真 Plan 模式
- `PROJECT_GUIDE` 是课程驱动器
- 不再使用考试分数

关键输出锚点：
- `LEARN_MAINLINE`
- `LEARN_CURRENT_STAGE`
- `LEARN_NEXT_STEP`
- `LEARN_REQUIRED_FILES_READ_LIST`
- `LEARN_MODEL_MAINLINE`
- `LEARN_MODEL_CURRENT_STAGE`
- `LEARN_MODEL_NEXT_STEP`
- `LEARN_MODEL_FILES_READ_LIST`
- `LEARN_MODEL_ORAL_Q_COUNT`
- `LEARN_MODEL_ORAL_QID1..N`
- `LEARN_MODEL_ORAL_Q1..N`
- `LEARN_MODEL_ORAL_A1..N`
- `LEARN_MODEL_ANCHOR_*`

非职责：
- 不决定需求方向
- 不生成 execution contract
- 不直接进入执行

下一跳：
- `ready`

### 3.3 `ready`

命令：
- `python3 tools/ready.py`

目标：
- 给当前 run/task 出开工许可

输入：
- `TASKS/STATE.md`
- 当前 task 合同
- `learn/<project_id>.json`
- 必要时当前 run evidence

输出：
- `reports/<RUN_ID>/ready.json`

职责：
- 校验 `learn` 是否通过
- 校验当前 `project/run/task` 是否明确
- 固定本次工作的最小合同：
  - `goal`
  - `scope`
  - `acceptance`
  - `stop_condition`
- 处理 unresolved run decision

非职责：
- 不再解释项目知识
- 不再承担学习任务
- 不生成方向草稿
- 不自动推进到讨论或执行

关键输出锚点：
- `READY_PROJECT_ID`
- `READY_RUN_ID`
- `READY_TASK_FILE`
- `READY_DECISION`
- `READY_FILE`
- `READY_NEXT_COMMAND`

下一跳：
- `orient`

## 4. S1 讨论层

### 4.1 `orient`

命令：
- `python3 tools/orient.py`

目标：
- 生成候选方向

输入：
- 当前 `project/run`
- owner docs
- `ready.json`
- 当前 state/evidence

输出：
- `chatlogs/discussion/<RUN_ID>/orient.json`
- `chatlogs/discussion/<RUN_ID>/orient.md`

职责：
- 产出多个方向选项
- 每个方向说明 why / risk / priority / scope_hint

下一跳：
- `choose`

### 4.2 `choose`

命令：
- `python3 tools/choose.py OPTION=<id>`

目标：
- 明确选择一个方向

输入：
- `orient.json`

输出：
- `reports/<RUN_ID>/orient_choice.json`
- `reports/<RUN_ID>/direction_contract.json`
- `reports/<RUN_ID>/direction_contract.md`

职责：
- 固定已选择方向
- 给后续 council 一个明确输入

下一跳：
- `council`

### 4.3 `council`

命令：
- `python3 tools/council.py`

目标：
- 让多角色独立评审

输入：
- `orient_choice.json`
- `direction_contract.json`

输出：
- `chatlogs/discussion/<RUN_ID>/council.json`
- `chatlogs/discussion/<RUN_ID>/council.md`

职责：
- 产品 / 架构 / 研发 / 测试独立给出意见
- 暴露 blocker / warn / disagreement

下一跳：
- `arbiter`

### 4.4 `arbiter`

命令：
- `python3 tools/arbiter.py`

目标：
- 把讨论收敛成执行合同

输入：
- `council.json`
- `direction_contract.json`

输出：
- `reports/<RUN_ID>/execution_contract.json`
- `reports/<RUN_ID>/execution_contract.md`

职责：
- 汇总独立视角
- 固定目标、非目标、scope、约束、风险

下一跳：
- `slice`

## 5. S2 拆解层

### 5.1 `slice`

命令：
- `python3 tools/slice_task.py`

目标：
- 把 execution contract 拆成 task 切片

输入：
- `execution_contract.json`

输出：
- `reports/<RUN_ID>/slice_state.json`
- `TASKS/QUEUE.md` slice blocks

职责：
- 生成最小 task 切片
- 维持 queue 幂等写入

下一跳：
- queue / task selection

### 5.2 `queue`

目标：
- 承接待执行切片，不定义需求本身

真相源：
- `TASKS/QUEUE.md`

规则：
- queue item 必须来自某个 run 的 slice
- queue item 被领取后，应实体化成 `TASKS/TASK-*.md`

下一跳：
- `do`

## 6. S3 执行层

### 6.1 `do`

命令：
- `bash tools/legacy.sh do queue-next`

目标：
- 领取并执行下一个 task

输入：
- `ready.json`
- `orient_choice.json`
- `council.json`
- `execution_contract.json`
- `slice_state.json`
- queue 中的待执行项

输出：
- 代码变更
- verify 结果
- run evidence 更新

职责：
- 领取 queue item
- 实现最小 diff
- 保持执行轨迹

门禁：
- 缺任一前置 gate 时必须失败

下一跳：
- `verify`

### 6.2 `verify`

目标：
- 确认实现满足合同

输入：
- 当前 diff
- task acceptance

输出：
- 本地验证结果
- summary/decision 更新

规则：
- 本地验证优先
- 未通过不得进入 ship

### 6.3 `review`

命令：
- `bash tools/legacy.sh review`

目标：
- 检查 drift、风险和文档一致性

输入：
- run evidence
- verify 结果

输出：
- `reports/<RUN_ID>/drift_review.json`
- `reports/<RUN_ID>/drift_review.md`

规则：
- strict blocker 未清空，不得 ship

下一跳：
- `smoke`

### 6.4 `smoke`

目标：
- 做 ship 前的 release-prep 检查

输入：
- 当前 task 合同
- verify 结果
- review 结果
- 当前 run evidence
- owner docs 更新状态

输出：
- ship-ready 结论
- 缺失材料清单（如有）

规则：
- smoke 不负责远端交付；它只判断是否具备 ship 条件
- 至少确认以下内容已经齐备：
  - verify 已通过
  - strict review blocker 已清空
  - `reports/<RUN_ID>/summary.md`
  - `reports/<RUN_ID>/decision.md`
  - `reports/<RUN_ID>/meta.json`
  - 若流程/规则/工具行为变化，对应 owner docs 已同步
- 缺材料、合同不清、验证未过时，必须退回 task owner / 项目负责人

下一跳：
- `ship`

## 7. S4 交付层

### 7.1 `ship`

命令：
- `tools/ship.sh`

目标：
- 完成交付与同步

输入：
- 已验证 diff
- 当前 task 合同
- 当前 run evidence

输出：
- commit / push / PR / merge
- `ship_state.json`（如适用）

规则：
- one task -> one branch -> one PR
- ship 前必须更新证据和 owner docs
- ship 负责 git / branch / commit / push / PR / merge / sync
- `ship_state.json` 属于 ship 自动回写的交付状态文件；业务材料不在 ship 阶段补写
- 成功路径下，`ship` 不应在 PR merge 之后继续重写已跟踪的 `ship_state.json`，避免为记录成功状态再次弄脏工作区并阻塞 post-ship sync；失败与恢复状态仍需落 `ship_state.json`

### 7.2 `run close`

目标：
- 关闭 run 或进入下一个 task

条件：
- 当前 run 下 task 全部完成
- 或明确终止

输出：
- `TASKS/STATE.md` 指针更新
- `decision.md` 记录 stop reason

## 8. Readiness Completion

进入执行前，至少必须有：
- `python3 tools/init.py`
- `python3 tools/learn.py`
- `python3 tools/ready.py`
- `python3 tools/orient.py`
- `python3 tools/choose.py`
- `python3 tools/council.py`
- `python3 tools/arbiter.py`
- `python3 tools/slice_task.py`

执行入口：
- `bash tools/legacy.sh do queue-next`

## 9. 默认日常流程

推荐日常顺序：

1. `python3 tools/init.py`
2. `python3 tools/learn.py -daily`
3. `python3 tools/ready.py`
4. `python3 tools/orient.py`
5. `python3 tools/choose.py OPTION=<id>`
6. `python3 tools/council.py`
7. `python3 tools/arbiter.py`
8. `python3 tools/slice_task.py`
9. `bash tools/legacy.sh do queue-next`
10. `bash tools/legacy.sh review RUN_ID=<run-id> STRICT=1 AUTO_FIX=1`
11. `tools/smoke.sh`
12. `tools/ship.sh`

说明：
- `-daily` 是日常同频入口，等价于 `-medium`，用于减少档位选择负担；不改变 `learn` 的强同频、app-server 和 oral restatement 硬门禁。
- `tools/smoke.sh` 是 ship 前的 readiness/checklist 层，不直接执行远端 PR/merge。
- `tools/task.sh` / `tools/ship.sh` 默认保持当前 active branch 作为发货基线；只有显式以 `main` 为基线时，`ship.sh` 才会执行 `fetch/pull origin main`。
- 当 `gh pr merge` 前发现 PR 不是 cleanly mergeable 时，`ship.sh` 会以 `pr_merge_blocked` 退出并打印 base-into-head 恢复命令，而不是继续盲重试。

说明：
- `-daily` 是日常同频入口，等价于 `-medium`，用于减少档位选择负担；不改变 `learn` 的强同频、app-server 和 oral restatement 硬门禁。
- `tools/task.sh` / `tools/ship.sh` 默认保持当前 active branch 作为发货基线；只有显式以 `main` 为基线时，`ship.sh` 才会执行 `fetch/pull origin main`。

## 10. Pause / Resume

当 run 中断时：
- 优先用 `bash tools/legacy.sh resume RUN_ID=<run-id>`
- 必要时先用 `bash tools/legacy.sh handoff RUN_ID=<run-id>` 生成接班摘要

停止原因统一记录到：
- `reports/<RUN_ID>/decision.md`

标准 stop reason：
- `task_done`
- `needs_human_decision`
- `infra_network`
- `infra_quota_or_auth`
- `tool_or_script_error`
- `verify_failed`
- `external_blocked`

## 11. Documentation Freshness Gate

流程、规则、工具行为变化时，必须在同一 run 更新：
- `AGENTS.md`
- `docs/WORKFLOW.md`
- `docs/ENTITIES.md`（若对象定义变化）
- `docs/PROJECT_GUIDE.md`（若学习语义变化）
- `reports/<RUN_ID>/summary.md`
- `reports/<RUN_ID>/decision.md`

没有文档同步，不得 ship。
