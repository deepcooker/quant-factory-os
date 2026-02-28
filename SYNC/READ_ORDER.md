# 阅读顺序

这是会话接班的强制阅读顺序。

## 第 0 步：启动
1. `tools/qf init`
2. 若 `TASKS/STATE.md` 存在 `CURRENT_RUN_ID`：执行 `tools/qf handoff`

## 第 1 步：同频层（必须按顺序）
1. `SYNC/README.md`
2. `SYNC/CURRENT_STATE.md`
3. `SYNC/SESSION_LATEST.md`
4. `SYNC/DECISIONS_LATEST.md`
5. `SYNC/LINKS.md`

## 第 1.5 步：同频考试（新/陌生 agent 必做）
1. `SYNC/EXAM_PLAN_PROMPT.md`
2. `SYNC/EXAM_ANSWER_TEMPLATE.md`
3. `SYNC/EXAM_WORKFLOW.md`
4. `SYNC/EXAM_RUBRIC.json`

## 第 2 步：治理核心
1. `AGENTS.md`
2. `docs/WORKFLOW.md`
3. `docs/ENTITIES.md`
4. `docs/PROJECT_GUIDE.md`
5. `TASKS/STATE.md`
6. `TASKS/QUEUE.md`

## 第 3 步：当前 RUN 证据
1. 最新 `reports/<RUN_ID>/handoff.md`（如果存在）
2. 最新 `reports/<RUN_ID>/conversation.md`（如果存在）
3. 最新 `reports/<RUN_ID>/decision.md`
4. 最新 `reports/<RUN_ID>/summary.md`

## 完成标准（必须复述）
- 目标（一句话）
- Scope（精确路径）
- 验收（verify/evidence/scope）
- 下一条命令（只给一条）
- 同频证据：`reports/<RUN_ID>/sync_report.json` 已生成且 `sync_passed=true`
- 门禁文件：`reports/<RUN_ID>/ready.json` 已生成
