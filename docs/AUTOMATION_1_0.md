# AUTOMATION_1_0

本文件定义自动化 1.0 的成功定义。

它回答的是：
- 当前基座做到什么程度，才算可以“开始稳定接项目”
- foundation repo 与 business project repo 的关系是什么
- 为什么 1.0 的目标不是继续解释基座，而是让基座退到后台

它不负责替代：
- `AGENTS.md` 的硬规则
- `docs/WORKFLOW.md` 的当前状态机
- `docs/ENTITIES.md` 的对象定义

## 1. 目标边界

自动化 1.0 的成功标准不是“基座永远自我元迭代”，而是：

- foundation repo 已经足够稳定
- business project repo 可以用一个入口接真实需求
- 系统能从项目同频一路跑到交付
- 失败时停在可恢复状态

1.0 验收到：
- 需求收敛
- 合同化执行
- 验证
- `smoke`
- `ship`

1.0 暂不把“上线后的 Observe / Operate / Iterate 闭环”算入完成条件。

## 2. 两层结构

### 2.1 Foundation Repo

当前仓库是 foundation repo。

职责：
- 维护宪法、工作流、对象模型
- 提供 `learn / ready / discuss / execute / review / smoke / ship` 能力
- 维护恢复路径与证据规则

非职责：
- 不作为业务项目日常入口
- 不要求业务项目用户显式学习基座

### 2.2 Business Project Repo

业务项目仓是自动化 1.0 的日常运行载体。

职责：
- 承接真实需求
- 以项目为中心做同频
- 调用 foundation 提供的稳定能力
- 按 `run -> task -> evidence -> ship` 交付

对日常用户只暴露：
- 一个正式入口
- 一页项目宪法
- 项目自己的需求、架构、验收、运行材料

## 3. 基座退到后台

当前难度高，是因为系统还在“造自己”。

1.0 成熟后，日常运行不应再显式重学基座；基座知识应被产品化到后台：

- 规则默认锁进流程与门禁
- 用户主要同频的是项目本身
- foundation 只在异常、升级、维护时显式出现

这不是“忘记规则”，而是：
- 规则被固化
- 正常路径不再依赖人工记忆基座

## 4. 1.0 Definition of Done

自动化 1.0 达成，至少必须满足以下条件。

### 4.1 单入口

business project repo 提供一个正式入口，例如：

`python tools/factory.py run --goal "<需求>"`

要求：
- 从需求输入一路跑到交付
- 用户不需要手工串联 `learn / ready / orient / ... / ship`
- 重跑不破坏 `TASKS/STATE.md` 与 `reports/<RUN_ID>/` 一致性

### 4.2 项目 learn 成为日常主入口

日常运行的 learn 重点是：
- 项目目标
- 项目约束
- 项目架构与当前状态
- 当前 run/task

而不是再次显式学习 foundation repo 本身。

### 4.3 因果顺序自检

系统必须自动拒绝以下反模式：
- 没有收敛合同就进入执行
- 没有 `execution_contract` 就切 task
- 把 queue 当主线
- 把 session 当 run
- 没有 ready 就进入执行层

### 4.4 Ready 自动化

`ready.json` 必须成为真正的开工许可。

至少固定：
- `goal`
- `scope`
- `acceptance`
- `stop_condition`

没有 ready 或 ready 不通过，不得进入执行层。

### 4.5 合同交接稳定

执行层必须只吃讨论层的收敛产物：
- `direction`
- `execution_contract`
- `slice_state`
- `task`

没有 contract，不得 task 化。

### 4.6 最低证据集自动落盘

每个 run 必须自动生成：
- `reports/<RUN_ID>/meta.json`
- `reports/<RUN_ID>/summary.md`
- `reports/<RUN_ID>/decision.md`

缺任意一个，就不算完成交付。

### 4.7 异常恢复一致

失败时必须明确：
- 当前停在哪一步
- 哪个文件是真相源
- 下一条恢复命令是什么
- 是否允许直接重跑

恢复能力是 1.0 的硬要求，不是附加优化。

## 5. 当前仓库与 1.0 的关系

当前仓库仍处于 foundation 强化阶段。

这意味着：
- 它已经在逼近自动化 1.0 的基座条件
- 但它自己还不是最终的 business project repo 日常入口
- 当前主线仍是把 foundation 做稳，直到项目仓可以主要学习项目本身

## 6. 一句话总结

自动化 1.0 的成功，不是让 agent 永远理解“如何造这台机器”，而是：

让 foundation repo 足够稳定，以至于 business project repo 可以像流水线一样，用一个入口稳定接需求并完成交付。
