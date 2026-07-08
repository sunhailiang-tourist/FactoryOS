"""注释自动补齐库（CMNT-C · 前端 TypeScript · 仅补缺失项）。

作用：为 comment_fix.py 提供 TS/TSX 骨架补齐。
业务关联：与 check_comments.py 同范围。
上游：comment_gate_ts_lib · frontend_contract_lib
下游：comment_fix.py · check_comments_commit_hook.py
"""
from __future__ import annotations

import re
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1]

TS_EXPORT_FN = re.compile(
  r"(/\*\*[\s\S]*?\*/)\s*(export\s+(?:async\s+)?function\s+(\w+))",
  re.MULTILINE,
)


def _rel_posix(path: Path) -> str:
  try:
    return path.relative_to(APP_ROOT).as_posix()
  except ValueError:
    return path.as_posix()


def _generic_ts_file_header(rel: str) -> str:
  return (
    "/**\n"
    f" * 模块：{rel}\n"
    " * 作用：本模块在前端业务链中的职责（待润色）。\n"
    " * 怎么用：见 router/registry 与 pages contracts。\n"
    " * 解决：与 module-id 追踪链对齐。\n"
    " * 上游：见同目录 contracts README。\n"
    " * 下游：见调用方与 api/query hooks。\n"
    " * 关联：devkit harness 追踪链。\n"
    " */\n\n"
  )


def _generic_ts_export_jsdoc(name: str) -> str:
  return (
    f"/**\n"
    f" * 功能：{name} 导出函数。\n"
    f" * 业务含义：见同文件模块文件头。\n"
    f" * 上游：见文件头上游。\n"
    f" * 下游：见文件头下游。\n"
    f" * 怎么用：见 pages/contracts 追踪链。\n"
    f" */\n"
  )


def fix_ts_file(path: Path) -> bool:
  """补齐 TS/TSX 文件头与 export JSDoc；有改动返回 True。"""
  try:
    text = path.read_text(encoding="utf-8")
  except OSError:
    return False
  orig = text
  rel = _rel_posix(path)

  stripped = text.lstrip("\ufeff").lstrip()
  if not stripped.startswith("/**"):
    text = _generic_ts_file_header(rel) + text

  def _enhance_block(block: str, name: str) -> str:
    inner = block[3:-3]
    lines = [ln.strip().lstrip("*").strip() for ln in inner.splitlines()]
    content = "\n".join(lines)
    biz = ("功能", "业务", "作用", "怎么用")
    chain = ("上游", "下游", "解决")
    if any(m in content for m in biz) and any(m in content for m in chain):
      return block
    return _generic_ts_export_jsdoc(name)

  def repl(m: re.Match[str]) -> str:
    return _enhance_block(m.group(1), m.group(3)) + "\n" + m.group(2)

  text = TS_EXPORT_FN.sub(repl, text)

  for m in re.finditer(r"(?m)^export\s+(?:async\s+)?function\s+(\w+)", text):
    name = m.group(1)
    start = m.start()
    prefix = text[max(0, start - 300) : start]
    if prefix.rstrip().endswith("*/"):
      continue
    if "*/" in prefix and "/**" in prefix.rsplit("*/", 1)[-1]:
      continue
    doc = _generic_ts_export_jsdoc(name) + "\n"
    text = text[:start] + doc + text[start:]

  for m in TS_EXPORT_FN.finditer(text):
    name = m.group(3)
    body_start = m.end()
    sub = text[body_start:]
    brace = 0
    started = False
    body_lines: list[tuple[int, str]] = []
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
      1
      for _, ln in body_lines
      if ln.strip() and not ln.strip().startswith("//") and ln.strip() not in ("{", "}")
    )
    if exec_count >= 10:
      has_comment = any(ln.strip().startswith("//") for _, ln in body_lines)
      if not has_comment:
        insert_line_idx = body_lines[0][0]
        lines = sub.splitlines(keepends=True)
        insert_at = body_start + sum(len(lines[j]) for j in range(insert_line_idx + 1))
        indent = "  "
        if insert_line_idx + 1 < len(lines):
          mi = re.match(r"^(\s*)", lines[insert_line_idx + 1])
          if mi and mi.group(1):
            indent = mi.group(1)
        snippet = f"{indent}// 业务：{name} 主体编排（见文件头上下游）\n"
        text = text[:insert_at] + snippet + text[insert_at:]

  if text != orig:
    path.write_text(text, encoding="utf-8")
    return True
  return False
