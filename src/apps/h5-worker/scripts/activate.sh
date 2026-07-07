#!/usr/bin/env bash
# h5-worker · 一键激活 DevKit AI 研发流（umbrella / standalone 自洽）
set -euo pipefail
APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_ROOT"

find_repo_root() {
  local dir="$APP_ROOT"
  while [ "$dir" != "/" ]; do
    if [ -f "$dir/devkit.manifest.yaml" ] && grep -q 'mode: umbrella' "$dir/devkit.manifest.yaml" 2>/dev/null; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  echo "$APP_ROOT"
}

REPO_ROOT="$(find_repo_root)"
export FACTORYOS_ROOT="$REPO_ROOT"
export DEVKIT_APP_ROOT="$APP_ROOT"
export DEVKIT_PROFILE=h5-worker

echo "▶ DevKit activate · profile=h5-worker · repo=$REPO_ROOT"

if [ "$REPO_ROOT" = "$APP_ROOT" ] \
  && [ -f "$APP_ROOT/devkit.manifest.yaml" ] \
  && grep -q 'mode: standalone' "$APP_ROOT/devkit.manifest.yaml" 2>/dev/null; then
  echo "▶ mode=standalone · bootstrap AI kernel（devkit/kernel 快照）"
  python "$APP_ROOT/scripts/devkit/bootstrap_standalone.py" "$APP_ROOT" "$APP_ROOT"
fi

if [ -f package.json ] && command -v pnpm >/dev/null 2>&1; then
  pnpm install --frozen-lockfile 2>/dev/null || pnpm install || true
  pnpm check 2>/dev/null || echo "⚠ pnpm check 待阶段 2 脚手架完成后启用"
fi

python "$APP_ROOT/scripts/check_harness.py"

cat <<EOF

════════════════════════════════════════════════════════════
  h5-worker DevKit 已激活 · AC-UX-001
════════════════════════════════════════════════════════════
  模式：$([ "$REPO_ROOT" = "$APP_ROOT" ] && echo standalone || echo umbrella→$REPO_ROOT)
  AI 口令：【Dev模式启动】· 【Test模式启动】· 【Verify回合】Step N
  落盘：$REPO_ROOT/_factoryos_pipeline/
  Gate：$REPO_ROOT/scripts/gate（umbrella）或 ./scripts/gate（standalone）

EOF
