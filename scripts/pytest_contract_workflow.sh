#!/usr/bin/env bash
# pre-commit pre-push · gate pr 同款 contract+workflow pytest（排除 pending AC）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
PY="${ROOT}/.venv/bin/python"
if [[ ! -x "$PY" ]]; then
  echo "Missing .venv — run: uv sync --extra dev" >&2
  exit 1
fi
exec "$PY" -m pytest src/tests/contract src/tests/workflow -q -m "not pending"
