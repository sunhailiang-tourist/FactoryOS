#!/usr/bin/env bash
# FactoryOS 开发环境激活 — 与根 README §激活开发环境 唯一真源一致
#
# 一条命令具备：
#   · uv.lock 封版依赖（含 pre-commit · pyyaml）
#   · docs 认知基线
#   · gate pr（harness 11 项 · pytest · static · deptry）
#   · git pre-commit / pre-push（含结构快照 commit 拦截）
# 不含：uv 本体安装 · Cursor Hooks 重启（需人工一步）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v uv >/dev/null 2>&1; then
  echo "uv 未安装。先执行：" >&2
  echo "  curl -LsSf https://astral.sh/uv/install.sh | sh" >&2
  echo "  source \$HOME/.local/bin/env" >&2
  exit 1
fi

echo "▶ uv sync --frozen --extra dev"
uv sync --frozen --extra dev

echo "▶ docs_baseline refresh"
./scripts/docs_baseline refresh

echo "▶ gate pr（harness 11 项 · pytest · static · deptry · 结构快照对账）"
uv run python scripts/gate_cli.py pr

echo "▶ pre-commit install（commit：结构快照 · lock · harness · push：pytest）"
uv run pre-commit install
uv run pre-commit install --hook-type pre-push

echo "▶ 验证结构快照 commit 门禁"
uv run python scripts/check_structure_change.py

cat <<'EOF'

════════════════════════════════════════════════════════════
  激活完成 · 以下能力已就绪（无需再装别的）
════════════════════════════════════════════════════════════

  [x] Python 依赖（uv.lock 封版）
  [x] docs 认知基线（.cursor/docs-baseline/）
  [x] gate pr / CI 同款 harness（含路径一致性 · 结构快照）
  [x] git commit 拦截：结构变更须同步 contracts/repo-structure.yaml
  [x] git push 拦截：contract + workflow pytest

  真源：contracts/repo-structure.yaml → .cursor/factoryos/PATH-SNAPSHOT.md
  自检：uv run python scripts/check_structure_change.py

  请再人工完成（仅一次）：
  1. Cursor 打开仓库根 → Settings → Hooks 见 protect-paths → 重启 Cursor
  2. 未说「可以开始」时写 src/server/os_core/*.py 应被 Cursor 拦截

  日常：
  · pull 后依赖有变 → 重跑本脚本
  · 勿只跑 uv sync（不会装 git hooks）
  · 新依赖：uv add <pkg>；pyproject.toml 与 uv.lock 同 commit

EOF
