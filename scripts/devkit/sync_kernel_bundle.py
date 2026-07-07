#!/usr/bin/env python3
"""将 FactoryOS AI 内核快照同步到各 App devkit/kernel/（standalone 迁出真源）。"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BUNDLE_PARTS = (
  (".cursor/factoryos", "factoryos"),
  (".cursor/rules", "rules"),
  ("_factoryos_pipeline/README.md", "pipeline/README.md"),
)


def sync_app(app_rel: str) -> list[str]:
  """复制内核快照到 app/devkit/kernel/；返回写入路径列表。"""
  app_root = ROOT / app_rel
  bundle_root = app_root / "devkit" / "kernel"
  written: list[str] = []
  for src_rel, dst_rel in BUNDLE_PARTS:
    src = ROOT / src_rel
    dst = bundle_root / dst_rel
    if not src.exists():
      continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.is_dir():
      if dst.exists():
        shutil.rmtree(dst)
      shutil.copytree(src, dst)
    else:
      shutil.copy2(src, dst)
    written.append(str(dst.relative_to(app_root)))
  marker = bundle_root / "BUNDLE_VERSION"
  marker.write_text("devkit_version=1.0.0\n", encoding="utf-8")
  written.append(str(marker.relative_to(app_root)))
  return written


def main() -> int:
  parser = argparse.ArgumentParser(description="Sync DevKit kernel bundle into app profiles")
  parser.add_argument(
    "--app",
    action="append",
    default=["src/apps/web-admin", "src/apps/h5-worker"],
    help="App relative path (repeatable)",
  )
  args = parser.parse_args()
  for app in args.app:
    paths = sync_app(app)
    print(f"Synced {app}: {', '.join(paths)}")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
