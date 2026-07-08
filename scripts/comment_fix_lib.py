"""注释自动补齐库（CMNT-C · 仅补缺失项）。

作用：为 comment_fix.py 提供 Python/TS 骨架补齐。
业务关联：双速双严 · 与 check_comments 同范围。
上游：comment_gate_lib · backfill 脚本逻辑
下游：comment_fix.py
"""
from __future__ import annotations

import ast
import re
from pathlib import Path

import comment_gate_lib as cg

ROOT = Path(__file__).resolve().parents[1]

TS_EXPORT_FN = re.compile(
  r"(/\*\*[\s\S]*?\*/)\s*(export\s+(?:async\s+)?function\s+(\w+))",
  re.MULTILINE,
)
TS_EXPORT_BARE = re.compile(r"(?m)^export\s+(?:async\s+)?function\s+(\w+)")


def _rel_posix(path: Path) -> str:
  try:
    return path.relative_to(ROOT).as_posix()
  except ValueError:
    return path.as_posix()


def _generic_py_module_doc(rel: str) -> str:
  return (
    f'"""\n'
    f"模块：{rel}\n"
    f"作用：本文件在 server 业务链中的职责（待按业务润色）。\n"
    f"业务关联：FactoryOS server 实现。\n"
    f"上游：见同目录 README 与调用方。\n"
    f"下游：见被调方与 os_core 服务层。\n"
    f'"""\n\n'
  )


def _generic_py_func_doc(name: str) -> str:
  return (
    f'  """\n'
    f"  功能：{name} 业务处理。\n"
    f"  业务含义：见模块文件头（待润色）。\n"
    f"  上游：见文件头上游。\n"
    f"  下游：见文件头下游。\n"
    f"  参数：见函数签名。\n"
    f"  返回：见类型注解。\n"
    f"  异常：见实现与 PlatformError。\n"
    f'  """\n'
  )


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


def _insert_py_block_comment(source: str, node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
  """在复杂函数体首行插入 # 块注释。"""
  lines = source.splitlines(keepends=True)
  if not node.body:
    return source
  insert_at = node.body[0].lineno - 1
  indent = "  "
  if insert_at < len(lines):
    m = re.match(r"^(\s*)", lines[insert_at])
    if m and m.group(1):
      indent = m.group(1)
  snippet = f"{indent}# 业务：{node.name} 主体编排（见文件头上下游）\n"
  lines.insert(insert_at, snippet)
  return "".join(lines)


def _add_py_field_descriptions(source: str, tree: ast.Module) -> str:
  """为缺 description 的 Field() 补上 description 关键字。"""
  lines = source.splitlines()
  changed = False
  for node in ast.walk(tree):
    if not isinstance(node, ast.ClassDef):
      continue
    if not cg._is_basemodel_class(node):
      continue
    for item in node.body:
      if not isinstance(item, ast.AnnAssign) or not isinstance(item.target, ast.Name):
        continue
      if cg._field_description_ok(item):
        continue
      if item.lineno > len(lines):
        continue
      line = lines[item.lineno - 1]
      fname = item.target.id
      if "Field(" in line and "description=" not in line:
        lines[item.lineno - 1] = line.replace(
          "Field(",
          f'Field(description="{fname} 字段（待润色）", ',
          1,
        )
        changed = True
  return "\n".join(lines) + ("\n" if source.endswith("\n") else "") if changed else source


def fix_python_file(path: Path) -> bool:
  """补齐 Python 注释缺失项；有改动返回 True。"""
  try:
    text = path.read_text(encoding="utf-8")
  except OSError:
    return False
  orig = text
  rel = _rel_posix(path)

  try:
    tree = ast.parse(text, filename=str(path))
  except SyntaxError:
    return False

  if ast.get_docstring(tree, clean=False) is None:
    text = _generic_py_module_doc(rel) + text.lstrip()

  tree = ast.parse(text, filename=str(path))
  funcs = [
    n
    for n in tree.body
    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name != "main"
  ]
  lines = text.splitlines(keepends=True)
  for node in sorted(funcs, key=lambda n: n.lineno, reverse=True):
    fdoc = ast.get_docstring(node, clean=False)
    msgs = cg._func_doc_ok(node.name, fdoc, len(node.body))
    if not msgs or fdoc is not None:
      continue
    idx = node.lineno
    if idx <= len(lines):
      lines.insert(idx, _generic_py_func_doc(node.name))
      text = "".join(lines)

  text = _add_py_field_descriptions(text, ast.parse(text, filename=str(path)))
  tree = ast.parse(text, filename=str(path))

  for node in tree.body:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
      continue
    stmt_count = cg._count_executable_stmts(node.body)
    if stmt_count >= cg.BLOCK_COMMENT_MIN_STMTS and not cg._body_has_line_comment(text, node):
      text = _insert_py_block_comment(text, node)
      tree = ast.parse(text, filename=str(path))

  if text != orig:
    path.write_text(text, encoding="utf-8")
    return True
  return False


def fix_ts_file(path: Path) -> bool:
  """补齐 TS/TSX 文件头与 export JSDoc。"""
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
    if "*/" in prefix and "/**" in prefix.rsplit("*/", 1)[-1]:
      continue
    if prefix.rstrip().endswith("*/"):
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
