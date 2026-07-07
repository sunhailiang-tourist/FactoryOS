#!/usr/bin/env bash
# 一键从 frontend-devkit 模板创建与 web-admin 等权的前端 App
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [ $# -lt 1 ]; then
  echo "Usage: $0 <app-id> [--package NAME] [--ac-scope SCOPE] [--title TITLE]" >&2
  echo "Example: $0 order-console" >&2
  exit 1
fi

exec uv run python scripts/devkit/scaffold_frontend_app.py --id "$1" "${@:2}"
