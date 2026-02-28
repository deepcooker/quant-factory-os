## 终点一致
自动化、自我迭代、涌现智能是这个仓库的统一北极星。本轮通过把同频考试接入单命令流程，减少人工步骤和会话摩擦，让后续执行可以持续迭代并稳定沉淀证据链。

## 阶段一致
当前阶段是治理与同频自动化强化；下一阶段是基于稳定门禁推进任务执行自动化。阶段切换条件是 ready/exam 通过、证据完整、并且命令链可重复执行。

## 上轮停止原因与恢复状态
上轮停止原因分类是 tool_or_script_error。停止时点是 ship/resume 收尾阶段；当前恢复状态是 main 已同步，RUN_ID 对应证据可追溯，可继续执行。

## 边界与非目标
本轮边界是只改治理与流程脚本，不改财富业务策略与量化逻辑；non-goals 是不做策略参数变更，不做外部系统接入，不做无证据的临时修补。

## 近况与最近提交
最近已交付（PR / RUN_ID）可从 TASKS/QUEUE.md Done 记录与 reports 目录核对；当前近况是 exam-auto 自动化增强在推进，最近提交主题为：run-2026-02-28-qf-resume-pr: task: TASK: qf resume 已合并场景避免重复创建 PR (#141)（7e6157a）。

## 下一步单命令
命令：tools/qf ready RUN_ID=run-2026-02-28-qf-exam-auto
为什么是这一条（因果解释）：先完成门禁文件，再进入 plan/do，保证执行有一致入口和可审计前置条件。

## 失败回退命令
命令：tools/qf resume RUN_ID=run-2026-02-28-qf-exam-auto
触发条件：ship 或 resume 中断、网络波动或本地同步失败时，使用该命令恢复并完成收尾。

## 学习更新清单
- 本轮必须新增/复习的技能或规则（至少 3 条）：qf 生命周期命令；exam 评分规则；ship/resume 故障恢复。
- 对应学习来源文件：AGENTS.md；docs/WORKFLOW.md；SYNC/EXAM_RUBRIC.json；TASKS/TASK-qf-exam-auto.md
