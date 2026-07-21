#!/usr/bin/env python3
"""WEB harness GC：死链 / 过期 draft / 税则镜像。"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
PIPELINE = APP_ROOT / "_web_pipeline"
CURSOR = APP_ROOT / ".cursor"


def scan_stale_drafts(*, days: int = 14) -> list[str]:
  warnings: list[str] = []
  now = datetime.now(timezone.utc).timestamp()
  for p in PIPELINE.glob("*/plan/*draft*"):
    if p.is_file() and now - p.stat().st_mtime > days * 86400:
      warnings.append(f"过期 draft：{p.relative_to(APP_ROOT)}")
  return warnings


def scan_dead_refs() -> list[str]:
  hits: list[str] = []
  for path in CURSOR.rglob("*"):
    if not path.is_file() or path.suffix not in {".md", ".mdc"}:
      continue
    text = path.read_text(encoding="utf-8", errors="ignore")
    if re.search(r"(?<!\.cursor/)(?<![\w-])_factoryos_pipeline/", text):
      # WEB 文档不应把落盘指到后端 pipeline（允许「禁止」叙述）
      if "禁止" in text and "_factoryos_pipeline" in text:
        continue
      if "切割" in text or "不用" in text:
        continue
      hits.append(f"可疑后端 pipeline 引用 → {path.relative_to(APP_ROOT)}")
  return hits


def main() -> int:
  p = argparse.ArgumentParser()
  p.add_argument("--strict", action="store_true")
  args = p.parse_args()
  sys.path.insert(0, str(APP_ROOT / "scripts"))
  import web_failure_taxonomy_lib as wftl

  critical = wftl.validate_taxonomy_integrity() + scan_dead_refs()
  warnings = scan_stale_drafts()
  for w in warnings:
    print(f"WARN  {w}")
  for c in critical:
    print(f"CRIT  {c}")
  print(f"\nweb harness-gc: {len(critical)} critical, {len(warnings)} warnings")
  if args.strict and critical:
    return 1
  print("Gate web harness-gc OK" if not critical else "DONE (has findings)")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
