# TOOLS_METHOD_FLOW_MAP

这份文档只描述当前正式主线的方法入口与调用关系。

阅读顺序固定为：
1. 先看主流程分层
2. 再看每个入口调用哪些底层方法
3. 最后再看历史兼容链路

不再把研发期过渡链路当成当前正式主流程。

---

## 1. 当前正式主线

当前正式主线固定为三层：

1. 准备层
   - `init`
2. 主流程层
   - `appserverclient`
   - `--learnbaseline`
   - `--fork-current`
   - `--current-turn`
   - `--summarize-current`
   - `--refresh-baseline`
3. 收尾层
   - `gitclient`
   - `--commit`
   - `--rollback-last`
   - `--rollback-commit`

---

## 2. 准备层

### 2.1 `init`

业务目标：
- 读取统一配置
- 补齐项目基础骨架
- 检查 Codex / Git 前置条件
- 给出下一步动作建议

主流程方法：

| 编号 | 方法名 | 中文说明 |
| --- | --- | --- |
| `1001` | `init_step_01_load_context` | 调用 `project_config.py` 读取统一配置、校验必填项、打印统一配置 JSON。 |
| `1002` | `init_step_02_check_project_files` | 确保项目根目录下的标准骨架存在：`tools/`、`docs/`、`AGENTS.md`、`PROJECT_GUIDE.md`。 |
| `1003` | `init_step_03_check_codex_runtime` | 检查 `codex`、`app-server`、登录状态与 session 前提。 |
| `1004` | `init_step_04_check_git_runtime` | 检查 git 仓库、远端、认证、连通性与工作区状态。 |
| `1005` | `init_step_05_finalize` | 汇总检查结果并给出 `INIT_STATUS / INIT_REASON_CODES / INIT_NEXT`。 |

支撑方法命名：
- `init_tools_01` ~ `init_tools_xx`

---

## 3. 主流程层

### 3.1 `appserverclient --learnbaseline`

业务目标：
- 建立项目级 baseline 学习 session
- 用一次重型 `plan` 完成主线同频

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `A1` | `run_learnbaseline()` | baseline 学习流程总入口。 |
| `A2` | `connect()` | 初始化 `codex app-server` 连接，完成 `initialize / initialized`。 |
| `A3` | `list_collaboration_modes()` | 检查当前支持的协作模式。 |
| `A4` | `start_thread()` | 创建 baseline 学习 thread。 |
| `A5` | `start_turn()` | 以 `plan` 模式发送 baseline 学习提示词。 |
| `A6` | `wait_for_turn_completion()` | 等待 `task_complete / turn completed`。 |
| `A7` | `wait_for_rollout_ready()` | 等待 baseline rollout 文件可用。 |
| `A8` | `update_session_registry()` | 写回 `learn_session_baseline`。 |

输出：
- `session_registry.learn_session_baseline`

### 3.2 `appserverclient --fork-current`

业务目标：
- 从 baseline 派生当前工作 session

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `B1` | `run_fork_current()` | current session fork 总入口。 |
| `B2` | `connect()` | 初始化连接。 |
| `B3` | `resume_thread()` | 恢复 baseline session。 |
| `B4` | `fork_thread()` | 从 baseline fork 当前工作 session。 |
| `B5` | `wait_for_rollout_ready()` | 等待 current rollout 文件可用。 |
| `B6` | `update_session_registry()` | 写回 `fork_current_session`。 |

输出：
- `session_registry.fork_current_session`

### 3.3 `appserverclient --current-turn`

业务目标：
- 在当前工作 session 上继续推进需求、讨论、验证

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `C1` | `run_current_turn()` | current turn 总入口。 |
| `C2` | `connect()` | 初始化连接。 |
| `C3` | `resume_thread()` | 恢复 current session。 |
| `C4` | `start_turn()` | 以 `default` 模式发送当前输入。 |
| `C5` | `wait_for_turn_completion()` | 等待当前 turn 收口。 |
| `C6` | `wait_for_rollout_ready()` | 等待 rollout 文件可用。 |
| `C7` | `update_session_registry()` | 维持 `fork_current_session` 为当前工作副本。 |

