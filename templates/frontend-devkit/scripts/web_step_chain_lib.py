"""WEB Dev→Test→Verify 联动链（按 plan 日期目录）。

作用：Step N 须 step-stop（含运行时证据）→ Test 验收 → Verify 通过。
业务关联：WEB-步步流；独立于 step_chain_lib（后端）
上游：web_gate step · web_harness_eval
下游：阻断跳验收
"""
from __future__ import annotations

import re
from pathlib import Path

import web_check_plan_spec as wcps
import web_plan_gate_lib as wpg

CONCLUSION_RE = re.compile(r"结论[：:]\s*(通过|需改进|阻断|PASS|BLOCK)", re.I)


def plan_pipeline_dir() -> Path | None:
  """当前 plan 所属 _web_pipeline/<date>/。"""
  state = wpg.read_workflow_state()
  raw = state.get("plan", "")
  if not raw:
    return None
  path = wpg.resolve_under_app(raw)
  if path.parent.name != "plan":
    return None
  return path.parent.parent


def find_step_stop(step: int, plan_dir: Path | None = None) -> Path | None:
  """查找 step-stop。"""
  plan_dir = plan_dir or plan_pipeline_dir()
  if plan_dir is None:
    return None
  hits = sorted(plan_dir.glob(f"step-stop/step-stop-*-step{step}.md"))
  return hits[-1] if hits else None


def find_test_regression(step: int, plan_dir: Path | None = None) -> Path | None:
  """查找 Test 单步验收。"""
  plan_dir = plan_dir or plan_pipeline_dir()
  if plan_dir is None:
    return None
  hits = sorted(plan_dir.glob(f"test/test-*-step{step}-regression.md"))
  return hits[-1] if hits else None


def find_verify(step: int, plan_dir: Path | None = None) -> Path | None:
  """查找 Verify。"""
  plan_dir = plan_dir or plan_pipeline_dir()
  if plan_dir is None:
    return None
  hits = sorted(plan_dir.glob(f"verify/verify-*-step{step}.md"))
  return hits[-1] if hits else None


def check_conclusion(path: Path, *, require_pass: bool) -> list[str]:
  """校验结论。"""
  text = path.read_text(encoding="utf-8")
  m = CONCLUSION_RE.search(text)
  if not m:
    return [f"{path.name}: missing 结论（通过/需改进/阻断）"]
  norm = m.group(1).lower()
  if norm in ("pass",):
    norm = "通过"
  if norm in ("block",):
    norm = "阻断"
  if require_pass and norm != "通过":
    return [f"{path.name}: 结论={m.group(1)} — 须「通过」"]
  return []


def validate_step_dev_done(step: int) -> list[str]:
  """Dev 停机完成。"""
  plan_dir = plan_pipeline_dir()
  if plan_dir is None:
    return ["WEB联动门禁：无法解析 plan 目录 — 须先确认规划"]
  stop = find_step_stop(step, plan_dir)
  if stop is None:
    return [f"WEB联动门禁 Step {step}：缺少 step-stop"]
  errors: list[str] = []
  errors.extend(wcps.check_step_stop_self_check(stop))
  errors.extend(wcps.check_step_stop_runtime_evidence(stop))
  return errors


def validate_step_test_done(step: int, *, require_pass: bool = True) -> list[str]:
  """Test 验收完成。"""
  plan_dir = plan_pipeline_dir()
  if plan_dir is None:
    return ["WEB联动门禁：无法解析 plan 目录"]
  reg = find_test_regression(step, plan_dir)
  if reg is None:
    return [f"WEB联动门禁 Step {step}：缺少 Test 单步验收落盘"]
  return check_conclusion(reg, require_pass=require_pass)


def validate_step_verify_done(step: int, *, require_pass: bool = True) -> list[str]:
  """Verify 完成。"""
  plan_dir = plan_pipeline_dir()
  if plan_dir is None:
    return ["WEB联动门禁：无法解析 plan 目录"]
  vf = find_verify(step, plan_dir)
  if vf is None:
    return [f"WEB联动门禁 Step {step}：缺少 Verify 落盘"]
  return check_conclusion(vf, require_pass=require_pass)


def validate_step_chain_closed(step: int, *, require_pass: bool = True) -> list[str]:
  """全链闭合。"""
  errors: list[str] = []
  errors.extend(validate_step_dev_done(step))
  errors.extend(validate_step_test_done(step, require_pass=require_pass))
  errors.extend(validate_step_verify_done(step, require_pass=require_pass))
  return errors
