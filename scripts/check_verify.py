#!/usr/bin/env python3
"""Verify 回合门禁：Step 须 Test 通过后落盘（plan 目录隔离 · 联动链）。

Usage:
  python scripts/check_verify.py --step 1
  python scripts/check_verify.py --step 2 --require-pass
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
  p = argparse.ArgumentParser(description="Verify round gate")
  p.add_argument("--step", type=int, required=True)
  p.add_argument("--require-pass", action="store_true", help="fail on 阻断")
  args = p.parse_args()

  plan_errors = plan_gate_lib.validate_plan_confirmed(require_phase_min="CAN_TEST")
  if plan_errors:
    print("Verify gate FAILED:", file=sys.stderr)
    for e in plan_errors:
      print(f"  {e}", file=sys.stderr)
    return 1

  test_errors = step_chain_lib.validate_step_test_done(
    args.step,
    require_pass=True,
  )
  if test_errors:
    print("Verify gate FAILED (Test 未通过):", file=sys.stderr)
    for e in test_errors:
      print(f"  {e}", file=sys.stderr)
    return 1

  vf = step_chain_lib.find_verify(args.step)
  if vf is None:
    plan_dir = step_chain_lib.plan_pipeline_dir()
    hint = plan_dir.name if plan_dir else "<date>"
    print(
      f"Verify MISSING: _factoryos_pipeline/{hint}/verify/verify-*-step{args.step}.md",
      file=sys.stderr,
    )
    return 1

  errors = step_chain_lib.check_conclusion(vf, require_pass=args.require_pass)
  if errors:
    for e in errors:
      print(e, file=sys.stderr)
    return 1

  print(f"Verify OK: {vf.name}")
  return 0


if __name__ == "__main__":
  sys.exit(main())
