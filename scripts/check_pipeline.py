#!/usr/bin/env python3
"""Validate SH-步步流 pipeline artifacts and workflow_state (stdlib only).

Usage:
  python scripts/check_pipeline.py --gate plan
  python scripts/check_pipeline.py --gate test
  python scripts/check_pipeline.py --gate step --step 1
  python scripts/check_pipeline.py --gate state

Exit 0 = artifacts present; 1 = missing required files.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "_factoryos_pipeline"
STATE_FILE = PIPELINE / "workflow_state.md"
PLAN_GATE = PIPELINE / ".gates" / "plan.ok"

VALID_PHASES = frozenset({"STEP0", "PLANNING", "CAN_TEST", "CAN_CODE", "DELIVERY"})


def read_state() -> dict[str, str]:
    if not STATE_FILE.is_file():
        return {}
    text = STATE_FILE.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for key in ("phase", "agent", "step", "plan", "test_plan"):
        m = re.search(rf"^{key}:\s*(\S+)", text, re.MULTILINE)
        if m:
            out[key] = m.group(1)
    return out


def today_dir() -> Path:
    return PIPELINE / date.today().isoformat()


def glob_any(pattern: str) -> list[Path]:
    return sorted(PIPELINE.glob(pattern))


def check_gate_plan() -> list[str]:
    errors: list[str] = []
    plans = glob_any("*/plan/plan-*.md")
    if not plans:
        errors.append("missing plan: _factoryos_pipeline/<date>/plan/plan-*.md")
    state = read_state()
    if state.get("phase") == "STEP0":
        errors.append("workflow_state phase still STEP0 — need 可以继续 → PLANNING")
    return errors


def check_gate_test() -> list[str]:
    errors: list[str] = []
    if not PLAN_GATE.is_file():
        errors.append("missing plan.ok — run ./scripts/gate plan after 确认规划")
    tests = glob_any("*/test/test-*.md")
    if not tests:
        errors.append("missing test-plan: _factoryos_pipeline/<date>/test/test-*.md")
    state = read_state()
    phase = state.get("phase", "STEP0")
    if phase not in ("CAN_TEST", "CAN_CODE", "DELIVERY"):
        errors.append(f"phase={phase} — need 确认规划 → CAN_TEST before test-plan")
    return errors


def check_gate_step(step: int) -> list[str]:
    errors: list[str] = []
    pattern = f"*/step-stop/step-stop-*-step{step}.md"
    stops = glob_any(pattern)
    if not stops:
        errors.append(f"missing step-stop for step {step}: {pattern}")
    test_pattern = f"*/test/test-*-step{step}-regression.md"
    if not glob_any(test_pattern):
        errors.append(
            f"missing Test step regression for step {step}: {test_pattern} "
            f"(【Test·Step {step} 验收】落盘)"
        )
    verify_pattern = f"*/verify/verify-*-step{step}.md"
    if not glob_any(verify_pattern):
        errors.append(f"missing verify for step {step}: {verify_pattern}")
    state = read_state()
    if state.get("phase") != "CAN_CODE":
        errors.append("phase must be CAN_CODE for step-stop (用户 可以开始 后)")
    return errors


def check_gate_delivery() -> list[str]:
    errors: list[str] = []
    final_pattern = "*/test/test-*-final-regression.md"
    if not glob_any(final_pattern):
        errors.append(
            "missing Test final regression: */test/test-*-final-regression.md "
            "(【Test·终轮回归】落盘)"
        )
    summaries = glob_any("*/summary/change-summary-*.md")
    if not summaries:
        errors.append("missing change-summary: */summary/change-summary-*.md")
    state = read_state()
    if state.get("phase") != "DELIVERY":
        errors.append("phase must be DELIVERY before gate delivery / commit")
    return errors


def check_gate_state() -> list[str]:
    errors: list[str] = []
    if not STATE_FILE.is_file():
        errors.append(f"missing {STATE_FILE}")
        return errors
    state = read_state()
    phase = state.get("phase")
    if phase not in VALID_PHASES:
        errors.append(f"invalid phase={phase!r}; allowed: {sorted(VALID_PHASES)}")
    agent = state.get("agent", "dev")
    if agent not in ("dev", "test"):
        errors.append(f"invalid agent={agent!r}")
    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="Pipeline artifact gates")
    p.add_argument(
        "--gate",
        required=True,
        choices=["plan", "test", "step", "delivery", "state", "all"],
    )
    p.add_argument("--step", type=int, default=1, help="for --gate step")
    args = p.parse_args()

    errors: list[str] = []
    if args.gate in ("plan", "all"):
        errors.extend(check_gate_plan())
    if args.gate in ("test", "all"):
        errors.extend(check_gate_test())
    if args.gate in ("step", "all"):
        errors.extend(check_gate_step(args.step))
    if args.gate in ("delivery", "all"):
        errors.extend(check_gate_delivery())
    if args.gate in ("state", "all"):
        errors.extend(check_gate_state())

    if errors:
        print("Pipeline check FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(f"Pipeline OK (gate={args.gate})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
