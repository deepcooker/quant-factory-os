# WEALTH_SYSTEM_NEW_PROJECT_GUIDE.md

## 目标
- 在不破坏基座规则的前提下，快速启动“财富系统”业务项目。
- 明确基座仓与业务仓边界，避免任务、证据、分支混乱。

## 输出物（完成定义）
- 新项目仓库建立并可执行最小验证命令。
- 基座仓中有该项目的集成合同与证据指针。
- 一次端到端 dry-run 完成并记录可回放证据。

## 启动前置
- 已完成基座同频：`tools/ops init -> tools/ops learn MODEL_SYNC=1 PLAN_MODE=strong -log -> tools/ops ready`
- 明确当前 `project_id`、`run_id` 与任务边界（以 `TASKS/STATE.md` 和任务文件为准）。
- 仅允许在任务 scope 内改动。

## 新建项目流程（建议 7 步）

### Step 1: 明确项目边界
- 定义业务仓职责：资产视图、风控、收益引擎接入、审计报表。
- 定义基座仓职责：流程门禁、任务编排、证据治理、评审收敛。

### Step 2: 创建业务仓最小结构
- 最小目录建议：
  - `README.md`
  - `docs/ARCHITECTURE.md`
  - `src/`
  - `tests/`
  - `Makefile`（至少有 `make verify`）
- 要求：`make verify` 可在无生产凭据场景下执行。

### Step 3: 定义集成合同
- 在基座仓记录合同文件（建议）：
  - `docs/INTEGRATION_WEALTH.md`
- 合同至少包含：
  - 允许调用的命令（如 `make verify`, `make dryrun`）
  - 输入输出路径约束
  - 禁止事项（禁止实盘、禁止生产密钥）
  - 必须回写的证据字段（repo URL、commit SHA、verify 结果）

### Step 4: 建立证据指针规则
- 基座仓 `reports/<RUN_ID>/decision.md` 必须记录：
  - 业务仓 PR 链接
  - 业务仓 commit SHA
  - 验证命令与结果摘要
- 大体积日志使用“指针化”记录（路径 + checksum），不直接塞进主文档。

### Step 5: 先跑 dry-run 再讨论实执行
- 先完成：
  - 配置校验
  - 风控阈值校验
  - 数据契约校验
- 通过后再进入“是否允许更高权限执行”的人类决策。

### Step 6: 多角色评审收敛
- 使用基座流程：
  - `tools/ops discuss TARGET=prepare`
  - `tools/ops choose OPTION=<id>`
  - `tools/ops execute TARGET=do CONFIRM_CONTRACT=1`
- 要求产品/架构/测试/研发视角均有证据产出再收敛。

### Step 7: 回写与复盘
- 更新：
  - `reports/<RUN_ID>/summary.md`
  - `reports/<RUN_ID>/decision.md`
  - 必要时 `MISTAKES/<RUN_ID>.md`
- 规则变更时同步更新：
  - `AGENTS.md`
  - `docs/WORKFLOW.md`
  - 对应操作手册

## 风险清单
- 基座仓与业务仓职责混淆，导致审计链断裂。
- 没有 dry-run 就进入高风险执行。
- 只写结论不写证据指针，后续无法复盘。
- 新项目接口不稳定时，过早插件化导致全局耦合。

## 推荐策略
- 当前阶段优先“独立业务仓 + 基座编排治理”。
- 等基座流程稳定、接口稳定后，再评估插件化分发。
