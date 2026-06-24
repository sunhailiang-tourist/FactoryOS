#!/usr/bin/env bash
# pyproject.toml 与 uv.lock 必须同步（A′ 漂移检测）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found on PATH — install: https://docs.astral.sh/uv/" >&2
  exit 1
fi
if uv lock --check; then
  echo "uv lock check OK"
else
  echo "uv.lock out of sync — run: uv lock && git add uv.lock" >&2
  exit 1
fi
