"""CMV 注册表只读加载（contracts/cmv/CMV注册表.yaml）。

作用：DSL registry GET 与 execution 动词校验共用真源。
业务关联：D-01 列出底座动词 · D-02 未知动词拒绝。
上游：contracts/cmv
下游：execution_service · GET /v1/dsl/registry
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError

_REPO_ROOT = Path(__file__).resolve().parents[3]
_CMV_PATH = _REPO_ROOT / "contracts" / "cmv" / "CMV注册表.yaml"
_DRAFT_CHECKSUM = "sha256:" + "0" * 64


@lru_cache(maxsize=1)
def _load_verbs_raw() -> list[dict[str, Any]]:
  """加载 CMV yaml verbs 列表（进程内缓存）。"""
  if not _CMV_PATH.is_file():
    msg = f"CMV 注册表缺失: {_CMV_PATH}"
    raise PlatformError(ErrorCode.DSL_UNKNOWN, msg, http_status=500)
  data = yaml.safe_load(_CMV_PATH.read_text(encoding="utf-8"))
  verbs = data.get("verbs") or []
  return list(verbs)


def list_dsl_actions() -> list[dict[str, Any]]:
  """返回 DSLAction 形状列表（D-01）。

  功能：对齐 OpenAPI DSLAction · schema required 字段。
  返回：verb/level/params_schema/compensator 等
  """
  out: list[dict[str, Any]] = []
  for item in _load_verbs_raw():
    out.append(
      {
        "verb": item["verb"],
        "level": item["level"],
        "description": item.get("description"),
        "params_schema": item.get("params_schema") or {"type": "object"},
        "compensator": item.get("compensator"),
        "connector_ops": item.get("connector_ops") or [],
        "idempotent": item.get("idempotent", False),
      }
    )
  return out


def get_verb_level(verb: str) -> str | None:
  """查动词 CMV level（L0/L2 等）；未知返回 None。"""
  for item in _load_verbs_raw():
    if item.get("verb") == verb:
      return str(item.get("level"))
  return None


def require_known_verb(verb: str) -> dict[str, Any]:
  """已知动词或抛 DSL_UNKNOWN（D-02）。"""
  for item in _load_verbs_raw():
    if item.get("verb") == verb:
      return item
  raise PlatformError(
    ErrorCode.DSL_UNKNOWN,
    f"Unknown DSL verb: {verb}",
    http_status=400,
  )


def draft_graph_checksum() -> str:
  """draft Graph 占位 checksum（对齐 schema 约定）。"""
  return _DRAFT_CHECKSUM
