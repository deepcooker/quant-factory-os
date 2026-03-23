# PROJECT_BOOTSTRAP_PROTOCOL.md

## 一句话定位
这是“陌生项目尚未接入基座时”的最小同频学习与 owner docs 补齐协议。

## 适用场景
- 目标项目只有一堆文档、半截代码、零散认知
- 对方项目没有我们的 `PROJECT_GUIDE / WORKFLOW / ENTITIES / AGENTS`
- 还没有按 `project_config / task / run / evidence` 接入自动化主线

## 核心原则
- 先学习，再补文档，再谈自动化接入。
- 通用 `PROJECT_GUIDE` 的题目结构保持不变，用它反向逼 AI 先理解项目。
- `PROJECT_GUIDE` 是通用学习协议；标准答案、owner docs 和 run/task 字段是项目化的。
- 面对陌生项目时，先产出协议层草稿，不急着写代码或复制工具。

## 最小接入顺序
1. 收集客户已有材料
   - 项目说明文档
   - 需求文档
   - 架构说明
   - 关键代码目录
   - 已有测试/运行方式
2. 先把 foundation 的最小工具层同步到目标项目
   - 在 foundation 仓执行 `python3 tools/sync_tools.py -p <target_project_root>`
   - 这一步只下沉固定清单中的 `tools/` / `tools/prompts/` 与 `docs/FOUNDATION_BRIDGE.md`
   - 不覆盖目标项目自己的 `tools/project_config.json`
3. 切到目标项目根目录执行 `python3 tools/init.py`
   - 由目标项目自己的 `init` 负责补齐 `tools/`、`docs/`、`TASKS/` 等最小骨架并做预检
4. 用通用 `PROJECT_GUIDE` 提问并自我学习
   - 先答 `Q1 -> Q2 -> Q5 -> Q6 -> Q7 -> Q8 -> Q17`
   - 再答 `Q3 / Q4 / Q9 ... Q16`
5. 先输出一版 `Markdown intake draft`
   - 把背景、目标、范围、不做项、影响面、风险、验收整理出来
6. 基于学习结果补项目化 owner docs
   - `PROJECT_GUIDE`：只补标准答案，不重写题库
   - `WORKFLOW`：补该项目自己的主流程和阶段边界
   - `ENTITIES`：补该项目的对象词典
   - `AGENTS`：补该项目的硬规则
7. 再决定是否接入自动化主线
   - `project_config`
   - `run/task`
   - evidence
   - appserverclient / gitclient

## AI 首轮应输出什么
第一轮不要直接输出实现方案，至少先输出：
- `run_goal`
- `scope`
- `non_goals`
- `impacted_modules`
- `risks`
- `non_functional_constraints`
- `acceptance`
- `role_plan`
- `task_ready`
- `missing_boundaries`

## 需求分析参考
- 传统需求整理方法论可作为 `run 主线程` 的参考材料。
- 它主要服务：
  - 背景澄清
  - 范围边界
  - 影响分析
  - 异常流
  - 非功能要求
  - 验收方式
- 它不直接替代 `PROJECT_GUIDE`，而是帮助 `run-main` 在新主线里做更高质量的需求收敛。

## 不该做的事
- 不要要求陌生项目先按我们的格式整理完再开始。
- 不要只复制零散 `tools/` 文件后就开始接入；固定入口是 `sync_tools -> 目标项目 init -> 文档同频 -> 自动化接入`。
- 不要把 `Markdown intake draft` 误当成机器真相源。
- 不要在还没完成项目级学习前，就直接切到实现细节。
