"""Connector 连通测试（Studio Step 1 · P-03 Override）。

作用：解析 tenant Override + Blueprint base_url，返回连通报告。
业务关联：POST /v1/integration/connect/test · IntegrationConnectReport。
上游：server.api.modules.integration
下游：platform_registry pack_store · tenant_config_store
"""
from __future__ import annotations

import time
from typing import Any, Literal

from sqlalchemy.orm import Session

from os_core.platform_registry import pack_store, tenant_config_store

ConnectStatus = Literal["ok", "failed"]


def resolve_pack_base_url(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
) -> str:
  """Blueprint base_url 与 tenant connector_overrides 合并（P-03）。

  功能：Override 差量覆盖 catalog 默认 URL。
  业务含义：runtime / connect/test 须与 overrides.yaml 一致。
  """
  blueprint = pack_store.get_pack_blueprint(session, pack_id=pack_id)
  default_url = "http://mock.local"
  if blueprint:
    spec = blueprint.get("spec") or {}
    default_url = str(spec.get("base_url") or default_url)

  overrides = tenant_config_store.get_connector_overrides(session, tenant_id=tenant_id)
  pack_override = overrides.get(pack_id)
  if isinstance(pack_override, dict):
    override_url = pack_override.get("base_url")
    if override_url:
      return str(override_url)
  return default_url


def run_connect_test(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
) -> dict[str, Any]:
  """POST /v1/integration/connect/test 内核（P-03）。

  功能：校验 system_relation 存在并返回 resolved base_url。
  业务含义：Studio Connect 步；Override 后 URL 须可见于报告。
  """
  started = time.perf_counter()
  overrides = tenant_config_store.get_connector_overrides(session, tenant_id=tenant_id)
  has_override = pack_id in overrides
  has_relation = tenant_config_store.has_system_relation_for_pack(
    session,
    tenant_id=tenant_id,
    pack_id=pack_id,
  )
  if not has_relation and not has_override:
    return {
      "status": "failed",
      "pack_id": pack_id,
      "message": f"Connector {pack_id} not configured for tenant {tenant_id}",
    }

  base_url = resolve_pack_base_url(session, tenant_id=tenant_id, pack_id=pack_id)
  latency_ms = int((time.perf_counter() - started) * 1000)
  return {
    "status": "ok",
    "pack_id": pack_id,
    "latency_ms": latency_ms,
    "edge_agent_status": "n/a",
    "base_url": base_url,
    "resolved_base_url": base_url,
  }
