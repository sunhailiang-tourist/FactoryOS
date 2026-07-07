#!/usr/bin/env python3
"""将 web-admin 金样同步到 templates/frontend-devkit（模板真源刷新）。

作用：web-admin 工程基座演进后，运行本脚本刷新可复刻模板。
业务关联：templates/frontend-devkit · scaffold_frontend_app.py
上游：src/apps/web-admin
下游：一键 scaffold 新前端 App
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLDEN = ROOT / "src" / "apps" / "web-admin"
TEMPLATE = ROOT / "templates" / "frontend-devkit"

EXCLUDE_DIRS = {
  "node_modules",
  "dist",
  "storybook-static",
  ".playwright-browsers",
  "test-results",
  "playwright-report",
  "__pycache__",
}

# 模板元数据 — 不同步覆盖（手写 / scaffold 专用）
PRESERVE_FILES = {
  "TEMPLATE.md",
  "template.manifest.yaml",
}


def _ignore(_dir: str, names: list[str]) -> set[str]:
  return {n for n in names if n in EXCLUDE_DIRS}


def sync_template(*, dry_run: bool = False) -> list[str]:
  """复制金样 → 模板目录；返回写入相对路径列表。"""
  if not GOLDEN.is_dir():
    raise SystemExit(f"golden app missing: {GOLDEN}")

  written: list[str] = []
  if not dry_run:
    TEMPLATE.mkdir(parents=True, exist_ok=True)
    for child in TEMPLATE.iterdir():
      if child.name in PRESERVE_FILES:
        continue
      if child.is_dir():
        shutil.rmtree(child)
      else:
        child.unlink()

  for src in GOLDEN.rglob("*"):
    if any(part in EXCLUDE_DIRS for part in src.parts):
      continue
    rel = src.relative_to(GOLDEN)
    if rel.name in PRESERVE_FILES:
      continue
    dst = TEMPLATE / rel
    if src.is_dir():
      if not dry_run:
        dst.mkdir(parents=True, exist_ok=True)
      continue
    written.append(str(rel))
    if not dry_run:
      dst.parent.mkdir(parents=True, exist_ok=True)
      shutil.copy2(src, dst)

  return written


def main() -> int:
  parser = argparse.ArgumentParser(description="Sync web-admin golden app → templates/frontend-devkit")
  parser.add_argument("--dry-run", action="store_true", help="List files only")
  args = parser.parse_args()
  paths = sync_template(dry_run=args.dry_run)
  action = "would sync" if args.dry_run else "synced"
  print(f"{action} {len(paths)} files → {TEMPLATE.relative_to(ROOT)}")
  if not args.dry_run:
    print("next: uv run python scripts/devkit/check_frontend_template_parity.py")
    print("then: bump contracts/frontend-devkit-lock.yaml + template.manifest.yaml if structural change")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
