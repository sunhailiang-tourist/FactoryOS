#!/usr/bin/env python3
"""Validate server/api router registry ↔ modules on disk.

Usage:
  python scripts/check_router_registry.py

Exit 0 = pass; 1 = violations.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = ROOT / "src" / "server" / "api"
V1_REGISTRY = API / "router" / "v1" / "registry.py"
MAIN = API / "main.py"


def _const_str(node: ast.expr) -> str | None:
  if isinstance(node, ast.Constant) and isinstance(node.value, str):
    return node.value
  return None


def _domain_names_from_api_router_domains(tree: ast.Module) -> list[str] | None:
  tuple_node: ast.Tuple | None = None
  for node in tree.body:
    if isinstance(node, ast.Assign):
      for target in node.targets:
        if isinstance(target, ast.Name) and target.id == "API_ROUTER_DOMAINS":
          if isinstance(node.value, ast.Tuple):
            tuple_node = node.value
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
      if node.target.id == "API_ROUTER_DOMAINS" and isinstance(node.value, ast.Tuple):
        tuple_node = node.value
  if tuple_node is None:
    return None
  names: list[str] = []
  for elt in tuple_node.elts:
    if not isinstance(elt, ast.Call):
      continue
    for kw in elt.keywords:
      if kw.arg == "name":
        val = _const_str(kw.value)
        if val:
          names.append(val)
          break
  return names if names else None


def _provider_modules_legacy(tree: ast.Module) -> list[str] | None:
  tuple_node: ast.Tuple | None = None
  for node in tree.body:
    if isinstance(node, ast.Assign):
      for target in node.targets:
        if isinstance(target, ast.Name) and target.id == "ROUTER_PROVIDERS":
          if isinstance(node.value, ast.Tuple):
            tuple_node = node.value
    elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
      if node.target.id == "ROUTER_PROVIDERS" and isinstance(node.value, ast.Tuple):
        tuple_node = node.value
  if tuple_node is None:
    return None
  mods: list[str] = []
  for elt in tuple_node.elts:
    if isinstance(elt, ast.Attribute) and isinstance(elt.value, ast.Name):
      mods.append(elt.value.id)
  return mods if mods else None


def _provider_modules(path: Path) -> list[str]:
  tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
  domains = _domain_names_from_api_router_domains(tree)
  if domains:
    return domains
  legacy = _provider_modules_legacy(tree)
  if legacy:
    return legacy
  raise ValueError(f"API_ROUTER_DOMAINS or ROUTER_PROVIDERS not found in {path}")


def main() -> int:
  errors: list[str] = []

  if not V1_REGISTRY.is_file():
    print(f"FAIL: missing {V1_REGISTRY.relative_to(ROOT)}", file=sys.stderr)
    return 1

  if MAIN.is_file():
    main_src = MAIN.read_text(encoding="utf-8")
    if "include_router" in main_src:
      errors.append("main.py must not call include_router (use router/registry.py)")

  try:
    providers = _provider_modules(V1_REGISTRY)
  except (OSError, ValueError, SyntaxError) as exc:
    print(f"router registry parse error: {exc}", file=sys.stderr)
    return 1

  modules_dir = API / "modules"
  for mod in providers:
    mod_dir = modules_dir / mod
    routers_py = mod_dir / "routers.py"
    if not routers_py.is_file():
      errors.append(f"modules/{mod}/routers.py missing for router domain {mod!r}")

  if errors:
    for err in errors:
      print(f"FAIL: {err}", file=sys.stderr)
    return 1

  print(f"OK: router registry aligned ({len(providers)} providers)")
  return 0


if __name__ == "__main__":
  sys.exit(main())
