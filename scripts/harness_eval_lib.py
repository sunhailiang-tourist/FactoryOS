"""Harness 微评测真源（L4 · P0）。

作用：冻结 10 道黄金题，改 rules/hook/门禁脚本后回归，防止治理回退。
业务关联：SH-步步流 L3 之上的「评测科学」外环；不替代业务 pytest。
上游：gate harness-eval · check_harness_eval · CI 可选
下游：check_plan_spec · step_chain_lib · plan_gate_lib · failure_taxonomy
关联文档：.cursor/factoryos/HARNESS-EVAL.md · FAILURE-TAXONOMY.md
"""
from __future__ import annotations

import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import check_plan_spec as cps
import failure_taxonomy_lib as ftl
import step_chain_lib as scl

ROOT = Path(__file__).resolve().parents[1]

MIN_PLAN = """# 预开发说明：harness-eval

- **类型**：Bug修复
- **材料准入**：N/A（eval）

## 2. AC 对账表（必填）

| AC ID | 标题 |
|-------|------|
| G-01 | gate |

## 4. Step 总览（必填 · 一眼看全部分步）

| Step | 名称 |
|------|------|
| 1 | demo |

## 6. 分步详表

### Step 1 — demo

#### 6.3 函数（新增 / 修改）

| 符号 | 文件路径 |
|------|----------|
| `f` | x.py |

#### 6.4 文件落位

| 路径 | 是否合理 |
|------|----------|
| x.py | 是 |

#### 6.6 入参数据结构

| 字段 |
|------|
| — |

#### 6.7 返回数据结构

| 字段 |
|------|
| status |

## 8. UI / 原型字段对账

- **命中判定**：否（无图）
"""


@dataclass(frozen=True)
class EvalCase:
  """单道黄金题。

  功能：描述期望「应失败」或「应通过」的 harness 行为。
  业务含义：改门禁后必须仍成立，否则视为治理回退。
  """

  id: str
  name: str
  expect_errors: bool
  taxonomy: str
  run: Callable[[], list[str]]


@dataclass(frozen=True)
class EvalResult:
  """单题执行结果。"""

  id: str
  name: str
  ok: bool
  expect_errors: bool
  error_count: int
  detail: str
  taxonomy: str


def _case_he01_missing_step_overview() -> list[str]:
  """缺 §4 Step 总览 → 结构门禁失败。"""
  text = MIN_PLAN.replace("## 4. Step 总览（必填 · 一眼看全部分步）", "## 4. 其他")
  return cps.check_structure_v2(Path("plan-he01.md"), text)


def _case_he02_min_plan_ok() -> list[str]:
  """最小合法 plan v2 → 结构/材料/UI 均空错。"""
  p = Path("plan-he02.md")
  errs: list[str] = []
  errs.extend(cps.check_structure_v2(p, MIN_PLAN))
  errs.extend(cps.check_materials(p, MIN_PLAN))
  errs.extend(cps.check_ui_reconcile(p, MIN_PLAN))
  return errs


def _case_he03_new_feature_na_materials() -> list[str]:
  """新功能材料 N/A → 失败。"""
  text = MIN_PLAN.replace("**类型**：Bug修复", "**类型**：新功能").replace(
    "**材料准入**：N/A（eval）", "**材料准入**：N/A"
  )
  return cps.check_materials(Path("plan-he03.md"), text)


def _case_he04_new_feature_with_materials() -> list[str]:
  """新功能 + materials 文件 → 通过。"""
  with tempfile.TemporaryDirectory() as td:
    base = Path(td)
    mat = base / "materials-0900-eval.md"
    mat.write_text("# materials\n", encoding="utf-8")
    text = MIN_PLAN.replace("**类型**：Bug修复", "**类型**：新功能").replace(
      "**材料准入**：N/A（eval）", f"**材料准入**：`{mat.name}`"
    )
    plan = base / "plan-he04.md"
    plan.write_text(text, encoding="utf-8")
    return cps.check_materials(plan, text)


def _case_he05_ui_pending_forbidden() -> list[str]:
  """UI 命中=是且含待实现 → 失败。"""
  text = MIN_PLAN.replace(
    "- **命中判定**：否（无图）",
    "- **命中判定**：是\n\n"
    "### 8.1 界面字段表\n\n| 视图ID |\n|--------|\n| v1 |\n\n"
    "### 8.2 接口字段对账表\n\n"
    "| UI字段 | 路径 | Schema | 落点 | 状态 |\n"
    "|--------|------|--------|------|------|\n"
    "| a | data.a | A | api | 待实现 |\n",
  )
  return cps.check_ui_reconcile(Path("plan-he05.md"), text)


def _case_he06_step_stop_missing_ui() -> list[str]:
  """step-stop 缺 UI字段对账 → 失败。"""
  with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "step-stop-0900-step1.md"
    p.write_text("# stop\n## 4. 自检\n无 UI 项\n", encoding="utf-8")
    return scl.check_step_stop_ui_gate(p)


def _case_he07_step_stop_runtime_evidence() -> list[str]:
  """step-stop 缺运行时证据 → 失败。"""
  with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "step-stop-0900-step1.md"
    p.write_text("# stop\n| 11 | UI字段对账 | N/A |\n", encoding="utf-8")
    return scl.check_step_stop_runtime_evidence(p)


