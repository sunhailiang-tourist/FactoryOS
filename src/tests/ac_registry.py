"""AC-BASE-001 ID 注册表（从 contracts 验收文档解析）。"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ACCEPTANCE = ROOT / "contracts" / "acceptance" / "验收用例-BASE-001-平台底座.md"


def load_ac_ids() -> list[str]:
  if not ACCEPTANCE.is_file():
    return []
  text = ACCEPTANCE.read_text(encoding="utf-8")
  return sorted(set(re.findall(r"\b([A-Z]-\d{2})\b", text)))
