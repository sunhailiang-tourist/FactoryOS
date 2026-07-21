"""check_plan_spec v2 结构门禁单测（stdlib pytest · 不依赖 plan.ok）。

运行：
  uv run pytest scripts/test_check_plan_spec_v2.py -q
"""
from __future__ import annotations

import tempfile
from pathlib import Path

import check_plan_spec as cps
import step_chain_lib as scl

MIN_PLAN = """# 预开发说明：单测样例

- **类型**：Bug修复
- **材料准入**：N/A（单测）

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


def test_plan_v2_structure_ok(tmp_path: Path) -> None:
  p = tmp_path / "plan-0900-demo.md"
  p.write_text(MIN_PLAN, encoding="utf-8")
  assert cps.check_structure_v2(p, MIN_PLAN) == []
  assert cps.check_materials(p, MIN_PLAN) == []
  assert cps.check_ui_reconcile(p, MIN_PLAN) == []


def test_plan_missing_step_overview_fails(tmp_path: Path) -> None:
  text = MIN_PLAN.replace("## 4. Step 总览（必填 · 一眼看全部分步）", "## 4. 其他")
  p = tmp_path / "plan-bad.md"
  errs = cps.check_structure_v2(p, text)
  assert any("Step 总览" in e for e in errs)


def test_new_feature_requires_materials(tmp_path: Path) -> None:
  text = MIN_PLAN.replace("**类型**：Bug修复", "**类型**：新功能").replace(
    "**材料准入**：N/A（单测）", "**材料准入**：N/A"
  )
  p = tmp_path / "plan-nf.md"
  errs = cps.check_materials(p, text)
  assert any("新功能" in e and "N/A" in e for e in errs)


def test_new_feature_with_materials_file_ok(tmp_path: Path) -> None:
  mat = tmp_path / "materials-0900-demo.md"
  mat.write_text("# materials\n", encoding="utf-8")
  text = MIN_PLAN.replace("**类型**：Bug修复", "**类型**：新功能").replace(
    "**材料准入**：N/A（单测）", f"**材料准入**：`{mat.name}`"
  )
  p = tmp_path / "plan-nf-ok.md"
  p.write_text(text, encoding="utf-8")
  assert cps.check_materials(p, text) == []


def test_ui_hit_forbids_pending_status(tmp_path: Path) -> None:
  text = MIN_PLAN.replace(
    "## 8. UI / 原型字段对账\n\n- **命中判定**：否（无图）\n",
    "## 8. UI / 原型字段对账\n\n"
    "- **命中判定**：是\n\n"
    "### 8.1 界面字段表\n\n| 视图ID |\n|--------|\n| v1 |\n\n"
    "### 8.2 接口字段对账表\n\n"
    "| UI字段 | 路径 | Schema | 落点 | 状态 |\n"
    "|--------|------|--------|------|------|\n"
    "| a | data.a | A | api | 待实现 |\n",
  )
  p = tmp_path / "plan-ui.md"
  p.write_text(text, encoding="utf-8")
  errs = cps.check_ui_reconcile(p, text)
  assert any("待实现" in e or "未确认" in e for e in errs)


def test_step_stop_ui_gate() -> None:
  with tempfile.NamedTemporaryFile(
    "w", suffix=".md", delete=False, encoding="utf-8"
  ) as f:
    f.write("# stop\n| 10 | 注释 | |\n")
    path = Path(f.name)
  try:
    assert scl.check_step_stop_ui_gate(path)
  finally:
    path.unlink(missing_ok=True)

  with tempfile.NamedTemporaryFile(
    "w", suffix=".md", delete=False, encoding="utf-8"
  ) as f:
    f.write("# stop\n| 11 | UI字段对账（未命中填 N/A） | N/A |\n")
    path = Path(f.name)
  try:
    assert scl.check_step_stop_ui_gate(path) == []
  finally:
    path.unlink(missing_ok=True)


def test_step_stop_runtime_evidence_gate() -> None:
  with tempfile.NamedTemporaryFile(
    "w", suffix=".md", delete=False, encoding="utf-8"
  ) as f:
    f.write("# stop\n| 11 | UI字段对账 | N/A |\n")
    path = Path(f.name)
  try:
    assert scl.check_step_stop_runtime_evidence(path)
  finally:
    path.unlink(missing_ok=True)

  with tempfile.NamedTemporaryFile(
    "w", suffix=".md", delete=False, encoding="utf-8"
  ) as f:
    f.write("# stop\n- **运行时证据**：N/A（无服务）\n")
    path = Path(f.name)
  try:
    assert scl.check_step_stop_runtime_evidence(path) == []
  finally:
    path.unlink(missing_ok=True)


def test_materials_stamp_required() -> None:
  import plan_gate_lib as pgl

  backup = None
  gate = pgl.MATERIALS_GATE
  existed = gate.is_file()
  content = gate.read_text(encoding="utf-8") if existed else None
  try:
    if gate.is_file():
      gate.unlink()
    errs = pgl.validate_materials_stamp()
    assert any("materials.ok" in e for e in errs)
    pgl.write_materials_gate_stamp(mode="na", reason="Bug修复")
    assert pgl.validate_materials_stamp() == []
  finally:
    if content is not None:
      gate.write_text(content, encoding="utf-8")
    elif gate.is_file() and not existed:
      gate.unlink()


def test_materials_invalidates_plan_ok() -> None:
  import plan_gate_lib as pgl

  GATES = pgl.GATES_DIR
  GATES.mkdir(parents=True, exist_ok=True)
  backups = {}
  for p in (pgl.MATERIALS_GATE, pgl.PLAN_GATE, pgl.TEST_GATE, pgl.CODE_GATE):
    backups[p] = p.read_text(encoding="utf-8") if p.is_file() else None
  try:
    pgl.PLAN_GATE.write_text("plan=x\nat=z\n", encoding="utf-8")
    pgl.TEST_GATE.write_text("plan=x\ntest_plan=y\nat=z\n", encoding="utf-8")
    pgl.write_materials_gate_stamp(mode="na", reason="reset")
    assert pgl.MATERIALS_GATE.is_file()
    assert not pgl.PLAN_GATE.is_file()
    assert not pgl.TEST_GATE.is_file()
  finally:
    for p, c in backups.items():
      if c is None:
        if p.is_file():
          p.unlink()
      else:
        p.write_text(c, encoding="utf-8")
