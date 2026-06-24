#!/usr/bin/env python3
"""SH-步步流统一 Gate CLI — T4.5 Spec×Harness×Verify×静态质量。

Usage:
  python scripts/gate_cli.py plan [--plan P]     # 确认规划 + 写 plan.ok 闸门
  python scripts/gate_cli.py test
  python scripts/gate_cli.py step [-k AC] [--step N]  # 停机：harness+pytest+静态+verify
  python scripts/gate_cli.py verify --step N
  python scripts/gate_cli.py pr                  # PR 全量验收盘
  python scripts/gate_cli.py gate0
  python scripts/gate_cli.py analyze [--plan P]
  python scripts/gate_cli.py docs-sync           # docs 基线分级门禁
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
PIPELINE = ROOT / "_factoryos_pipeline"
PLAN_GATE = PIPELINE / ".gates" / "plan.ok"


def run(cmd: list[str]) -> int:
    print(f"\n▶ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=ROOT).returncode


def pytest_available() -> bool:
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "--version"],
        cwd=ROOT,
        capture_output=True,
    )
    return r.returncode == 0


def write_plan_gate(plan: Path | None) -> None:
    PLAN_GATE.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    plan_line = str(plan) if plan else "latest"
    PLAN_GATE.write_text(f"plan={plan_line}\nat={ts}\n", encoding="utf-8")
    print(f"Wrote {PLAN_GATE.relative_to(ROOT)}")


def run_static_quality() -> int:
    return run([sys.executable, str(SCRIPTS / "check_static_quality.py")])


def run_contract_workflow_pytest(*, exclude_pending: bool) -> int:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "src/tests/contract",
        "src/tests/workflow",
        "-v",
        "--tb=short",
    ]
    if exclude_pending:
        cmd.extend(["-m", "not pending"])
    return run(cmd)


def gate_plan(plan: Path | None) -> int:
    if run([sys.executable, str(SCRIPTS / "check_harness.py"), "--tier", "contracts"]) != 0:
        return 1
    cmd = [sys.executable, str(SCRIPTS / "check_plan_spec.py")]
    if plan:
        cmd.extend(["--plan", str(plan)])
    if run(cmd) != 0:
        return 1
    if run([sys.executable, str(SCRIPTS / "check_pipeline.py"), "--gate", "plan"]) != 0:
        return 1
    write_plan_gate(plan)
    print("\nGate plan OK (analyze passed · plan.ok stamped)")
    return 0


def gate_test() -> int:
    if not PLAN_GATE.is_file():
        print("Missing plan.ok — run ./scripts/gate plan first", file=sys.stderr)
        return 1
    if run([sys.executable, str(SCRIPTS / "check_pipeline.py"), "--gate", "test"]) != 0:
        return 1
    print("\nGate test OK")
    return 0


def gate_verify(step: int, require_pass: bool) -> int:
    cmd = [sys.executable, str(SCRIPTS / "check_verify.py"), "--step", str(step)]
    if require_pass:
        cmd.append("--require-pass")
    if run(cmd) != 0:
        return 1
    print("\nGate verify OK")
    return 0


def gate_step(pytest_k: str | None, extra: list[str], step: int) -> int:
    cmd = [sys.executable, str(SCRIPTS / "check_harness.py"), "--tier", "full"]
    if pytest_k:
        cmd.extend(["--pytest", pytest_k, *extra])
    elif extra:
        cmd.extend(extra)
    if run(cmd) != 0:
        return 1
    if not pytest_k and pytest_available():
        if run_contract_workflow_pytest(exclude_pending=True) != 0:
            return 1
    if run_static_quality() != 0:
        return 1
    if gate_verify(step, require_pass=True) != 0:
        return 1
    if run([sys.executable, str(SCRIPTS / "check_pipeline.py"), "--gate", "step", "--step", str(step)]) != 0:
        return 1
    print("\nGate step OK (harness · pytest · static · verify)")
    return 0


def gate_pr() -> int:
    if run([sys.executable, str(SCRIPTS / "check_harness.py"), "--tier", "full"]) != 0:
        return 1
    if run([sys.executable, str(SCRIPTS / "check_pipeline.py"), "--gate", "state"]) != 0:
        return 1
    if not pytest_available():
        print("⚠ pytest missing — uv sync --extra dev", file=sys.stderr)
        return 1
    if run_contract_workflow_pytest(exclude_pending=False) != 0:
        return 1
    if run_static_quality() != 0:
        return 1
    print("\nGate pr OK (T4.5 full)")
    return 0


def gate_gate0() -> int:
    if run([sys.executable, str(SCRIPTS / "check_harness.py"), "--tier", "full"]) != 0:
        return 1
    if not pytest_available():
        print("⚠ pytest missing — uv sync --extra dev", file=sys.stderr)
        return 1
    if run_contract_workflow_pytest(exclude_pending=True) != 0:
        return 1
    if run_static_quality() != 0:
        return 1
    # 52 P0 全绿后启用：uv run pytest -v
    print("\nGate gate0 prep OK (enable full pytest in CI when AC suite green)")
    return 0


def gate_docs_sync() -> int:
    return run([sys.executable, str(SCRIPTS / "docs_baseline.py"), "gate"])


def gate_analyze(plan: Path | None) -> int:
    cmd = [sys.executable, str(SCRIPTS / "check_plan_spec.py")]
    if plan:
        cmd.extend(["--plan", str(plan)])
    return run(cmd)


def main() -> int:
    p = argparse.ArgumentParser(description="FactoryOS Gate CLI (T4.5)")
    sub = p.add_subparsers(dest="gate", required=True)

    sp = sub.add_parser("plan", help="确认规划 + analyze + plan.ok")
    sp.add_argument("--plan", type=Path)

    sub.add_parser("test", help="test-plan 节点")

    ss = sub.add_parser("step", help="Step 停机全量")
    ss.add_argument("-k", "--pytest", metavar="EXPR")
    ss.add_argument("--step", type=int, default=1)
    ss.add_argument("pytest_extra", nargs="*")

    sv = sub.add_parser("verify", help="Verify 回合检查")
    sv.add_argument("--step", type=int, required=True)
    sv.add_argument("--require-pass", action="store_true", default=True)

    sub.add_parser("pr", help="PR 验收盘")
    sub.add_parser("gate0", help="Gate 0")

    sub.add_parser("docs-sync", help="docs 认知基线分级门禁")

    sa = sub.add_parser("analyze", help="plan↔contracts")
    sa.add_argument("--plan", type=Path)

    args = p.parse_args()

    if args.gate == "plan":
        return gate_plan(args.plan)
    if args.gate == "test":
        return gate_test()
    if args.gate == "step":
        return gate_step(getattr(args, "pytest", None), args.pytest_extra, args.step)
    if args.gate == "verify":
        return gate_verify(args.step, args.require_pass)
    if args.gate == "pr":
        return gate_pr()
    if args.gate == "gate0":
        return gate_gate0()
    if args.gate == "docs-sync":
        return gate_docs_sync()
    if args.gate == "analyze":
        return 0 if gate_analyze(args.plan) == 0 else 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
