#!/usr/bin/env python3
"""落盘 web-admin 独立边界门禁 + 可迁出 AI 步步流 + harness 校验脚本。

用法：uv run python scripts/install_web_admin_independence_workflow.py
作用：托管 FactoryOS 时强制拦截越权；架构锁机器校验。
业务关联：src/apps/web-admin/.cursor/ · contracts/WEB-ARCHITECTURE-LOCK.yaml
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "src" / "apps" / "web-admin"

BOUNDARY_LIB = '''"""web-admin 独立边界与架构锁校验库。

作用：托管于 FactoryOS 时强制拦截越权写码与结构漂移。
业务关联：contracts/WEB-ARCHITECTURE-LOCK.yaml
上游：check_boundary_lock.py · check_harness.py
下游：activate.sh 验收盘
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

LOCK_REL = "contracts/WEB-ARCHITECTURE-LOCK.yaml"


def load_lock(app_root: Path) -> dict:
  path = app_root / LOCK_REL
  if not path.is_file():
    raise FileNotFoundError(f"missing architecture lock: {path}")
  return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def validate_locked_sectors(app_root: Path, lock: dict) -> list[str]:
  errors: list[str] = []
  src = app_root / "src"
  if not src.is_dir():
    return [f"missing src/: {src}"]
  allowed = {str(s) for s in lock.get("sectors") or []}
  for child in src.iterdir():
    if not child.is_dir():
      continue
    if child.name not in allowed:
      errors.append(
        f"architecture lock: unexpected src/{child.name}/ "
        f"(locked sectors: {sorted(allowed)}; need user 「确认结构变更」)"
      )
  for sector in sorted(allowed):
    if not (src / sector).is_dir():
      errors.append(f"architecture lock: missing locked sector src/{sector}/")
  return errors


def validate_forbidden_imports(app_root: Path, lock: dict) -> list[str]:
  errors: list[str] = []
  patterns = [re.compile(re.escape(p)) for p in lock.get("forbidden_import_patterns") or []]
  src = app_root / "src"
  if not src.is_dir():
    return errors
  for path in src.rglob("*"):
    if path.suffix not in {".ts", ".tsx", ".js", ".mjs"}:
      continue
    if "api/generated" in path.as_posix():
      continue
    text = path.read_text(encoding="utf-8")
    for pat in patterns:
      if pat.search(text):
        errors.append(
          f"independence violation: {_rel(app_root, path)} imports forbidden backend pattern "
          f"{pat.pattern!r} (need user 「确认越权」 to integrate)"
        )
  return errors


def validate_staged_paths_outside_app(
  app_root: Path,
  lock: dict,
  staged_paths: list[str],
) -> list[str]:
  errors: list[str] = []
  forbidden = tuple(lock.get("forbidden_write_outside_app") or [])
  app_prefix = _app_prefix(app_root)
  for rel in staged_paths:
    norm = rel.replace("\\\\", "/").lstrip("./")
    if norm.startswith(app_prefix) or norm.startswith("src/apps/web-admin/"):
      continue
    for prefix in forbidden:
      if norm.startswith(prefix) or norm == prefix.rstrip("/"):
        errors.append(
          f"independence violation: staged change touches forbidden path {norm!r} "
          f"(web-admin must stay independent; need user 「确认越权」)"
        )
        break
  return errors


def validate_lock_metadata(app_root: Path, lock: dict) -> list[str]:
  errors: list[str] = []
  if str(lock.get("profile") or "") != "WEB-PROFILE":
    errors.append("WEB-ARCHITECTURE-LOCK.yaml profile must be WEB-PROFILE")
  if not lock.get("sectors"):
    errors.append("WEB-ARCHITECTURE-LOCK.yaml missing sectors")
  eng = app_root / "ENGINEERING.md"
  arch = app_root / "ARCHITECTURE.md"
  if eng.is_file() and lock.get("engineering_revision"):
    if lock["engineering_revision"] not in eng.read_text(encoding="utf-8"):
      errors.append(
        "ENGINEERING.md revision drift vs WEB-ARCHITECTURE-LOCK.yaml "
        f"(expected {lock['engineering_revision']!r}; need 「确认结构变更」)"
      )
  if arch.is_file() and lock.get("architecture_revision"):
    if lock["architecture_revision"] not in arch.read_text(encoding="utf-8"):
      errors.append(
        "ARCHITECTURE.md revision drift vs WEB-ARCHITECTURE-LOCK.yaml "
        f"(expected {lock['architecture_revision']!r}; need 「确认结构变更」)"
      )
  return errors


