---
name: demo-echo
description: 用于 app-server demo 的最小 skill 联通测试。被显式调用时，只返回最小 JSON，不展开项目分析。
---

# demo-echo

## 目的
这是一个最小联通测试 skill，只用于验证 app-server 是否能显式加载 repo-local skill。

## 执行规则
- 不做项目分析。
- 不读取无关文件。
- 不展开解释。
- 只返回最小 JSON。

## 输出
只返回：

```json
{"ok": true, "skill": "demo-echo"}
```
