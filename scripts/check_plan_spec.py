#!/usr/bin/env python3
"""Validate Dev plan markdown against contracts/ (analyze 门 · stdlib only).

Usage:
  python scripts/check_plan_spec.py
  python scripts/check_plan_spec.py --plan _factoryos_pipeline/2026-06-16/plan/plan-1200-w1.md

Exit 0 = AC IDs and HTTP paths in plan are backed by contracts; 1 = gaps.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "_factoryos_pipeline"
ACCEPTANCE_DIR = ROOT / "contracts" / "acceptance"
OPENAPI = ROOT / "contracts" / "openapi" / "工厂操作系统-v1.1.yaml"

AC_RE = re.compile(r"\b([A-Z]-\d{2})\b")
HTTP_RE = re.compile(
    r"\b(GET|POST|PUT|PATCH|DELETE)\s+(/v1/[A-Za-z0-9_./{}-]+)",
    re.IGNORECASE,
)


def latest_plan() -> Path | None:
    candidates = sorted(PIPELINE.glob("*/plan/plan-*.md"), key=lambda p: p.stat().st_mtime)
    return candidates[-1] if candidates else None


def load_acceptance_text() -> str:
    parts: list[str] = []
    if ACCEPTANCE_DIR.is_dir():
        for p in sorted(ACCEPTANCE_DIR.glob("*.md")):
            parts.append(p.read_text(encoding="utf-8"))
    return "\n".join(parts)


def load_openapi_text() -> str:
    if not OPENAPI.is_file():
        return ""
    return OPENAPI.read_text(encoding="utf-8")


def check_plan(path: Path) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    ac_ids = sorted(set(AC_RE.findall(text)))
    http_ops = sorted(set(HTTP_RE.findall(text)))

    if not ac_ids:
        errors.append(f"{path}: no AC IDs found (expect G-01, E-03, …)")
        return errors

    acceptance = load_acceptance_text()
    openapi = load_openapi_text()

    for ac_id in ac_ids:
        if ac_id not in acceptance:
            errors.append(f"{path}: AC {ac_id} not found in contracts/acceptance/")

    for method, api_path in http_ops:
        norm_path = api_path.split("{")[0].rstrip("/")
        if norm_path and norm_path not in openapi:
            errors.append(
                f"{path}: {method.upper()} {api_path} not found in contracts/openapi"
            )

    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="Plan ↔ contracts consistency check")
    p.add_argument("--plan", type=Path, help="plan markdown path (default: latest in pipeline)")
    args = p.parse_args()

    plan = args.plan or latest_plan()
    if plan is None or not plan.is_file():
        print("No plan file found under _factoryos_pipeline/*/plan/", file=sys.stderr)
        return 1

    errors = check_plan(plan.resolve())
    if errors:
        print("Plan/spec mismatches:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(f"Plan/spec OK: {plan.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