def _case_he08_verify_block_not_pass() -> list[str]:
  """结论=阻断 + require_pass → 失败。"""
  with tempfile.TemporaryDirectory() as td:
    p = Path(td) / "verify-0900-step1.md"
    p.write_text("# verify\n结论：阻断\n", encoding="utf-8")
    return scl.check_conclusion(p, require_pass=True)


def _case_he09_new_feature_materials_na_stamp() -> list[str]:
  """gate plan 前置：新功能 + materials.ok mode=na → 失败。"""
  import plan_gate_lib as pgl

  with tempfile.TemporaryDirectory() as td:
    base = Path(td)
    plan = base / "plan-he09.md"
    plan.write_text(
      MIN_PLAN.replace("**类型**：Bug修复", "**类型**：新功能"),
      encoding="utf-8",
    )
    gates = base / ".gates"
    gates.mkdir()
    (gates / "materials.ok").write_text(
      "mode=na\nreason=eval-wrong\nat=2026-01-01T00:00:00Z\n",
      encoding="utf-8",
    )
    old_mat = pgl.MATERIALS_GATE
    old_root = pgl.ROOT
    try:
      pgl.MATERIALS_GATE = gates / "materials.ok"
      # validate_materials_stamp 会拼 ROOT；mode=na 不读文件路径
      errs = pgl.validate_materials_for_plan(plan)
    finally:
      pgl.MATERIALS_GATE = old_mat
      pgl.ROOT = old_root
    return errs


def _case_he10_taxonomy_complete() -> list[str]:
  """失败税则表完整且含回灌目标。"""
  return ftl.validate_taxonomy_integrity()


CASES: list[EvalCase] = [
  EvalCase(
    "HE-01",
    "plan 缺 Step 总览应失败",
    True,
    "FT-PLAN-STRUCTURE",
    _case_he01_missing_step_overview,
  ),
  EvalCase(
    "HE-02",
    "最小合法 plan v2 应通过",
    False,
    "FT-PLAN-STRUCTURE",
    _case_he02_min_plan_ok,
  ),
  EvalCase(
    "HE-03",
    "新功能材料 N/A 应失败",
    True,
    "FT-MATERIALS-MISSING",
    _case_he03_new_feature_na_materials,
  ),
  EvalCase(
    "HE-04",
    "新功能+materials 文件应通过",
    False,
    "FT-MATERIALS-MISSING",
    _case_he04_new_feature_with_materials,
  ),
  EvalCase(
    "HE-05",
    "UI 待实现应失败",
    True,
    "FT-PLAN-UI",
    _case_he05_ui_pending_forbidden,
  ),
  EvalCase(
    "HE-06",
    "step-stop 缺 UI 对账应失败",
    True,
    "FT-STEP-STOP-UI",
    _case_he06_step_stop_missing_ui,
  ),
  EvalCase(
    "HE-07",
    "step-stop 缺运行时证据应失败",
    True,
    "FT-RUNTIME-EVIDENCE",
    _case_he07_step_stop_runtime_evidence,
  ),
  EvalCase(
    "HE-08",
    "Verify 结论阻断不可当通过",
    True,
    "FT-VERIFY-BLOCK",
    _case_he08_verify_block_not_pass,
  ),
  EvalCase(
    "HE-09",
    "新功能禁止 materials mode=na",
    True,
    "FT-STAMP-CHAIN",
    _case_he09_new_feature_materials_na_stamp,
  ),
  EvalCase(
    "HE-10",
    "失败税则表完整可回灌",
    False,
    "FT-TAXONOMY",
    _case_he10_taxonomy_complete,
  ),
]


def run_case(case: EvalCase) -> EvalResult:
  """执行单题并判定是否符合 expect_errors。"""
  try:
    errs = case.run()
  except Exception as exc:  # noqa: BLE001 — eval 须吞异常并计失败
    return EvalResult(
      id=case.id,
      name=case.name,
      ok=False,
      expect_errors=case.expect_errors,
      error_count=1,
      detail=f"EXCEPTION: {exc}",
      taxonomy=case.taxonomy,
    )
  has_err = bool(errs)
  ok = has_err if case.expect_errors else not has_err
  detail = "; ".join(errs[:3]) if errs else "no errors"
  if len(errs) > 3:
    detail += f" …(+{len(errs) - 3})"
  return EvalResult(
    id=case.id,
    name=case.name,
    ok=ok,
    expect_errors=case.expect_errors,
    error_count=len(errs),
    detail=detail,
    taxonomy=case.taxonomy,
  )


def run_all(*, case_ids: set[str] | None = None) -> list[EvalResult]:
  """跑全部或指定 HE-ID。"""
  out: list[EvalResult] = []
  for case in CASES:
    if case_ids and case.id not in case_ids:
      continue
    out.append(run_case(case))
  return out


def summary_line(results: list[EvalResult]) -> str:
  """一行汇总。"""
  passed = sum(1 for r in results if r.ok)
  return f"harness-eval {passed}/{len(results)} passed"
