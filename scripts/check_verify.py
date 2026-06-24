#!/usr/bin/env python3
"""Verify 回合门禁：Step 停机须有独立 verify 落盘（stdlib only）。

Usage:
  python scripts/check_verify.py --step 1
  python scripts/check_verify.py --step 2 --require-pass

Fresh-agent Verify 模板：.cursor/factoryos/templates/verify-template.md
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "_factoryos_pipeline"


def find_verify(step: int) -> Path | None:
    pattern = f"*/verify/verify-*-step{step}.md"
    hits = sorted(PIPELINE.glob(pattern), key=lambda p: p.stat().st_mtime)
    return hits[-1] if hits else None


def check_verify(path: Path, require_pass: bool) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if "结论" not in text and "conclusion" not in text.lower():
        errors.append(f"{path}: missing 结论 section")
    m = re.search(r"结论[：:]\s*(通过|需改进|阻断|PASS|BLOCK)", text, re.IGNORECASE)
    if not m:
        errors.append(f"{path}: 结论 must be 通过/需改进/阻断")
    elif require_pass and m.group(1) in ("阻断", "BLOCK"):
        errors.append(f"{path}: Verify 阻断 — 禁止停机/PR")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="Verify round gate")
    p.add_argument("--step", type=int, required=True)
    p.add_argument("--require-pass", action="store_true", help="fail on 阻断")
    args = p.parse_args()

    vf = find_verify(args.step)
    if vf is None:
        print(
            f"Verify MISSING: _factoryos_pipeline/<date>/verify/verify-*-step{args.step}.md",
            file=sys.stderr,
        )
        return 1

    errors = check_verify(vf, args.require_pass)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1

    print(f"Verify OK: {vf.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
