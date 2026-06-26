#!/usr/bin/env python3
"""Validate os_core/registry.py ↔ on-disk kernel modules.

Usage:
  python scripts/check_kernel_registry.py

Exit 0 = pass; 1 = violations.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OS_CORE = ROOT / "src" / "server" / "os_core"
REGISTRY = OS_CORE / "registry.py"

SKIP_DIRS = frozenset({"__pycache__"})


def _load_kernel_names() -> set[str]:
  if not REGISTRY.is_file():
    raise FileNotFoundError(f"missing {REGISTRY.relative_to(ROOT)}")
  tree = ast.parse(REGISTRY.read_text(encoding="utf-8"), filename=str(REGISTRY))
  tuple_node: ast.Tuple | None = None
  for node in tree.body:
    if isinstance(node, ast.Assign):
      for target in node.targets:
        if isinstance(target, ast.Name) and target.id == "KERNEL_MODULES":
          if isinstance(node.value, ast.Tuple):
            tuple_node = node.value
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
      if node.target.id == "KERNEL_MODULES" and isinstance(node.value, ast.Tuple):
        tuple_node = node.value
  if tuple_node is None:
    raise ValueError("KERNEL_MODULES not found in os_core/registry.py")
  names: set[str] = set()
  for elt in tuple_node.elts:
    if not isinstance(elt, ast.Call):
      continue
    if elt.args and isinstance(elt.args[0], ast.Constant) and isinstance(elt.args[0].value, str):
      names.add(elt.args[0].value)
      continue
    for kw in elt.keywords:
      if kw.arg == "name" and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
        names.add(kw.value.value)
        break
  return names


def _disk_module_dirs() -> set[str]:
  out: set[str] = set()
  for child in OS_CORE.iterdir():
    if not child.is_dir() or child.name in SKIP_DIRS:
      continue
    if (child / "README.md").is_file() or any(child.glob("*.py")):
      out.add(child.name)
  return out


def main() -> int:
  errors: list[str] = []
  try:
    registered = _load_kernel_names()
  except (OSError, ValueError, SyntaxError) as exc:
    print(f"kernel registry parse error: {exc}", file=sys.stderr)
    return 1

  on_disk = _disk_module_dirs()
  missing_readme = [
    name for name in registered if not (OS_CORE / name / "README.md").is_file()
  ]
  unregistered = sorted(on_disk - registered)
  stale = sorted(registered - on_disk)

  if missing_readme:
    errors.append(f"registered modules missing README.md: {missing_readme}")
  if unregistered:
    errors.append(f"on-disk os_core modules not in KERNEL_MODULES: {unregistered}")
  if stale:
    errors.append(f"KERNEL_MODULES entries missing on disk: {stale}")

  if errors:
    for err in errors:
      print(f"FAIL: {err}", file=sys.stderr)
    return 1

  print(f"OK: kernel registry aligned ({len(registered)} modules)")
  return 0


if __name__ == "__main__":
  sys.exit(main())
