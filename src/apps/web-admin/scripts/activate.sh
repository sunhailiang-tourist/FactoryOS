#!/usr/bin/env bash
# web-admin · 一键激活 DevKit AI 研发流（umbrella / standalone 自洽）
set -euo pipefail
APP_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$APP_ROOT"

find_repo_root() {
  local dir="$APP_ROOT"
  while [ "$dir" != "/" ]; do
    if [ -f "$dir/devkit.manifest.yaml" ]; then
      if grep -q 'mode: umbrella' "$dir/devkit.manifest.yaml" 2>/dev/null; then
        echo "$dir"
        return 0
      fi
    fi
    dir="$(dirname "$dir")"
  done
  echo "$APP_ROOT"
}

REPO_ROOT="$(find_repo_root)"
export FACTORYOS_ROOT="$REPO_ROOT"
export DEVKIT_APP_ROOT="$APP_ROOT"
export DEVKIT_PROFILE=web-admin
PY="$APP_ROOT/scripts/py.sh"
chmod +x "$PY" 2>/dev/null || true

# standalone 脚本依赖（pyyaml · PEP 668 安全：App 内 .venv）
if ! "$PY" -c "import yaml" 2>/dev/null; then
  echo "▶ create .venv + install scripts/requirements.txt (pyyaml)"
  if [ ! -x "$APP_ROOT/.venv/bin/python" ]; then
    python3 -m venv "$APP_ROOT/.venv" 2>/dev/null || python -m venv "$APP_ROOT/.venv"
  fi
  "$APP_ROOT/.venv/bin/pip" install -q -r "$APP_ROOT/scripts/requirements.txt"
fi

echo "▶ DevKit activate · profile=web-admin · repo=$REPO_ROOT"

# standalone：仅当本仓即 repo 根且 manifest 为 standalone
if [ "$REPO_ROOT" = "$APP_ROOT" ] \
  && [ -f "$APP_ROOT/devkit.manifest.yaml" ] \
  && grep -q 'mode: standalone' "$APP_ROOT/devkit.manifest.yaml" 2>/dev/null; then
  echo "▶ mode=standalone · bootstrap AI kernel（devkit/kernel 快照）"
  "$PY" "$APP_ROOT/scripts/devkit/bootstrap_standalone.py" "$APP_ROOT" "$APP_ROOT"
fi

if [ -f package.json ]; then
  if command -v pnpm >/dev/null 2>&1; then
    echo "▶ pnpm install"
    pnpm install --frozen-lockfile 2>/dev/null || pnpm install
    echo "▶ pnpm check"
    pnpm check
  else
    echo "⚠ pnpm 未安装，跳过前端 check"
  fi
fi

echo "▶ python scripts/check_boundary_lock.py"
"$PY" "$APP_ROOT/scripts/check_boundary_lock.py"
echo "▶ python scripts/check_harness.py"
"$PY" "$APP_ROOT/scripts/check_harness.py"

cat <<EOF

════════════════════════════════════════════════════════════
  web-admin DevKit 已激活
════════════════════════════════════════════════════════════
  模式：$([ "$REPO_ROOT" = "$APP_ROOT" ] && echo standalone || echo umbrella→$REPO_ROOT)
  工程真源：ENGINEERING.md · ARCHITECTURE.md
  开发者手册：$REPO_ROOT/contracts/README.md#前端工程全流程开发者手册
  AI 口令：【WebDev模式启动】· 【WebTest模式启动】· 【WebVerify回合】Step N
  落盘：_web_pipeline/（web-admin 独立 · 可迁出 .cursor/）
  绝对门禁：WEB-00 独立边界 · WEB-01 架构锁
  FactoryOS gate：仅 umbrella 调度；web-admin 验收盘以本目录 activate 为准

────────────────────────────────────────────────────────────
  下一步（开发）
  1. pnpm dev                    # 本地预览（VITE_MSW=1 无后端）
  2. 读 ARCHITECTURE.md → ENGINEERING.md
  3. 新业务：pnpm create:module  # 含 i18n/rbac/permissions + contracts 登记
  4. 提交前：pnpm check          # 与 activate 同链
  AI 工作流：.cursor/INDEX.md（【WebDev模式启动】· 独立步步流）
  红灯：contracts/README.md § 红灯怎么办
────────────────────────────────────────────────────────────

EOF
