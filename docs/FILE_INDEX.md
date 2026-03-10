# FILE_INDEX.md

## 一句话定位
这是实验性的全量文件职责索引，用来帮助新 agent 在最短时间内定位“先看什么、为什么看、文件各自负责什么”。

## 使用方式
- 先看 owner docs 索引，再看 tools 索引，最后看 task / reports 索引。
- 这个文件不是流程文档，也不是设计白皮书；它只负责快速定位。
- 文件职责变化时，应同步更新这里的一句话说明。

## 1. Owner Docs

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `AGENTS.md` | 宪法与硬规则，定义门禁、允许命令、文档新鲜度和 PR 纪律。 | 每次 session 开始时 |
| `docs/PROJECT_GUIDE.md` | 学习课程、问题库、标准答案、主线回拉锚点。 | baseline 学习和主线漂移时 |
| `docs/WORKFLOW.md` | 状态机、阶段定义、主流程说明。 | 理解流程和阶段边界时 |
| `docs/ENTITIES.md` | 核心对象、状态和交付单元的词典。 | 理解 task/run/project/pr 等名词时 |
| `TOOLS_METHOD_FLOW_MAP.md` | 实验性主流程方法索引与调用图。 | 看主流程入口和方法调用时 |

## 2. Runtime / Config

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/project_config.json` | 项目最小配置数据源，含 required / git / runtime_state / session_registry。 | 看项目接入最小字段和当前运行状态时 |
| `tools/project_config.template.json` | 其他项目接入时可复用的最小配置模板。 | 新项目接入时 |
| `tools/project_config.py` | 统一配置出口；把 JSON 最小数据、系统常量和运行时状态拼成统一大配置视图。 | 任何脚本取配置时 |
| `tools/result_schema.py` | 可组合流程方法统一返回协议：`err_code / err_desc / data`。 | 新增流程入口时 |

## 3. Prepare / Runtime / Git

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/init.py` | 环境准备、项目骨架补齐、Codex/Git 前置检查。 | 开工前环境准备时 |
| `tools/appserverclient.py` | Codex app-server runtime 核心；负责 baseline / fork / current-turn。 | 学习基线和当前 session 推进时 |
| `tools/gitclient.py` | Git 底层；负责 commit、PR、merge、rollback、main 同步。 | 收尾交付和回滚时 |

## 4. Learning / Workflow

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/learn.py` | 当前 learn 工作流入口；包含课程化学习和产物收口逻辑。 | 看 learn 旧实现和迁移边界时 |
| `tools/ready.py` | `learn` 后的门禁与合同准备。 | 看是否允许进入方向讨论时 |
| `tools/orient.py` | 方向草案生成。 | 需求方向收敛开始时 |
| `tools/choose.py` | 方向确认与合同生成。 | 确认方向时 |
| `tools/council.py` | 多角色独立评审。 | 做独立评审时 |
| `tools/arbiter.py` | 收敛 execution contract。 | 需要统一合同和 blockers 时 |
| `tools/slice_task.py` | 把执行合同拆成最小 task。 | 进入最小任务拆分时 |
| `tools/run_main.py` | Python 总入口骨架。 | 看统一 orchestrator 主入口时 |

## 5. Prompt / Learning Assets

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/learnbaseline_prompt.md` | baseline 学习固定前言 prompt 文件。 | 调整 baseline 学习提示词时 |
| `tools/learn_prompt_compare.md` | `learn.py` 与 `appserverclient` baseline prompt 对比说明。 | 做提示词迁移时 |

## 6. Task / State / Evidence

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `TASKS/QUEUE.md` | 待办队列与意图入口。 | 选择下一个 task 时 |
| `TASKS/TASK-tools-orchestrator-entry.md` | 当前活跃任务文件。 | 确认本轮目标和验收时 |
| `TASKS/STATE.md` | runtime_state 的镜像输出。 | 兼容查看当前 run/task 指针时 |
| `reports/<RUN_ID>/summary.md` | 当前 run 的总结证据。 | 看最近做了什么时 |
| `reports/<RUN_ID>/decision.md` | 当前 run 的决策证据。 | 看为什么这么做时 |

## 7. Legacy / Compatibility

| 文件 | 作用 | 什么时候优先看 |
| --- | --- | --- |
| `tools/legacy.sh` | 兼容入口路由。 | 老 shell 子命令仍在使用时 |
| `tools/doctor.sh` | 辅助诊断脚本。 | 排查环境和 Git/Codex 体检时 |
| `tools/ship.sh` | 旧 ship 实现。 | 对照旧发货逻辑时 |
| `tools/view.sh` | 分块读取长文件。 | 按仓库规则读长文件时 |

## 8. 当前建议阅读顺序

1. `AGENTS.md`
2. `docs/PROJECT_GUIDE.md`
3. `docs/WORKFLOW.md`
4. `docs/ENTITIES.md`
5. `TOOLS_METHOD_FLOW_MAP.md`
6. `tools/project_config.py`
7. `tools/appserverclient.py`
8. `tools/gitclient.py`
