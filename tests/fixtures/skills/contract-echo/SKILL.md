---
name: contract-echo
description: Use for the smallest possible real app-server contract smoke. Return a single JSON fenced block and nothing else.
---

# Contract Echo

## Purpose
用于真实 `tools/app.py` / `codex app-server` 集成烟测的最小 skill。

## Instructions
- 收到请求后，只返回一个 JSON fenced block。
- 不要额外解释。
- 不要运行其他命令。
- 输出必须严格是：

```json
{"ok": true, "kind": "contract_echo"}
```
