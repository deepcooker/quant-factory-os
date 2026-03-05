# CODEX CLI Playbook（默认流程 + 高级附录）

版本基线：
- `codex-cli 0.106.0`
- 校验命令：`codex --version`

配套目录：
- `test_codex/`

## 1) 默认流程（只记这 3 条）

### 1.1 讨论模式（只读）

```bash
codex --sandbox read-only --ask-for-approval never --search
```

用途：
- 需求澄清、方案讨论、证据查阅
- 只允许读，不修改仓库

### 1.2 learn 同频模式（非交互 + 可审计）

```bash
codex --search --ask-for-approval never exec \
  --sandbox read-only \
  --json \
  --output-last-message <ABS_PATH>/learn.model.raw.txt \
  "<PROMPT>"
```

必备产物：
- `learn.model.prompt.txt`
- `learn.model.raw.txt`
- `learn.model.events.jsonl`
- `learn.model.stderr.log`

判定规则：
- 必须看到 `thread.started`（events）
- 必须有非空 `output-last-message`
- 必须有至少一个 `item.completed`

### 1.3 执行模式（可写）

```bash
codex --sandbox workspace-write --ask-for-approval on-request --search
```

用途：
- 已确认方向后的实现/修复
- 高风险命令可人工审批

## 2) 软失败策略（当前版本必须知道）

现象：
- `exec` 内容已成功返回，但退出码是 `1`
- 常见错误：`Failed to shutdown rollout recorder`

处理：
- 若 `events + last_message` 都有效，判定为 `PASS_SOFT`（可用于 learn 同频）
- 退出码非零保留告警，不直接判 learn 失败

## 3) 一键 smoke（自动化）

推荐命令：

```bash
test_codex/smoke.sh
```

输出：
- 表格化测试结果（`PASS` / `PASS_SOFT` / `FAIL`）
- 日志落盘到 `test_codex/logs/`
- 产物落盘到 `test_codex/artifacts/`

## 4) 高级附录（默认不需要记）

基础/账号：

```bash
codex --help
codex login status
codex logout --help
```

review：

```bash
codex review --help
codex exec review --help
codex exec review --uncommitted --json > /abs/path/review.events.jsonl
```

resume/fork：

```bash
codex resume --help
codex fork --help
codex exec resume --help
```

mcp：

```bash
codex mcp --help
codex mcp list
codex mcp add --help
codex mcp get --help
codex mcp remove --help
codex mcp-server --help
```

sandbox：

```bash
codex sandbox --help
codex sandbox linux -- /bin/bash -lc 'echo CODEX_SANDBOX_OK'
```

app-server / completion / cloud / features / apply：

```bash
codex app-server --help
codex app-server generate-json-schema --out test_codex/app_server_out
codex app-server generate-ts --out test_codex/app_server_ts

codex completion bash | head -n 30
codex completion zsh | head -n 30

codex cloud --help
codex cloud list

codex features list
codex apply --help
```

## 5) 官方文档入口

- CLI reference: `https://developers.openai.com/codex/cli/reference`
- CLI features: `https://developers.openai.com/codex/cli/features`
- Slash commands: `https://developers.openai.com/codex/cli/slash-commands`
- Non-interactive: `https://developers.openai.com/codex/noninteractive`
- Rules: `https://developers.openai.com/codex/rules`
- AGENTS.md guide: `https://developers.openai.com/codex/guides/agents-md`
- Open-source repo: `https://github.com/openai/codex`
