"""WEB harness 微评测（WHE-01～10 · 独立于后端 HE-*）。

作用：冻结黄金题，改 WEB 门禁后回归。
关联文档：.cursor/factoryos/WEB-HARNESS-EVAL.md
"""
from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import web_check_plan_spec as wcps
import web_failure_taxonomy_lib as wftl
import web_step_chain_lib as wscl

MIN_PLAN = """# plan WEB eval

- **类型**：Bug修复
- **材料准入**：N/A（eval）

## 4. Step 总览

| Step | 名称 |
|------|------|
| 1 | demo |

## Step 列表

### Step 1 — demo

- **路径**：`src/pages/demo/`
- **AC**：W-01
- **验收盘**：`check_boundary_lock` · `check_harness` · vitest
- **风险**：无

## 8. UI

- **命中判定**：否
"""


@dataclass(frozen=True)
class EvalCase:
  id: str
  name: str
  expect_errors: bool
  taxonomy: str
  run: Callable[[], list[str]]


@dataclass(frozen=True)
class EvalResult:
  id: str
  name: str
  ok: bool
  expect_errors: bool
  detail: str
  taxonomy: str


def _he01() -> list[str]:
  text = MIN_PLAN.replace("## 4. Step 总览", "## 4. 其他").replace("## Step 列表", "## 其他列表")
  return wcps.check_plan_structure(Path("p.md"), text)


def _he02() -> list[str]:
  p = Path("p.md")
  return (
    wcps.check_plan_structure(p, MIN_PLAN)
    + wcps.check_plan_materials(p, MIN_PLAN)
    + wcps.check_plan_ui(p, MIN_PLAN)
  )


def _he03() -> list[str]:
  text = MIN_PLAN.replace("**类型**：Bug修复", "**类型**：新功能").replace(
    "**材料准入**：N/A（eval）", "**材料准入**：N/A"
  )
  return wcps.check_plan_materials(Path("p.md"), text)


def _he04() -> list[str]:
  with tempfile.TemporaryDirectory() as td:
    base = Path(td)
    mat = base / "materials-0900.md"
    mat.write_text("# m\n", encoding="utf-8")
    text = MIN_PLAN.replace("**类型**：Bug修复", "**类型**：新功能").replace(
      "**材料准入**：N/A（eval）", f"**材料准入**：`{mat.name}`"
    )
    plan = base / "plan.md"
    plan.write_text(text, encoding="utf-8")
    return wcps.check_plan_materials(plan, text)


def _he05() -> list[str]:
  text = MIN_PLAN.replace(
    "- **命中判定**：否",
    "- **命中判定**：是\n\n| 字段 | 状态 |\n|------|------|\n| a | 待实现 |\n",
  )
  return wcps.check_plan_ui(Path("p.md"), text)


def _he06() -> list[str]:
  with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "step-stop-1.md"
    p.write_text("# stop\n无自检\n", encoding="utf-8")
    return wcps.check_step_stop_self_check(p)


def _he07() -> list[str]:
  with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "step-stop-1.md"
    p.write_text("# stop\n## 自检\n| 1 | 层界 | Pass |\n", encoding="utf-8")
    return wcps.check_step_stop_runtime_evidence(p)


def _he08() -> list[str]:
  with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "verify-1.md"
    p.write_text("结论：阻断\n", encoding="utf-8")
    return wscl.check_conclusion(p, require_pass=True)


def _he09() -> list[str]:
  import web_plan_gate_lib as wpg

  with tempfile.TemporaryDirectory() as td:
    base = Path(td)
    plan = base / "plan.md"
    plan.write_text(
      MIN_PLAN.replace("**类型**：Bug修复", "**类型**：新功能"),
      encoding="utf-8",
    )
    gates = base / ".gates"
    gates.mkdir()
    (gates / "materials.ok").write_text(
      "mode=na\nreason=wrong\nat=t\n", encoding="utf-8"
    )
    old = (
      wpg.MATERIALS_GATE,
      wpg.APP_ROOT,
      wpg.GATES_DIR,
      wpg.PIPELINE,
    )
    try:
      wpg.APP_ROOT = base
      wpg.PIPELINE = base
      wpg.GATES_DIR = gates
      wpg.MATERIALS_GATE = gates / "materials.ok"
      return wpg.validate_materials_for_plan(plan)
    finally:
      wpg.MATERIALS_GATE, wpg.APP_ROOT, wpg.GATES_DIR, wpg.PIPELINE = old


def _he10() -> list[str]:
  return wftl.validate_taxonomy_integrity()


CASES: list[EvalCase] = [
  EvalCase("WHE-01", "缺 Step 总览应失败", True, "WFT-PLAN-STRUCTURE", _he01),
  EvalCase("WHE-02", "最小 plan 应通过", False, "WFT-PLAN-STRUCTURE", _he02),
  EvalCase("WHE-03", "新功能材料 N/A 应失败", True, "WFT-MATERIALS-MISSING", _he03),
  EvalCase("WHE-04", "新功能+materials 应通过", False, "WFT-MATERIALS-MISSING", _he04),
  EvalCase("WHE-05", "UI 待实现应失败", True, "WFT-PLAN-UI", _he05),
  EvalCase("WHE-06", "step-stop 缺自检应失败", True, "WFT-RUNTIME-EVIDENCE", _he06),
  EvalCase("WHE-07", "缺运行时证据应失败", True, "WFT-RUNTIME-EVIDENCE", _he07),
  EvalCase("WHE-08", "Verify 阻断不可当通过", True, "WFT-VERIFY-BLOCK", _he08),
  EvalCase("WHE-09", "新功能禁 materials na", True, "WFT-STAMP-CHAIN", _he09),
  EvalCase("WHE-10", "税则完整", False, "WFT-TAXONOMY", _he10),
]


def run_case(case: EvalCase) -> EvalResult:
  try:
    errs = case.run()
  except Exception as exc:  # noqa: BLE001
    return EvalResult(case.id, case.name, False, case.expect_errors, str(exc), case.taxonomy)
  has = bool(errs)
  ok = has if case.expect_errors else not has
  detail = "; ".join(errs[:3]) if errs else "no errors"
  return EvalResult(case.id, case.name, ok, case.expect_errors, detail, case.taxonomy)


def run_all(*, case_ids: set[str] | None = None) -> list[EvalResult]:
  out: list[EvalResult] = []
  for c in CASES:
    if case_ids and c.id not in case_ids:
      continue
    out.append(run_case(c))
  return out
