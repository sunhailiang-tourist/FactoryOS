#!/usr/bin/env bash
# 使用 App .venv 执行 Python 脚本（pre-commit / CMNT-C）
set -euo pipefail
APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PY="${APP_ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "Missing .venv — run: ./scripts/activate.sh" >&2
  exit 1
fi
if [[ $# -lt 1 ]]; then
  echo "usage: venv_exec.sh <script.py> [args...]" >&2
  exit 1
fi
SCRIPT="$1"
shift
exec "$PY" "$APP_ROOT/$SCRIPT" "$@"
