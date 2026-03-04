# CODEX_CLI_OPERATION

本文件定义本项目内 Codex CLI 的标准打开方式、参数语义、同频操作顺序与证据落盘规范。

## 1. 本机确认
- 版本：`codex-cli 0.106.0`
- 证据：运行 `codex --version`

## 2. 两种运行模式

### 2.1 讨论模式（只读）
```bash
codex --search --ask-for-approval never exec --sandbox read-only --json
```
用途：只读分析、方案讨论、同频口述，不改仓库文件。  
注意：`read-only` 下不能执行会写入仓库证据的命令（如 `tools/qf learn/ready`）。

### 2.2 执行模式（可写）
```bash
codex --search --ask-for-approval on-request exec --sandbox workspace-write --json
```
用途：执行实现、跑命令、修改文件（仍受审批与仓库门禁约束）。

## 3. 关键参数语义
- `--sandbox read-only`：只允许读，不允许写。
- `--sandbox workspace-write`：允许写工作区。
- `--ask-for-approval never`：不向用户弹审批；失败直接回给模型。
- `--ask-for-approval on-request`：模型可请求审批。
- `--search`：启用 web_search 工具。
- `exec --json`：输出 JSONL 事件流，可审计 tool 调用/命令执行/消息。
- `--output-last-message <file>`：把最终模型消息写入文件。

## 4. Plan -> Confirm -> Execute（本项目约定）
1. 先做交互规划：使用 Codex `/plan`（interactive slash command）。
2. 产出并确认六段包：`goal/non_goal/evidence/alternatives/rebuttal/decision_stop_condition`。
3. 确认后再进入执行链路（`discuss/execute/do`）。
4. 去歧义：`tools/qf plan` 是队列提案工具，不是 `/plan`。

## 5. 项目内标准同频动作（Codex）
1. `tools/qf init`
2. `tools/qf learn MODEL_SYNC=1 PLAN_MODE=strong -log`
3. `tools/qf ready`
4. `tools/qf discuss`（讨论收敛）
5. `tools/qf execute TARGET=do CONFIRM_CONTRACT=1`（执行）
6. `tools/qf review STRICT=1 AUTO_FIX=1`

## 6. /compact 使用规则
- `/compact` 不是每个 task 的硬门禁。
- 推荐触发点：里程碑完成后、切换到新子任务前、退出会话前。
- 固定顺序：先 `tools/qf snapshot NOTE="..."`，再 `/compact`。

## 7. 事件流证据落盘模板
```bash
mkdir -p reports/<RUN_ID>
set +e
codex --search --ask-for-approval never exec --sandbox read-only --json \
  --output-last-message reports/<RUN_ID>/codex_exec.last.txt \
  - < reports/<RUN_ID>/prompt.txt \
  > reports/<RUN_ID>/codex_exec.events.jsonl \
  2> reports/<RUN_ID>/codex_exec.stderr.log
rc=$?
set -e
echo CODEX_EXEC_RC:$rc
```

## 8. 已观测到的现实行为（本机）
- 在本机环境中，`codex exec --json` 可能出现 `Failed to shutdown rollout recorder`，导致返回码非 0。
- 即使返回码非 0，`events.jsonl` 与 `output-last-message` 可能已经完整生成。
- 因此本项目在 learn 模型同频中采用“结果文件+schema 校验”作为通过依据，而不是单看退出码。

## 9. 官方参考
- CLI 参考：`https://developers.openai.com/codex/cli/reference`
- CLI 功能：`https://developers.openai.com/codex/cli/features`
- slash 命令：`https://developers.openai.com/codex/cli/slash-commands`
- 非交互模式：`https://developers.openai.com/codex/noninteractive`
- rules：`https://developers.openai.com/codex/rules`
- AGENTS 指南：`https://developers.openai.com/codex/guides/agents-md`
