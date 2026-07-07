#!/usr/bin/env python3
"""一次性安装 web-admin standalone P0 工具到 App scripts/。"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "src" / "apps" / "web-admin"
SCRIPTS = APP / "scripts"

PY_SH = """#!/usr/bin/env bash
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
"""

REQUIREMENTS = """# web-admin scripts/ 最小 Python 依赖（standalone 自给）
pyyaml>=6.0
"""


def _write_error_registry_lib() -> None:
  path = SCRIPTS / "error_registry_lib.py"
  path.write_text(
    Path(__file__).with_name("_web_admin_error_registry_lib.py").read_text(encoding="utf-8"),
    encoding="utf-8",
  )


def _write_sync_and_check() -> None:
  (SCRIPTS / "sync_error_registry.py").write_text(
    Path(__file__).with_name("_web_admin_sync_error_registry.py").read_text(encoding="utf-8"),
    encoding="utf-8",
  )
  (SCRIPTS / "check_error_registry_sync.py").write_text(
    Path(__file__).with_name("_web_admin_check_error_registry_sync.py").read_text(encoding="utf-8"),
    encoding="utf-8",
  )


def _write_vendor_forwarder() -> None:
  vendor = APP / "vendor/factoryos-contracts/scripts/sync_error_registry.py"
  vendor.write_text(
    """#!/usr/bin/env python3
\"\"\"委托 App scripts/sync_error_registry.py（devkit.manifest sync_script 入口）。\"\"\"
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[3]
script = APP_ROOT / "scripts" / "sync_error_registry.py"
raise SystemExit(subprocess.call([sys.executable, str(script), *sys.argv[1:]]))
""",
    encoding="utf-8",
  )
  vendor.chmod(0o755)


def _write_py_runtime() -> None:
  py_sh = SCRIPTS / "py.sh"
  py_sh.write_text(PY_SH, encoding="utf-8")
  py_sh.chmod(0o755)
  (SCRIPTS / "requirements.txt").write_text(REQUIREMENTS, encoding="utf-8")


def _patch_check_harness() -> None:
  path = SCRIPTS / "check_harness.py"
  text = path.read_text(encoding="utf-8")
  if "_script_python_argv" not in text:
    text = text.replace(
      "REPO_ROOT = _resolve_repo_root()\n",
      """REPO_ROOT = _resolve_repo_root()


def _script_python_argv(script: Path) -> list[str]:
  \"\"\"py.sh 优先 umbrella .venv，standalone 走 activate 已装的 pyyaml。\"\"\"
  py_sh = APP_ROOT / "scripts" / "py.sh"
  if py_sh.is_file():
    return ["bash", str(py_sh), str(script)]
  return [sys.executable, str(script)]
""",
    )
  text = text.replace(
    "[sys.executable, str(script)]",
    "_script_python_argv(script)",
  )
  path.write_text(text, encoding="utf-8")


def _patch_standalone_ready() -> None:
  path = SCRIPTS / "check_standalone_ready.py"
  text = path.read_text(encoding="utf-8")
  if 'scripts/py.sh' not in text:
    needle = """  if not (APP_ROOT / "scripts" / "check_error_registry_sync.py").is_file():
    errors.append("missing scripts/check_error_registry_sync.py")
"""
    repl = """  if not (APP_ROOT / "scripts" / "py.sh").is_file():
    errors.append("missing scripts/py.sh")

  if not (APP_ROOT / "scripts" / "requirements.txt").is_file():
    errors.append("missing scripts/requirements.txt")

  if not (APP_ROOT / "scripts" / "check_error_registry_sync.py").is_file():
    errors.append("missing scripts/check_error_registry_sync.py")
"""
    text = text.replace(needle, repl)
    path.write_text(text, encoding="utf-8")


def _patch_simulate_activate() -> None:
  path = SCRIPTS / "simulate_standalone_activate.sh"
  text = path.read_text(encoding="utf-8")
  if "create .venv + install scripts/requirements.txt" in text:
    return
  pip_block = """if ! $PY -c "import yaml" 2>/dev/null; then
  echo "▶ install scripts/requirements.txt (pyyaml)"
  $PY -m pip install -q -r scripts/requirements.txt
fi"""
  venv_block = """if ! $PY -c "import yaml" 2>/dev/null; then
  echo "▶ create .venv + install scripts/requirements.txt (pyyaml)"
  if [ ! -x .venv/bin/python ]; then
    python3 -m venv .venv 2>/dev/null || python -m venv .venv
  fi
  .venv/bin/pip install -q -r scripts/requirements.txt
fi"""
  if pip_block in text:
    path.write_text(text.replace(pip_block, venv_block), encoding="utf-8")
    path.chmod(0o755)
    return
  old = """export FACTORYOS_ROOT="$WORK"
export DEVKIT_APP_ROOT="$WORK"
export WEB_PROFILE_STANDALONE=1
unset FACTORYOS_UMBRELLA_ROOT 2>/dev/null || true

echo "▶ bootstrap_standalone"
python scripts/devkit/bootstrap_standalone.py "$WORK" "$WORK"

echo "▶ check_standalone_ready"
python scripts/check_standalone_ready.py

echo "▶ codegen:check (standalone paths)"
python scripts/check_codegen_fresh.py

echo "▶ check_harness"
python scripts/check_harness.py
"""
  new = """export FACTORYOS_ROOT="$WORK"
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
"""
  if old not in text:
    raise SystemExit("simulate_standalone_activate.sh layout changed; update installer patch")
  path.write_text(text.replace(old, new), encoding="utf-8")
  path.chmod(0o755)


def _patch_activate() -> None:
  path = SCRIPTS / "activate.sh"
  text = path.read_text(encoding="utf-8")
  old = """# standalone 脚本依赖（pyyaml）
if ! "$PY" -c "import yaml" 2>/dev/null; then
  echo "▶ installing scripts/requirements.txt (pyyaml)"
  "$PY" -m pip install -q -r "$APP_ROOT/scripts/requirements.txt"
fi
"""
  new = """# standalone 脚本依赖（pyyaml · PEP 668 安全：App 内 .venv）
if ! "$PY" -c "import yaml" 2>/dev/null; then
  echo "▶ create .venv + install scripts/requirements.txt (pyyaml)"
  if [ ! -x "$APP_ROOT/.venv/bin/python" ]; then
    python3 -m venv "$APP_ROOT/.venv" 2>/dev/null || python -m venv "$APP_ROOT/.venv"
  fi
  "$APP_ROOT/.venv/bin/pip" install -q -r "$APP_ROOT/scripts/requirements.txt"
fi
"""
  if old in text:
    path.write_text(text.replace(old, new), encoding="utf-8")


def main() -> int:
  _write_error_registry_lib()
  _write_sync_and_check()
  _write_vendor_forwarder()
  _write_py_runtime()
  _patch_check_harness()
  _patch_standalone_ready()
  _patch_simulate_activate()
  _patch_activate()
  for name in ("sync_error_registry.py", "check_error_registry_sync.py"):
    (SCRIPTS / name).chmod(0o755)
  print("Installed standalone P0 tools into", SCRIPTS.relative_to(ROOT))
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
