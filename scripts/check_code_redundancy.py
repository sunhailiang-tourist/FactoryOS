#!/usr/bin/env python3
"""代码冗余检查（编码绝对门禁 §4.2）。

Usage:
  python scripts/check_code_redundancy.py
"""
from __future__ import annotations

import ast
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCAN_DIRS = [ROOT / "src" / "server" / "os_core", ROOT / "src" / "server" / "api"]
MIN_LINES = 8
SKIP_PARTS = {"__pycache__", ".venv", "node_modules", "tests"}


def _normalize_source(source: str) -> str:
    lines: list[str] = []
    for line in source.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        lines.append(stripped)
    return "\n".join(lines)


def _file_hashes(path: Path) -> list[tuple[str, int, str]]:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        return []
    out: list[tuple[str, int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            seg = ast.get_source_segment(source, node)
            if not seg:
                continue
            norm = _normalize_source(seg)
            if norm.count("\n") + 1 < MIN_LINES:
                continue
            digest = hashlib.sha256(norm.encode()).hexdigest()[:16]
            out.append((digest, node.lineno, node.name))
    return out


def main() -> int:
    errors: list[str] = []
    digest_map: dict[str, list[str]] = {}

    for base in SCAN_DIRS:
        if not base.is_dir():
            continue
        for py in base.rglob("*.py"):
            if any(p in SKIP_PARTS for p in py.parts):
                continue
            for digest, lineno, name in _file_hashes(py):
                digest_map.setdefault(digest, []).append(
                    f"{py.relative_to(ROOT)}:{lineno} ({name})"
                )

    for digest, locations in digest_map.items():
        if len(locations) > 1:
            unique_files = {loc.split(":")[0] for loc in locations}
            if len(unique_files) > 1:
                errors.append(
                    f"疑似重复逻辑 {digest}:\n  " + "\n  ".join(locations)
                )

    if errors:
        print("Code redundancy violations:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print("Code redundancy check OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
