# CODEX CLI Playbook（默认流程 + 高级附录）

版本基线：
- `codex-cli 0.110.0`
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

### 1.2 learn 同频模式（`/plan` 强模式 + 可审计）

```bash
python3 tools/learn.py \
  [-minimal|-low|-medium|-high|-xhigh]
```

说明：
- 传输固定为自动编排：`app-server -> exec` 回退（无需传 `plan_transport`）。
- 模型固定：`gpt-5.3-codex`。
- `-minimal` 在当前工具约束下会自动提升为 `low`（控制台会打印原因）。

必备产物：
- `learn/<project_id>.model.prompt.txt`
- `learn/<project_id>.model.raw.txt`
- `learn/<project_id>.model.events.jsonl`
- `learn/<project_id>.model.stderr.log`

判定规则：
- `MODEL_SYNC=1`、`PLAN_MODE=strong` 为 learn 内部固定门禁
- 必须产出 `/plan` 强模式 JSON 包（含 plan/oral/anchor/practice）
- 必须有 `tools/view.sh` 覆盖 required files 的实践证据

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
