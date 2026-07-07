#!/usr/bin/env bash
# 解析 web-admin 脚本用 Python（umbrella .venv 优先 · standalone 须已 pip install -r scripts/requirements.txt）
set -euo pipefail
APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ -n "${FACTORYOS_ROOT:-}" ] && [ -x "$FACTORYOS_ROOT/.venv/bin/python" ]; then
  exec "$FACTORYOS_ROOT/.venv/bin/python" "$@"
fi
if [ -x "$APP_ROOT/.venv/bin/python" ]; then
  exec "$APP_ROOT/.venv/bin/python" "$@"
fi
if command -v python3 >/dev/null 2>&1; then
  exec python3 "$@"
fi
exec python "$@"
