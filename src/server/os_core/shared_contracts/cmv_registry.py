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
_L0_LEVELS = frozenset({"L0"})
_L2_LEVELS = frozenset({"L2", "L3"})


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


def register_dsl_verb(
  *,
  verb: str,
  level: str,
  compensator: str | None,
  params_schema: dict[str, Any] | None = None,
  description: str | None = None,
  connector_ops: list[dict[str, Any]] | None = None,
  idempotent: bool = False,
) -> dict[str, Any]:
  """校验并登记 CMV 动词（D-04 · L2/L3 须 compensator）。

  功能：注册前结构校验；不直接写 Registry DB（须 change-request 人审落库）。
  业务含义：拒绝无 compensator 的 L2 动词，对齐 check_cmv_sync 规则。
  上游：POST /v1/registry/cmv/verbs
  下游：Studio 提案前置校验
  """
  if level in _L2_LEVELS and not compensator and not verb.endswith("_REVERT"):
    raise PlatformError(
      ErrorCode.BLUEPRINT_INVALID,
      f"L2 verb {verb} must declare compensator",
      http_status=422,
    )
  if level in _L0_LEVELS and compensator:
    raise PlatformError(
      ErrorCode.BLUEPRINT_INVALID,
      f"L0 verb {verb} must not have compensator",
      http_status=422,
    )
  return {
    "verb": verb,
    "level": level,
    "description": description,
    "params_schema": params_schema or {"type": "object"},
    "compensator": compensator,
    "connector_ops": connector_ops or [],
    "idempotent": idempotent,
  }
