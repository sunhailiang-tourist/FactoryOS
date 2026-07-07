#!/usr/bin/env bash
# 模拟 standalone 迁出：临时目录 · 零父仓 · activate 关键路径全绿（W-11）
set -euo pipefail
APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WORK="$(mktemp -d "${TMPDIR:-/tmp}/web-admin-standalone-XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

echo "▶ simulate standalone · work=$WORK"

rsync -a \
  --exclude node_modules \
  --exclude dist \
  --exclude storybook-static \
  --exclude .git \
  --exclude playwright-report \
  --exclude test-results \
  "$APP_ROOT/" "$WORK/"

cd "$WORK"
cp devkit.manifest.standalone.yaml devkit.manifest.yaml

# codegen 依赖 openapi-typescript；模拟仓链到源 node_modules 避免重复 install
if [ ! -e node_modules ] && [ -d "$APP_ROOT/node_modules" ]; then
  ln -s "$APP_ROOT/node_modules" node_modules
fi

export FACTORYOS_ROOT="$WORK"
export DEVKIT_APP_ROOT="$WORK"
export WEB_PROFILE_STANDALONE=1
unset FACTORYOS_UMBRELLA_ROOT 2>/dev/null || true

PY="bash scripts/py.sh"
chmod +x scripts/py.sh 2>/dev/null || true
if ! $PY -c "import yaml" 2>/dev/null; then
  echo "▶ create .venv + install scripts/requirements.txt (pyyaml)"
  if [ ! -x .venv/bin/python ]; then
    python3 -m venv .venv 2>/dev/null || python -m venv .venv
  fi
  .venv/bin/pip install -q -r scripts/requirements.txt
fi

echo "▶ bootstrap_standalone"
$PY scripts/devkit/bootstrap_standalone.py "$WORK" "$WORK"

echo "▶ check_standalone_ready"
$PY scripts/check_standalone_ready.py

echo "▶ codegen:check (standalone paths)"
$PY scripts/check_codegen_fresh.py

echo "▶ check_harness"
$PY scripts/check_harness.py

echo "OK: simulate_standalone_activate — zero-parent harness green"
