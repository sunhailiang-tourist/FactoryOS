#!/usr/bin/env python3
"""Unified SH-步步流 Harness runner (stdlib only).

Usage:
  python scripts/check_harness.py                      # full (CI / Step 停机)
  python scripts/check_harness.py --tier contracts     # L0 契约
  python scripts/check_harness.py --tier boundaries    # L0+L1 模块边界
  python scripts/check_harness.py --tier step          # L0+L1+L2 静态四门
  python scripts/check_harness.py --tier full          # 同 step
  python scripts/check_harness.py --tier auto          # git diff 推断层级
  python scripts/check_harness.py --tier step --pytest -k 'G-01'

Tiers:
  contracts (L0)  — check_openapi_schema_refs · check_cmv_sync
  boundaries (L1) — + check_import_boundaries
  step / full     — + check_code_redundancy（四门全跑）
  auto            — 按改动面选 contracts → boundaries → step；无 diff 时 full

Exit 0 = pass; 1 = failure.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent


def resolve_python() -> str:
  """Prefer project .venv so PyYAML / pytest match pyproject.toml."""
  venv_py = ROOT / ".venv" / "bin" / "python"
  if venv_py.is_file():
    return str(venv_py)
  return sys.executable


PYTHON = resolve_python()

CHECKS: dict[str, tuple[str, str]] = {
    "openapi": ("check_openapi_schema_refs.py", "OpenAPI schema refs"),
    "cmv": ("check_cmv_sync.py", "CMV sync"),
    "import": ("check_import_boundaries.py", "Import boundaries"),
    "kernel_registry": ("check_kernel_registry.py", "os_core kernel registry"),
    "router_registry": ("check_router_registry.py", "api router registry"),
    "integration_registry": ("check_integration_registry.py", "integration GIP registry"),
    "registry_annotations": ("check_registry_annotations.py", "Registry annotations"),
    "legacy_paths": ("check_legacy_paths.py", "legacy path cleanup"),
    "repo_structure": ("check_repo_structure.py", "repo-structure snapshot sync"),
    "structure_change": ("check_structure_change.py", "structure drift gate"),
    "path_consistency": ("audit_path_consistency.py", "docs path consistency"),
    "redundancy": ("check_code_redundancy.py", "Code redundancy"),
}

TIER_ORDER = ("contracts", "boundaries", "step", "full")

TIER_CHECKS: dict[str, list[str]] = {
    "contracts": ["openapi", "cmv"],
    "boundaries": ["openapi", "cmv", "import", "kernel_registry", "router_registry", "integration_registry", "registry_annotations"],
    "step": ["openapi", "cmv", "import", "kernel_registry", "router_registry", "integration_registry", "registry_annotations", "legacy_paths", "repo_structure", "structure_change", "path_consistency", "redundancy"],
    "full": ["openapi", "cmv", "import", "kernel_registry", "router_registry", "integration_registry", "registry_annotations", "legacy_paths", "repo_structure", "structure_change", "path_consistency", "redundancy"],
}

TIER_LABEL: dict[str, str] = {
    "contracts": "L0 · contracts",
    "boundaries": "L1 · boundaries",
    "step": "L2 · step (static harness)",
    "full": "full · step stop / CI",
}


def _tier_rank(tier: str) -> int:
    order = {name: i for i, name in enumerate(TIER_ORDER)}
    return order.get(tier, len(order))


def _max_tier(a: str, b: str) -> str:
    return a if _tier_rank(a) >= _tier_rank(b) else b


def git_changed_paths() -> list[str]:
    """Staged + unstaged + untracked paths (relative to repo root)."""
    paths: set[str] = set()
    cmds = [
        ["git", "diff", "--name-only", "HEAD"],
        ["git", "diff", "--name-only", "--cached"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    ]
    for cmd in cmds:
        try:
            r = subprocess.run(
                cmd,
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            return []
        if r.returncode != 0:
            continue
        for line in r.stdout.splitlines():
            line = line.strip()
            if line:
                paths.add(line.replace("\\", "/"))
    return sorted(paths)


def tier_from_paths(paths: list[str]) -> str:
    if not paths:
        return "full"
    tier = "contracts"
    for p in paths:
        norm = p.replace("\\", "/")
        if norm.startswith("contracts/"):
            tier = _max_tier(tier, "contracts")
        if norm.startswith("src/server/os_core/") or norm.startswith("src/integration/"):
            tier = _max_tier(tier, "boundaries")
        if norm.endswith(".py") and (
            norm.startswith("src/server/os_core/") or norm.startswith("src/server/api/")
        ):
            tier = _max_tier(tier, "step")
    return tier


def resolve_tier(name: str) -> str:
    if name == "auto":
        detected = tier_from_paths(git_changed_paths())
        print(f"Harness auto → tier={detected} ({TIER_LABEL.get(detected, detected)})")
        return detected
    if name in TIER_CHECKS:
        return name
    raise SystemExit(
        f"Unknown tier {name!r}; choose: contracts, boundaries, step, full, auto"
    )


def run_check(key: str) -> int:
    script, label = CHECKS[key]
    path = SCRIPTS / script
    print(f"\n── {label} ({script})")
    r = subprocess.run([PYTHON, str(path)], cwd=ROOT)
    return r.returncode


def run_pytest(k: str, extra: list[str]) -> int:
    cmd = [PYTHON, "-m", "pytest", "-k", k, "-v", *extra]
    print(f"\n── pytest -k {k!r}")
    r = subprocess.run(cmd, cwd=ROOT)
    return r.returncode


def run_harness(tier: str, pytest_k: str | None = None, pytest_extra: list[str] | None = None) -> int:
    resolved = resolve_tier(tier)
    checks = TIER_CHECKS[resolved]
    if PYTHON != sys.executable:
        print(f"Harness python: {PYTHON} (project .venv)")
    print(f"FactoryOS Harness · {TIER_LABEL.get(resolved, resolved)} · {len(checks)} check(s)")
    for key in checks:
        if run_check(key) != 0:
            print(f"\nHarness FAILED at {CHECKS[key][1]}", file=sys.stderr)
            return 1
    if pytest_k:
        if run_pytest(pytest_k, pytest_extra or []) != 0:
            print("\nHarness FAILED at pytest", file=sys.stderr)
            return 1
    print("\nHarness OK")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="FactoryOS unified Harness (SH-步步流 L0–L2 static checks)",
    )
    p.add_argument(
        "--tier",
        "-t",
        default="full",
        choices=["contracts", "boundaries", "step", "full", "auto"],
        help="contracts=L0, boundaries=L1, step/full=L0+L1+L2, auto=git diff",
    )
    p.add_argument(
        "--pytest",
        "-k",
        metavar="EXPR",
        help="L3: run pytest -k EXPR after static checks",
    )
    p.add_argument(
        "pytest_extra",
        nargs="*",
        help="Extra args passed to pytest (e.g. -x)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return run_harness(args.tier, args.pytest, args.pytest_extra)


if __name__ == "__main__":
    sys.exit(main())
