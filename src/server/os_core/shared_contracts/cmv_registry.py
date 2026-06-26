"""CMV 注册表只读加载（Contract Registry 真源 · ADR-008）。

作用：DSL registry GET 与 execution 动词校验共用真源。
业务关联：D-01 列出底座动词 · D-02 未知动词拒绝。
上游：platform_registry.contract_store（优先）· contracts/cmv export 镜像
下游：execution_service · GET /v1/dsl/registry
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

import yaml

from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError
from os_core.shared_contracts.repo_paths import contracts_dir

_CMV_PATH = contracts_dir() / "cmv" / "CMV注册表.yaml"
_DRAFT_CHECKSUM = "sha256:" + "0" * 64


def clear_cache() -> None:
  """Session 切换或 bootstrap 后清空进程内缓存。"""
  _load_verbs_raw.cache_clear()


@lru_cache(maxsize=1)
def _load_verbs_raw() -> list[dict[str, Any]]:
  """加载 CMV verbs（DB 优先 · export 文件回退）。"""
  from os_core.platform_registry import contract_store
  from os_core.platform_registry.session import get_registry_session

  session = get_registry_session()
  if session is not None:
    body = contract_store.get_cmv_body(session)
    if body:
      data = yaml.safe_load(body)
      if isinstance(data, dict):
        verbs = data.get("verbs") or []
        return list(verbs)

  if not _CMV_PATH.is_file():
    msg = f"CMV 注册表缺失: {_CMV_PATH}"
    raise PlatformError(ErrorCode.DSL_UNKNOWN, msg, http_status=500)
  data = yaml.safe_load(_CMV_PATH.read_text(encoding="utf-8"))
  verbs = data.get("verbs") or []
  return list(verbs)


def list_dsl_actions() -> list[dict[str, Any]]:
  """返回 DSLAction 形状列表（D-01）。"""
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
