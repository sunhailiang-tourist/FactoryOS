#!/usr/bin/env python3
"""Run ruff + pyright on server/ + src/tests (stdlib launcher).

Usage:
  python scripts/check_static_quality.py
  python scripts/check_static_quality.py --ruff-only

Exit 0 = pass; 1 = violations or tool missing (use --allow-missing for soft gate).
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINT_TARGETS = ["src/server", "src/tests"]


def _collect_py_files() -> list[Path]:
    out: list[Path] = []
    for rel in LINT_TARGETS:
        base = ROOT / rel
        if base.is_dir():
            out.extend(base.rglob("*.py"))
    return out


def run_module(module: str, args: list[str], allow_missing: bool) -> int | None:
    """Return exit code, or None if module missing and allow_missing."""
    r = subprocess.run(
        [sys.executable, "-m", module, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if r.returncode != 0 and "No module named" in (r.stderr or ""):
        if allow_missing:
            return None
        print(f"{module} not installed — uv sync --extra dev", file=sys.stderr)
        return 1
    if r.stdout:
        print(r.stdout, end="")
    if r.stderr:
        print(r.stderr, end="", file=sys.stderr)
    return r.returncode


def main() -> int:
    p = argparse.ArgumentParser(description="Static quality: ruff + pyright")
    p.add_argument("--ruff-only", action="store_true")
    p.add_argument("--allow-missing", action="store_true", help="skip if tools not installed")
    args = p.parse_args()

    if not _collect_py_files():
        print("No Python files under server/ or src/tests — skip")
        return 0

    failed = False
    for module, margs, label in [
        ("ruff", ["check", *LINT_TARGETS], "ruff"),
        *([] if args.ruff_only else [("pyright", LINT_TARGETS, "pyright")]),
    ]:
        print(f"\n── {label}")
        code = run_module(module, margs, args.allow_missing)
        if code is None:
            print(f"  skip {label} (not installed)")
            continue
        if code != 0:
            failed = True

    if failed:
        print("\nStatic quality FAILED", file=sys.stderr)
        return 1
    print("\nStatic quality OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
