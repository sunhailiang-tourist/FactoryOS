"""前端 App contracts/README ↔ registry 对账库（DevKit harness 共用）。"""
from __future__ import annotations

import re
from pathlib import Path

REQUIRED_MODULE_SECTIONS = ("## 是什么", "## 追踪链", "## 开发说明", "## 变更规则")
REQUIRED_SECTOR_SECTIONS = ("## 是什么", "## 登记索引", "## 变更规则")

ROUTE_NAME = re.compile(r'name:\s*"([^"]+)"')
ROUTE_MODULE_ID = re.compile(r'moduleId:\s*"([^"]+)"')
ROUTE_LAYOUT = re.compile(r'layoutId:\s*"([^"]+)"')
ROUTE_PATH = re.compile(r'path:\s*"([^"]+)"')
ROUTE_INDEX = re.compile(r"\bindex:\s*true\b")
LAYOUT_PREFIX = re.compile(r'pathPrefix:\s*"([^"]+)"')
LAYOUT_ID = re.compile(r'\bid:\s*"([^"]+)"')
STORE_KEY = re.compile(r'key:\s*"([^"]+)"')
API_ID = re.compile(r'\bid:\s*"([^"]+)"')
CONFIG_ID = re.compile(r'\bid:\s*"([^"]+)"')
TRACKING_TABLE_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|\s*$", re.MULTILINE)
REGISTRY_INDEX_ROW = re.compile(
  r"^\|\s*`?([a-z0-9][a-z0-9.-]*)`?\s*\|\s*.+\|\s*$",
  re.MULTILINE,
)
SKIP_INDEX_IDS = frozenset({"module-id", "domain-id", "config-id", "domain", "项"})

# 对齐 docs/文档/架构/编码绝对门禁.md §3.2 + web-admin 扩展「怎么用 / 解决」
REQUIRED_FILE_HEADER_LABELS = (
  "模块",
  "作用",
  "怎么用",
  "解决",
  "上游",
  "下游",
  "关联",
)
HEADER_EXCLUDE_FILENAMES = frozenset({"vite-env.d.ts"})


def normalize_cell(raw: str) -> str:
  """追踪链单元格归一：去反引号 · 截断 → 后缀说明。"""
  value = raw.strip().strip("`")
  if "→" in value:
    value = value.split("→", 1)[0].strip().strip("`")
  return value


def parse_tracking_table(text: str) -> dict[str, str]:
  """解析 ## 追踪链 表格为 {项: 值}。"""
  start = text.find("## 追踪链")
  if start < 0:
    return {}
  section = text[start:]
  next_heading = section.find("\n## ", 4)
  if next_heading > 0:
    section = section[:next_heading]
  rows: dict[str, str] = {}
  for match in TRACKING_TABLE_ROW.finditer(section):
    key = match.group(1).strip().lower()
    if key in ("项", "----"):
      continue
    rows[key] = normalize_cell(match.group(2))
  return rows


def parse_registry_index(text: str) -> set[str]:
  """解析板块 ## 登记索引 表格第一列 id。"""
  start = text.find("## 登记索引")
  if start < 0:
    return set()
  section = text[start:]
  next_heading = section.find("\n## ", 4)
  if next_heading > 0:
    section = section[:next_heading]
  ids: set[str] = set()
  for line in section.splitlines():
    match = REGISTRY_INDEX_ROW.match(line.strip())
    if not match:
      continue
    entry_id = match.group(1)
    if entry_id in SKIP_INDEX_IDS:
      continue
    ids.add(entry_id)
  return ids


def parse_route_entry(reg_text: str) -> dict[str, str | bool]:
  """从 router/modules/{id}/registry.ts 提取首条路由元数据。"""
  return {
    "name": ROUTE_NAME.search(reg_text).group(1) if ROUTE_NAME.search(reg_text) else "",
    "moduleId": ROUTE_MODULE_ID.search(reg_text).group(1) if ROUTE_MODULE_ID.search(reg_text) else "",
    "layoutId": ROUTE_LAYOUT.search(reg_text).group(1) if ROUTE_LAYOUT.search(reg_text) else "",
    "path": ROUTE_PATH.search(reg_text).group(1) if ROUTE_PATH.search(reg_text) else "",
    "index": bool(ROUTE_INDEX.search(reg_text)),
  }


def load_layout_prefixes(layout_modules: Path) -> dict[str, str]:
  """layoutId → pathPrefix。"""
  prefixes: dict[str, str] = {}
  if not layout_modules.is_dir():
    return prefixes
  for reg in layout_modules.glob("*/registry.ts"):
    text = reg.read_text(encoding="utf-8")
    layout_id = LAYOUT_ID.search(text)
    prefix = LAYOUT_PREFIX.search(text)
    if layout_id and prefix:
      prefixes[layout_id.group(1)] = prefix.group(1)
  return prefixes


def compute_route_path(route: dict[str, str | bool], prefixes: dict[str, str]) -> str:
  """由 layout pathPrefix + route path/index 计算契约 path。"""
  layout_id = str(route.get("layoutId") or "")
  prefix = prefixes.get(layout_id, "")
  if route.get("index"):
    return prefix or "/"
  segment = str(route.get("path") or "").strip("/")
  if not prefix:
    return f"/{segment}" if segment else "/"
  return prefix if not segment else f"{prefix}/{segment}"


def contract_mentions(haystack: str, needle: str) -> bool:
  """契约正文是否包含某 api id / store key（允许表格或正文）。"""
  return needle in haystack


def missing_sections(text: str, required: tuple[str, ...]) -> list[str]:
  return [section for section in required if section not in text]


def _header_has_label(header: str, label: str) -> bool:
  """JSDoc 行内须含「标签：」或「标签:」。"""
  return f"{label}：" in header or f"{label}:" in header


def parse_file_header(text: str) -> tuple[str | None, list[str]]:
  """返回 (header 块或 None, 缺失标签列表)。闭合行须为单独的 `*/`。"""
  stripped = text.lstrip("\ufeff").lstrip()
  lines = stripped.splitlines()
  if not lines or not lines[0].strip().startswith("/**"):
    return None, list(REQUIRED_FILE_HEADER_LABELS)

  header_lines = [lines[0]]
  close_idx: int | None = None
  for i in range(1, len(lines)):
    line = lines[i]
    if line.strip() == "*/":
      header_lines.append(line)
      close_idx = i
      break
    if line.lstrip().startswith("*") or not line.strip():
      header_lines.append(line)
      continue
    break

  if close_idx is None:
    return None, list(REQUIRED_FILE_HEADER_LABELS)

  header = "\n".join(header_lines)
  for line in header_lines[1:-1]:
    if "*/" in line or line.strip().startswith("*") and "*" in line.lstrip()[1:]:
      # 行内 */ 会破坏 TS 块注释；行内裸 * 亦易误触
      if "*/" in line:
        missing = list(REQUIRED_FILE_HEADER_LABELS) + ["FORBIDDEN_COMMENT_CLOSE"]
        return header, missing
  missing = [
    label for label in REQUIRED_FILE_HEADER_LABELS if not _header_has_label(header, label)
  ]
  return header, missing


def file_header_valid(text: str) -> bool:
  """源文件顶部 block comment 是否含全部必含标签。"""
  _, missing = parse_file_header(text)
  return not missing
