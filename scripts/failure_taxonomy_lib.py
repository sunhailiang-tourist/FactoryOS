"""失败税则（Failure Taxonomy）· Harness 自进化回灌真源。

作用：把 Test/Verify/门禁失败归类为稳定 FT-* 码，并指向可回灌的契约/规则/脚本。
业务关联：L4 P0「失败分类→回写 harness」，禁止只修业务码不升门禁。
上游：Verify/Test 落盘 · gate step 失败输出 · harness-eval
下游：templates/harness-feedback-pr-template.md · FAILURE-TAXONOMY.md
关联文档：.cursor/factoryos/FAILURE-TAXONOMY.md
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_MD = ROOT / ".cursor" / "factoryos" / "FAILURE-TAXONOMY.md"

# 稳定税则表（代码即真源；Markdown 为人类可读镜像）
TAXONOMY: dict[str, dict[str, str]] = {
  "FT-MATERIALS-MISSING": {
    "summary": "材料准入缺失或新功能滥用 N/A",
    "detect": "materials.ok 缺失 · check_materials · HE-03/04/09",
    "feedback": "STEP0.md §材料准入 · gate materials · protect-paths",
  },
  "FT-STAMP-CHAIN": {
    "summary": "四重 stamp 垂直链断裂或伪造",
    "detect": "plan_gate_lib.validate_* · protect-paths",
    "feedback": "GATES.md · plan_gate_lib · gate_cli",
  },
  "FT-PLAN-STRUCTURE": {
    "summary": "plan v2 缺总览/Step 详表",
    "detect": "check_plan_spec.check_structure_v2 · HE-01/02",
    "feedback": "plan-template.md · DEV-GATES Gate 3",
  },
  "FT-PLAN-UI": {
    "summary": "UI 对账命中但状态非法/缺表",
    "detect": "check_plan_spec.check_ui_reconcile · HE-05",
    "feedback": "STEP0 UI 门禁 · plan §8",
  },
  "FT-STEP-STOP-UI": {
    "summary": "step-stop 缺 UI 字段对账",
    "detect": "step_chain_lib.check_step_stop_ui_gate · HE-06",
    "feedback": "step-stop-template.md · DEV-GATES",
  },
  "FT-RUNTIME-EVIDENCE": {
    "summary": "step-stop 缺运行时证据合同",
    "detect": "step_chain_lib.check_step_stop_runtime_evidence · HE-07",
    "feedback": "step-stop-template §运行时证据 · gate step",
  },
  "FT-TEST-FAIL": {
    "summary": "Test 单步/终轮结论非通过或缺落盘",
    "detect": "check_test_regression · step_chain_lib.validate_step_test_done",
    "feedback": "TEST-GATES.md · test-*-regression.md",
  },
  "FT-VERIFY-BLOCK": {
    "summary": "Verify 阻断/需改进被当成通过",
    "detect": "check_conclusion · HE-08",
    "feedback": "VERIFY-GATES.md · check_verify.py",
  },
  "FT-CONTRACT-AC": {
    "summary": "AC/OpenAPI 与 plan 不对账",
    "detect": "check_plan_spec.check_contracts",
    "feedback": "contracts/acceptance · OpenAPI export",
  },
  "FT-SENSOR-LINT": {
    "summary": "PostToolUse 传感器发现语法/静态问题",
    "detect": "post-edit-sensor.py · sensor_scoped_check.py",
    "feedback": "强化 ruff 修复说明书 · scoped pytest",
  },
  "FT-TAXONOMY": {
    "summary": "税则表自身不完整（meta）",
    "detect": "validate_taxonomy_integrity · HE-10",
    "feedback": "failure_taxonomy_lib.TAXONOMY · FAILURE-TAXONOMY.md",
  },
  "FT-HARNESS-DRIFT": {
    "summary": "文档死链/过期 draft/规则漂移",
    "detect": "harness_gc.py",
    "feedback": "INDEX.md · HARNESS-SCRIPTS · 删除死引用",
  },
}


@dataclass(frozen=True)
class TaxonomyEntry:
  """单条失败税则。"""

  code: str
  summary: str
  detect: str
  feedback: str


def all_entries() -> list[TaxonomyEntry]:
  """列出全部税则。"""
  return [
    TaxonomyEntry(
      code=code,
      summary=meta["summary"],
      detect=meta["detect"],
      feedback=meta["feedback"],
    )
    for code, meta in sorted(TAXONOMY.items())
  ]


def lookup(code: str) -> TaxonomyEntry | None:
  """按 FT-* 查询。"""
  meta = TAXONOMY.get(code)
  if not meta:
    return None
  return TaxonomyEntry(
    code=code,
    summary=meta["summary"],
    detect=meta["detect"],
    feedback=meta["feedback"],
  )


def classify_from_text(text: str) -> list[str]:
  """从失败日志/Verify 正文启发式归类（可多码）。

  功能：给 Agent/人一个稳定码，便于回灌 PR。
  """
  hits: list[str] = []
  rules = (
    ("materials.ok", "FT-MATERIALS-MISSING"),
    ("材料准入", "FT-MATERIALS-MISSING"),
    ("plan.ok", "FT-STAMP-CHAIN"),
    ("code.ok", "FT-STAMP-CHAIN"),
    ("Step 总览", "FT-PLAN-STRUCTURE"),
    ("待实现", "FT-PLAN-UI"),
    ("UI字段对账", "FT-STEP-STOP-UI"),
    ("运行时证据", "FT-RUNTIME-EVIDENCE"),
    ("结论：阻断", "FT-VERIFY-BLOCK"),
    ("结论：需改进", "FT-VERIFY-BLOCK"),
    ("contracts/acceptance", "FT-CONTRACT-AC"),
    ("ruff", "FT-SENSOR-LINT"),
    ("SyntaxError", "FT-SENSOR-LINT"),
  )
  for needle, code in rules:
    if needle in text and code not in hits:
      hits.append(code)
  return hits


def validate_taxonomy_integrity() -> list[str]:
  """税则完整性：每项须有 summary/detect/feedback；Markdown 镜像存在。"""
  errors: list[str] = []
  if len(TAXONOMY) < 10:
    errors.append(f"TAXONOMY 条目过少：{len(TAXONOMY)} < 10")
  for code, meta in TAXONOMY.items():
    if not code.startswith("FT-"):
      errors.append(f"{code}: 码须以 FT- 开头")
    for key in ("summary", "detect", "feedback"):
      val = (meta.get(key) or "").strip()
      if len(val) < 4:
        errors.append(f"{code}: 缺 {key} 或过短")
  if not TAXONOMY_MD.is_file():
    errors.append(f"缺少人类镜像：{TAXONOMY_MD.relative_to(ROOT)}")
  else:
    text = TAXONOMY_MD.read_text(encoding="utf-8")
    for code in TAXONOMY:
      if code not in text:
        errors.append(f"{TAXONOMY_MD.name}: 未登记 {code}")
  return errors


def format_feedback_stub(codes: list[str], *, evidence: str = "") -> str:
  """生成回灌 PR 草稿正文片段。"""
  lines = ["## Harness 回灌（自动草稿）", "", f"税则：{', '.join(codes) or '（未识别）'}", ""]
  for code in codes:
    entry = lookup(code)
    if not entry:
      continue
    lines.append(f"### {code} — {entry.summary}")
    lines.append(f"- 检测面：{entry.detect}")
    lines.append(f"- 建议回灌：{entry.feedback}")
    lines.append("")
  if evidence:
    lines.append("## 证据摘录")
    lines.append("```")
    lines.append(evidence[:2000])
    lines.append("```")
  return "\n".join(lines)
