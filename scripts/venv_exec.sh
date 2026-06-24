#!/usr/bin/env bash
# 使用项目 .venv 执行 Python 脚本（pre-commit / 本地门禁）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="${ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "Missing .venv — run: uv sync --frozen --extra dev" >&2
  exit 1
fi
if [[ $# -lt 1 ]]; then
  echo "usage: venv_exec.sh <script.py> [args...]" >&2
  exit 1
fi
exec "$PY" "$@"
