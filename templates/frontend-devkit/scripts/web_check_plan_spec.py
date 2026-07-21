"""WEB plan / step-stop 结构门禁（stdlib）。

作用：校验 plan v2 表格与 step-stop 运行时证据（WEB 等价后端 check_plan_spec）。
业务关联：WEB-DEV-GATES · plan-template · step-stop-template
上游：web_gate plan/step · web_harness_eval
下游：阻断残缺 plan / 无证据停机
"""
from __future__ import annotations

import re
from pathlib import Path

STEP_HEAD_RE = re.compile(r"^###\s+Step\s+(\d+)\b", re.MULTILINE | re.IGNORECASE)
FORBIDDEN_UI = re.compile(r"待实现|未知|未确认")


def check_plan_structure(path: Path, text: str) -> list[str]:
  """plan 须含 Step 总览 + ### Step N + 路径/验收。"""
  errors: list[str] = []
  if not re.search(r"##\s*4[\.．]?\s*.*Step\s*总览|##\s*Step\s*总览", text, re.I):
    if not re.search(r"##\s*Step\s*列表", text, re.I):
      errors.append(f"{path.name}: 缺少「Step 总览」或「Step 列表」节")
  steps = list(STEP_HEAD_RE.finditer(text))
  if not steps:
    errors.append(f"{path.name}: 缺少「### Step N」展开")
    return errors
  for i, m in enumerate(steps):
    start = m.start()
    end = steps[i + 1].start() if i + 1 < len(steps) else len(text)
    chunk = text[start:end]
    n = m.group(1)
    if not re.search(r"路径|文件|src/", chunk):
      errors.append(f"{path.name}: Step {n} 缺少路径/文件说明")
    if not re.search(r"验收|AC|vitest|harness|boundary", chunk, re.I):
      errors.append(f"{path.name}: Step {n} 缺少验收盘说明")
  return errors


def check_plan_materials(path: Path, text: str) -> list[str]:
  """新功能须材料准入非 N/A。"""
  errors: list[str] = []
  type_m = re.search(r"\*\*类型\*\*[：:]\s*(.+)", text)
  type_val = type_m.group(1).strip() if type_m else ""
  mat_m = re.search(r"\*\*材料准入\*\*[：:]\s*(.+)", text)
  mat_val = mat_m.group(1).strip() if mat_m else ""
  if "新功能" in type_val:
    if not mat_val or mat_val.upper().startswith("N/A"):
      errors.append(f"{path.name}: 类型=新功能 禁止「材料准入：N/A」")
    else:
      ref = mat_val.strip("`").strip()
      cand = path.parent / Path(ref).name
      if not cand.is_file() and not (path.parent / ref).is_file():
        # 允许相对 App 的路径在 gate 阶段再查；此处仅拦空
        if "materials-" not in ref:
          errors.append(f"{path.name}: 材料准入须指向 materials-*.md")
  return errors


def check_plan_ui(path: Path, text: str) -> list[str]:
  """命中 UI 对账时禁止待实现。"""
  hit = re.search(
    r"命中\*?\*?判定\*?\*?[：:]\s*\*?\*?\s*(是|否)",
    text,
  )
  if not hit or hit.group(1) != "是":
    return []
  if FORBIDDEN_UI.search(text):
    return [f"{path.name}: UI 命中=是 仍含「待实现/未知/未确认」"]
  return []


def check_step_stop_runtime_evidence(path: Path) -> list[str]:
  """step-stop 须含运行时证据或 N/A。"""
  text = path.read_text(encoding="utf-8")
  if "运行时证据" not in text:
    return [
      f"{path.name}: 缺少「运行时证据」（pnpm/vitest/截图/activate 摘要或 N/A+理由）"
      " — WFT-RUNTIME-EVIDENCE"
    ]
  if re.search(r"运行时证据\s*[：:]\s*N/?A", text, re.I):
    return []
  if re.search(r"运行时证据[\s\S]{0,400}N/?A", text, re.I):
    return []
  if re.search(
    r"vitest|playwright|activate|pnpm |https?://|\.png|截图|PASS",
    text,
    re.I,
  ):
    return []
  return [f"{path.name}: 「运行时证据」须含 N/A+理由或可复检痕迹"]


def check_step_stop_self_check(path: Path) -> list[str]:
  """step-stop 须含自检表（层界/追踪链 + 表格）。"""
  text = path.read_text(encoding="utf-8")
  if "层界" not in text and "追踪链" not in text:
    return [f"{path.name}: 缺少自检表（须含层界/追踪链等项）"]
  if "|" not in text:
    return [f"{path.name}: 自检须为表格"]
  return []


def validate_plan_file(path: Path) -> list[str]:
  """完整校验单个 plan。"""
  text = path.read_text(encoding="utf-8")
  errs: list[str] = []
  errs.extend(check_plan_structure(path, text))
  errs.extend(check_plan_materials(path, text))
  errs.extend(check_plan_ui(path, text))
  return errs
