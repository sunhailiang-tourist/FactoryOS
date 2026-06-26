"""Dev → Test → Verify 联动绝对门禁（按 plan 目录隔离）。

作用：Step N 须 step-stop → Test 单步验收 → Verify 通过，方可 gate step / 进入 Step N+1 Dev。
业务关联：SH-步步流 v2.1 三 Agent 次序不可跳。
上游：check_pipeline · check_verify · check_test_regression · protect-paths hook
下游：阻断跨轮次误用 W2 Verify 冒充 W3
"""
from __future__ import annotations

import re
from pathlib import Path

from plan_gate_lib import read_workflow_state, resolve_plan_path

ROOT = Path(__file__).resolve().parents[1]
PIPELINE = ROOT / "_factoryos_pipeline"

CONCLUSION_RE = re.compile(r"结论[：:]\s*(通过|需改进|阻断|PASS|BLOCK)", re.IGNORECASE)
STEP_STOP_RE = re.compile(r"step-stop-.*-step(\d+)\.md$")
TEST_STEP_RE = re.compile(r"test-.*-step(\d+)-regression\.md$")
VERIFY_STEP_RE = re.compile(r"verify-.*-step(\d+)\.md$")


def plan_pipeline_dir(state: dict[str, str] | None = None) -> Path | None:
  """当前 plan 所属 `_factoryos_pipeline/<date>/` 目录。"""
  state = state or read_workflow_state()
  plan_path = resolve_plan_path(state)
  if plan_path is None:
    return None
  # .../<date>/plan/plan-*.md → .../<date>
  if plan_path.parent.name != "plan":
    return None
  return plan_path.parent.parent


def _glob_in_plan(plan_dir: Path, pattern: str) -> list[Path]:
  return sorted(plan_dir.glob(pattern), key=lambda p: p.stat().st_mtime)


def find_step_stop(step: int, plan_dir: Path | None = None) -> Path | None:
  """当前 plan 目录下 step-stop（Step N Dev 停机）。"""
  plan_dir = plan_dir or plan_pipeline_dir()
  if plan_dir is None:
    return None
  hits = _glob_in_plan(plan_dir, f"step-stop/step-stop-*-step{step}.md")
  return hits[-1] if hits else None


def find_test_regression(step: int, plan_dir: Path | None = None) -> Path | None:
  """当前 plan 目录下 Test·Step N 验收落盘。"""
  plan_dir = plan_dir or plan_pipeline_dir()
  if plan_dir is None:
    return None
  hits = _glob_in_plan(plan_dir, f"test/test-*-step{step}-regression.md")
  return hits[-1] if hits else None


def find_verify(step: int, plan_dir: Path | None = None) -> Path | None:
  """当前 plan 目录下 Verify·Step N 落盘。"""
  plan_dir = plan_dir or plan_pipeline_dir()
  if plan_dir is None:
    return None
  hits = _glob_in_plan(plan_dir, f"verify/verify-*-step{step}.md")
  return hits[-1] if hits else None


def find_final_regression(plan_dir: Path | None = None) -> Path | None:
  plan_dir = plan_dir or plan_pipeline_dir()
  if plan_dir is None:
    return None
  hits = _glob_in_plan(plan_dir, "test/test-*-final-regression.md")
  return hits[-1] if hits else None


def read_conclusion(path: Path) -> str | None:
  """读取验收/Verify 结论词。"""
  text = path.read_text(encoding="utf-8")
  if "结论" not in text and "conclusion" not in text.lower():
    return None
  m = CONCLUSION_RE.search(text)
  return m.group(1).upper() if m else None


def check_conclusion(path: Path, *, require_pass: bool) -> list[str]:
  """校验结论段；require_pass 时阻断/需改进不含通过均失败。"""
  errors: list[str] = []
  conclusion = read_conclusion(path)
  if conclusion is None:
    errors.append(f"{path.name}: missing 结论 (通过/需改进/阻断)")
    return errors
  norm = conclusion.lower()
  if norm in ("pass",):
    norm = "通过"
  if norm in ("block",):
    norm = "阻断"
  if require_pass and norm != "通过":
    errors.append(f"{path.name}: 结论={conclusion} — 须「通过」才能继续联动链")
  return errors


