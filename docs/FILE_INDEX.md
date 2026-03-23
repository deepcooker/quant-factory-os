# FILE_INDEX.md

## 一句话定位
这是当前实验线的快速索引。它回答的是：
- 新 agent 先看什么
- 当前正式主线文件在哪
- 哪些只是补充总览
- 哪些已经降级为历史兼容资产

## 1. 第一阅读顺序

新 agent 当前建议阅读顺序：

1. `AGENTS.md`
2. `docs/PROJECT_GUIDE.md`
3. `docs/WORKFLOW.md`
4. `tools/project_config.json`
5. `state/registry.json`
6. `tools/main.py`
7. `docs/ENTITIES.md`
8. `tests/run_gate.py`

## 2. 正式入口文档

| 文件 | 作用 | 什么时候先看 |
| --- | --- | --- |
| `AGENTS.md` | 宪法、硬规则、执行边界。 | 每次 session 开始 |
| `docs/PROJECT_GUIDE.md` | 学习课程、问题库、主线回拉锚点。 | baseline 学习、主线漂移 |
| `docs/WORKFLOW.md` | 当前实验线状态机。 | 理解阶段与下一跳 |
| `docs/ENTITIES.md` | 当前实验线对象系统。 | 分清 project/job/claim/thread/triage 等对象 |

## 3. 当前运行真相

| 文件 | 作用 | 什么时候先看 |
| --- | --- | --- |
| `tools/project_config.json` | 当前实验线配置源；承载 skills、thread policy、verification policy、human gates。 | 看当前主线配置 |
| `state/registry.json` | 根目录实验线运行真相源；承载 jobs、threads、claims、baseline_snapshot。 | 看当前状态和恢复点 |
| `state/events.jsonl` | 审计日志。 | 回放最近阶段推进 |
| `state/checkpoints/` | 阶段快照。 | 看 resume / recover 依据 |
| `reports/<RUN_ID>/summary.md` | 当前 run 的人类总结证据。 | 看最近做了什么 |
| `reports/<RUN_ID>/decision.md` | 当前 run 的决策证据。 | 看为什么这么做 |

## 4. 当前正式实验线代码

| 文件 | 作用 | 什么时候先看 |
| --- | --- | --- |
| `tools/main.py` | 当前实验线主入口；承载 baseline、coach、verification、correction、planning、role execution、triage、merge、refresh、resume。 | 理解主状态机 |
| `tools/app.py` | 当前正式 app-server client 核心；承载 thread lifecycle、turn、plan/default、skill 挂载、`run_business_turn(...)`。 | 看运行时交互与统一业务入口 |
| `tools/init.py` | 当前实验线准备层入口；补齐并校验 runtime 骨架、配置模板、Codex/app-server、git 工作区。 | 开新 session 或检查仓状态 |
| `tools/sync_tools.py` | 当前实验线同步层入口；向目标项目同步 docs、schemas、skills 和 runtime bundle。 | 向第二个项目下沉新 runtime |
| `tools/project_config.template.json` | 新实验线最小配置模板。 | 看 init / sync / bootstrap 期望的配置骨架 |
| `core/schema_utils.py` | schema 校验工具。 | 看输出校验 |
| `schemas/*.json` | 实验线所有结构化结果模板。 | 看对象和 skill 输出契约 |

## 5. Skills

