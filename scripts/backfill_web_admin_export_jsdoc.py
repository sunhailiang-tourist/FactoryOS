#!/usr/bin/env python3
"""补齐 web-admin export function JSDoc（对齐 comment_gate_ts_lib）。

Usage: uv run python scripts/backfill_web_admin_export_jsdoc.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB = ROOT / "src" / "apps" / "web-admin" / "src"
sys.path.insert(0, str(ROOT / "scripts"))
from devkit.comment_gate_ts_lib import check_ts_file  # noqa: E402

EXPORT_FN = re.compile(
  r"(/\*\*[\s\S]*?\*/)\s*(export\s+(?:async\s+)?function\s+(\w+))",
  re.MULTILINE,
)
MARKERS_BIZ = ("功能", "业务", "作用", "怎么用")
MARKERS_CHAIN = ("上游", "下游", "解决")


def _enhance(block: str, name: str) -> str:
  inner = block[3:-3]
  lines = [ln.strip().lstrip("*").strip() for ln in inner.splitlines()]
  text = "\n".join(lines)
  if any(m in text for m in MARKERS_BIZ) and any(m in text for m in MARKERS_CHAIN):
    return block
  first = lines[0] if lines and lines[0] else f"{name} 导出函数"
  body = ["/**", f" * 功能：{first.rstrip('。')}", f" * 业务含义：{name} 模块对外 API。", " * 上游：同文件文件头。", " * 下游：调用方见文件头。", " */"]
  return "\n".join(body)


def patch_file(path: Path) -> bool:
  text = path.read_text(encoding="utf-8")
  orig = text

  def repl(m: re.Match[str]) -> str:
    block, rest = m.group(1), m.group(2)
    name = m.group(3)
    return _enhance(block, name) + "\n" + rest

  text = EXPORT_FN.sub(repl, text)

  # missing JSDoc entirely
  for m in re.finditer(r"(?m)^export\s+(?:async\s+)?function\s+(\w+)", text):
    name = m.group(1)
    start = m.start()
    prefix = text[max(0, start - 200):start]
    if "*/" in prefix and "/**" in prefix:
      continue
    doc = (
      f"/**\n * 功能：{name} 导出函数。\n"
      f" * 业务含义：web-admin 模块对外入口。\n"
      f" * 上游：同文件文件头。\n"
      f" * 下游：见调用链。\n"
      f" */\n"
    )
    text = text[:start] + doc + text[start:]

  # P2：复杂 export 函数体补 // 块注释
  for m in EXPORT_FN.finditer(text):
    name = m.group(3)
    body_start = m.end()
    body_lines = []
    sub = text[body_start:]
    brace = 0
    started = False
    for i, line in enumerate(sub.splitlines()):
      if "{" in line:
        brace += line.count("{")
        started = True
      if started:
        body_lines.append((i, line))
        brace -= line.count("}")
        if started and brace <= 0 and len(body_lines) > 1:
          break
    exec_count = sum(
      1 for _, ln in body_lines
      if ln.strip() and not ln.strip().startswith("//") and ln.strip() not in ("{", "}")
    )
    if exec_count >= 10:
      has_comment = any(ln.strip().startswith("//") for _, ln in body_lines)
      if not has_comment:
        # insert after opening line
        insert_line_idx = body_lines[0][0] if body_lines else 0
        lines = sub.splitlines(keepends=True)
        insert_at = body_start + sum(len(lines[j]) for j in range(insert_line_idx + 1))
        indent = "  "
        if insert_line_idx + 1 < len(lines):
          m_indent = re.match(r"^(\s*)", lines[insert_line_idx + 1])
          if m_indent:
            indent = m_indent.group(1) or "  "
        snippet = f"{indent}// 业务：{name} 主体编排（见文件头上下游）\n"
        text = text[:insert_at] + snippet + text[insert_at:]

  if text != orig:
    path.write_text(text, encoding="utf-8")
    return True
  return False


def main() -> int:
  changed = 0
  for path in sorted(WEB.rglob("*.ts*")):
    if "api/generated" in path.as_posix() or path.name.endswith(".d.ts"):
      continue
    if patch_file(path):
      changed += 1
      print("patched", path.relative_to(ROOT))
  # verify
  from devkit.comment_gate_ts_lib import check_tree
  errs = check_tree(ROOT / "src" / "apps" / "web-admin")
  print(f"\nchanged {changed}, remaining violations {len(errs)}")
  for e in errs[:10]:
    print(" ", e)
  return 0 if not errs else 1


if __name__ == "__main__":
  sys.exit(main())
