#!/usr/bin/env python3
"""Harness 微评测 CLI（L4 · P0）。

Usage:
  python scripts/check_harness_eval.py
  python scripts/check_harness_eval.py --case HE-01 --case HE-07
  ./scripts/gate harness-eval

Exit 0 = 全部黄金题符合预期；1 = 有回退。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
  sys.path.insert(0, str(SCRIPTS))

import harness_eval_lib as hel  # noqa: E402


def main() -> int:
  p = argparse.ArgumentParser(description="FactoryOS harness-eval（10 题冻结集）")
  p.add_argument("--case", action="append", dest="cases", help="仅跑指定 HE-ID（可重复）")
  p.add_argument("--list", action="store_true", help="列出题目后退出")
  args = p.parse_args()

  if args.list:
    for c in hel.CASES:
      print(f"{c.id}\t{'FAIL' if c.expect_errors else 'PASS'}\t{c.taxonomy}\t{c.name}")
    return 0

  case_ids = set(args.cases) if args.cases else None
  if case_ids:
    known = {c.id for c in hel.CASES}
    unknown = case_ids - known
    if unknown:
      print(f"未知 HE-ID: {sorted(unknown)}", file=sys.stderr)
      return 1

  results = hel.run_all(case_ids=case_ids)
  failed = [r for r in results if not r.ok]
  for r in results:
    mark = "OK" if r.ok else "FAIL"
    print(f"[{mark}] {r.id} {r.name} (expect_errors={r.expect_errors}) — {r.detail}")
  print()
  print(hel.summary_line(results))
  if failed:
    print("\n回退题（须修 harness 而非跳过）：", file=sys.stderr)
    for r in failed:
      print(f"  {r.id} [{r.taxonomy}] {r.detail}", file=sys.stderr)
    return 1
  print("Gate harness-eval OK")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
