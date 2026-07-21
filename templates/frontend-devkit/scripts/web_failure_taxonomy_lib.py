"""WEB 失败税则（独立 FT 码前缀 WFT-*）。

作用：失败归类 → 回灌 WEB 规则/脚本；不依赖后端 FAILURE-TAXONOMY。
关联文档：.cursor/factoryos/WEB-FAILURE-TAXONOMY.md
"""
from __future__ import annotations

from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_MD = APP_ROOT / ".cursor" / "factoryos" / "WEB-FAILURE-TAXONOMY.md"

TAXONOMY: dict[str, dict[str, str]] = {
  "WFT-MATERIALS-MISSING": {
    "summary": "材料准入缺失或新功能滥用 N/A",
    "detect": "web_plan_gate_lib · WHE-03",
    "feedback": "WEB-STEP0 · web_gate materials",
  },
  "WFT-STAMP-CHAIN": {
    "summary": "WEB 四重 stamp 断裂",
    "detect": "web_plan_gate_lib · protect-paths WEB 分支",
    "feedback": "WEB-GATES.md · web_gate_cli",
  },
  "WFT-PLAN-STRUCTURE": {
    "summary": "plan 缺 Step 总览/详表",
    "detect": "web_check_plan_spec · WHE-01",
    "feedback": "plan-template.md · WEB-DEV-GATES",
  },
  "WFT-PLAN-UI": {
    "summary": "UI 对账非法状态",
    "detect": "web_check_plan_spec.check_plan_ui",
    "feedback": "plan §UI · WEB-STEP0",
  },
  "WFT-RUNTIME-EVIDENCE": {
    "summary": "step-stop 缺运行时证据",
    "detect": "web_step_chain_lib · WHE-07",
    "feedback": "step-stop-template §运行时证据",
  },
  "WFT-TEST-FAIL": {
    "summary": "Test 结论非通过或缺落盘",
    "detect": "web_step_chain_lib.validate_step_test_done",
    "feedback": "WEB-TEST-GATES",
  },
  "WFT-VERIFY-BLOCK": {
    "summary": "Verify 阻断被当成通过",
    "detect": "check_conclusion · WHE-08",
    "feedback": "WEB-VERIFY-GATES",
  },
  "WFT-BOUNDARY": {
    "summary": "独立边界/架构锁失败",
    "detect": "check_boundary_lock · check_harness",
    "feedback": "WEB-00 · WEB-01 · WEB-ARCHITECTURE-LOCK",
  },
  "WFT-SENSOR-LINT": {
    "summary": "WEB 传感器发现 TS/语法问题",
    "detect": "post-edit-web-sensor · web_sensor_scoped_check",
    "feedback": "强化 eslint 修复说明书",
  },
  "WFT-TAXONOMY": {
    "summary": "税则表不完整",
    "detect": "validate_taxonomy_integrity · WHE-10",
    "feedback": "web_failure_taxonomy_lib · WEB-FAILURE-TAXONOMY.md",
  },
  "WFT-HARNESS-DRIFT": {
    "summary": "WEB 文档死链/过期 draft",
    "detect": "web_harness_gc",
    "feedback": "INDEX.md · WEB-HARNESS-EVAL",
  },
  "WFT-CLAIM-GREEN": {
    "summary": "未绿宣称通过",
    "detect": "WEB-REDLINES R-WEB-claim",
    "feedback": "activate.sh · check_harness",
  },
}


def validate_taxonomy_integrity() -> list[str]:
  """税则完整性。"""
  errors: list[str] = []
  if len(TAXONOMY) < 10:
    errors.append(f"TAXONOMY 过少: {len(TAXONOMY)}")
  for code, meta in TAXONOMY.items():
    if not code.startswith("WFT-"):
      errors.append(f"{code}: 须 WFT- 前缀")
    for key in ("summary", "detect", "feedback"):
      if len((meta.get(key) or "").strip()) < 4:
        errors.append(f"{code}: 缺 {key}")
  if not TAXONOMY_MD.is_file():
    errors.append(f"缺少 {TAXONOMY_MD.relative_to(APP_ROOT)}")
  else:
    text = TAXONOMY_MD.read_text(encoding="utf-8")
    for code in TAXONOMY:
      if code not in text:
        errors.append(f"{TAXONOMY_MD.name}: 未登记 {code}")
  return errors


def classify_from_text(text: str) -> list[str]:
  """启发式归类。"""
  hits: list[str] = []
  rules = (
    ("materials.ok", "WFT-MATERIALS-MISSING"),
    ("材料准入", "WFT-MATERIALS-MISSING"),
    ("plan.ok", "WFT-STAMP-CHAIN"),
    ("code.ok", "WFT-STAMP-CHAIN"),
    ("Step 总览", "WFT-PLAN-STRUCTURE"),
    ("运行时证据", "WFT-RUNTIME-EVIDENCE"),
    ("结论：阻断", "WFT-VERIFY-BLOCK"),
    ("boundary", "WFT-BOUNDARY"),
    ("确认越权", "WFT-BOUNDARY"),
    ("eslint", "WFT-SENSOR-LINT"),
  )
  for needle, code in rules:
    if needle in text and code not in hits:
      hits.append(code)
  return hits
