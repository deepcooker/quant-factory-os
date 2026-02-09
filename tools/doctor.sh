#!/usr/bin/env bash
set -euo pipefail

echo "== doctor: repo =="
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "❌ 不在 git 仓库内"; exit 1; }
echo "✅ git repo: $(basename "$(git rev-parse --show-toplevel)")"
echo "branch: $(git branch --show-current)"

echo
echo "== doctor: remote =="
remote_url="$(git remote get-url origin 2>/dev/null || true)"
if [[ -z "$remote_url" ]]; then
  echo "❌ 没有 origin remote"
else
  echo "origin: $remote_url"
fi

echo
echo "== doctor: gh =="
if command -v gh >/dev/null 2>&1; then
  echo "✅ gh: $(gh --version | head -n1)"
  if gh auth status -h github.com >/dev/null 2>&1; then
    echo "✅ gh 已登录 github.com"
  else
    echo "❌ gh 未登录"
    echo "   修复：gh auth login -h github.com -p https"
  fi
else
  echo "❌ 未安装 gh"
  echo "   修复：sudo apt install -y gh"
fi

echo
echo "== doctor: CI workflow =="
if [[ -f ".github/workflows/ci.yml" ]]; then
  echo "✅ found .github/workflows/ci.yml"
else
  echo "❌ 缺少 .github/workflows/ci.yml（CI 不会跑）"
fi

echo
echo "== doctor: python =="
py_bin=""
if [[ -f "Makefile" ]]; then
  py_bin="$(awk -F'[:= ]+' '/^PY[[:space:]]*:?=/{print $3; exit}' Makefile)"
fi
if [[ -z "$py_bin" ]]; then
  if command -v python >/dev/null 2>&1; then
    py_bin="$(command -v python)"
  elif command -v python3 >/dev/null 2>&1; then
    py_bin="$(command -v python3)"
  fi
fi

if [[ -n "$py_bin" && -x "$py_bin" ]]; then
  echo "python: $("$py_bin" --version)"
elif [[ -n "$py_bin" ]]; then
  echo "❌ PY 不可执行：$py_bin"
  echo "   修复：检查 Makefile 的 PY 或修复该路径"
else
  echo "❌ 没有 python/python3"
  echo "   修复：安装 python3 并确保 Makefile PY 指向可执行 python"
fi

echo
echo "== doctor: pytest =="
if [[ -n "$py_bin" && -x "$py_bin" ]]; then
  if "$py_bin" - <<'PY'
import importlib.util
import sys
sys.exit(0 if importlib.util.find_spec("pytest") else 1)
PY
  then
    echo "✅ pytest 可用（$py_bin -m pytest）"
    echo "running: $py_bin -m pytest -q (may fail if deps missing)"
    set +e
    "$py_bin" -m pytest -q
    rc=$?
    set -e
    if [[ $rc -eq 0 ]]; then
      echo "✅ pytest OK"
    else
      echo "⚠️ pytest failed (rc=$rc). 这不一定是坏事，可能是缺依赖/环境。"
    fi
  else
    echo "⚠️ pytest 不可用"
    echo "   修复：$py_bin -m pip install -r requirements-dev.txt"
    echo "         或：$py_bin -m pip install pytest"
  fi
else
  echo "⚠️ 无法检查 pytest（缺少可执行 python）"
fi

echo
echo "== doctor: view tool =="
if [[ -x "tools/view.sh" ]]; then
  echo "✅ tools/view.sh 可执行"
else
  echo "❌ tools/view.sh 不可执行"
  echo "   修复：chmod +x tools/view.sh"
fi

echo
echo "Done."
