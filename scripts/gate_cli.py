#!/usr/bin/env python3
"""SH-步步流统一 Gate CLI — T4.5 Spec×Harness×Verify×静态质量。

Usage:
  python scripts/gate_cli.py materials [--materials P | --na --reason R]
  python scripts/gate_cli.py plan [--plan P]     # 确认规划 + 写 plan.ok（须先 materials.ok）
  python scripts/gate_cli.py test                # test-plan + 写 test.ok
  python scripts/gate_cli.py start --step N      # 可以开始 + 写 code.ok
  python scripts/gate_cli.py step [-k AC] [--step N]  # 停机：harness+pytest+静态+verify
  python scripts/gate_cli.py verify --step N
  python scripts/gate_cli.py delivery            # 终轮回归验收盘（commit 前）
  python scripts/gate_cli.py pr                  # PR 验收盘（含 deptry）
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

from pipeline_artifacts import write_artifact

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
PIPELINE = ROOT / "_factoryos_pipeline"
PLAN_GATE = PIPELINE / ".gates" / "plan.ok"
MATERIALS_GATE = PIPELINE / ".gates" / "materials.ok"


def run(cmd: list[str]) -> int:
    print(f"\n▶ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=ROOT).returncode


def run_logged(*, bucket: str, stem: str, cmd: list[str]) -> int:
    """运行命令并强制落盘输出（dev/test/verify）。

    功能/业务含义：
    - gate 的“结论/证据”必须落到 `_factoryos_pipeline/<date>/<bucket>/HH-MM_*.md`，
      让使用者只关注当天目录即可复盘。

    上游调用方：
    - `gate_plan/gate_test/gate_step/gate_verify/gate_pr/...`

    下游被调方：
    - `scripts/pipeline_artifacts.write_artifact`
    """

    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    print(f"\n▶ {' '.join(cmd)}")
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    finished = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    stdout = (p.stdout or "").rstrip()
    stderr = (p.stderr or "").rstrip()
    body = "\n".join(
        [
            f"# Gate 结论：`{stem}`",
            "",
            f"- 时间(UTC): {started} → {finished}",
            f"- exit_code: {p.returncode}",
            f"- cmd: `{' '.join(cmd)}`",
            "",
            "## stdout",
            "```text",
            stdout,
            "```",
            "",
            "## stderr",
            "```text",
            stderr,
            "```",
            "",
        ]
    )
    ref = write_artifact(bucket=bucket, stem=stem, content=body)
    print(f"Wrote {ref.relpath}")

    if p.returncode != 0:
        # 失败时把 stderr 尾部再提示一次，减少来回翻文件成本
        tail = "\n".join(stderr.splitlines()[-40:]) if stderr else ""
        if tail:
            print("\n--- stderr (tail) ---", file=sys.stderr)
            print(tail, file=sys.stderr)
    return p.returncode


def pytest_available() -> bool:
    r = subprocess.run(
        [sys.executable, "-m", "pytest", "--version"],
        cwd=ROOT,
        capture_output=True,
    )
    return r.returncode == 0


def write_materials_gate(
    *,
    materials: Path | None,
    na: bool,
    reason: str,
) -> None:
    """写入 materials.ok。"""
    sys.path.insert(0, str(SCRIPTS))
    import plan_gate_lib

    if na:
        plan_gate_lib.write_materials_gate_stamp(mode="na", reason=reason)
        print(f"Wrote {MATERIALS_GATE.relative_to(ROOT)} (mode=na)")
        return
    assert materials is not None
    try:
        rel = materials.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        rel = str(materials)
    plan_gate_lib.write_materials_gate_stamp(materials_rel=rel, mode="file")
    print(f"Wrote {MATERIALS_GATE.relative_to(ROOT)} (materials={rel})")


def write_plan_gate(plan: Path | None) -> None:
    sys.path.insert(0, str(SCRIPTS))
    import plan_gate_lib

    if plan is not None:
        try:
            plan_line = plan.relative_to(ROOT).as_posix()
        except ValueError:
            plan_line = str(plan)
    else:
        state = plan_gate_lib.read_workflow_state()
        plan_line = state.get("plan", "").strip() or "latest"
    plan_gate_lib.write_plan_gate_stamp(plan_line)
    print(f"Wrote {PLAN_GATE.relative_to(ROOT)}")


def write_test_gate() -> None:
    sys.path.insert(0, str(SCRIPTS))
    import plan_gate_lib

    state = plan_gate_lib.read_workflow_state()
    plan_line = state.get("plan", "").strip()
    test_line = state.get("test_plan", "").strip()
    if not plan_line or not test_line:
        print(
            "绝对门禁：workflow_state 缺少 plan 或 test_plan — 禁止写 test.ok",
            file=sys.stderr,
        )
        raise SystemExit(1)
    plan_gate_lib.write_test_gate_stamp(plan_rel=plan_line, test_plan_rel=test_line)
    print(f"Wrote {(PIPELINE / '.gates' / 'test.ok').relative_to(ROOT)}")


def write_code_gate(step: int) -> None:
    sys.path.insert(0, str(SCRIPTS))
    import plan_gate_lib

    state = plan_gate_lib.read_workflow_state()
    plan_line = state.get("plan", "").strip()
    if not plan_line:
        print("绝对门禁：workflow_state.plan 未填写", file=sys.stderr)
        raise SystemExit(1)
    plan_gate_lib.write_code_gate_stamp(plan_rel=plan_line, step=step)
    print(f"Wrote {(PIPELINE / '.gates' / 'code.ok').relative_to(ROOT)}")


def require_plan_confirmed(*, require_phase_min: str, label: str) -> int:
    sys.path.insert(0, str(SCRIPTS))
    import plan_gate_lib

    errors = plan_gate_lib.validate_plan_confirmed(require_phase_min=require_phase_min)
    if errors:
        print(f"{label} FAILED — 确认规划绝对门禁:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    return 0


def run_static_quality() -> int:
    return run([sys.executable, str(SCRIPTS / "check_static_quality.py")])


def run_full_regression_pytest(*, bucket: str, stem: str, exclude_pending: bool) -> int:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "src/tests/contract",
        "src/tests/workflow",
        "src/tests/integration",
        "-v",
        "--tb=short",
    ]
    if exclude_pending:
        cmd.extend(["-m", "not pending"])
    return run_logged(bucket=bucket, stem=stem, cmd=cmd)


def run_contract_workflow_pytest(*, bucket: str, stem: str, exclude_pending: bool) -> int:
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
    return run_logged(bucket=bucket, stem=stem, cmd=cmd)


def gate_materials(
    materials: Path | None,
    *,
    na: bool,
    reason: str,
) -> int:
    """用户「材料已齐」后的机械凭证：写 materials.ok。"""
    sys.path.insert(0, str(SCRIPTS))

    if na:
        if not reason.strip():
            print(
                "Gate materials FAILED: --na 须同时给 --reason（如 Bug修复/联调）",
                file=sys.stderr,
            )
            return 1
        write_materials_gate(materials=None, na=True, reason=reason.strip())
        print(
            "\nGate materials OK (materials.ok mode=na)\n"
            "下一步：可进入 Step 0 / 规划；确认规划前更新 workflow_state.materials=na"
        )
        return 0

    if materials is None:
        print(
            "Gate materials FAILED: 须 --materials <path> 或 --na --reason …",
            file=sys.stderr,
        )
        return 1
    path = materials if materials.is_absolute() else ROOT / materials
    if not path.is_file():
        print(f"Gate materials FAILED: 文件不存在 — {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    if "功能需求文案" not in text and "一句话目标" not in text:
        print(
            "Gate materials FAILED: materials 文件须含「功能需求文案」或「一句话目标」"
            "（见 materials-intake-template）",
            file=sys.stderr,
        )
        return 1
    if "需求资料" not in text and "资料类型" not in text:
        print(
            "Gate materials FAILED: materials 文件须含「需求资料」表"
            "（见 materials-intake-template）",
            file=sys.stderr,
        )
        return 1
    write_materials_gate(materials=path, na=False, reason="")
    print(
        "\nGate materials OK (materials.ok stamped)\n"
        "下一步：更新 workflow_state.materials=<相对路径> → 进入 Step 0 需求分析"
    )
    return 0


def gate_plan(plan: Path | None) -> int:
    sys.path.insert(0, str(SCRIPTS))
    import plan_gate_lib

    state = plan_gate_lib.read_workflow_state()
    if state.get("phase") == "STEP0":
        print(
            "绝对门禁：phase=STEP0 — 须用户「可以继续」进入 PLANNING 后再「确认规划」",
            file=sys.stderr,
        )
        return 1
    plan_path = plan_gate_lib.resolve_plan_path(state)
    if plan_path is None or not plan_path.is_file():
        print(
            "绝对门禁：workflow_state.plan 未填写或文件不存在 — 禁止 gate plan",
            file=sys.stderr,
        )
        return 1
    mat_errors = plan_gate_lib.validate_materials_for_plan(plan_path)
    if mat_errors:
        print("Gate plan FAILED — 材料准入绝对门禁:", file=sys.stderr)
        for err in mat_errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    if run_logged(
        bucket="dev",
        stem="gate-plan_harness-contracts",
        cmd=[sys.executable, str(SCRIPTS / "check_harness.py"), "--tier", "contracts"],
    ) != 0:
        return 1
    cmd = [sys.executable, str(SCRIPTS / "check_plan_spec.py")]
    if plan:
        cmd.extend(["--plan", str(plan)])
    if run_logged(bucket="dev", stem="gate-plan_check-plan-spec", cmd=cmd) != 0:
        return 1
    if run_logged(
        bucket="dev",
        stem="gate-plan_check-pipeline",
        cmd=[sys.executable, str(SCRIPTS / "check_pipeline.py"), "--gate", "plan"],
    ) != 0:
        return 1
    stamped = plan if plan is not None else Path(state.get("plan", ""))
    write_plan_gate(stamped)
    print("\nGate plan OK (analyze passed · plan.ok stamped)")
    return 0


def gate_test() -> int:
    if require_plan_confirmed(require_phase_min="CAN_TEST", label="Gate test") != 0:
        return 1
    if run_logged(
        bucket="test",
        stem="gate-test_check-pipeline",
        cmd=[sys.executable, str(SCRIPTS / "check_pipeline.py"), "--gate", "test"],
    ) != 0:
        return 1
    write_test_gate()
    print("\nGate test OK (test.ok stamped)")
    return 0


def gate_start(step: int) -> int:
    """用户「可以开始」后的机械凭证：写 code.ok。"""
    sys.path.insert(0, str(SCRIPTS))
    import plan_gate_lib

    errors = plan_gate_lib.validate_test_stamp()
    if errors:
        print("Gate start FAILED — 绝对门禁:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    if step < 1:
        print("Gate start FAILED: --step 须 >= 1", file=sys.stderr)
        return 1
    if step > 1:
        chain_errors = require_step_chain_closed(step - 1)
        if chain_errors != 0:
            return chain_errors
    write_code_gate(step)
    print(
        f"\nGate start OK (code.ok stamped for step {step})\n"
        "下一步：更新 workflow_state → phase=CAN_CODE · agent=dev · step=N"
    )
    return 0


def gate_verify(step: int, require_pass: bool) -> int:
    cmd = [sys.executable, str(SCRIPTS / "check_verify.py"), "--step", str(step)]
    if require_pass:
        cmd.append("--require-pass")
    if run_logged(bucket="verify", stem=f"gate-verify_step{step}", cmd=cmd) != 0:
        return 1
    print("\nGate verify OK")
    return 0


def require_step_chain_closed(step: int) -> int:
    """Step N 须 Dev step-stop → Test 验收 → Verify 通过（联动绝对门禁）。"""
    sys.path.insert(0, str(SCRIPTS))
    import step_chain_lib

    errors = step_chain_lib.validate_step_chain_closed(step, require_pass=True)
    if errors:
        print("Gate step FAILED — 联动门禁 (Dev→Test→Verify):", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1
    return 0


def gate_step(pytest_k: str | None, extra: list[str], step: int) -> int:
    if require_plan_confirmed(require_phase_min="CAN_CODE", label="Gate step") != 0:
        return 1
    if require_step_chain_closed(step) != 0:
        return 1
    cmd = [sys.executable, str(SCRIPTS / "check_harness.py"), "--tier", "full"]
    if pytest_k:
        cmd.extend(["--pytest", pytest_k, *extra])
    elif extra:
        cmd.extend(extra)
    if run_logged(bucket="dev", stem=f"gate-step_harness-full_step{step}", cmd=cmd) != 0:
        return 1
    if not pytest_k and pytest_available():
        if (
            run_contract_workflow_pytest(
                bucket="test",
                stem=f"gate-step_pytest-contract-workflow_step{step}",
                exclude_pending=True,
            )
            != 0
        ):
            return 1
    if run_logged(
        bucket="dev",
        stem=f"gate-step_static-quality_step{step}",
        cmd=[sys.executable, str(SCRIPTS / "check_static_quality.py")],
    ) != 0:
        return 1
    if run_logged(
        bucket="test",
        stem=f"gate-step_check-test-regression_step{step}",
        cmd=[
            sys.executable,
            str(SCRIPTS / "check_test_regression.py"),
            "--step",
            str(step),
            "--require-pass",
        ],
    ) != 0:
        return 1
    if gate_verify(step, require_pass=True) != 0:
        return 1
    if run_logged(
        bucket="dev",
        stem=f"gate-step_check-pipeline_step{step}",
        cmd=[
            sys.executable,
            str(SCRIPTS / "check_pipeline.py"),
            "--gate",
            "step",
            "--step",
            str(step),
        ],
    ) != 0:
        return 1
    sys.path.insert(0, str(SCRIPTS))
    import plan_gate_lib

    plan_gate_lib.clear_code_gate_stamp()
    print("\nGate step OK (harness · pytest · static · verify)")
    print("code.ok 已作废 — 下一 Step 须用户「可以开始」+ ./scripts/gate start")
    return 0


def gate_delivery() -> int:
    if require_plan_confirmed(require_phase_min="CAN_TEST", label="Gate delivery") != 0:
        return 1
    if run_logged(
        bucket="test",
        stem="gate-delivery_check-test-final-regression",
        cmd=[
            sys.executable,
            str(SCRIPTS / "check_test_regression.py"),
            "--final",
            "--require-pass",
        ],
    ) != 0:
        return 1
    if not pytest_available():
        print("⚠ pytest missing — uv sync --extra dev", file=sys.stderr)
        return 1
    if run_full_regression_pytest(
        bucket="test",
        stem="gate-delivery_pytest-full-regression",
        exclude_pending=True,
    ) != 0:
        return 1
    if run_logged(
        bucket="dev",
        stem="gate-delivery_check-pipeline",
        cmd=[sys.executable, str(SCRIPTS / "check_pipeline.py"), "--gate", "delivery"],
    ) != 0:
        return 1
    print("\nGate delivery OK (终轮回归 · 可提示 commit)")
    return 0


def gate_pr() -> int:
    if run_logged(
        bucket="dev",
        stem="gate-pr_harness-full",
        cmd=[sys.executable, str(SCRIPTS / "check_harness.py"), "--tier", "full"],
    ) != 0:
        return 1
    if run_logged(
        bucket="dev",
        stem="gate-pr_check-pipeline-state",
        cmd=[sys.executable, str(SCRIPTS / "check_pipeline.py"), "--gate", "state"],
    ) != 0:
        return 1
    if not pytest_available():
        print("⚠ pytest missing — uv sync --extra dev", file=sys.stderr)
        return 1
    if run_contract_workflow_pytest(bucket="test", stem="gate-pr_pytest", exclude_pending=False) != 0:
        return 1
    if run_logged(
        bucket="dev",
        stem="gate-pr_static-quality",
        cmd=[sys.executable, str(SCRIPTS / "check_static_quality.py")],
    ) != 0:
        return 1
    if run_logged(
        bucket="dev",
        stem="gate-pr_deptry",
        cmd=[sys.executable, str(SCRIPTS / "check_deptry.py")],
    ) != 0:
        return 1
    print("\nGate pr OK (T4.5 full)")
    return 0


def gate_gate0() -> int:
    if run_logged(
        bucket="dev",
        stem="gate-gate0_harness-full",
        cmd=[sys.executable, str(SCRIPTS / "check_harness.py"), "--tier", "full"],
    ) != 0:
        return 1
    if not pytest_available():
        print("⚠ pytest missing — uv sync --extra dev", file=sys.stderr)
        return 1
    if run_contract_workflow_pytest(bucket="test", stem="gate-gate0_pytest", exclude_pending=True) != 0:
        return 1
    if run_logged(
        bucket="dev",
        stem="gate-gate0_static-quality",
        cmd=[sys.executable, str(SCRIPTS / "check_static_quality.py")],
    ) != 0:
        return 1
    # 52 P0 全绿后启用：uv run pytest -v
    print("\nGate gate0 prep OK (enable full pytest in CI when AC suite green)")
    return 0


def gate_docs_sync() -> int:
    return run_logged(
        bucket="dev",
        stem="gate-docs-sync",
        cmd=[sys.executable, str(SCRIPTS / "docs_baseline.py"), "gate"],
    )


def gate_analyze(plan: Path | None) -> int:
    cmd = [sys.executable, str(SCRIPTS / "check_plan_spec.py")]
    if plan:
        cmd.extend(["--plan", str(plan)])
    return run_logged(bucket="dev", stem="gate-analyze_check-plan-spec", cmd=cmd)


def gate_harness_eval(cases: list[str] | None = None) -> int:
    """L4 P0：冻结黄金题，改门禁后回归。"""
    cmd = [sys.executable, str(SCRIPTS / "check_harness_eval.py")]
    if cases:
        for c in cases:
            cmd.extend(["--case", c])
    return run_logged(bucket="dev", stem="gate-harness-eval", cmd=cmd)


def gate_harness_gc(*, strict: bool = False) -> int:
    """L4 P2：熵清理扫描。"""
    cmd = [sys.executable, str(SCRIPTS / "harness_gc.py")]
    if strict:
        cmd.append("--strict")
    return run_logged(bucket="dev", stem="gate-harness-gc", cmd=cmd)


def main() -> int:
    p = argparse.ArgumentParser(description="FactoryOS Gate CLI (T4.5)")
    sub = p.add_subparsers(dest="gate", required=True)

    sm = sub.add_parser("materials", help="材料已齐 + materials.ok")
    sm.add_argument("--materials", type=Path, help="materials-*.md（新功能）")
    sm.add_argument("--na", action="store_true", help="非新功能跳过材料文件")
    sm.add_argument("--reason", default="", help="--na 时必填理由")

    sp = sub.add_parser("plan", help="确认规划 + analyze + plan.ok（须先 materials.ok）")
    sp.add_argument("--plan", type=Path)

    sub.add_parser("test", help="test-plan 节点 + test.ok")

    st = sub.add_parser("start", help="可以开始 Step N + code.ok")
    st.add_argument("--step", type=int, required=True)

    ss = sub.add_parser("step", help="Step 停机全量")
    ss.add_argument("-k", "--pytest", metavar="EXPR")
    ss.add_argument("--step", type=int, default=1)
    ss.add_argument("pytest_extra", nargs="*")

    sv = sub.add_parser("verify", help="Verify 回合检查")
    sv.add_argument("--step", type=int, required=True)
    sv.add_argument("--require-pass", action="store_true", default=True)

    sub.add_parser("delivery", help="终轮回归验收盘（commit 前）")
    sub.add_parser("pr", help="PR 验收盘")
    sub.add_parser("gate0", help="Gate 0")

    sub.add_parser("docs-sync", help="docs 认知基线分级门禁")

    sa = sub.add_parser("analyze", help="plan↔contracts")
    sa.add_argument("--plan", type=Path)

    se = sub.add_parser("harness-eval", help="L4：harness 黄金题回归（10 题）")
    se.add_argument("--case", action="append", dest="cases", help="仅跑指定 HE-ID")

    sg = sub.add_parser("harness-gc", help="L4：harness 熵清理扫描")
    sg.add_argument("--strict", action="store_true", help="有 critical 则失败")

    args = p.parse_args()

    if args.gate == "materials":
        return gate_materials(args.materials, na=args.na, reason=args.reason)
    if args.gate == "plan":
        return gate_plan(args.plan)
    if args.gate == "test":
        return gate_test()
    if args.gate == "start":
        return gate_start(args.step)
    if args.gate == "step":
        return gate_step(getattr(args, "pytest", None), args.pytest_extra, args.step)
    if args.gate == "verify":
        return gate_verify(args.step, args.require_pass)
    if args.gate == "delivery":
        return gate_delivery()
    if args.gate == "pr":
        return gate_pr()
    if args.gate == "gate0":
        return gate_gate0()
    if args.gate == "docs-sync":
        return gate_docs_sync()
    if args.gate == "analyze":
        return 0 if gate_analyze(args.plan) == 0 else 1
    if args.gate == "harness-eval":
        return gate_harness_eval(getattr(args, "cases", None))
    if args.gate == "harness-gc":
        return gate_harness_gc(strict=args.strict)
    return 1


if __name__ == "__main__":
    sys.exit(main())
