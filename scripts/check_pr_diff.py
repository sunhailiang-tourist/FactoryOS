#!/usr/bin/env python3
"""PR diff 门禁：业务改动须伴随 tests；Test 专 PR 不得改业务（stdlib only）。

Usage:
  python scripts/check_pr_diff.py --base origin/main

Exit 0 = pass; 1 = policy violation.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BUSINESS_PREFIXES = ("src/server/os_core/", "src/server/api/")
TEST_PREFIX = "src/tests/"


def changed_files(base: str) -> list[str]:
    r = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        r2 = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        raw = r2.stdout
    else:
        raw = r.stdout
    return [ln.strip().replace("\\", "/") for ln in raw.splitlines() if ln.strip()]


def main() -> int:
    p = argparse.ArgumentParser(description="PR diff policy")
    p.add_argument("--base", default="origin/main")
    p.add_argument("--test-only-title", help="PR title prefix meaning Test-only, e.g. [Test]")
    args = p.parse_args()

    files = changed_files(args.base)
    if not files:
        print("PR diff OK (no changes)")
        return 0

    business = [f for f in files if f.startswith(BUSINESS_PREFIXES) and f.endswith(".py")]
    tests = [f for f in files if f.startswith(TEST_PREFIX)]
    only_tests = bool(files) and not business and bool(tests)

    errors: list[str] = []
    if business and not tests:
        errors.append(
            "business .py changed without src/tests/ changes — add/regress tests or split PR"
        )

    title_flag = (args.test_only_title or "").strip()
    if title_flag and business:
        errors.append(f"title indicates Test-only ({title_flag}) but business .py changed")

    if errors:
        print("PR diff policy FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    kind = "test-only" if only_tests else "dev"
    print(f"PR diff OK ({kind}, {len(files)} files)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
