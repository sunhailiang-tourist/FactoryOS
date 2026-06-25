#!/usr/bin/env python3
"""Test 单步/终轮回归落盘门禁（stdlib only）。

Usage:
  python scripts/check_test_regression.py --step 1
  python scripts/check_test_regression.py --step 2 --require-pass
  python scripts/check_test_regression.py --final
  python scripts/check_test_regression.py --final --require-pass

模板：
  .cursor/factoryos/templates/test-step-regression-template.md
  .cursor/factoryos/templates/test-final-regression-template.md
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "_factoryos_pipeline"


def find_step_regression(step: int) -> Path | None:
    pattern = f"*/test/test-*-step{step}-regression.md"
    hits = sorted(PIPELINE.glob(pattern), key=lambda p: p.stat().st_mtime)
    return hits[-1] if hits else None


def find_final_regression() -> Path | None:
    pattern = "*/test/test-*-final-regression.md"
    hits = sorted(PIPELINE.glob(pattern), key=lambda p: p.stat().st_mtime)
    return hits[-1] if hits else None


def check_conclusion(path: Path, require_pass: bool) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    if "结论" not in text:
        errors.append(f"{path}: missing 结论 section")
    m = re.search(r"结论[：:]\s*(通过|需改进|阻断|PASS|BLOCK)", text, re.IGNORECASE)
    if not m:
        errors.append(f"{path}: 结论 must be 通过/需改进/阻断")
    elif require_pass and m.group(1) in ("阻断", "BLOCK"):
        errors.append(
            f"{path}: Test 结论={m.group(1)} — 禁止 gate step / delivery / 可以继续"
        )
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="Test step/final regression gate")
    p.add_argument("--step", type=int, help="step number for per-step regression")
    p.add_argument("--final", action="store_true", help="final regression artifact")
    p.add_argument(
        "--require-pass",
        action="store_true",
        help="fail on 阻断",
    )
    args = p.parse_args()

    if args.final:
        tf = find_final_regression()
        if tf is None:
            print(
                "Test final regression MISSING: "
                "_factoryos_pipeline/<date>/test/test-*-final-regression.md",
                file=sys.stderr,
            )
            return 1
        errors = check_conclusion(tf, args.require_pass)
        if errors:
            for e in errors:
                print(e, file=sys.stderr)
            return 1
        print(f"Test final regression OK: {tf.name}")
        return 0

    if args.step is None:
        print("Provide --step N or --final", file=sys.stderr)
        return 1

    sf = find_step_regression(args.step)
    if sf is None:
        print(
            f"Test step regression MISSING: "
            f"_factoryos_pipeline/<date>/test/test-*-step{args.step}-regression.md",
            file=sys.stderr,
        )
        return 1

    errors = check_conclusion(sf, args.require_pass)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1

    print(f"Test step regression OK: {sf.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
