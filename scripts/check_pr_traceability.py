#!/usr/bin/env python3
"""PR 追溯门禁：body 须含 plan 路径与 AC ID（stdlib only）。

Usage:
  echo "$PR_BODY" | python scripts/check_pr_traceability.py
  python scripts/check_pr_traceability.py --body-file /tmp/pr.md

CI: GitHub Actions 注入 github.event.pull_request.body
"""
from __future__ import annotations

import argparse
import re
import sys

PLAN_RE = re.compile(r"_factoryos_pipeline/[^\s)]+\/plan/plan-[^\s)]+\.md")
AC_RE = re.compile(r"\b[A-Z]-\d{2}\b")


def main() -> int:
    p = argparse.ArgumentParser(description="PR traceability gate")
    p.add_argument("--body-file", type=argparse.FileType("r", encoding="utf-8"))
    p.add_argument("--stdin", action="store_true", default=True)
    args = p.parse_args()

    if args.body_file:
        body = args.body_file.read()
    else:
        body = sys.stdin.read()

    errors: list[str] = []
    if not PLAN_RE.search(body):
        errors.append("PR body missing plan path: _factoryos_pipeline/.../plan/plan-*.md")
    if not AC_RE.search(body):
        errors.append("PR body missing AC ID (e.g. G-01, E-03)")

    if errors:
        print("PR traceability FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        print("\nSee .github/pull_request_template.md", file=sys.stderr)
        return 1

    print("PR traceability OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
