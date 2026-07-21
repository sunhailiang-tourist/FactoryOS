#!/usr/bin/env python3
"""WEB harness-eval CLI。"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import web_harness_eval_lib as hel  # noqa: E402


def main() -> int:
  p = argparse.ArgumentParser()
  p.add_argument("--case", action="append", dest="cases")
  p.add_argument("--list", action="store_true")
  args = p.parse_args()
  if args.list:
    for c in hel.CASES:
      print(f"{c.id}\t{c.name}")
    return 0
  ids = set(args.cases) if args.cases else None
  results = hel.run_all(case_ids=ids)
  failed = [r for r in results if not r.ok]
  for r in results:
    print(f"[{'OK' if r.ok else 'FAIL'}] {r.id} {r.name} — {r.detail}")
  print(f"\nweb harness-eval {sum(1 for r in results if r.ok)}/{len(results)} passed")
  if failed:
    return 1
  print("Gate web harness-eval OK")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
