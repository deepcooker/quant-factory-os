# CODEX CLI Source Audit (官方核对 + 本地源码 + 全功能实测)

更新时间（UTC）：2026-03-05T05:45:00Z  
审计范围：官方文档、当前机器安装的 `codex-cli 0.106.0`、本地源码入口、命令级功能实测

## 1) 本机安装与源码结构（事实）

### 1.1 版本与入口
- `codex --version`：`codex-cli 0.106.0`
- 可执行入口：`/usr/bin/codex`
- 入口真实目标：`/usr/lib/node_modules/@openai/codex/bin/codex.js`

### 1.2 本地“源码”到底是什么
- 本地 NPM 包是 JS 包装层，负责分发到平台二进制并 `spawn` 真正 CLI。
- 关键文件：`/usr/lib/node_modules/@openai/codex/bin/codex.js`
- 该文件确认了：`Node wrapper -> vendor native binary` 的调用链。

### 1.3 本地二进制位置
- native binary：`/usr/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/codex/codex`
- 打包内 `rg`：`/usr/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/path/rg`
- 二进制是 stripped，可读本地源码有限（包装层可读，核心 Rust 需看开源仓库）。

### 1.4 对应开源源码（用于绕过本地二进制不可读）
- 已拉取：`/tmp/openai-codex`
- 拉取时 commit：`3eb9115`
- 仓库：`https://github.com/openai/codex`

## 2) Codex 与大模型交互闭环（核对结果）

闭环链路：
1. 你执行 `codex ...`
2. `bin/codex.js` 选择平台包并启动 native binary
3. native binary 创建 thread / turn
4. 模型执行推理并发起工具调用（shell/web_search/mcp 等）
5. CLI 收集事件流输出（普通文本或 JSONL）
6. 收尾写 last message / rollout / 退出码

本地实测证据：
- `test_codex/artifacts/exec_json.events.jsonl`
  - 含 `thread.started`, `turn.started`, `item.started/completed`, `command_execution`
- `test_codex/artifacts/exec_search.events.jsonl`
  - 含 `web_search` 相关事件
- `test_codex/artifacts/exec_basic_last_message.txt`
  - 模型响应落盘成功

## 3) 官方文档 vs 本地核对（关键结论）

| 主题 | 官方文档结论 | 本地核对结论 |
|---|---|---|
| sandbox 模式 | 支持 `read-only / workspace-write / danger-full-access` | `codex --help` 与源码参数一致；`codex sandbox linux -- ...` 实测通过 |
| 审批策略 | 支持 `untrusted / on-request / on-failure(弃用) / never` | `codex --help` 与运行输出一致 |
| `--search` 行为 | 文档说明默认是 cached，可用 `--search` 开 live | 实测 `codex --search exec ...` 事件中确有 `web_search` |
| 非交互事件流 | `codex exec --json` 输出 JSONL 事件流 | `exec_json.events.jsonl` / `exec_search.events.jsonl` 已验证 |
| `--output-last-message` | 可输出最后一条 agent 消息到文件 | 多个场景落盘成功（`exec_basic_last_message.txt` 等） |
| AGENTS 指令链 | 全局 -> repo root -> CWD，越深优先级越高 | 官方与源码逻辑一致（project doc 按 root->cwd 收集） |
| Rules 优先级 | `forbidden > prompt > allow` | 官方规则页给出同结论 |
| `/plan` `/compact` | `/plan` 先规划，`/compact` 用于长会话压缩 | 官方 slash 文档已核对 |

## 4) 全功能测试覆盖（“所有功能”）

说明：
- “功能覆盖”分两层：`help/结构验证` + `可执行 smoke`。
- 结果日志均在 `test_codex/logs/`，产物在 `test_codex/artifacts/`。

### 4.1 顶层命令覆盖

| 命令 | 覆盖方式 | 结果 |
|---|---|---|
| `exec` | `--help` + `exec_basic` + `--json` + `--search` + `output-schema` + `resume` + `--skip-git-repo-check` | 已覆盖（执行返回码存在已知异常，见第 5 节） |
| `review` | `--help` + `exec review --help` | 已覆盖（真实全仓 review 路径耗时重，建议按 scope 跑） |
| `login` | `--help` + `login status` | 已覆盖（当前状态：Logged in using ChatGPT） |
| `logout` | `--help` | 已覆盖（未执行真实登出，避免影响会话） |
| `mcp` | `--help` + `list/get/add/remove` + `login/logout` 帮助 | 已覆盖（在隔离 `CODEX_HOME` 下完成 add/get/remove） |
| `mcp-server` | `--help` | 已覆盖 |
| `app-server` | `--help` + `generate-json-schema --out` + `generate-ts --out` | 已覆盖（真实产物已生成） |
| `completion` | `--help` + `completion bash/zsh` | 已覆盖 |
| `sandbox` | `--help` + `sandbox linux -- ...` | 已覆盖（linux 实跑通过） |
| `debug` | `--help` + `debug app-server --help` | 已覆盖 |
| `apply` | `--help` | 已覆盖（真实 apply 需 cloud task id） |
| `resume` | `--help` | 已覆盖 |
| `fork` | `--help` | 已覆盖 |
| `cloud` | `--help` + `list` + `exec/status/apply/diff --help` | 已覆盖（`cloud list` 本机为 `No tasks found`） |
| `features` | `--help` + `list` + `enable/disable`（隔离 `CODEX_HOME`） | 已覆盖 |

