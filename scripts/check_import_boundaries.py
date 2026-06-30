#!/usr/bin/env python3
"""Validate os_core/ import boundaries per 膨胀期架构守则 §2 (stdlib only).

Usage:
  python scripts/check_import_boundaries.py

Exit 0 = pass; 1 = violations found.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OS_CORE = ROOT / "src" / "server" / "os_core"
INTEGRATION = ROOT / "src" / "integration"

ALLOWED: dict[str, set[str]] = {
    "shared_contracts": {"platform_registry"},
    "platform_registry": {"shared_contracts"},
    "audit_service": {"shared_contracts"},
    "graph_service": {"shared_contracts", "audit_service"},
    "rule_engine": {"shared_contracts", "audit_service"},
    "execution_service": {
        "shared_contracts",
        "audit_service",
        "connector_sdk",
        "rule_engine",
        "graph_service",
        "license_service",
    },
    "connector_sdk": {"shared_contracts", "platform_registry"},
    "agent_orchestrator": {"shared_contracts"},
    "license_service": {"shared_contracts"},
    "reconciliation_service": {
        "shared_contracts",
        "connector_sdk",
        "execution_service",
    },
    "mcp_gateway": {"shared_contracts", "agent_orchestrator"},
}

INTEGRATION_ALLOWED_PACKAGES = {"shared_contracts", "connector_sdk"}


def module_name_from_path(path: Path) -> str | None:
    try:
        rel = path.relative_to(OS_CORE)
    except ValueError:
        return None
    parts = rel.parts
    if not parts or parts[0] not in ALLOWED:
        return None
    return parts[0]


def parse_imports(path: Path) -> list[tuple[int, str]]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except SyntaxError as exc:
        return [(-1, f"syntax error: {exc}")]
    out: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                out.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom) and node.module:
            out.append((node.lineno, node.module))
    return out


def imported_package(module: str) -> str | None:
    if module.startswith("os_core."):
        rest = module[len("os_core.") :]
        return rest.split(".")[0] if rest else None
    return None


def check_os_core() -> list[str]:
    errors: list[str] = []
    if not OS_CORE.is_dir():
        return errors
    for py in OS_CORE.rglob("*.py"):
        if "__pycache__" in py.parts:
            continue
        owner = module_name_from_path(py)
        if owner is None:
            continue
        allowed = ALLOWED[owner]
        for lineno, mod in parse_imports(py):
            if lineno < 0:
                errors.append(f"{py}: {mod}")
                continue
            pkg = imported_package(mod)
            if pkg is None or pkg == owner:
                continue
            if pkg not in ALLOWED:
                errors.append(f"{py}:{lineno}: unknown package import os_core.{pkg}")
            elif pkg not in allowed:
                errors.append(
                    f"{py}:{lineno}: {owner} must not import os_core.{pkg} "
                    f"(allowed: {sorted(allowed) or ['—']})"
                )
    return errors


def check_integration() -> list[str]:
    errors: list[str] = []
    if not INTEGRATION.is_dir():
        return errors
    for py in INTEGRATION.rglob("*.py"):
        if "__pycache__" in py.parts:
            continue
        for lineno, mod in parse_imports(py):
            if lineno < 0:
                errors.append(f"{py}: {mod}")
                continue
            pkg = imported_package(mod)
            if pkg is None:
                continue
            if pkg not in INTEGRATION_ALLOWED_PACKAGES:
                errors.append(
                    f"{py}:{lineno}: integration/ must not import os_core.{pkg} "
                    f"(allowed: {sorted(INTEGRATION_ALLOWED_PACKAGES)})"
                )
    return errors


def main() -> int:
    errors = check_os_core() + check_integration()
    if errors:
        print("Import boundary violations:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    print("Import boundaries OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
