# 实验线验证门

## 目的
这份文档只说明根目录实验线如何做最小验证，不涉及 `tools/` 正式主线。

## 1. fake smoke 验证
在仓库根目录执行：

```bash
python3 tests/run_smoke_suite.py
```

通过标准：
- 所有 smoke case 显示 `PASS`
- 会生成：
  - `state/test_reports/smoke_summary.json`

## 2. 发布级 gate 验证
在仓库根目录执行：

```bash
python3 tests/run_gate.py
```

这个入口会：
- 先跑 `py_compile`
- 再跑 `tests/run_smoke_suite.py`
- 默认跳过真实 app-server 集成烟测

通过标准：
- 命令退出码为 `0`
- 会生成：
  - `state/test_reports/gate_summary.json`
  - `state/test_reports/gate_summary.md`

## 3. 真实 app-server 集成烟测
如需验证 `app.py + codex app-server + skill` 的最小接线：

```bash
RUN_REAL_APP_SERVER=1 python3 tests/integration_real_app_smoke.py
```

或直接走 gate：

```bash
RUN_REAL_APP_SERVER=1 python3 tests/run_gate.py
```

通过标准：
- `integration_real_app_smoke.py` 输出 `INTEGRATION_REAL_APP_SMOKE_OK`
- 或 `gate_summary.json` 中：
  - `integration_real_app_status = "passed"`

## 4. 失败样例
如需验证 gate 在失败时的输出可读性，可单独执行：

```bash
python3 tests/smoke_failure_sample.py
```

这个脚本默认会失败，用来检查失败摘要与报告可读性。
