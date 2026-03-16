init-project: 接下来请你对一个尚未接入基座的新项目执行首轮初始化反写规划。

目标：
- 基于项目已有文档和现有实现，完成首轮 owner docs 反写规划
- 先学习、再补证据、最后反写，不允许直接跳到写结论
- 保护 PROJECT_GUIDE 等关键 owner docs，避免误覆盖

硬规则：
- 你面对的是“未初始化项目”，只有在首轮接入完成后，项目才允许进入 baseline 主线
- 输入材料不是最终真相，必须结合现有实现确认项目已经做到哪里
- 不允许把我们自己的 owner docs 当成原始输入材料
- 如果证据不够，必须明确提出“下一批必读文件”，不能假装已经理解完整
- 第一阶段默认是 plan/gating 阶段；在 `can_write_owner_docs = true` 之前，不允许输出 owner docs 正文

默认读取顺序：
1. 先读项目根目录的 `README.md`，把它当作 guide / 材料理解说明
2. 再读原始 docs 材料（`docs/**/*.md|txt|doc|docx`），但排除以下 owner docs 目标文件：
   - `AGENTS.md`
   - `docs/PROJECT_GUIDE.md`
   - `docs/WORKFLOW.md`
   - `docs/ENTITIES.md`
   - `docs/FILE_INDEX.md`
   - `docs/TOOLS_METHOD_FLOW_MAP.md`
   - `docs/PROJECT_BOOTSTRAP_PROTOCOL.md`
3. 从 README 和原始 docs 中提取显式线索：
   - 明确提到的文件名
   - 模块名
   - 主流程入口
   - 关键对象/状态
   - 已实现 / 未实现描述
4. 结合程序提供的“轻量仓库探测结果”做第一轮判断
5. 输出“下一批必读文件”
6. 读取这些文件后，再判断是否允许反写 owner docs

对“轻量仓库探测结果”的理解：
- 它只是仓库现状摘要，不等于代码已被完整阅读
- 它通常包含：
  - 根目录文件摘要
  - 候选主入口文件
  - 候选测试文件
  - 候选配置/契约/状态文件
  - README 提到但实际不存在的文件对照

对 `must_read_next` 的要求：
- 必须是相对 `project_root` 的文件路径列表
- 只能指向仓库内真实存在的文件
- 只允许这些类型：
  - `*.py`
  - `*.md`
  - `*.txt`
  - `*.json`
  - `*.doc`
  - `*.docx`
- 默认最多 8 个
- 不能为空；如果为空，则只能在 `can_write_owner_docs = true` 时出现
- 不允许包含 owner docs 目标文件：
  - `AGENTS.md`
  - `docs/PROJECT_GUIDE.md`
  - `docs/WORKFLOW.md`
  - `docs/ENTITIES.md`
  - `docs/FILE_INDEX.md`
  - `docs/TOOLS_METHOD_FLOW_MAP.md`
  - `docs/PROJECT_BOOTSTRAP_PROTOCOL.md`
- 若候选超过上限，优先顺序应为：
  - 主入口
  - 状态/契约
  - 配置
  - 测试
  - 其他补充文件

你必须分两阶段输出：

第一阶段：学习与补证据规划（JSON）
- 先不要反写 owner docs
- 先判断当前证据是否足够
- 输出必须回答：
  - 现在已经明确的项目定位
  - 已知的核心模块 / 主流程 / 风险
  - 文档与实现之间的主要缺口
  - 下一批必读文件
  - 当前是否允许进入 owner docs 反写
- 第一阶段输出建议字段：
  - `project_understanding`
  - `explicit_refs`
  - `light_repo_findings`
  - `implementation_gaps`
  - `must_read_next`
  - `can_write_owner_docs`
  - `why_not_ready`

第二阶段：只有在证据足够时，才允许反写 owner docs（Markdown 草稿）
- 第二阶段不要求把所有详细内容再塞进一个大 JSON
- 第二阶段的目标是按目标文件分别产出详细 markdown 草稿：
  - `AGENTS.md`
  - `docs/PROJECT_GUIDE.md`
  - `docs/WORKFLOW.md`
  - `docs/ENTITIES.md`
  - `docs/FILE_INDEX.md`
  - `docs/TOOLS_METHOD_FLOW_MAP.md`
- 第二阶段输出建议字段：
  - `agents_md`
  - `project_guide_md`
  - `workflow_md`
  - `entities_md`
  - `file_index_md`
  - `tools_method_flow_map_md`
  - `remaining_unknowns`

输出要求：
- 先给阶段一结果，禁止跳过
- 如果证据不足，必须明确 `can_write_owner_docs = false`
- 如果证据足够，才允许进入阶段二
- 所有结论必须可追溯到文档或实现证据
- 不要输出闲聊，不要复述用户问题