| 文件 | 作用 | 什么时候先看 |
| --- | --- | --- |
| `.agents/skills/` | 正式 repo-local skills 目录。 | 看当前真正生效的 skills |
| `skills/` | `.agents/skills/` 的可视化镜像。 | 页面浏览或人工查看 |
| `.agents/skills/learn-baseline/SKILL.md` | baseline 学习协议。 | 看长期真相如何建立 |
| `.agents/skills/project-coach/SKILL.md` | 需求澄清协议。 | 看 raw_request 如何进入系统 |
| `.agents/skills/run-manager/SKILL.md` | planning / merge / run 汇总协议。 | 看 run 级收敛 |
| `.agents/skills/doc-evidence-worker/SKILL.md` | 文档证据收集。 | 看 verification |
| `.agents/skills/code-evidence-worker/SKILL.md` | 代码证据收集。 | 看 verification |
| `.agents/skills/runtime-evidence-worker/SKILL.md` | 运行时证据收集。 | 看 verification |
| `.agents/skills/contradiction-checker/SKILL.md` | 冲突检查。 | 看 verification |
| `.agents/skills/demand-critic/SKILL.md` | 需求批判。 | 看 correction |
| `.agents/skills/solution-designer/SKILL.md` | 方案设计。 | 看 correction |
| `.agents/skills/risk-reviewer/SKILL.md` | 风险审查。 | 看 correction |
| `.agents/skills/dev-worker/SKILL.md` | 开发角色协议。 | 看 role execution |
| `.agents/skills/test-worker/SKILL.md` | 测试角色协议。 | 看 role execution |
| `.agents/skills/arch-reviewer/SKILL.md` | 架构评审协议。 | 看 role execution |
| `.agents/skills/defect-triage/SKILL.md` | 缺陷分流协议。 | 看 triage / repair / replan / discussion |

## 6. 验证与发布

| 文件 | 作用 | 什么时候先看 |
| --- | --- | --- |
| `tests/run_smoke_suite.py` | 一键 smoke 入口。 | 做开发级回归 |
| `tests/run_gate.py` | 一键 gate 入口。 | 做发布级验证 |
| `tests/integration_real_app_smoke.py` | 最小真实 app-server 烟测。 | 看真实 runtime 最小集成 |

## 7. 新项目接入

| 文件 | 作用 | 什么时候先看 |
| --- | --- | --- |
| `scripts/bootstrap_experiment_project.py` | 新项目 bootstrap 入口。 | 给第二个项目生成骨架 |
| `templates/experiment_project/` | 新项目模板目录。 | 看接入时会生成哪些最小文件 |

## 8. 补充总览文档

| 文件 | 作用 | 什么时候先看 |
| --- | --- | --- |
| `docs/archive/总纲.md` | 当前实验线流程总纲摘要。 | 先快速看一页总流程 |
| `docs/archive/a.md` | 完成度矩阵 / 汇报稿。 | 需要看“做到哪了”的总表 |
| `docs/archive/EXPERIMENT_LINE_GATE.md` | 旧 gate 说明文档；核心内容已并入 `docs/WORKFLOW.md`。 | 需要回看历史独立 gate 文档时 |
| `docs/archive/PROJECT_BOOTSTRAP.md` | 旧 bootstrap 说明文档；当前接入方式仍属实验性，已从主目录降级归档。 | 需要回看历史独立 bootstrap 说明时 |

说明：
- 这两份有用
- 但它们不是正式入口
- 它们用于总览、复盘、汇报，不替代主线文档

## 9. 历史兼容资产

以下内容现在不再是当前正式主线解释中心，只保留为：
- 历史对照
- 兼容资产
- 迁移参考

| 文件 | 作用 |
| --- | --- |
| `docs/archive/project_guide_backup.md` | 旧版 `PROJECT_GUIDE` 备份 |
| `tools/backup/legacy_runtime/` | 旧 `tools/` runtime 备份目录 |
| `tools/backup/runtime_demo_archive/appserver_demo.py` | 已归档的 app-server 协议验证稿 |
| `tools/gitclient.py` | 当前保留的 git / PR / rollback 交付层 |
| `tools/view.sh` | 当前保留的稳定阅读器 |

## 10. 当前最短操作面

当前实验线最短稳定操作面：

```text
baseline
-> coach
-> verification
-> correction
-> planning
-> role execution
-> defect triage
-> merge
-> baseline refresh
-> smoke / gate
```

如果是新项目接入：

```text
bootstrap_experiment_project.py
-> skeleton / runnable / runtime-bundle
-> 再进入主运行流程
```
