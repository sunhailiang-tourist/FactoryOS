#!/usr/bin/env python3
"""vendor error-registry ↔ error-codes.ts 对账库（standalone 自给）。"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from contracts_paths import app_root_from_here, vendor_contracts_root

APP_ROOT = app_root_from_here(__file__)
REGISTRY_PATH = vendor_contracts_root(APP_ROOT) / "error-registry.yaml"
TS_CODES_PATH = APP_ROOT / "src" / "api" / "request" / "error-codes.ts"

TS_KEY_RE = re.compile(r"^\s+([A-Z][A-Z0-9_]*):\s*\"([A-Z][A-Z0-9_]*)\"\s*,?\s*$")
TS_MSG_ZH_RE = re.compile(r'^\s+([A-Z][A-Z0-9_]*):\s+"(.*)",\s*$')


@dataclass(frozen=True)
class ErrorRegistryEntry:
  code: str
  mirror_typescript: bool
  message_zh: str


def load_registry(path: Path = REGISTRY_PATH) -> tuple[dict[str, Any], list[ErrorRegistryEntry]]:
  raw = yaml.safe_load(path.read_text(encoding="utf-8"))
  entries: list[ErrorRegistryEntry] = []
  for item in raw.get("codes") or []:
    entries.append(
      ErrorRegistryEntry(
        code=str(item["code"]),
        mirror_typescript=bool(item.get("mirror_typescript", False)),
        message_zh=str(item.get("message_zh", "")),
      )
    )
  return raw, entries


def mirror_ts_codes(entries: list[ErrorRegistryEntry]) -> set[str]:
  return {e.code for e in entries if e.mirror_typescript}


def expected_messages(entries: list[ErrorRegistryEntry]) -> dict[str, str]:
  codes = mirror_ts_codes(entries)
  return {e.code: e.message_zh for e in entries if e.code in codes}


def parse_typescript_codes(path: Path = TS_CODES_PATH) -> set[str]:
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


def _unescape_ts_string(value: str) -> str:
  return value.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")


def _escape_ts_string(value: str) -> str:
  return value.replace("\\", "\\\\").replace('"', '\\"')


@dataclass
class DriftReport:
  add_typescript: list[str]
  delete_typescript: list[str]
  message_drift_typescript: list[str]
  missing_message_zh: list[str]

  def has_hard_fail(self) -> bool:
    return bool(
      self.add_typescript
      or self.delete_typescript
      or self.message_drift_typescript
      or self.missing_message_zh
    )


def compute_drift() -> DriftReport:
  _, entries = load_registry()
  expected = mirror_ts_codes(entries)
  actual = parse_typescript_codes()
  exp_msg = expected_messages(entries)
  act_msg = parse_typescript_messages()
  return DriftReport(
    add_typescript=sorted(expected - actual),
    delete_typescript=sorted(actual - expected),
    message_drift_typescript=sorted(
      code for code in expected if exp_msg.get(code) != act_msg.get(code)
    ),
    missing_message_zh=sorted(
      code for code, msg in exp_msg.items() if not str(msg).strip()
    ),
  )


def format_drift_report(report: DriftReport) -> str:
  lines = [
    "=== Error Registry（vendor SSOT → error-codes.ts）===",
    f"SSOT: {REGISTRY_PATH.relative_to(APP_ROOT)}",
  ]
  if not report.has_hard_fail():
    lines.append("OK · ERROR_CODES 与 ERROR_MESSAGES_ZH 与 vendor mirror 一致。")
    return "\n".join(lines)
  if report.add_typescript:
    lines.append("\n[ADD] error-codes.ts 须新增:")
    for code in report.add_typescript:
      lines.append(f"  + {code}")
  if report.delete_typescript:
    lines.append("\n[DELETE] error-codes.ts 多余:")
    for code in report.delete_typescript:
      lines.append(f"  - {code}")
  if report.missing_message_zh:
    lines.append("\n[MISSING] vendor 缺少 message_zh:")
    for code in report.missing_message_zh:
      lines.append(f"  ! {code}")
  if report.message_drift_typescript:
    lines.append("\n[MESSAGE] message_zh 漂移（--apply）:")
    for code in report.message_drift_typescript:
      lines.append(f"  ~ {code}")
  lines.append("\n策略：改 vendor/error-registry.yaml → scripts/sync_error_registry.py --apply")
  return "\n".join(lines)


def render_typescript_module(entries: list[ErrorRegistryEntry]) -> str:
  ts_codes = sorted(mirror_ts_codes(entries))
  messages = expected_messages(entries)
  code_lines: list[str] = []
  for code in ts_codes:
    code_lines.append(f"  /** {messages[code]} */")
    code_lines.append(f'  {code}: "{code}",')
  msg_lines = [f'  {code}: "{_escape_ts_string(messages[code])}",' for code in ts_codes]
  return (
    "/**\n"
    " * 模块：src/apps/web-admin/src/api/request/error-codes.ts\n"
    " * 作用：业务错误码 + 中文 message_zh mirror（vendor SSOT）\n"
    " * 怎么用：ERROR_CODES · getErrorMessageZh · formatErrorLabel\n"
    " * 上游：vendor/factoryos-contracts/error-registry.yaml\n"
    " */\n"
    "export const ERROR_CODES = {\n"
    + "\n".join(code_lines)
    + "\n} as const;\n\n"
    "export type ErrorCodeValue = (typeof ERROR_CODES)[keyof typeof ERROR_CODES];\n\n"
    "export const ERROR_MESSAGES_ZH: Record<ErrorCodeValue, string> = {\n"
    + "\n".join(msg_lines)
    + "\n} as const;\n\n"
    "export function getErrorMessageZh(code: ErrorCodeValue | string): string {\n"
    "  const key = code as ErrorCodeValue;\n"
    "  return ERROR_MESSAGES_ZH[key] ?? ERROR_MESSAGES_ZH.UNKNOWN_ERROR;\n"
    "}\n\n"
    "export function formatErrorLabel(code: ErrorCodeValue | string): string {\n"
    "  return `${code} · ${getErrorMessageZh(code)}`;\n"
    "}\n"
  )
