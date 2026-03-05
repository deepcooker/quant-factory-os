# Codex App-Server Python 调用手册（本地实测版）

本手册对应脚本：
- `CODEX_APP_SERVER_PYTHON_TEST.py`

运行产物目录：
- `test_codex/app_server_runtime/`

## 1. app-server 是什么

`codex app-server` 是 Codex CLI 的程序化接口模式，默认通过 `stdio://` 提供 JSON-RPC 通道。  
它适合 Python/脚本自动化编排，不依赖 TUI 的 PTY 交互。

和其他模式关系：
- 交互式 `codex`：适合人工对话、`/plan`、`/compact`。
- 非交互 `codex exec`：适合 CI/脚本的一次性任务执行。
- `codex app-server`：适合你自己写“会话编排器”（thread/turn 协议级控制）。

## 2. 本地基线

- 本机命令：`codex --version`
- 当前实测版本：`codex-cli 0.110.0`
- 推荐默认参数：
  - `model = gpt-5.3-codex`
  - `mode = plan`
  - `effort = xhigh`
  - `sandboxPolicy = readOnly`

`effort` 合法枚举（本地 schema + 实测）：
- `none`, `minimal`, `low`, `medium`, `high`, `xhigh`

`fast` 非法（会报 unknown variant）。

## 3. Python 测试脚本怎么用

### 3.1 快速握手（低成本）

```bash
python CODEX_APP_SERVER_PYTHON_TEST.py --quick
```

用途：
- 验证初始化链路与模式发现是否正常，不跑完整推理。
- 说明：`quick` 模式下 `TURN/PLAN/EFFORT` 标记会以“跳过即通过”输出，详细原因写在对应 `summary.json` 的 `checks.detail`。

### 3.2 完整链路（推荐）

```bash
python CODEX_APP_SERVER_PYTHON_TEST.py --mode plan --effort xhigh --model gpt-5.3-codex
```

用途：
- 验证完整协议：
  - `initialize`
  - `initialized`
  - `collaborationMode/list`
  - `thread/start`
  - `turn/start`（`plan` + `xhigh` + `readOnly`）
- 验证负例：`effort=fast` 必须失败。

### 3.3 可选参数

```bash
python CODEX_APP_SERVER_PYTHON_TEST.py --help
```

参数：
- `--quick`：仅握手模式
- `--mode`：`plan|default`（默认 `plan`）
- `--effort`：`none|minimal|low|medium|high|xhigh`（默认 `xhigh`）
- `--model`：默认 `gpt-5.3-codex`
- `--cwd`：thread/turn 的工作目录（默认当前目录）
- `--timeout`：完整 turn 等待超时秒数（默认 120）

## 4. 成功判定（控制台锚点）

脚本固定输出以下键值，便于自动化判断：
- `APP_SERVER_INIT_OK`
- `APP_SERVER_MODES`
- `APP_SERVER_THREAD_OK`
- `APP_SERVER_TURN_OK`
- `APP_SERVER_PLAN_SIGNAL`
- `APP_SERVER_EFFORT_VALIDATION_OK`
- `APP_SERVER_EFFORT_NEGATIVE_OK`

并输出产物路径：
- `APP_SERVER_ARTIFACT_EVENTS`
- `APP_SERVER_ARTIFACT_STDERR`
- `APP_SERVER_ARTIFACT_SUMMARY`

## 5. 常见问题与排查

1. `codex` 不存在  
处理：确认 CLI 已安装且在 `PATH`。

2. `initialize` 或 `thread/start` 报认证/网络错误  
处理：先执行 `codex login status`，再确认网络与配额。

2.1 启动时出现 `arg0 temp dir permission denied`  
处理：这是当前环境常见告警，通常不影响测试主流程；只要脚本锚点全部为 `true` 即可视为通过。

3. `collaborationMode/list` 报能力不足  
处理：`initialize` 请求必须带 `capabilities.experimentalApi=true`。

4. `effort=fast` 报错  
这是预期行为；合法值只有 `none|minimal|low|medium|high|xhigh`。

5. 没有计划信号  
处理：确保 `--mode plan`，并检查 `turn` 是否完成及返回内容是否包含计划结构。

## 6. 什么时候选 app-server

优先用 `app-server` 的场景：
- 你要自己控制 `thread/turn` 生命周期。
- 你要把 Plan/Execute 做成可编排状态机。
- 你要保留协议级事件和错误语义，供后续流程自动处理。

优先用 `codex exec` 的场景：
- 一次性任务、CI、批处理。
- 不需要协议级细粒度控制，只要“给 prompt 拿结果”。

## 7. 官方文档对照

- CLI reference: `https://developers.openai.com/codex/cli/reference`
- CLI features: `https://developers.openai.com/codex/cli/features`
- Slash commands: `https://developers.openai.com/codex/cli/slash-commands`
- Non-interactive: `https://developers.openai.com/codex/noninteractive`
- AGENTS.md guide: `https://developers.openai.com/codex/guides/agents-md`