def _app_prefix(app_root: Path) -> str:
  parts = app_root.as_posix().split("/")
  if "src" in parts and "apps" in parts:
    idx = parts.index("src")
    return "/".join(parts[idx:])
  return app_root.name + "/"


def _rel(app_root: Path, path: Path) -> str:
  try:
    return str(path.relative_to(app_root))
  except ValueError:
    return str(path)


def run_all_checks(app_root: Path, *, staged_paths: list[str] | None = None) -> list[str]:
  errors: list[str] = []
  try:
    lock = load_lock(app_root)
  except FileNotFoundError as exc:
    return [str(exc)]
  errors.extend(validate_lock_metadata(app_root, lock))
  errors.extend(validate_locked_sectors(app_root, lock))
  errors.extend(validate_forbidden_imports(app_root, lock))
  if staged_paths:
    errors.extend(validate_staged_paths_outside_app(app_root, lock, staged_paths))
  return errors
'''

CHECK_BOUNDARY = '''#!/usr/bin/env python3
"""web-admin 独立边界 + 架构锁强制门禁。

用法：
  python scripts/check_boundary_lock.py
  WEB_STRICT_BOUNDARY=1 python scripts/check_boundary_lock.py

作用：托管于 FactoryOS 时拦截跨项目写码与结构漂移。
业务关联：contracts/WEB-ARCHITECTURE-LOCK.yaml · .cursor/rules/WEB-00*
上游：activate.sh · check_harness.py
下游：AI 工作流停机关键词「确认越权」「确认结构变更」
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_ROOT / "scripts"))

from boundary_lock_lib import run_all_checks  # noqa: E402


def _git_staged_paths(app_root: Path) -> list[str]:
  try:
    proc = subprocess.run(
      ["git", "diff", "--cached", "--name-only"],
      cwd=app_root,
      capture_output=True,
      text=True,
      check=False,
    )
  except OSError:
    return []
  if proc.returncode != 0:
    return []
  return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def main() -> int:
  strict = os.environ.get("WEB_STRICT_BOUNDARY", "").strip() in {"1", "true", "yes"}
  staged = _git_staged_paths(APP_ROOT) if strict else None
  errors = run_all_checks(APP_ROOT, staged_paths=staged)
  if errors:
    print("web-admin boundary/lock FAIL:", file=sys.stderr)
    for err in errors:
      print(f"  - {err}", file=sys.stderr)
    print(
      "\\n停机：须用户发送「确认结构变更」或「确认越权」后方可继续。",
      file=sys.stderr,
    )
    return 1
  mode = "strict+staged" if strict and staged else "static"
  print(f"OK: web-admin boundary lock ({mode})")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
'''


def w(rel: str, content: str) -> None:
  path = APP / rel
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(content, encoding="utf-8")
  print(f"  wrote {path.relative_to(ROOT)}")


def patch_harness() -> None:
  path = APP / "scripts" / "check_harness.py"
  text = path.read_text(encoding="utf-8")
  if "boundary_lock_lib" not in text:
    anchor = "SCRIPTS = _resolve_scripts_dir()"
    insert = '''SCRIPTS = _resolve_scripts_dir()

_BOUNDARY_LIB = APP_ROOT / "scripts" / "boundary_lock_lib.py"
if _BOUNDARY_LIB.is_file():
  import importlib.util
  _spec = importlib.util.spec_from_file_location("boundary_lock_lib", _BOUNDARY_LIB)
  _boundary = importlib.util.module_from_spec(_spec)
  assert _spec and _spec.loader
  _spec.loader.exec_module(_boundary)
else:
  _boundary = None
'''
    text = text.replace(anchor, insert, 1)

  if "_validate_boundary_lock" not in text:
    fn = '''

def _validate_boundary_lock(errors: list[str]) -> None:
  """独立边界 + 架构 sector 锁（WEB-ARCHITECTURE-LOCK.yaml）。"""
  if _boundary is None:
    errors.append("missing scripts/boundary_lock_lib.py (run install_web_admin_independence_workflow.py)")
    return
  for err in _boundary.run_all_checks(APP_ROOT):
    errors.append(err)
'''
    text = text.replace(
      "  _validate_resource_chain(errors)\n",
      "  _validate_resource_chain(errors)\n  _validate_boundary_lock(errors)\n",
    )
    text = text.replace(
      "def main() -> int:",
      fn + "\ndef main() -> int:",
    )

  path.write_text(text, encoding="utf-8")
  print(f"  patched {path.relative_to(ROOT)}")


def patch_profile() -> None:
  path = APP / "devkit.profile.yaml"
  text = path.read_text(encoding="utf-8")
  for check in ("web_admin_independence", "architecture_lock_sync"):
    if check not in text:
      text = text.replace(
        "  - rbac_route_permissions\n",
        f"  - rbac_route_permissions\n  - {check}\n",
      )
  path.write_text(text, encoding="utf-8")
  print(f"  patched {path.relative_to(ROOT)}")


def patch_activate() -> None:
  path = APP / "scripts" / "activate.sh"
  text = path.read_text(encoding="utf-8")
  if "check_boundary_lock.py" not in text:
    text = text.replace(
      'run_py "scripts/check_harness.py"',
      'run_py "scripts/check_boundary_lock.py"\nrun_py "scripts/check_harness.py"',
    )
  if "_web_pipeline" not in text:
    text = text.replace(
      "  红灯：contracts/README.md § 红灯怎么办",
      "  AI 工作流：.cursor/INDEX.md（【WebDev模式启动】· 独立步步流）\n  红灯：contracts/README.md § 红灯怎么办",
    )
  path.write_text(text, encoding="utf-8")
  print(f"  patched {path.relative_to(ROOT)}")


def patch_readme() -> None:
  path = APP / "README.md"
  text = path.read_text(encoding="utf-8")
  block = """
