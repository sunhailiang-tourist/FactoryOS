#!/usr/bin/env python3
"""Resolve OpenAPI component $ref paths to JSON Schema files on disk.

Usage:
  python scripts/check_openapi_schema_refs.py

Exit 0 = all refs resolve; 1 = missing files or parse errors.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OPENAPI = ROOT / "contracts" / "openapi" / "工厂操作系统-v1.1.yaml"
SCHEMA_DIR = ROOT / "contracts" / "schemas"

REF_PATTERN = re.compile(
    r"\$ref:\s*['\"]?\.\./schemas/([^'\"\s]+)['\"]?"
)


def main() -> int:
    if not OPENAPI.is_file():
        print(f"Missing OpenAPI: {OPENAPI}", file=sys.stderr)
        return 1
    text = OPENAPI.read_text(encoding="utf-8")
    refs = sorted(set(REF_PATTERN.findall(text)))
    errors: list[str] = []
    for name in refs:
        path = SCHEMA_DIR / name
        if not path.is_file():
            errors.append(f"Unresolved $ref: {name} (expected {path})")
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1
    print(f"OpenAPI schema refs OK ({len(refs)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