说明：
- `mode` 是 `turn` 级别，不是 `thread` 级别。
- baseline 学习使用 `plan`。
- 日常 current turn 使用 `default`。

### 3.4 `appserverclient --summarize-current`

业务目标：
- 对当前工作 session 做去噪总结，并写回 `session_registry.current_summary`

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `D1` | `run_summarize_current()` | current summary 总入口。 |
| `D2` | `connect()` | 初始化连接。 |
| `D3` | `resume_thread()` | 恢复 current session。 |
| `D4` | `start_turn()` | 发送 summarize prompt。 |
| `D5` | `wait_for_turn_completion()` | 等待总结 turn 收口。 |
| `D6` | `read_thread()` | 读取当前 thread 详情。 |
| `D7` | `extract_last_agent_message()` | 抽取最后一条 agent 摘要正文。 |
| `D8` | `update_current_summary()` | 写回 `session_registry.current_summary`。 |

### 3.5 `appserverclient --refresh-baseline`

业务目标：
- 只用 current summary 的去噪结论增量刷新 baseline

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `E1` | `run_refresh_baseline()` | baseline refresh 总入口。 |
| `E2` | `connect()` | 初始化连接。 |
| `E3` | `resume_thread()` | 恢复 baseline session。 |
| `E4` | `start_turn()` | 发送 refresh prompt。 |
| `E5` | `wait_for_turn_completion()` | 等待 refresh turn 收口。 |
| `E6` | `read_thread()` | 读取 baseline thread 详情。 |
| `E7` | `extract_last_agent_message()` | 抽取最新 baseline 增量更新。 |
| `E8` | `update_session_registry()` | 维持 `learn_session_baseline` 最新状态。 |
| `E9` | `update_current_summary()` | 在 `current_summary` 中记录本次 baseline refresh 结果。 |

---

## 4. 收尾层

### 4.1 `gitclient --commit`

业务目标：
- 将当前工作区改动提交、创建 PR、合并并同步本地 `main`

主流程调用关系：

| 顺序 | 方法/动作 | 中文说明 |
| --- | --- | --- |
| `G1` | `run_commit()` | 提交入口。 |
| `G2` | `git checkout -b <work_branch>` | 从当前工作面建立提交分支。 |
| `G3` | `git add -A` | 收集改动。 |
| `G4` | `git commit` | 生成提交。 |
| `G5` | `git push` | 推远端分支。 |
| `G6` | `gh pr create` | 创建 PR。 |
| `G7` | `gh pr merge` / `gh pr merge --auto` | 合并或挂 auto merge。 |
| `G8` | `gh pr view` 轮询 | 等待真正 `MERGED`。 |
| `G9` | `git fetch / checkout main / pull --rebase` | 同步本地 `main`。 |

### 4.2 `gitclient --rollback-last`

业务目标：
- 回滚主线最近一次提交

主流程调用关系：
- 从最新 `main` 建回滚分支
- `git revert`
- push
- 创建回滚 PR
- 合并并同步本地 `main`

### 4.3 `gitclient --rollback-commit`

业务目标：
- 回滚指定提交

主流程调用关系：
- 与 `--rollback-last` 相同，只是回滚目标为指定 commit

---

## 5. 实验性流程扩展

当前正式主线之后的发展方向是：
- baseline fork 多角色 session
- 按角色拆最小 task
- 各角色 session 去噪总结
- 将有效结论回灌 baseline

这部分未来会继续沉到 `appserverclient` 附近，而不是再回到旧的长链路中。

---

## 6. 历史兼容链路

以下链路保留为研发期过渡材料或兼容实现，不再作为当前正式主线：
- `learn`
- `ready`
- `orient`
- `choose`
- `council`
- `arbiter`
- `slice_task`
- `run_main`

这些文件仍可作为历史实现参考，但不再代表当前正式业务主流程。
对应 shell 兼容入口已归档到 `tools/backup/`，原 `tools/*.sh` 只保留过渡转发层。
