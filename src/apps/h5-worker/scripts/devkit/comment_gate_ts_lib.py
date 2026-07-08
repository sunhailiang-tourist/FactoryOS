"""TypeScript/JavaScript 注释门禁（对齐 server comment_gate_lib · 编码绝对门禁 §3）。

作用：web-admin / h5-worker harness 复用。
业务关联：前端 DevKit activate · check_harness。
上游：frontend_contract_lib.REQUIRED_FILE_HEADER_LABELS
下游：check_harness.py · devkit.profile
"""
from __future__ import annotations

import re
from pathlib import Path

# 与 Python comment_gate_lib 对齐的导出函数 doc 关键词
FUNC_BUSINESS_MARKERS = ("功能", "业务", "业务含义", "作用")
FUNC_CHAIN_MARKERS = ("上游", "下游", "参数", "返回", "异常", "怎么用", "解决")
THROW_DOC_MARKERS = ("异常", "Error", "throw", "PlatformError", "错误")

EXPORT_FN = re.compile(
  r"/\*\*([\s\S]*?)\*/\s*export\s+(?:async\s+)?function\s+(\w+)",
  re.MULTILINE,
)
EXPORT_FN_BARE = re.compile(
  r"\bexport\s+(?:async\s+)?function\s+(\w+)",
  re.MULTILINE,
)
THROW_PATTERN = re.compile(r"\bthrow\s+new\s+\w+Error\b|\bthrow\s+\w+")
BLOCK_COMMENT_MIN_LINES = 10

# 生成代码 / 声明文件跳过
SKIP_PATH_PARTS = (
  "api/generated/",
  ".d.ts",
  "vite-env.d.ts",
  "node_modules/",
)


def _should_skip(path: Path) -> bool:
  posix = path.as_posix()
  return any(part in posix for part in SKIP_PATH_PARTS)


def _parse_jsdoc(block: str) -> str:
  lines = []
  for line in block.splitlines():
    s = line.strip().lstrip("*").strip()
    if s and not s.startswith("/"):
      lines.append(s)
  return "\n".join(lines)


def _export_functions(text: str) -> list[tuple[str, str | None, int]]:
  """返回 [(name, doc_or_none, line_approx)]。"""
  documented: dict[str, tuple[str | None, int]] = {}
  for m in EXPORT_FN.finditer(text):
    doc = _parse_jsdoc(m.group(1))
    name = m.group(2)
    line = text[: m.start()].count("\n") + 1
    documented[name] = (doc, line)

  out: list[tuple[str, str | None, int]] = [
    (name, doc, line) for name, (doc, line) in documented.items()
  ]
  for m in EXPORT_FN_BARE.finditer(text):
    name = m.group(1)
    if name in documented:
      continue
    line = text[: m.start()].count("\n") + 1
    out.append((name, None, line))
  return out


def _fn_body_lines(text: str, start_pos: int) -> list[str]:
  """从 export function 起粗略取函数体行（brace 计数）。"""
  sub = text[start_pos:]
  brace = 0
  started = False
  lines: list[str] = []
  for line in sub.splitlines():
    if "{" in line:
      brace += line.count("{")
      started = True
    if started:
      lines.append(line)
      brace -= line.count("}")
      if started and brace <= 0 and len(lines) > 1:
        break
  return lines


def _has_block_comment(body_lines: list[str]) -> bool:
  for line in body_lines:
    s = line.strip()
    if s.startswith("//") and len(s) > 4:
      payload = s[2:].strip()
      if len(payload) >= 6 or re.search(r"[\u4e00-\u9fff]", payload):
        return True
  return False


def _executable_line_count(body_lines: list[str]) -> int:
  count = 0
  for line in body_lines:
    s = line.strip()
    if not s or s in ("{", "}"):
      continue
    if s.startswith("//"):
      continue
    count += 1
  return count


def check_ts_file(path: Path, text: str) -> list[str]:
  """单文件 TS/TSX 注释规则（P0 文件头由 harness 另检）。"""
  errors: list[str] = []
  rel = str(path)

  for name, doc, line in _export_functions(text):
    if doc is None or not doc.strip():
      errors.append(f"{rel}:{line}: {name} — exported function missing JSDoc")
      continue
    if not any(m in doc for m in FUNC_BUSINESS_MARKERS):
      errors.append(f"{rel}:{line}: {name} — JSDoc missing 功能/业务/作用")
    if not any(m in doc for m in FUNC_CHAIN_MARKERS):
      errors.append(f"{rel}:{line}: {name} — JSDoc missing 上游/下游/怎么用")

  # P2/P3：带 JSDoc 的 export function 体
  for m in EXPORT_FN.finditer(text):
    name = m.group(2)
    doc = _parse_jsdoc(m.group(1))
    body_start = m.end()
    body_lines = _fn_body_lines(text, body_start)
    if _executable_line_count(body_lines) >= BLOCK_COMMENT_MIN_LINES:
      if not _has_block_comment(body_lines):
        line = text[: m.start()].count("\n") + 1
        errors.append(
          f"{rel}:{line}: {name} — complex body missing // block comment"
        )
    body_text = "\n".join(body_lines)
    if THROW_PATTERN.search(body_text) and not any(
      t in doc for t in THROW_DOC_MARKERS
    ):
      line = text[: m.start()].count("\n") + 1
      errors.append(f"{rel}:{line}: {name} — throws but JSDoc missing 异常/Error")

  return errors


def check_tree(root: Path, *, suffixes: tuple[str, ...] = (".ts", ".tsx")) -> list[str]:
  errors: list[str] = []
  src = root / "src"
  if not src.is_dir():
    return errors
  for path in sorted(src.rglob("*")):
    if path.suffix not in suffixes:
      continue
    if _should_skip(path):
      continue
    text = path.read_text(encoding="utf-8")
    errors.extend(check_ts_file(path, text))
  return errors
