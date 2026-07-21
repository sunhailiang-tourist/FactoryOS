#!/usr/bin/env python3
"""Harness 熵清理（L4 · P2）只读扫描。

作用：发现死链、废止路径引用、过期 draft plan、税则镜像漂移。
业务关联：OpenAI 式 GC agent 的轻量版；默认报告，--strict 时有 critical 则 exit 1。
上游：./scripts/gate harness-gc · 人工周更
下游：人工清文档 / 回灌 PR
关联文档：FAILURE-TAXONOMY.md · FT-HARNESS-DRIFT
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACTORYOS = ROOT / ".cursor" / "factoryos"
PIPELINE = ROOT / "_factoryos_pipeline"
DEAD_REF_PATTERNS = (
  r"(?<![\w./-])rules/coder-expert-workflow",
  r"coder-expert-workflow\.mdc",
  # 仅拦仓库根 rules/（已废止），勿误伤 .cursor/rules/
  r"(?<!\.cursor/)(?<![\w-])rules/factoryos",
)


def scan_dead_refs() -> list[str]:
  """扫描 .cursor 下对已废止路径的引用。"""
  hits: list[str] = []
  roots = [ROOT / ".cursor", ROOT / "scripts"]
  for base in roots:
    if not base.is_dir():
      continue
    for path in base.rglob("*"):
      if not path.is_file():
        continue
      if path.suffix not in {".md", ".mdc", ".py", ".json", ".yml", ".yaml"}:
        continue
      if "node_modules" in path.parts or "__pycache__" in path.parts:
        continue
      try:
        text = path.read_text(encoding="utf-8")
      except OSError:
        continue
      for pat in DEAD_REF_PATTERNS:
        if re.search(pat, text):
          # 允许在 HARNESS-EVAL / 本脚本 / FAILURE 中作为反例提及
          rel = str(path.relative_to(ROOT))
          if any(
            x in rel
            for x in (
              "harness_gc.py",
              "HARNESS-EVAL.md",
              "FAILURE-TAXONOMY.md",
            )
          ):
            continue
          hits.append(f"死链引用 {pat} → {rel}")
          break
  return hits


def scan_stale_drafts(*, days: int = 14) -> list[str]:
  """过期 *draft* plan 警告。"""
  warnings: list[str] = []
  now = datetime.now(timezone.utc).timestamp()
  cutoff = days * 86400
  for p in PIPELINE.glob("*/plan/*draft*"):
    if not p.is_file():
      continue
    age = now - p.stat().st_mtime
    if age > cutoff:
      warnings.append(
        f"过期 draft（>{days}d）：{p.relative_to(ROOT)} — 确认后删除或归档"
      )
  return warnings


def scan_taxonomy_mirror() -> list[str]:
  """税则 MD 与代码表对账。"""
  sys.path.insert(0, str(ROOT / "scripts"))
  import failure_taxonomy_lib as ftl

  return ftl.validate_taxonomy_integrity()


def main() -> int:
  p = argparse.ArgumentParser(description="FactoryOS harness GC（只读）")
  p.add_argument("--strict", action="store_true", help="有 critical 则 exit 1")
  p.add_argument("--draft-days", type=int, default=14)
  args = p.parse_args()

  critical: list[str] = []
  warnings: list[str] = []
  critical.extend(scan_dead_refs())
  critical.extend(scan_taxonomy_mirror())
  warnings.extend(scan_stale_drafts(days=args.draft_days))

  for w in warnings:
    print(f"WARN  {w}")
  for c in critical:
    print(f"CRIT  {c}", file=sys.stderr if args.strict else sys.stdout)

  print(
    f"\nharness-gc: {len(critical)} critical, {len(warnings)} warnings"
  )
  if args.strict and critical:
    return 1
  print("Gate harness-gc OK" if not critical else "Gate harness-gc DONE (has findings)")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
