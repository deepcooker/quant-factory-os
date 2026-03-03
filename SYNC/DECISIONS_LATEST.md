# 最新决策

日期：2026-03-04
RUN_ID: `run-2026-03-04-docs-governance-cleanup`

## 决策 1：文档边界必须 owner 唯一化
- 结论：同一主题只能有一个 owner 文档，其他文件只允许链接，不允许重复定义。
- 原因：当前痛点不是信息不够，而是重复定义导致同频冲突。
- 影响：新会话定位规则速度更快，冲突排查成本更低。

## 决策 2：删除过时/占位文档，降低噪声
- 结论：删除 `docs/BOUNDARY_A9.md`、`docs/CODEX_ONBOARDING_CONSTITUTION.md`、`docs/INTEGRATION_A9.md`。
- 原因：三者存在过时流程、占位内容或重复约束，继续保留会误导新 agent。
- 影响：文档树更干净，入口更明确。

## 决策 3：SYNC 链接层去历史 run 固定列表
- 结论：`SYNC/LINKS.md` 改为稳定入口与 `<RUN_ID>` 模板，不再硬编码历史 run 列表。
- 原因：硬编码历史 run 会把同频注意力拉偏到旧证据。
- 影响：接班默认围绕 `TASKS/STATE.md` 指针读取当前证据。

## 决策 4：边界判定方法写入硬规则
- 结论：在 `AGENTS.md` 增加 `Documentation boundary (Hard)`。
- 原因：边界不能靠口头约定，必须有可审计的硬规则。
- 影响：后续清理/新增文档可以按同一判定标准执行（保留/删除/合并/细化）。
