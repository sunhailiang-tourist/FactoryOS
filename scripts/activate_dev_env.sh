#!/usr/bin/env bash
# FactoryOS 开发环境激活 — 与根 README §激活开发环境 唯一真源一致
#
# 含：uv.lock 封版安装 · docs 基线 · gate pr（含 deptry）· pre-commit（.venv）
# 不含：uv 本体安装 · Cursor Hooks 重启（需人工）
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

echo "▶ gate pr（harness · pytest · static · deptry）"
uv run python scripts/gate_cli.py pr

echo "▶ pre-commit install（.venv · lock-check · harness · pytest on push）"
uv run pre-commit install
uv run pre-commit install --hook-type pre-push

cat <<'EOF'

激活脚本完成。

请人工完成：
  1. Cursor 打开仓库根 → Settings → Hooks 见 protect-paths → 重启 Cursor
  2. 试写 src/os_core/x.py 应被拦截（未说「可以开始」）

日常纪律（已编入 pre-commit / gate，无需另记流程）：
  · pull 后：再跑本脚本，或 uv sync --frozen --extra dev
  · 新依赖：uv add <pkg> 或 uv add --dev <pkg>（禁止 pip install）
  · 改 pyproject.toml：uv lock 并同 commit 提交 uv.lock

EOF
