#!/usr/bin/env bash
set -euo pipefail

venv_root="${START_VENV_PATH:-/root/policy/venv}"
activate_path="${venv_root}/bin/activate"
if [[ ! -f "$activate_path" ]]; then
  echo "❌ policy venv missing: ${activate_path}"
  echo "   修复：创建 /root/policy/venv 或设置 START_VENV_PATH 指向有效 venv"
  exit 1
fi

# shellcheck source=/dev/null
source "$activate_path"

python_path="$(which python)"
echo "python: ${python_path}"

if [[ -n "${PROXY_URL:-}" ]]; then
  export http_proxy="${PROXY_URL}"
  export https_proxy="${PROXY_URL}"
  export HTTP_PROXY="${PROXY_URL}"
  export HTTPS_PROXY="${PROXY_URL}"
  echo "proxy: enabled"
else
  echo "proxy: disabled"
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"
cd "${repo_root}"

if [[ "${START_DRY_RUN:-0}" == "1" ]]; then
  echo "dry-run: would run tools/enter.sh"
  echo "dry-run: would exec codex"
  exit 0
fi

if ! bash tools/enter.sh; then
  exit 1
fi

exec codex
