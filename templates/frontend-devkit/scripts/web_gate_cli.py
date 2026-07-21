#!/usr/bin/env python3
"""WEB Gate CLI（独立于仓库根 ./scripts/gate）。

Usage（在 App 根）:
  ./scripts/web_gate materials --materials _web_pipeline/.../materials-….md
  ./scripts/web_gate materials --na --reason 'Bug修复'
  ./scripts/web_gate plan --plan _web_pipeline/.../plan-….md
  ./scripts/web_gate test
  ./scripts/web_gate start --step 1
  ./scripts/web_gate step --step 1
  ./scripts/web_gate harness-eval
  ./scripts/web_gate harness-gc
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import web_check_plan_spec as wcps  # noqa: E402
import web_plan_gate_lib as wpg  # noqa: E402
import web_step_chain_lib as wscl  # noqa: E402


def _rel(path: Path) -> str:
  try:
    return str(path.resolve().relative_to(APP_ROOT.resolve()))
  except ValueError:
    return str(path)


def gate_materials(materials: Path | None, *, na: bool, reason: str) -> int:
  wpg.ensure_pipeline_scaffold()
  if na:
    if not reason.strip():
      print("web_gate materials --na 须 --reason", file=sys.stderr)
      return 1
    wpg.write_materials_gate_stamp(mode="na", reason=reason.strip())
    print("Wrote _web_pipeline/.gates/materials.ok (mode=na)")
    print("Gate materials OK")
    return 0
  if materials is None:
    print("须 --materials 或 --na", file=sys.stderr)
    return 1
  path = materials if materials.is_absolute() else APP_ROOT / materials
  if not path.is_file():
    print(f"materials 不存在: {path}", file=sys.stderr)
    return 1
  wpg.write_materials_gate_stamp(materials_rel=_rel(path), mode="file")
  print(f"Wrote materials.ok → {_rel(path)}")
  print("Gate materials OK")
  return 0


def gate_plan(plan: Path | None, *, with_harness: bool = False) -> int:
  wpg.ensure_pipeline_scaffold()
  if plan is None:
    state = wpg.read_workflow_state()
    raw = state.get("plan")
    if not raw:
      print("须 --plan 或先填 workflow_state.plan", file=sys.stderr)
      return 1
    plan_path = wpg.resolve_under_app(raw)
  else:
    plan_path = plan if plan.is_absolute() else APP_ROOT / plan
  if not plan_path.is_file():
    print(f"plan 不存在: {plan_path}", file=sys.stderr)
    return 1
  errs = wpg.validate_materials_for_plan(plan_path)
  errs.extend(wcps.validate_plan_file(plan_path))
  if errs:
    for e in errs:
      print(e, file=sys.stderr)
    return 1
  scripts_to_run = ["check_boundary_lock.py"]
  if with_harness:
    scripts_to_run.append("check_harness.py")
  for script in scripts_to_run:
    sp = SCRIPTS / script
    if sp.is_file():
      r = subprocess.run([sys.executable, str(sp)], cwd=str(APP_ROOT), check=False)
      if r.returncode != 0:
        print(f"{script} FAILED", file=sys.stderr)
        return 1
  rel = _rel(plan_path)
  wpg.write_plan_gate_stamp(rel)
  print(f"Wrote plan.ok → {rel}")
  print("Gate plan OK")
  return 0


def gate_test() -> int:
  errs = wpg.validate_plan_stamp()
  if errs:
    for e in errs:
      print(e, file=sys.stderr)
    return 1
  state = wpg.read_workflow_state()
  plan_rel = state.get("plan", "")
  test_rel = state.get("test_plan", "")
  if not test_rel:
    # 允许最新 test-*.md
    tests = sorted((wpg.PIPELINE).glob("*/test/test-*.md"))
    if not tests:
      print("缺少 test-plan 落盘 _web_pipeline/<date>/test/test-*.md", file=sys.stderr)
      return 1
    test_rel = _rel(tests[-1])
  wpg.write_test_gate_stamp(plan_rel=plan_rel, test_plan_rel=test_rel)
  print(f"Wrote test.ok → {test_rel}")
  print("Gate test OK")
  return 0


def gate_start(step: int) -> int:
  errs = wpg.validate_test_stamp()
  if errs:
    for e in errs:
      print(e, file=sys.stderr)
    return 1
  if step > 1:
    chain = wscl.validate_step_chain_closed(step - 1)
    if chain:
      for e in chain:
        print(e, file=sys.stderr)
      return 1
  state = wpg.read_workflow_state()
  wpg.write_code_gate_stamp(plan_rel=state.get("plan", ""), step=step)
  print(f"Wrote code.ok step={step}")
  print("Gate start OK")
  return 0


def gate_step(step: int) -> int:
  errs = wpg.validate_plan_stamp()
  if errs:
    for e in errs:
      print(e, file=sys.stderr)
    return 1
  chain = wscl.validate_step_chain_closed(step, require_pass=True)
  if chain:
    for e in chain:
      print(e, file=sys.stderr)
    return 1
  for script in ("check_boundary_lock.py", "check_harness.py"):
    sp = SCRIPTS / script
    if sp.is_file():
      r = subprocess.run([sys.executable, str(sp)], cwd=str(APP_ROOT), check=False)
      if r.returncode != 0:
        return 1
  wpg.clear_code_gate_stamp()
  print("Gate step OK（code.ok 已作废 — 下一 Step 须重新 start）")
  return 0


def gate_harness_eval(cases: list[str] | None) -> int:
  cmd = [sys.executable, str(SCRIPTS / "web_check_harness_eval.py")]
  if cases:
    for c in cases:
      cmd.extend(["--case", c])
  return subprocess.run(cmd, cwd=str(APP_ROOT), check=False).returncode


def gate_harness_gc(*, strict: bool) -> int:
  cmd = [sys.executable, str(SCRIPTS / "web_harness_gc.py")]
  if strict:
    cmd.append("--strict")
  return subprocess.run(cmd, cwd=str(APP_ROOT), check=False).returncode


def main() -> int:
  p = argparse.ArgumentParser(description="WEB Gate CLI（App 内独立）")
  sub = p.add_subparsers(dest="gate", required=True)

  sm = sub.add_parser("materials")
  sm.add_argument("--materials", type=Path)
  sm.add_argument("--na", action="store_true")
  sm.add_argument("--reason", default="")

  sp = sub.add_parser("plan")
  sp.add_argument("--plan", type=Path)
  sp.add_argument(
    "--with-harness",
    action="store_true",
    help="确认规划时额外跑 check_harness（默认仅 boundary）",
  )

  sub.add_parser("test")
  st = sub.add_parser("start")
  st.add_argument("--step", type=int, required=True)
  ss = sub.add_parser("step")
  ss.add_argument("--step", type=int, required=True)

  se = sub.add_parser("harness-eval")
  se.add_argument("--case", action="append", dest="cases")
  sg = sub.add_parser("harness-gc")
  sg.add_argument("--strict", action="store_true")

  args = p.parse_args()
  if args.gate == "materials":
    return gate_materials(args.materials, na=args.na, reason=args.reason)
  if args.gate == "plan":
    return gate_plan(args.plan, with_harness=getattr(args, "with_harness", False))
  if args.gate == "test":
    return gate_test()
  if args.gate == "start":
    return gate_start(args.step)
  if args.gate == "step":
    return gate_step(args.step)
  if args.gate == "harness-eval":
    return gate_harness_eval(getattr(args, "cases", None))
  if args.gate == "harness-gc":
    return gate_harness_gc(strict=args.strict)
  return 1


if __name__ == "__main__":
  raise SystemExit(main())
