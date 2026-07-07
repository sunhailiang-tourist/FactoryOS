"""web-admin 独立边界与架构锁校验库。

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
    norm = rel.replace("\\", "/").lstrip("./")
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
