#!/usr/bin/env python3
"""error-registry.yaml 解析与 mirror 集合 — check/sync 共用。

作用：SSOT 与 Python/TS mirror 对账真源（code + message_zh）。
业务关联：contracts/error-registry.yaml · 状态码与错误约定。
上游：PyYAML
下游：check_error_registry_sync · sync_error_registry
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "contracts" / "error-registry.yaml"
PYTHON_ENUM_PATH = ROOT / "src" / "server" / "os_core" / "shared_contracts" / "errors.py"
TS_CODES_PATH = ROOT / "src" / "apps" / "web-admin" / "src" / "api" / "request" / "error-codes.ts"

ENUM_MEMBER_RE = re.compile(r"^\s+([A-Z][A-Z0-9_]*)\s*=\s*\"([A-Z][A-Z0-9_]*)\"\s*$")
TS_KEY_RE = re.compile(r"^\s+([A-Z][A-Z0-9_]*):\s*\"([A-Z][A-Z0-9_]*)\"\s*,?\s*$")
PY_MSG_ZH_RE = re.compile(r'^\s+"([A-Z][A-Z0-9_]*)":\s+"(.*)",\s*$')
TS_MSG_ZH_RE = re.compile(r'^\s+([A-Z][A-Z0-9_]*):\s+"(.*)",\s*$')


@dataclass(frozen=True)
class ErrorRegistryEntry:
  """单条业务错误码元数据。"""

  code: str
  status: str
  mirror_python: bool
  mirror_typescript: bool
  http_default: int
  source: str
  domain: str
  message_zh: str


def load_registry(path: Path = REGISTRY_PATH) -> tuple[dict[str, Any], list[ErrorRegistryEntry]]:
  """加载 SSOT YAML。"""
  raw = yaml.safe_load(path.read_text(encoding="utf-8"))
  entries: list[ErrorRegistryEntry] = []
  for item in raw.get("codes") or []:
    entries.append(
      ErrorRegistryEntry(
        code=str(item["code"]),
        status=str(item.get("status", "active")),
        mirror_python=bool(item.get("mirror_python", False)),
        mirror_typescript=bool(item.get("mirror_typescript", False)),
        http_default=int(item.get("http_default", 500)),
        source=str(item.get("source", "B")),
        domain=str(item.get("domain", "platform")),
        message_zh=str(item.get("message_zh", "")),
      )
    )
  return raw, entries


def mirror_codes(entries: list[ErrorRegistryEntry], field: str) -> set[str]:
  """按 mirror_python / mirror_typescript 筛选应出现在 mirror 中的 code。"""
  out: set[str] = set()
  for entry in entries:
    if field == "mirror_python" and entry.mirror_python:
      out.add(entry.code)
    if field == "mirror_typescript" and entry.mirror_typescript:
      out.add(entry.code)
  return out


def expected_messages(entries: list[ErrorRegistryEntry], field: str) -> dict[str, str]:
  """SSOT 中应写入 mirror 的 code → message_zh。"""
  codes = mirror_codes(entries, field)
  out: dict[str, str] = {}
  for entry in entries:
    if entry.code in codes:
      out[entry.code] = entry.message_zh
  return out


def parse_python_enum(path: Path = PYTHON_ENUM_PATH) -> set[str]:
  """从 ErrorCode StrEnum 提取 code 字符串集合。"""
  codes: set[str] = set()
  for line in path.read_text(encoding="utf-8").splitlines():
    match = ENUM_MEMBER_RE.match(line)
    if match:
      name, value = match.group(1), match.group(2)
      if name != value:
        raise ValueError(f"{path}: enum 名与值须一致: {name} != {value}")
      codes.add(value)
  return codes


def parse_python_messages(path: Path = PYTHON_ENUM_PATH) -> dict[str, str]:
  """从 ERROR_MESSAGE_ZH 提取 code → 中文。"""
  messages: dict[str, str] = {}
  in_block = False
  for line in path.read_text(encoding="utf-8").splitlines():
    if line.startswith("ERROR_MESSAGE_ZH:"):
      in_block = True
      continue
    if in_block:
      if line.strip() == "}":
        break
      match = PY_MSG_ZH_RE.match(line)
      if match:
        messages[match.group(1)] = _unescape_py_string(match.group(2))
  return messages


def parse_typescript_codes(path: Path = TS_CODES_PATH) -> set[str]:
  """从 ERROR_CODES 常量对象提取 code 集合。"""
  if not path.is_file():
    return set()
  codes: set[str] = set()
  in_block = False
  for line in path.read_text(encoding="utf-8").splitlines():
    if "export const ERROR_CODES" in line:
      in_block = True
      continue
    if in_block:
      if line.strip().startswith("} as const"):
        break
      match = TS_KEY_RE.match(line)
      if match:
        key, value = match.group(1), match.group(2)
        if key != value:
          raise ValueError(f"{path}: TS key 与 value 须一致: {key} != {value}")
        codes.add(value)
  return codes


def parse_typescript_messages(path: Path = TS_CODES_PATH) -> dict[str, str]:
  """从 ERROR_MESSAGES_ZH 提取 code → 中文。"""
  if not path.is_file():
    return {}
  messages: dict[str, str] = {}
  in_block = False
  for line in path.read_text(encoding="utf-8").splitlines():
    if "export const ERROR_MESSAGES_ZH" in line:
      in_block = True
      continue
    if in_block:
      if line.strip().startswith("} as const"):
        break
      match = TS_MSG_ZH_RE.match(line)
      if match:
        messages[match.group(1)] = _unescape_ts_string(match.group(2))
  return messages


def _unescape_py_string(value: str) -> str:
  return value.encode("utf-8").decode("unicode_escape") if "\\" in value else value


def _unescape_ts_string(value: str) -> str:
  return (
    value.replace('\\"', '"')
    .replace("\\n", "\n")
    .replace("\\\\", "\\")
  )


def _escape_py_string(value: str) -> str:
  return value.replace("\\", "\\\\").replace('"', '\\"')


def _escape_ts_string(value: str) -> str:
  return value.replace("\\", "\\\\").replace('"', '\\"')


@dataclass
class DriftReport:
  """ADD / DELETE / CHANGE 对账结果。"""

  add_python: list[str]
  delete_python: list[str]
  add_typescript: list[str]
  delete_typescript: list[str]
  change_metadata: list[str]
  message_drift_python: list[str]
  message_drift_typescript: list[str]
  missing_message_zh: list[str]

  def has_drift(self) -> bool:
    return bool(
      self.add_python
      or self.delete_python
      or self.add_typescript
      or self.delete_typescript
      or self.change_metadata
      or self.message_drift_python
      or self.message_drift_typescript
      or self.missing_message_zh
    )

  def has_hard_fail(self) -> bool:
    return bool(
      self.add_python
      or self.delete_python
      or self.add_typescript
      or self.delete_typescript
      or self.message_drift_python
      or self.message_drift_typescript
      or self.missing_message_zh
    )


def compute_drift() -> DriftReport:
  """对比 SSOT 与 mirrors（code + message_zh）。"""
  meta, entries = load_registry()
  expected_py = mirror_codes(entries, "mirror_python")
  expected_ts = mirror_codes(entries, "mirror_typescript")
  actual_py = parse_python_enum() if PYTHON_ENUM_PATH.is_file() else set()
  actual_ts = parse_typescript_codes()

  add_py = sorted(expected_py - actual_py)
  del_py = sorted(actual_py - expected_py)
  add_ts = sorted(expected_ts - actual_ts)
  del_ts = sorted(actual_ts - expected_ts)

  exp_py_msg = expected_messages(entries, "mirror_python")
  exp_ts_msg = expected_messages(entries, "mirror_typescript")
  act_py_msg = parse_python_messages() if PYTHON_ENUM_PATH.is_file() else {}
  act_ts_msg = parse_typescript_messages()

  missing_zh = sorted(
    code
    for code, msg in exp_py_msg.items()
    if not str(msg).strip()
  )
  msg_drift_py = sorted(
    code for code in expected_py if exp_py_msg.get(code) != act_py_msg.get(code)
  )
  msg_drift_ts = sorted(
    code for code in expected_ts if exp_ts_msg.get(code) != act_ts_msg.get(code)
  )

  changes: list[str] = []
  registry_updated = str(meta.get("updated", ""))
  for path, label in ((PYTHON_ENUM_PATH, "python"), (TS_CODES_PATH, "typescript")):
    if path.is_file() and registry_updated:
      import datetime

      reg_date = datetime.date.fromisoformat(registry_updated)
      file_date = datetime.date.fromtimestamp(path.stat().st_mtime)
      if reg_date > file_date and not add_py and not del_py and not add_ts and not del_ts:
        changes.append(
          f"CHANGE · {label}: registry updated={registry_updated} 新于 mirror 文件日期 {file_date}，请复核 http_default/message 是否需 sync --apply"
        )

  return DriftReport(
    add_python=add_py,
    delete_python=del_py,
    add_typescript=add_ts,
    delete_typescript=del_ts,
    change_metadata=changes,
    message_drift_python=msg_drift_py,
    message_drift_typescript=msg_drift_ts,
    missing_message_zh=missing_zh,
  )


def format_drift_report(report: DriftReport) -> str:
  """人类可读的 ADD/DELETE/CHANGE 报告。"""
  lines = ["=== Error Registry 一致性检查（SSOT: contracts/error-registry.yaml）==="]
  code_ok = not (
    report.add_python
    or report.delete_python
    or report.add_typescript
    or report.delete_typescript
  )
  msg_ok = not (
    report.message_drift_python
    or report.message_drift_typescript
    or report.missing_message_zh
  )
  if code_ok and msg_ok and not report.change_metadata:
    lines.append("OK · code 与 message_zh mirror（Python · TypeScript）与 SSOT 一致。")
    return "\n".join(lines)

  if report.add_python or report.add_typescript:
    lines.append("\n[ADD] 须在 mirror 中新增（确认后: ./scripts/sync_error_registry.py --apply）:")
    for code in report.add_python:
      lines.append(f"  + {code} → errors.py (mirror_python)")
    for code in report.add_typescript:
      lines.append(f"  + {code} → error-codes.ts (mirror_typescript)")

  if report.delete_python or report.delete_typescript:
    lines.append("\n[DELETE] mirror 中存在但 SSOT 未登记（确认后 --apply 或恢复 registry）:")
    for code in report.delete_python:
      lines.append(f"  - {code} ← errors.py")
    for code in report.delete_typescript:
      lines.append(f"  - {code} ← error-codes.ts")

  if report.missing_message_zh:
    lines.append("\n[MISSING] mirror 码在 SSOT 缺少 message_zh（须补 registry）:")
    for code in report.missing_message_zh:
      lines.append(f"  ! {code}")

  if report.message_drift_python or report.message_drift_typescript:
    lines.append("\n[MESSAGE] message_zh 与 mirror 不一致（确认后 --apply）:")
    for code in report.message_drift_python:
      lines.append(f"  ~ {code} → errors.py ERROR_MESSAGE_ZH")
    for code in report.message_drift_typescript:
      lines.append(f"  ~ {code} → error-codes.ts ERROR_MESSAGES_ZH")

  if report.change_metadata:
    lines.append("\n[CHANGE] 元数据/日期提示（须人工确认是否 sync --apply）:")
    for item in report.change_metadata:
      lines.append(f"  ~ {item}")

  lines.append(
    "\n策略：禁止手改 mirror；变更须先改 SSOT 再 sync_error_registry.py --apply。"
  )
  return "\n".join(lines)


def render_python_module(entries: list[ErrorRegistryEntry]) -> str:
  """生成完整 errors.py（enum + ERROR_MESSAGE_ZH + helpers）。"""
  py_codes = sorted(mirror_codes(entries, "mirror_python"))
  messages = expected_messages(entries, "mirror_python")
  enum_lines = [f'  {code} = "{code}"' for code in py_codes]
  msg_lines = [
    f'  "{code}": "{_escape_py_string(messages[code])}",' for code in py_codes
  ]
  return f'''"""平台统一错误码常量。

