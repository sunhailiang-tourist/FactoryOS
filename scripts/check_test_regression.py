#!/usr/bin/env python3
"""Test 单步/终轮回归落盘门禁（stdlib only · plan 目录隔离 · Dev 联动）。

Usage:
  python scripts/check_test_regression.py --step 1
  python scripts/check_test_regression.py --step 2 --require-pass
  python scripts/check_test_regression.py --final
  python scripts/check_test_regression.py --final --require-pass
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import plan_gate_lib  # noqa: E402
import step_chain_lib  # noqa: E402


def main() -> int:
  p = argparse.ArgumentParser(description="Test step/final regression gate")
  p.add_argument("--step", type=int, help="step number for per-step regression")
  p.add_argument("--final", action="store_true", help="final regression artifact")
  p.add_argument("--require-pass", action="store_true", help="fail on 阻断")
  args = p.parse_args()

  plan_errors = plan_gate_lib.validate_plan_confirmed(require_phase_min="CAN_TEST")
  if plan_errors:
    print("Test regression gate FAILED:", file=sys.stderr)
    for e in plan_errors:
      print(f"  {e}", file=sys.stderr)
    return 1

  if args.final:
    tf = step_chain_lib.find_final_regression()
    if tf is None:
      plan_dir = step_chain_lib.plan_pipeline_dir()
      hint = plan_dir.name if plan_dir else "<date>"
      print(
        f"Test final regression MISSING: "
        f"_factoryos_pipeline/{hint}/test/test-*-final-regression.md",
        file=sys.stderr,
      )
      return 1
    errors = step_chain_lib.check_conclusion(tf, require_pass=args.require_pass)
    if errors:
      for e in errors:
        print(e, file=sys.stderr)
      return 1
    print(f"Test final regression OK: {tf.name}")
    return 0

  if args.step is None:
    print("Provide --step N or --final", file=sys.stderr)
    return 1

  dev_errors = step_chain_lib.validate_step_dev_done(args.step)
  if dev_errors:
    print("Test regression gate FAILED (Dev 未停机):", file=sys.stderr)
    for e in dev_errors:
      print(f"  {e}", file=sys.stderr)
    return 1

  sf = step_chain_lib.find_test_regression(args.step)
  if sf is None:
    plan_dir = step_chain_lib.plan_pipeline_dir()
    hint = plan_dir.name if plan_dir else "<date>"
    print(
      f"Test step regression MISSING: "
      f"_factoryos_pipeline/{hint}/test/test-*-step{args.step}-regression.md",
      file=sys.stderr,
    )
    return 1

  errors = step_chain_lib.check_conclusion(sf, require_pass=args.require_pass)
  if errors:
    for e in errors:
      print(e, file=sys.stderr)
    return 1

  print(f"Test step regression OK: {sf.name}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
