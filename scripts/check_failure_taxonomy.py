#!/usr/bin/env python3
"""失败税则 CLI：归类 + 生成回灌草稿。

Usage:
  python scripts/check_failure_taxonomy.py --validate
  python scripts/check_failure_taxonomy.py --classify - <<EOF
  ...失败日志...
  EOF
  python scripts/check_failure_taxonomy.py --codes FT-PLAN-UI FT-VERIFY-BLOCK
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
if str(SCRIPTS) not in sys.path:
  sys.path.insert(0, str(SCRIPTS))

import failure_taxonomy_lib as ftl  # noqa: E402


def main() -> int:
  p = argparse.ArgumentParser(description="FactoryOS 失败税则")
  p.add_argument("--validate", action="store_true", help="校验税则完整性")
  p.add_argument("--classify", action="store_true", help="从 stdin 启发式归类")
  p.add_argument("--codes", nargs="*", help="按码生成回灌草稿")
  p.add_argument("--list", action="store_true", help="列出全部税则")
  args = p.parse_args()

  if args.list:
    for e in ftl.all_entries():
      print(f"{e.code}\t{e.summary}")
    return 0

  if args.validate:
    errs = ftl.validate_taxonomy_integrity()
    if errs:
      for e in errs:
        print(e, file=sys.stderr)
      return 1
    print(f"failure-taxonomy OK ({len(ftl.TAXONOMY)} codes)")
    return 0

  if args.classify:
    text = sys.stdin.read()
    codes = ftl.classify_from_text(text)
    print(",".join(codes) if codes else "(none)")
    print()
    print(ftl.format_feedback_stub(codes, evidence=text[:500]))
    return 0

  if args.codes is not None:
    print(ftl.format_feedback_stub(list(args.codes)))
    return 0

  p.print_help()
  return 2


if __name__ == "__main__":
  raise SystemExit(main())