作用：HTTP/API 与内核异常共用的机器可读错误码与中文默认文案。
业务关联：对齐 OpenAPI 响应与 AC 负向断言（如 GRAPH_NOT_FROZEN）。
上游：contracts/error-registry.yaml（SSOT）· mirror_python 真源
下游：server/api 异常处理器、os_core 各 service、web-admin error-codes.ts
关联文档：docs/文档/规格说明/状态码与错误约定.md
"""
from __future__ import annotations

from enum import StrEnum


class ErrorCode(StrEnum):
  """FactoryOS 业务错误码 — mirror contracts/error-registry.yaml (mirror_python)。

  禁止手改漂移；变更须先改 SSOT 再 sync --apply。
  """

{chr(10).join(enum_lines)}


ERROR_MESSAGE_ZH: dict[str, str] = {{
{chr(10).join(msg_lines)}
}}


def default_message(code: ErrorCode | str) -> str:
  """SSOT message_zh 默认中文；抛出 PlatformError 时 message 可 override。"""
  key = code.value if isinstance(code, ErrorCode) else code
  return ERROR_MESSAGE_ZH.get(key, ERROR_MESSAGE_ZH["UNKNOWN_ERROR"])


def format_error_label(code: ErrorCode | str) -> str:
  """开发者可读：英文 code + 中文描述（日志 / 调试一眼懂）。"""
  key = code.value if isinstance(code, ErrorCode) else code
  return f"{{key}} · {{default_message(key)}}"
'''


def render_typescript_module(entries: list[ErrorRegistryEntry]) -> str:
  """生成完整 error-codes.ts（ERROR_CODES + ERROR_MESSAGES_ZH + helpers）。"""
  ts_codes = sorted(mirror_codes(entries, "mirror_typescript"))
  messages = expected_messages(entries, "mirror_typescript")
  code_lines: list[str] = []
  for code in ts_codes:
    zh = messages[code]
    code_lines.append(f"  /** {zh} */")
    code_lines.append(f'  {code}: "{code}",')
  msg_lines = [
    f'  {code}: "{_escape_ts_string(messages[code])}",' for code in ts_codes
  ]
  return f'''/**
 * 模块：src/apps/web-admin/src/api/request/error-codes.ts
 * 作用：业务错误码 + 中文 message_zh mirror（SSOT error-registry.yaml）
 * 怎么用：ERROR_CODES · getErrorMessageZh · formatErrorLabel
 * 解决：英文 code 必带中文描述，开发者一眼懂
 * 上游：contracts/error-registry.yaml · sync_error_registry.py
 * 下游：errors.ts · ApiErrorBanner · 页面分支
 * 关联：docs/文档/规格说明/状态码与错误约定.md
 */
export const ERROR_CODES = {{
{chr(10).join(code_lines)}
}} as const;

export type ErrorCodeValue = (typeof ERROR_CODES)[keyof typeof ERROR_CODES];

export const ERROR_MESSAGES_ZH: Record<ErrorCodeValue, string> = {{
{chr(10).join(msg_lines)}
}} as const;

/** SSOT 默认中文；API 未返回 message 时 fallback。 */
export function getErrorMessageZh(code: ErrorCodeValue | string): string {{
  const key = code as ErrorCodeValue;
  return ERROR_MESSAGES_ZH[key] ?? ERROR_MESSAGES_ZH.UNKNOWN_ERROR;
}}

/** 日志 / UI 调试：CODE · 中文 */
export function formatErrorLabel(code: ErrorCodeValue | string): string {{
  return `${{code}} · ${{getErrorMessageZh(code)}}`;
}}
'''