## AI 工作流（独立 · 可迁出）

| 项 | 路径 |
|----|------|
| 入口 | [`.cursor/INDEX.md`](./.cursor/INDEX.md) |
| Dev 口令 | `【WebDev模式启动】` |
| 绝对门禁 | `WEB-00` 独立边界 · `WEB-01` 架构锁 |
| 落盘 | `_web_pipeline/<date>/` |
| 边界校验 | `python scripts/check_boundary_lock.py` |

**迁出**：复制 `.cursor/` + `contracts/WEB-ARCHITECTURE-LOCK.yaml` 到新仓库即可。
"""
  if "AI 工作流（独立" not in text:
    text = text.rstrip() + "\n" + block + "\n"
    path.write_text(text, encoding="utf-8")
    print(f"  patched {path.relative_to(ROOT)}")


def patch_umbrella_rules() -> None:
  rules = ROOT / ".cursor" / "rules"
  rules.mkdir(parents=True, exist_ok=True)
  content = """---
description: web-admin 托管边界 — 编辑 src/apps/web-admin 时强制加载独立门禁（指向 App 内 .cursor）
alwaysApply: true
---

# FactoryOS 内 web-admin 托管声明

当本轮任务涉及 **`src/apps/web-admin/**`** 或用户明确 web-admin 前端时：

1. **强制遵守** `src/apps/web-admin/.cursor/rules/WEB-00-独立边界绝对门禁.mdc`
2. **强制遵守** `src/apps/web-admin/.cursor/rules/WEB-01-架构版图锁死门禁.mdc`
3. **工作流**用 `【WebDev模式启动】` / `【WebTest模式启动】`，**不用** FactoryOS `【Dev模式启动】` 写 web-admin 业务
4. **落盘** `_web_pipeline/`（非 `_factoryos_pipeline/`）
5. 越权/结构变更 → 停机 → 用户 `确认越权` / `确认结构变更`

web-admin 验收盘：`src/apps/web-admin/scripts/activate.sh`（非 pytest · 非后端 gate）。
"""
  path = rules / "WEB-admin-托管边界.mdc"
  path.write_text(content, encoding="utf-8")
  print(f"  wrote {path.relative_to(ROOT)}")


def main() -> None:
  print("▶ install web-admin independence workflow")
  w("scripts/boundary_lock_lib.py", BOUNDARY_LIB)
  w("scripts/check_boundary_lock.py", CHECK_BOUNDARY)
  (APP / "scripts" / "check_boundary_lock.py").chmod(0o755)
  patch_harness()
  patch_profile()
  patch_activate()
  patch_readme()
  patch_umbrella_rules()
  print("✅ done — run: cd src/apps/web-admin && python scripts/check_boundary_lock.py")


if __name__ == "__main__":
  main()
