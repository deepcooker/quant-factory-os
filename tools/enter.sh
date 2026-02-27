#!/usr/bin/env bash
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel 2>/dev/null || true)"
cwd="$(pwd)"
if [[ -z "$repo_root" ]]; then
  echo "❌ 不在 git 仓库内"
  echo "   修复：cd 到仓库根目录后再运行"
  exit 1
fi

if [[ "$cwd" != "$repo_root" ]]; then
  echo "❌ 请在仓库根目录运行 tools/enter.sh"
  echo "   修复：cd \"$repo_root\""
  exit 1
fi

# Keep legacy default: dirty worktree fails unless ENTER_AUTOSTASH=1.
if [[ "${ENTER_AUTOSTASH:-0}" == "1" ]]; then
  export QF_AUTOSTASH=1
else
  export QF_AUTOSTASH=0
fi

echo "NOTICE: tools/enter.sh is deprecated; use tools/qf init"
exec bash tools/qf init