### 4.2 learn 场景相关实测（你关心的核心）

已验证可用调用形态（真实模型交互）：

```bash
codex --search --ask-for-approval never exec \
  --sandbox read-only \
  --json \
  --output-last-message <path> \
  "<prompt>"
```

这与 `learn` 需要的“强制模型同步 + 事件可审计”目标一致：  
- `--sandbox read-only`：只读，不改仓库  
- `--ask-for-approval never`：非交互自动跑  
- `--json`：拿到完整事件流  
- `--output-last-message`：拿最终答复落盘  
- `--search`：需要外部知识时可开 live web_search

## 5) 这轮实测发现的关键坑（高优先级）

### 5.1 退出码异常：业务成功但命令返回 1
- 现象：多次 `exec` 明明拿到正确回答，但退出码仍为 `1`。
- 错误串：`ERROR: Failed to shutdown rollout recorder`
- 证据：
  - 日志：`test_codex/logs/*exec*.log`
  - 源码位置：
    - `codex-rs/core/src/codex.rs`（shutdown 时发送该错误）
    - `codex-rs/core/src/rollout/recorder.rs`（queue rollout items 失败）

### 5.2 环境权限告警
- 现象：每次启动都会出现：
  - `failed to clean up stale arg0 temp dirs: Permission denied`
  - `proceeding, even though we could not update PATH: Permission denied`
- 源码位置：`codex-rs/arg0/src/lib.rs`
- 含义：`CODEX_HOME/tmp/arg0` 清理或 PATH 助手创建权限不足，CLI 会继续运行但会带噪音。

### 5.3 `output-schema` 不能“少填 required”
- 现象：schema 中 `properties` 里有字段但 `required` 未全列，会 400：
  - `invalid_json_schema ... Missing 'note'`
- 处理：`required` 必须覆盖你声明为必须的字段，建议先最小 schema 验证。
- 严格 schema 成功样例：
  - `test_codex/artifacts/echo_schema_strict.json`
  - `test_codex/artifacts/exec_schema_strict_output.json`

### 5.4 `--output-last-message` 路径是按当前 cwd 解析
- 在 `cd /tmp` 后使用相对路径会写失败。
- 处理：统一传绝对路径。

### 5.5 当前运行策略（针对 0.106.0）
- 对 learn 场景采用“软失败判定”：
  - 退出码非 0 但 `events + last_message` 完整时，记为 `PASS_SOFT`
  - 退出码告警保留，避免静默忽略问题
- 对应自动化脚本：`test_codex/smoke.sh`

## 6) 直接可复用的证据目录

- 测试脚本：`test_codex/run_all.sh`
- 快速自检脚本：`test_codex/smoke.sh`
- 汇总：
  - `test_codex/logs/summary-20260304T173935Z.tsv`
  - `test_codex/logs/extended-20260304T174228Z.tsv`
  - `test_codex/logs/subcommands-20260305T053939Z.tsv`
- 关键产物：
  - `test_codex/artifacts/exec_json.events.jsonl`
  - `test_codex/artifacts/exec_search.events.jsonl`
  - `test_codex/artifacts/exec_basic_last_message.txt`
  - `test_codex/artifacts/exec_search_last_message.txt`
  - `test_codex/artifacts/exec_schema_strict_output.json`
  - `test_codex/artifacts/exec_skip_git_last_message.txt`

## 7) 官方来源（本次核对）

- CLI 参考：`https://developers.openai.com/codex/cli/reference`
- CLI 功能与 web search：`https://developers.openai.com/codex/cli/features`
- Slash 命令：`https://developers.openai.com/codex/cli/slash-commands`
- 非交互：`https://developers.openai.com/codex/noninteractive`
- Rules：`https://developers.openai.com/codex/rules`
- AGENTS.md 指南：`https://developers.openai.com/codex/guides/agents-md`
- 开源仓库：`https://github.com/openai/codex`
