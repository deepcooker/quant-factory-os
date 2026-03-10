# Learn Prompt Compare

## 1. 当前结论

`appserverclient --learnbaseline` 使用的 baseline 学习提示词，已经不再只是固定前言。

当前真实来源是：
- 固定前言文件: `tools/learnbaseline_prompt.md`
- 动态拼装出口: `tools/project_config.py`
- runtime 取值字段: `runtime_defaults.learn_init_turn_text`

也就是说，`appserverclient.py` 当前拿到的是：
- 固定学习前言
- 动态项目上下文
- owner files
- `PROJECT_GUIDE` 必查文件
- `PROJECT_GUIDE` 问题列表
- 输出要求
- JSON schema

## 2. 当前 baseline 提示词组成

### 2.1 固定前言

来源:
- `tools/learnbaseline_prompt.md`

作用:
- 定义学习同频的主目标
- 强调 `PROJECT_GUIDE.md` 是学习起点
- 强调高质量提问和主线回拉

### 2.2 动态项目上下文

来源:
- `tools/project_config.py -> build_learnbaseline_prompt_text(...)`

当前会拼入:
- `PROJECT_ID`
- `CURRENT_RUN_ID`
- `CURRENT_TASK_FILE`

### 2.3 Owner files

当前固定 owner files:
- `docs/PROJECT_GUIDE.md`
- `AGENTS.md`
- `docs/WORKFLOW.md`

### 2.4 Additional required files

来源:
- `PROJECT_GUIDE.md` 各题目的 `必查文件`

当前会动态解析并拼入。

### 2.5 PROJECT_GUIDE 问题列表

来源:
- `PROJECT_GUIDE.md`

当前会动态解析并拼入:
- `Q1..Qn`
- 每题标题

### 2.6 输出要求

当前会拼入:
- 先读 owner files
- 再读 additional required files
- 使用 `tools/view.sh`
- 不跳题
- 保持回答简洁
- 只返回 JSON

### 2.7 输出 JSON schema

当前会拼入 schema，要求模型返回这些核心字段：
- `mainline`
- `current_stage`
- `next_step`
- `files_read`
- `plan_protocol`
- `oral_restate`
- `guide_oral`
- `anchor_realign`

## 3. 和旧 learn.py 的关系

旧的 `learn.py` 仍然保留了课程化 learn 工作流，但 baseline 提示词这一层，已经基本迁到：
- `tools/learnbaseline_prompt.md`
- `tools/project_config.py`
- `tools/appserverclient.py --learnbaseline`

当前更准确的关系是：
- `appserverclient --learnbaseline`
  - 已经承接 baseline 学习 session 建立
  - 已经承接 baseline 动态 prompt 拼装
- `learn.py`
  - 还保留更重的课程编排和 learn 产物收口

## 4. 还没完全迁完的部分

当前还没有完全迁进 `appserverclient` 的，是这些更重的 learn 工作流层能力：
- learn 产物文件写回
- model raw/json 收口
- evidence 收口
- baseline 更新后的结构化学习快照
- current session 总结回灌 baseline

## 5. 当前建议

下一步不要再讨论“baseline 提示词是不是还是旧的一句常量”。

当前真正该继续做的是：
1. 用 `tools/appserverclient.py --learnbaseline -new` 实跑验证这份动态 prompt
2. 再决定哪些 learn 产物层能力要继续往 `appserverclient` 迁
