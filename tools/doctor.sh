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
    echo "❌ gh 未登录：运行 gh auth login -h github.com -p https"
  fi
else
  echo "❌ 未安装 gh：sudo apt install -y gh"
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
if command -v python >/dev/null 2>&1; then
  echo "python: $(python --version)"
elif command -v python3 >/dev/null 2>&1; then
  echo "python3: $(python3 --version)"
else
  echo "❌ 没有 python/python3"
fi

echo
echo "== doctor: pytest =="
if command -v pytest >/dev/null 2>&1; then
  echo "✅ pytest: $(pytest --version)"
  echo "running: pytest -q (may fail if deps missing)"
  set +e
  pytest -q
  rc=$?
  set -e
  if [[ $rc -eq 0 ]]; then
    echo "✅ pytest OK"
  else
    echo "⚠️ pytest failed (rc=$rc). 这不一定是坏事，可能是缺依赖/环境。"
  fi
else
  echo "⚠️ 没有 pytest：如果你要跑测试，先 pip install -r requirements-dev.txt 或 pip install pytest"
fi

echo
echo "Done."