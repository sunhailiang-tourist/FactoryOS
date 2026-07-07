#!/usr/bin/env python3
# web-admin 构建产物体积门禁（W-07 + S4 vendor-react/index）
from __future__ import annotations

import json
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
DIST = APP_ROOT / "dist" / "assets"

LIMITS: dict[str, int] = {
  "vendor-react": 260_000,
  "vendor-mui": 650_000,
  "vendor-echarts": 1_000_000,
  "vendor-animate": 120_000,
  "index": 120_000,
}
DEFAULT_MAX = 1_500_000


def _chunk_limit(name: str) -> int:
  for prefix, limit in LIMITS.items():
    if name.startswith(prefix) or f"-{prefix}" in name or prefix in name:
      return limit
  return DEFAULT_MAX


def main() -> int:
  if not DIST.is_dir():
    print("FAIL: dist/assets missing — run pnpm build first", file=sys.stderr)
    return 1

  js_files = sorted(DIST.glob("*.js"))
  if not js_files:
    print("FAIL: no JS assets in dist/assets", file=sys.stderr)
    return 1

  report: list[dict[str, int | str]] = []
  errors: list[str] = []

  for path in js_files:
    size = path.stat().st_size
    limit = _chunk_limit(path.name)
    report.append({"file": path.name, "bytes": size, "limit": limit})
    if size > limit:
      errors.append(f"{path.name}: {size} > {limit} bytes")

  print(json.dumps({"chunks": report}, ensure_ascii=False, indent=2))

  if errors:
    print("bundle size FAIL:", file=sys.stderr)
    for err in errors:
      print(f"  - {err}", file=sys.stderr)
    return 1

  print("OK: bundle size within limits")
  return 0


if __name__ == "__main__":
  sys.exit(main())