def validate_step_dev_done(step: int) -> list[str]:
  """Dev Step N 完成：须有 step-stop。"""
  errors: list[str] = []
  plan_dir = plan_pipeline_dir()
  if plan_dir is None:
    return ["联动门禁：无法解析 plan 目录 — 须先确认规划"]
  stop = find_step_stop(step, plan_dir)
  if stop is None:
    errors.append(
      f"联动门禁 Step {step}：缺少 Dev step-stop "
      f"({plan_dir.name}/step-stop/step-stop-*-step{step}.md)"
    )
  return errors


def validate_step_test_done(step: int, *, require_pass: bool = True) -> list[str]:
  """Test Step N 验收完成：须有 test-*-stepN-regression 且结论通过。"""
  errors: list[str] = []
  plan_dir = plan_pipeline_dir()
  if plan_dir is None:
    return ["联动门禁：无法解析 plan 目录 — 须先确认规划"]
  reg = find_test_regression(step, plan_dir)
  if reg is None:
    errors.append(
      f"联动门禁 Step {step}：缺少 Test 单步验收 "
      f"({plan_dir.name}/test/test-*-step{step}-regression.md) — "
      f"Dev 完成后须【Test·Step {step} 验收】"
    )
    return errors
  errors.extend(check_conclusion(reg, require_pass=require_pass))
  return errors


def validate_step_verify_done(step: int, *, require_pass: bool = True) -> list[str]:
  """Verify Step N 完成：须有 verify-*-stepN 且结论通过。"""
  errors: list[str] = []
  plan_dir = plan_pipeline_dir()
  if plan_dir is None:
    return ["联动门禁：无法解析 plan 目录 — 须先确认规划"]
  vf = find_verify(step, plan_dir)
  if vf is None:
    errors.append(
      f"联动门禁 Step {step}：缺少 Verify 落盘 "
      f"({plan_dir.name}/verify/verify-*-step{step}.md) — "
      f"Test 通过后须【Verify回合】Step {step}"
    )
    return errors
  errors.extend(check_conclusion(vf, require_pass=require_pass))
  return errors


def validate_step_chain_closed(step: int, *, require_pass: bool = True) -> list[str]:
  """Step N 全链闭合：Dev → Test → Verify（gate step 用）。"""
  errors: list[str] = []
  errors.extend(validate_step_dev_done(step))
  errors.extend(validate_step_test_done(step, require_pass=require_pass))
  errors.extend(validate_step_verify_done(step, require_pass=require_pass))
  return errors


def validate_prior_steps_closed(before_step: int, *, require_pass: bool = True) -> list[str]:
  """Step 1..before_step-1 均已 Dev→Test→Verify 闭合（开 Step N Dev 前）。"""
  errors: list[str] = []
  for s in range(1, before_step):
    errors.extend(validate_step_chain_closed(s, require_pass=require_pass))
  return errors


def validate_can_start_step_dev(step: int) -> list[str]:
  """可以开始 Step N Dev：Step 1 仅需 plan；Step N>1 须 Step N-1 全链闭合。"""
  if step <= 1:
    return []
  return validate_step_chain_closed(step - 1, require_pass=True)


def parse_step_from_pipeline_path(path: str) -> int | None:
  """从落盘文件名解析 Step 号。"""
  name = Path(path).name
  for regex in (TEST_STEP_RE, VERIFY_STEP_RE, STEP_STOP_RE):
    m = regex.match(name)
    if m:
      return int(m.group(1))
  return None


def format_chain_errors(errors: list[str]) -> str:
  return errors[0] if len(errors) == 1 else " | ".join(errors)
