## 终点一致
- 一句话北极星：把当前项目打造成同频优先的自动化基建，最终走向自动化、自我迭代、涌现智能。
- 本轮动作如何服务“自动化 -> 自我迭代 -> 涌现智能”：先建立统一题面与评分程序，确保每个新 agent 上岗前的世界模型一致，再进入执行自动化，后续可在错题中持续自我迭代并形成稳定协作。
- 证据路径：docs/PROJECT_GUIDE.md, SYNC/README.md

## 阶段一致
- 当前阶段：治理与同频层强化阶段。
- 下一阶段：在稳定同频前提下推进更高自动化密度。
- 阶段切换条件：同频考试通过率稳定、执行门禁和证据链持续通过。
- 证据路径：SYNC/CURRENT_STATE.md, docs/WORKFLOW.md

## 上轮停止原因与恢复状态
- 上轮停止原因分类：tool_or_script_error（ship/resume 收尾切分支时的本地改动冲突）。
- 停止时点：PR 已合并后本地回 main 收尾阶段。
- 当前恢复状态：已通过 stash 清理与同步恢复到 main。
- 证据路径：reports/run-2026-02-27-qf-stash-clean-command/, reports/run-2026-02-27-p0-clean-garbage-reports-and-add-archive-structure/

## 边界与非目标
- 本轮必须守住的边界（至少 3 条）：不改业务策略；不跳过 ready/证据门禁；不破坏 PR 驱动主流程。
- 本轮明确不做的事情（non-goals）：不重写任务系统；不引入 CI 依赖。
- 证据路径：AGENTS.md, docs/WORKFLOW.md

## 近况与最近提交
- 最近已交付（PR / RUN_ID）：PR #134 / run-2026-02-27-qf-stash-clean-command；PR #135 / run-2026-02-27-p0-clean-garbage-reports-and-add-archive-structure。
- 当前项目近况一句话：同频入口已稳定，正在把思想对齐做成可量化门禁。
- 下一阶段最关键的 1~2 件事：统一同频考核口径；推进任务/报告归档收敛。
- 证据路径：TASKS/STATE.md, SYNC/DECISIONS_LATEST.md

## 下一步单命令
- 命令：tools/qf handoff
- 为什么是这一条（因果解释）：先生成最新接班摘要，再进入 ready/do，能减少断线和账号切换造成的状态漂移。

## 失败回退命令
- 命令：tools/qf resume RUN_ID=run-2026-02-27-sync-learning-exam-cli-web
- 触发条件：ship/resume 中断、网络异常或本地切分支失败时。

## 学习更新清单
- 本轮必须新增/复习的技能或规则（至少 3 条）：同频考试题面的稳定复用；评分规则与必过项；停止原因分类统一。
- 对应学习来源文件：SYNC/EXAM_PLAN_PROMPT.md, SYNC/EXAM_RUBRIC.json, docs/WORKFLOW.md
